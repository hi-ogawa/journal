# Agent-Driven Development Experiment

**Status**: Research/brainstorm phase. Actual coding will happen in a dedicated repo.

## Background

Interested in evaluating autonomous coding agent workflows (Ralph method, etc.) for real projects. Need a concrete, well-scoped target to test the methodology.

## Motivation

- Have Claude Code Max subscription - waste if not utilized
- Ralph loop can run AFK, making good use of unlimited usage
- Run locally (not CI) - no extra setup, stays free
- **Requirement**: Need proper isolation so agent can run with full capabilities safely

## Goals

1. **Primary**: Experiment with and evaluate agent-driven development methodologies
   - Test Ralph loop and variations
   - Document what works, what breaks, human intervention points
   - Develop intuition for prompt engineering and task decomposition
2. **Secondary**: Port a Linux LV2 plugin to Windows VST3 as the test project

## Why Plugin Porting as Test Case

- Well-defined success criteria (builds, loads, sounds correct)
- Mechanical work (API wrapping, build config) suits agents
- DSP code is platform-agnostic, mostly copy-paste
- Clear scope - not open-ended

## Structure

This repo (`llm-tasks`) = **research & planning**

```
2026-01-17-agent-driven-dev/
  plan.md                   # Action items, progress log
  notes/
    ralph-method.md         # Ralph loop methodology
    isolation.md            # Docker/container options
    test-project.md         # NIH-plug, Faust, porting strategy
    references.md           # Plugin repos, clone commands
  refs/                     # Local reference clones (gitignored)
```

Separate repo (TBD) = **actual Ralph-driven coding**

```
gx-tremolo-vst/             # Example name
  PROMPT.md                 # Instructions for Ralph loop
  src/                      # Agent commits progress here
  ...
```

Learnings from the experiment come back here for documentation.
