# OpenCode Compaction Mechanism

How opencode manages context window limits during long conversations.

## Overview

Compaction is a two-tier system:
1. **Pruning** - Clears old tool outputs (fast, frequent)
2. **Summarization** - LLM-generated conversation summary (heavy, when overflow detected)

## Trigger Conditions

After each assistant message completes, opencode checks for overflow:

```typescript
// compaction.ts:30-39
const count = input.tokens.input + input.tokens.cache.read + input.tokens.output
const usable = context - max_output_tokens
return count > usable
```

Key insight: It reserves space for the **next** response before triggering compaction.

## Timing: Between Turns, Not Mid-Stream

Despite appearing to happen "mid-interaction", compaction occurs at turn boundaries:

1. **Detection**: After assistant message completes (post-generation)
2. **Break**: If overflow, breaks out of current processing loop
3. **Compaction**: Handled in next iteration of conversation loop
4. **Continue**: Synthetic "continue" message sent to resume work

The user perceives this as mid-interaction because the assistant continues seamlessly after compaction.

## Two-Stage Process

### Stage 1: Pruning (Token Cleanup)

**Constants:**
- `PRUNE_PROTECT = 40,000` tokens - Keep recent tool outputs
- `PRUNE_MINIMUM = 20,000` tokens - Minimum savings to bother pruning

**Strategy:**
- Walks backward through history
- Clears tool call outputs beyond protection threshold
- Replaces with: `"[Old tool result content cleared]"`
- Preserves "skill" tool calls (not pruned)
- Sets `part.state.time.compacted = Date.now()` on pruned outputs

### Stage 2: Full Summarization

When pruning isn't enough, creates a compaction message:

**Prompt** (`agent/prompt/compaction.txt`):
```
You are a helpful AI assistant tasked with summarizing conversations.

Focus on information that would be helpful for continuing the conversation, including:
- What was done
- What is currently being worked on
- Which files are being modified
- What needs to be done next
- Key user requests, constraints, or preferences that should persist
- Important technical decisions and why they were made
```

**Result:**
- Creates message with `mode: "compaction"`, `summary: true`
- Emits `Event.Compacted` for UI notification
- Auto-generates "continue" message if `auto: true`

## What Gets Preserved vs. Compressed

**Preserved:**
- All user messages (text)
- Recent assistant responses
- Recent tool calls + inputs
- Skill tool outputs (protected)
- Message metadata/structure

**Compressed/Cleared:**
- Old tool outputs beyond threshold
- Entire conversation → single summary message

## Configuration

```json
// opencode.json
{
  "compaction": {
    "auto": true,    // Enable automatic compaction
    "prune": true    // Enable tool output pruning
  }
}
```

## Design Insights

1. **Non-destructive**: Messages preserved, tokens reduced via summarization layer
2. **Tool-aware**: Protects skill outputs, clears data-heavy tool results
3. **LLM-powered**: Contextual summary, not heuristic truncation
4. **Seamless continuation**: User doesn't notice the boundary

## Implications for Knowledge Work

This mechanism allows "unlimited" conversation length, but with tradeoffs:
- Early context gets summarized (lossy compression)
- Tool outputs from early exploration are lost
- Summary quality depends on LLM's ability to extract key points

For deep inquiry workflows, this means:
- Important findings should be persisted to files (not just conversation)
- Can't rely on conversation memory for detailed historical context
- Explicit checkpointing (writing notes/docs) is essential
