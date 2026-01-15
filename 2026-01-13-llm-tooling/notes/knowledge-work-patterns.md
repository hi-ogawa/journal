# Why Local Agents Excel at Knowledge Work

Analysis of what makes local agents (Claude Code, opencode) effective for deep inquiry, based on concrete experience.

## Case Study: Ableton Documentation Task

**Task**: Learn Ableton Live as a Linux user with specific context (bass player, active electronics, existing Ardour knowledge).

**What the agent did:**
1. Answered questions with personal context considered
2. Verified shortcuts against official Ableton documentation
3. Caught and corrected hallucinations (marked with verification status)
4. Built structured reference documents
5. Iterated on documents across multiple sessions

**Output**: 400+ line workflow guide, 900+ line bass tone guide - both verified and personalized.

## Capabilities That Made This Work

### 1. File System as Memory

**What it enables:**
- Documents persist across sessions
- Can reference and build on previous work
- Context accumulates in files, not just conversation window
- Artifacts are immediately usable (not trapped in chat)

**Consumer chat gap:** Artifacts exist but are ephemeral. Must copy-paste to preserve. No way to reference previous artifacts easily.

### 2. Web Fetching for Verification

**What it enables:**
- Cross-reference claims against official documentation
- Catch hallucinations before they become "knowledge"
- Build verified reference material

**Example from Ableton task:**
- LLM claimed `A` key was "select mode" in MIDI editor
- Verification against official docs showed this was wrong
- Corrected and marked in document

**Consumer chat gap:** No web access (or very limited). Cannot verify claims. Must trust or manually check.

### 3. Iterative Document Editing

**What it enables:**
- Refine documents based on new information
- Add verification status markers
- Restructure and expand over time
- Treat output as living document, not one-shot generation

**Consumer chat gap:** Each generation is standalone. Must manually merge/edit in external tool.

### 4. Tool Execution

**What it enables:**
- Run conversion scripts (e.g., HTML to Markdown for documentation)
- Execute validation/testing
- Automate repetitive parts of research workflow

**Consumer chat gap:** No code execution. Everything manual.

### 5. Large Context via Filesystem

**What it enables:**
- Reference large documents without hitting context limits
- Read specific sections on demand
- Agent decides what context is relevant

**Consumer chat gap:** Limited to uploaded files. No dynamic reading based on need.

## The Workflow Pattern

```
1. EXPLORE: Ask questions, get initial information
        ↓
2. CAPTURE: Write to file (creates persistent artifact)
        ↓
3. VERIFY: Fetch authoritative sources, check claims
        ↓
4. REFINE: Edit document with corrections/additions
        ↓
5. ITERATE: Return to step 1 with new questions
        ↓
   (Context accumulates in filesystem across sessions)
```

**Key insight:** The filesystem acts as external memory. Each session builds on previous work without re-explaining context.

## What Consumer Chat Would Need

To match this workflow, consumer chat would need:

1. **Persistent, editable artifacts** - Not just generation, but refinement
2. **Web access** - For verification against sources
3. **Project-level memory** - Context that persists across sessions
4. **File export/import** - Seamless movement between chat and filesystem

**Current state:**
- Claude Projects: Has file upload and project context, but no web access, limited artifact iteration
- Claude Desktop + MCP: Potentially bridges the gap? (needs investigation)
- ChatGPT: Similar limitations

## Open Questions

1. **Does MCP in Claude Desktop provide enough capability?** Could add file access and web fetching via MCP servers.

2. **Is there a web UI that provides agent capabilities?** Open WebUI, LibreChat, etc.

3. **Is terminal UX the actual problem?** Or is it just unfamiliarity? Modern TUIs (opencode) have syntax highlighting, scrolling, etc.

4. **Hybrid workflow?** Use chat for exploration, switch to agent for execution/verification.
