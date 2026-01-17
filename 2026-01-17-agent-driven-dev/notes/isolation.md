# Isolation Options for Agent-Driven Development

## TL;DR Recommendation

For Ralph loop with Claude Code Max:

1. **Simplest**: Docker Sandbox (`docker sandbox run claude-code`)
2. **Most control**: DevContainer with `--dangerously-skip-permissions`
3. **Lightest**: Native sandbox (`/sandbox` command) - but less isolation

## Option 1: Docker Sandboxes (Recommended)

Docker Desktop 4.50+ includes native agent sandboxing.

### Setup

```bash
docker sandbox run claude-code
```

First run authenticates and stores credentials in a Docker volume.

### Features

- Mounts workspace at same absolute path
- Preserves Git attribution (your commits)
- One sandbox per workspace, reuses across sessions
- Runs with `--dangerously-skip-permissions` by default
- Includes: Docker CLI, gh, Node.js, Go, Python 3, Git, ripgrep, jq

### Pros

- Zero config, just works
- Official Docker support
- Agent runs as non-root with sudo access
- Full isolation from host

### Cons

- Experimental, may change
- Docker Desktop required
- Limited customization without recreating sandbox

## Option 2: DevContainer

Roll your own container with more control.

### Setup

1. Install Docker Desktop
2. Add `.devcontainer/` folder to project (copy from anthropics/claude-code repo)
3. Open project → "Reopen in Container"
4. Run `claude --dangerously-skip-permissions`

### Pros

- Full control over environment
- Can customize tooling, dependencies
- Works with VS Code / Cursor

### Cons

- More setup effort
- Must maintain devcontainer config
- Can't run emulators/simulators inside

## Option 3: Native Claude Code Sandbox

Built-in OS-level sandboxing (Linux: bubblewrap, macOS: Seatbelt).

### Setup

Run `/sandbox` command in Claude Code, select auto-allow mode.

Or configure in `settings.json`:

```json
{
  "sandbox": {
    "allowUnsandboxedCommands": false
  }
}
```

### Features

- **Filesystem**: Write only to CWD, read anywhere (except denied)
- **Network**: Only approved domains
- Reduces permission prompts by ~84%

### Pros

- No Docker required
- Lightweight, minimal overhead
- Fine-grained path/domain control

### Cons

- Shares host kernel (less isolation than VM/container)
- Some tools incompatible (Docker, Watchman)
- Not as strong as full container isolation

## Comparison

| Aspect | Docker Sandbox | DevContainer | Native Sandbox |
| --- | --- | --- | --- |
| Isolation level | High (container) | High (container) | Medium (OS-level) |
| Setup effort | Minimal | Moderate | Minimal |
| Customization | Low | High | Medium |
| Docker required | Yes | Yes | No |
| Ralph loop ready | Yes | Yes | Partial |
| Full permissions | Yes (default) | Yes (flag) | No (still prompts) |

## For Ralph Loop Specifically

**Docker Sandbox** is ideal because:

- Agent needs full bash/file access → container provides this safely
- `--dangerously-skip-permissions` enabled by default
- No approval prompts = uninterrupted loop execution
- If agent goes haywire, only container affected

**Native Sandbox** might still prompt for some operations, breaking the loop.

## Security Notes

Container isolation means:

- Agent can't touch host filesystem (except mounted project)
- Agent can't steal SSH keys, credentials outside project
- Agent can't phone home to arbitrary servers
- Worst case: nuke the container, start fresh

## Sources

- [Docker Sandboxes Docs](https://docs.docker.com/ai/sandboxes)
- [Claude Code Sandboxing](https://code.claude.com/docs/en/sandboxing)
- [DevContainer Guide](https://codewithandrea.com/articles/run-ai-agents-inside-devcontainer/)
- [Docker Blog - Agent Safety](https://www.docker.com/blog/docker-sandboxes-a-new-approach-for-coding-agent-safety/)
