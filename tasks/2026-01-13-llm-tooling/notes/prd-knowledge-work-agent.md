# PRD: Repurposing Local Coding Agents for Knowledge Work

> **See also:**
> - [directory-backed-chat.md](directory-backed-chat.md) - research on "ideal" solutions (Cowork, Open WebUI, etc.)
> - [cloud-sync-alternative.md](cloud-sync-alternative.md) - simpler alternative using cloud sync + VSCode

**Status:** Draft v6

## Problem Statement

Local coding agents (Claude Code, opencode, Codex CLI, gemini-cli, etc.) are built for software development but have properties that make them excellent for general knowledge work:

- **Directory-bound sessions** - work lives in a folder, not a cloud account
- **Tool access** - read/write files, fetch web, run scripts
- **File-backed outputs** - artifacts persist, conversation is ephemeral

However, using them for knowledge work has friction across the **session lifecycle**:

| Phase | Friction |
|-------|----------|
| **Quick questions** | Overkill to start agent for one-off questions |
| **Starting** | Scaffolding new task directories, remembering structure |
| **Resuming** | Finding context, remembering where you left off |
| **Capturing** | Deciding what to save, where to put notes |
| **Finishing** | Git ceremony (add, commit, push) |
| **Syncing** | Pulling latest before starting |

Cloud chat (Claude.ai) has smoother UX for each phase - but lacks the tool access and file persistence that make local agents powerful.

## Goal

Reduce lifecycle friction through **portable workflow conventions** that any coding agent can follow:

1. Define conventions in `AGENTS.md` (agent-agnostic)
2. Provide meta-commands for common actions (`[new]`, `[done]`, etc.)
3. Support spectrum from quick questions to deep research
4. Enable testing different agents with consistent behavior

## What's Good (Keep)

- [x] Terminal interaction
- [x] Ephemeral chat (files are source of truth, not conversation)
- [x] User controls what/how to save
- [x] Directory-bound sessions
- [x] File-backed outputs
- [x] `--resume`/`--continue` for session continuity (already exists)
- [x] File explorer for discoverability (no fancy search needed)

## What's Bad (Fix)

- [ ] **Sync** - git pull before starting (get latest)
- [ ] **Startup** - cd to dir, run agent
- [ ] **Finish** - git commit + push after done (persist work)

## Proposed Solution: AGENTS.md Conventions

Instead of a wrapper script, define conventions in `AGENTS.md` that any agent reads.

### Why AGENTS.md?

| File | Portability |
|------|-------------|
| `CLAUDE.md` | Claude Code only |
| `.opencode/` | opencode only |
| `AGENTS.md` | Emerging convention, multiple agents |

Many agents look for `AGENTS.md` or can be configured to read it.

### Proposed AGENTS.md Content

```markdown
# Agent Conventions

## Session Lifecycle

### Starting a New Task
When user says "new task [topic]" or "explore [topic]":
1. Create `tasks/YYYY-MM-DD-[topic]/`
2. Create `README.md` with brief overview
3. Create `plan.md` for detailed planning
4. Create `notes/` directory
5. Begin working in that directory

### Resuming Work
When user says "continue [topic]" or references existing task:
1. Find matching task directory
2. Read `README.md` and `plan.md` for context
3. Continue from where left off

### Finishing Up
When user says "done", "finish", "commit", or "let's save":
1. `git add -A`
2. `git commit -m "[descriptive message]"`
3. `git push`
4. Confirm completion to user

### Syncing
When user says "sync" or "pull latest":
1. `git pull --rebase --autostash`
2. Report any conflicts

## Directory Structure

tasks/
  YYYY-MM-DD-[topic]/
    README.md      # What and why (brief)
    plan.md        # Detailed planning, progress log
    notes/         # Research notes, references
    scripts/       # Any automation
    data/          # Generated outputs (often gitignored)
```

### Usage (Natural Language)

No special commands needed. Just talk:

```
User: "new task exploring vim keybindings"
Agent: [creates tasks/2026-01-14-exploring-vim-keybindings/, scaffolds files]

User: "continue on the llm-tooling research"
Agent: [reads tasks/2026-01-13-llm-tooling/plan.md, resumes]

User: "looks good, let's commit and push"
Agent: [git add, commit, push]
```

## Agent-Specific Extensions

For agent-specific features, use their native config:

| Agent | Config Location | Use For |
|-------|-----------------|---------|
| Claude Code | `CLAUDE.md` | Custom commands, MCP |
| opencode | `.opencode/` | Custom agents, permissions |
| Codex CLI | (flags) | Sandbox settings |
| gemini-cli | (flags) | Trust settings |

The `AGENTS.md` provides the portable base; agent-specific configs add extras.

## Non-Goals

- Wrapper scripts (natural language is enough)
- Agent-specific deep integration (keep portable)
- Session persistence/history (files ARE the history)
- Web UI

## Open Questions

1. **AGENTS.md adoption** - Which agents actually read it? Need to verify.

2. **Trigger phrases** - What natural language patterns should be recognized? Keep it loose or define explicitly?

3. **Commit message** - Auto-generate? Or let user specify in "done" message?

4. **Conflict handling** - What if pull has conflicts? Abort and let user handle?

5. **Non-git repos** - What's the "finish" behavior for non-git directories?

## Next Steps

1. [ ] Update this repo's `AGENTS.md` with the conventions
2. [ ] Test with Claude Code (current)
3. [ ] Test with opencode
4. [ ] Test with Codex CLI / gemini-cli
5. [ ] Iterate on trigger phrases based on what feels natural

---

## Changelog

### v6 (2026-01-14)
- Renamed to "Repurposing Local Coding Agents for Knowledge Work"
- Broadened problem statement: lifecycle friction, not just persistence
- Added friction table for each phase (quick questions → syncing)

### v5 (2026-01-14)
- Pivoted from wrapper script to AGENTS.md conventions
- Key insight: natural language prompting already works, just needs conventions
- Agent-agnostic approach enables testing multiple agents
- Added next steps for testing

### v4 (2026-01-14)
- Corrected framing: cloud auto-save is superior, git is just the practical option
- Goal is to reduce friction, not claim git is better

### v3 (2026-01-14)
- Added full lifecycle: sync → session → finish
- `a done` for git commit + push
- Sync (git pull) runs automatically on start

### v2 (2026-01-14)
- Simplified drastically after feedback
- Removed session persistence (not needed - files are source of truth)
- Removed discoverability (file explorer is fine)
- Focus is purely on startup friction
