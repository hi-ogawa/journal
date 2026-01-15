# Alternative: Cloud Sync + VSCode

> Alternative to git-based workflow in [prd-knowledge-work-agent.md](prd-knowledge-work-agent.md)

## Conclusion (2026-01-15)

**Git wins for now.** Cloud sync alternatives were explored but each has significant tradeoffs:

| Alternative | Blocker |
|-------------|---------|
| Google Drive | No Linux client; no ignore patterns for large data |
| Dropbox | No pattern-based ignore (folder-level only) |
| Syncthing | Requires 2+ devices online; self-managed |
| MCP to cloud | Loses local file advantages (agent becomes remote client) |

The git friction (`[sync]`, `[done]`) is real but manageable. The local agent strength depends on files being in the working directory with direct read/write access - this is worth preserving.

**Revisit if:**
- Google releases official Linux client with ignore patterns
- Workflow shifts to multi-machine with frequent switching
- A sync solution emerges with gitignore-like patterns + zero-config

---

## Proposal

Replace git with cloud folder sync. Use VSCode as the unified interface for viewing markdown and running terminal agents.

## Setup

```
~/Dropbox/llm-tasks/        ← Or Google Drive, OneDrive, etc.
  tasks/
    2026-01-13-topic/
      README.md
      plan.md
      notes/
```

Open folder in VSCode. Split view: markdown preview + integrated terminal.

## Comparison

| Aspect | Git Workflow | Cloud Sync |
|--------|--------------|------------|
| Sync | Manual (`git pull/push`) | Automatic |
| Checkpoints | Explicit commits | Continuous |
| History | Full version history | Limited (cloud versioning) |
| Conflicts | Merge conflicts | Last-write-wins |
| Ceremony | `[sync]`, `[done]` commands | None |
| Multi-machine | Pull before work | Just open |

## What Changes in AGENTS.md

**Remove:**
- `[done]` - No git commit/push needed
- `[sync]` - No git pull needed

**Keep:**
- `[new]` - Scaffold task directory
- `[continue]` - Find task, read context
- `[note]` - Append to scratch.md
- `[q]` - Quick questions

**Simplified lifecycle:**
1. Open folder in VSCode
2. Run agent in terminal
3. Work gets saved to files
4. Cloud syncs automatically
5. Done

## Tradeoffs

**Advantages:**
- Zero friction for sync/save
- No git knowledge required
- Works immediately on any machine with cloud client
- Simpler mental model

**Disadvantages:**
- No semantic versioning ("this is v1.0")
- Can't easily revert to specific point
- Conflict resolution is opaque
- No offline-first guarantee (depends on cloud client)
- **Large data handling** - see below

## Large Data Problem

Git's `.gitignore` gives precise control over what gets tracked. Cloud sync services vary:

| Service | Ignore Support |
|---------|----------------|
| **Syncthing** | `.stignore` - full pattern matching (like gitignore) |
| **Dropbox** | Folder-level selective sync only, unofficial `.dropboxignore` |
| **Google Drive** | No ignore mechanism |
| **OneDrive** | No ignore patterns |

**Workarounds:**

1. **Use Syncthing** - P2P sync with proper ignore patterns
   ```
   # .stignore
   data/
   *.parquet
   *.csv
   __pycache__/
   .venv/
   ```

2. **Structure around it** - Keep heavy data outside synced tree
   ```
   ~/Dropbox/llm-tasks/     ← Synced (notes, plans, scripts)
   ~/local/llm-data/        ← Not synced (large outputs)
   ```

3. **Hybrid approach** - Cloud sync for light work, git for data-heavy tasks

4. **Task-specific** - Some tasks in synced folder, data-heavy tasks elsewhere

## When to Use Which

| Scenario | Recommendation |
|----------|----------------|
| Personal knowledge work | Cloud sync |
| Shared/collaborative | Git (explicit coordination) |
| Need version history | Git |
| Quick experiments | Cloud sync |
| Publishing/releasing | Git |
| **Large data processing** | Git (or Syncthing with .stignore) |
| Notes + light scripts | Cloud sync |

## VSCode as Unified Interface

VSCode provides everything needed:

- **Markdown preview** - Ctrl+Shift+V or side-by-side (Ctrl+K V)
- **Integrated terminal** - Run Claude Code, opencode, etc.
- **File explorer** - Navigate tasks/
- **Search** - Ctrl+Shift+F across all files
- **Git integration** - Available if needed later

No need for separate tools (Obsidian, dedicated markdown editors).

## Migration Path

Can start with cloud sync and add git later if needed:

1. Start with Dropbox/Google Drive
2. If versioning becomes important: `git init`
3. Git and cloud sync can coexist (just gitignore cloud metadata)
