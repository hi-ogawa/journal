@README.md

# Agent Conventions

Portable workflow conventions for any coding agent (Claude Code, opencode, Codex CLI, gemini-cli, etc.).

## Session Lifecycle

### Quick Questions (One-shot)

For lightweight questions that don't need a dedicated task:

1. Just answer in conversation (ephemeral)
2. If user wants to keep it: append to `notes/scratch.md` with date header
3. If it grows substantial: user can say "let's make this a task" → promote to full task

### Starting a New Task

When user says "new task [topic]", "explore [topic]", or similar:

1. Create `tasks/YYYY-MM-DD-[topic]/`
2. Create `README.md` with brief overview (what, why)
3. Create `plan.md` for detailed planning and progress
4. Create `notes/` directory
5. Begin working in that directory

### Resuming Work

When user says "continue [topic]" or references an existing task:

1. Find matching task directory in `tasks/`
2. Read `README.md` and `plan.md` for context
3. Continue from where left off

### Finishing Up

When user says "done", "finish", "let's commit", or "save and push":

1. `git add -A`
2. `git commit -m "[descriptive message based on work done]"`
3. `git push`
4. Confirm completion to user

### Syncing

When user says "sync" or "pull latest":

1. `git pull --rebase --autostash`
2. Report any conflicts if they occur

## Directory Structure

```
tasks/
  YYYY-MM-DD-[topic]/
    README.md      # What and why (brief)
    plan.md        # Detailed planning, progress log
    notes/         # Research notes, references
    scripts/       # Any automation (with pyproject.toml if Python)
    data/          # Generated outputs (often gitignored)
```

## Meta Commands

Shorthand commands for common workflow actions. Use `[command]` syntax:

| Command | Action |
|---------|--------|
| `[q]` | Quick question - answer ephemerally, no files |
| `[new]` | Create new task directory, scaffold files, start working |
| `[continue]` | Find task, read context, resume |
| `[note]` | Append to `notes/scratch.md` with timestamp |
| `[promote]` | Convert scratch notes into dedicated task |
| `[done]` | Git add, commit (with message), push |
| `[sync]` | Git pull --rebase --autostash |

Examples:
```
[q what's the difference between MCP and LSP?]
[new vim-keybindings]
[note check out this approach for modal editing]
[save]
[done added research on directory-backed chat]
```

Natural language alternatives work too ("let's commit", "save this note", etc.).

## Principles

- **Files are the source of truth** - conversation is ephemeral, outputs persist
- **User controls what to save** - agent writes what user instructs
- **Commands and natural language** - both work, user's choice
