# Ralph Method for Agent-Driven Development

## Overview

The "Ralph Wiggum Loop" (named after the Simpsons character) is an autonomous AI development technique created by Geoffrey Huntley in May 2025. Core insight: **progress lives in files and git, not in the LLM's context window**.

## Original Script

```bash
while :; do cat PROMPT.md | claude-code ; done
```

That's it. An infinite loop feeding the same prompt repeatedly.

## How It Works

1. **PROMPT.md** contains the development instructions
2. Each loop iteration spawns a fresh agent with clean context
3. Agent reads current state from files, makes progress, commits
4. When context fills up, loop restarts with fresh agent
5. New agent picks up from git history and file state
6. Repeat until done

## Key Principles

| Principle | Meaning |
| --- | --- |
| Naive persistence | Keep trying until success criteria met |
| Files are memory | State lives in filesystem, not context |
| Iteration > perfection | Continuous refinement beats upfront planning |
| Operator skill | Success reflects prompt engineering ability |
| Right-sized tasks | Each task must fit in one context window |

## Practical Implementations

### Original (Huntley)

- 5-line bash script
- Relies on operator skill to refine PROMPT.md
- Brute force approach

### snarktank/ralph

- Structured task list (`prd.json`)
- Quality checks between iterations
- Progress log (`progress.txt`) accumulates learnings
- Updates AGENTS.md with discovered patterns

### frankbria/ralph-claude-code

- Claude Code specific with `--continue` for session continuity
- Intelligent exit detection (dual-condition check)
- Safety mechanisms: rate limiting, circuit breaker, error filtering
- Structured project layout with specs/

## Relevance to Plugin Porting

Good fit because:

- Well-defined success criteria (plugin builds, loads in DAW, produces correct audio)
- Mechanical tasks (API wrapping, build config) suit agents well
- Code changes are testable at each step
- DSP code is largely copy-paste, minimal creativity needed

Challenges:

- Audio correctness hard to verify automatically
- Platform-specific debugging may stall the loop
- Build system issues can be opaque

## Sources

- [Geoffrey Huntley - Ralph](https://ghuntley.com/ralph/)
- [snarktank/ralph GitHub](https://github.com/snarktank/ralph)
- [frankbria/ralph-claude-code GitHub](https://github.com/frankbria/ralph-claude-code)
- [VentureBeat - Ralph Wiggum AI](https://venturebeat.com/technology/how-ralph-wiggum-went-from-the-simpsons-to-the-biggest-name-in-ai-right-now)
