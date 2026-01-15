# Agent Permission Systems Comparison

How local coding agents handle permissions/approvals - critical for long-running autonomous tasks.

## The Core Problem

For long autonomous tasks, agents get **blocked waiting for user approval**. This interrupts workflow and wastes time. Solutions vary by agent:

1. **Auto-approve everything** (dangerous)
2. **Granular permission rules** (pre-approve safe patterns)
3. **Notification hooks** (alert user when blocked)
4. **Sandboxing** (let agent run freely in isolated environment)

---

## Claude Code

### Permission Modes

| Mode | Behavior |
|------|----------|
| `default` | Ask for most operations |
| `plan` | Read-only analysis |
| `acceptEdits` | Auto-approve file edits, ask for bash |
| `dontAsk` | Auto-approve common operations |
| `bypassPermissions` | Skip all approvals (use `--dangerously-skip-permissions`) |

### Granular Permissions in settings.json

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run lint)",
      "Bash(npm run test:*)",
      "Read(~/.zshrc)"
    ],
    "deny": [
      "Bash(curl:*)",
      "Read(./.env)"
    ]
  }
}
```

**Note:** Bash rules use prefix matching (not regex), and can be bypassed.

### Notification Hooks (Your Solution!)

Claude Code has a `Notification` hook event that fires when:
- `permission_prompt` - Claude needs permission approval (blocked, needs attention)
- `idle_prompt` - Claude finished task and waiting for next instruction (60+ seconds idle) - **useful for task completion alerts!**
- `auth_success` - Authentication completed
- `elicitation_dialog` - MCP tool needs input

**Two key use cases:**
1. **Blocked notification** (`permission_prompt`) - Alert when Claude can't proceed
2. **Task complete notification** (`idle_prompt`) - Alert when Claude finished and is ready for next task

**Example notification hook configuration:**
```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "permission_prompt",
        "hooks": [{
          "type": "command",
          "command": "/path/to/permission-alert.sh"
        }]
      },
      {
        "matcher": "idle_prompt", 
        "hooks": [{
          "type": "command",
          "command": "/path/to/idle-notification.sh"
        }]
      }
    ]
  }
}
```

The hook receives JSON via stdin with:
```json
{
  "session_id": "abc123",
  "hook_event_name": "Notification",
  "message": "Claude needs your permission to use Bash",
  "notification_type": "permission_prompt"
}
```

This enables desktop notifications, Slack alerts, etc. when Claude is blocked.

### Other Hook Events

- `PreToolUse` / `PostToolUse` - Intercept/validate tool calls
- `Stop` / `SubagentStop` - Control when agent should stop
- `SessionStart` / `SessionEnd` - Setup/cleanup
- `UserPromptSubmit` - Validate/augment user prompts

### Sandboxing

Claude Code has an optional sandbox mode:
```json
{
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "excludedCommands": ["git", "docker"]
  }
}
```

When sandboxed, bash commands can auto-approve since they're isolated.

---

## OpenCode

### Permission System

Three actions per tool: `"allow"`, `"ask"`, `"deny"`

```json
{
  "permission": {
    "*": "ask",
    "bash": "allow",
    "edit": "deny"
  }
}
```

### Granular Bash Permissions

```json
{
  "permission": {
    "bash": {
      "*": "ask",
      "git *": "allow",
      "npm *": "allow", 
      "rm *": "deny"
    }
  }
}
```

Last matching rule wins - put catch-all `*` first, specific rules after.

### "Always" Approval in UI

When prompted, you can choose:
- `once` - approve just this request
- `always` - approve future matching requests (session-scoped)
- `reject` - deny the request

### Per-Agent Permissions

```json
{
  "agent": {
    "build": {
      "permission": {
        "bash": {
          "*": "ask",
          "git push": "allow"
        }
      }
    }
  }
}
```

### Defaults

- Most permissions default to `"allow"` (more permissive than Claude Code)
- `doom_loop` and `external_directory` default to `"ask"`
- `.env` files denied by default

### Notification System - In Progress!

OpenCode has a **plugin hook system** but lacks built-in notification hooks like Claude Code. However, there's active development:

**Existing Plugin Hooks** (`packages/plugin/src/index.ts`):
- `event` - Subscribe to all bus events (including `session.idle`)
- `permission.ask` - Intercept permission requests
- `tool.execute.before` / `tool.execute.after` - Tool lifecycle
- `chat.message`, `chat.params` - Message handling
- `experimental.text.complete` - Text completion events

**The `session.idle` event exists!** (in `session/status.ts`)
- Fires when session transitions to idle state
- Plugins can subscribe via the `event` hook

**Active Issues & PRs:**

1. **Issue #5515** - "[FEATURE]: Finish hook, when LLM is ready for new instructions"
   - Requests notification when task completes (exactly what we want)
   - Assigned to core team

2. **Issue #213** - "[feature request] notifications"
   - Early feature request referencing Claude Code's notifications

3. **PR #7672** - "feat: add notify hook system with input_required and timeout support"
   - Adds `input_required` hook type for notifications
   - Closes #5515
   - Status: Open, under review

4. **PR #6755** - "feat(cli): emit OSC 9 notifications for responses"
   - Terminal-level notifications (works with terminal emulators)
   - Aligns with Codex/Claude Code behavior

5. **Ecosystem Plugins** (community-built):
   - **opencode-message-notify** (PR #7785) - iOS notifications via Bark app
   - **opencode-ntfy** (PR #7865) - Cross-platform notifications via ntfy.sh

**Current Workaround:**
Create a plugin that subscribes to `session.idle` events:

```typescript
import type { Plugin } from "@opencode-ai/plugin"

const notifyPlugin: Plugin = async (input) => ({
  event: async ({ event }) => {
    if (event.type === "session.idle") {
      // Send notification (desktop, Slack, etc.)
      await fetch("https://ntfy.sh/your-topic", {
        method: "POST",
        body: "OpenCode task completed!"
      })
    }
  }
})

export default notifyPlugin
```

**Bottom line:** OpenCode is close to having full notification support. The `session.idle` event already exists - it just needs better exposure via hooks or built-in notification support.

---

## Codex CLI (OpenAI)

### Sandbox + Approval Two-Layer System

**Sandbox modes:**
- `read-only` - Can only read files
- `workspace-write` - Can edit files in workspace (default for git repos)
- `danger-full-access` - No sandbox (requires explicit flag)

**Approval policies:**
- `on-request` - Ask for permission when needed (default)
- `untrusted` - Ask before any command
- `on-failure` - Only ask on failures
- `never` - Never ask

### Common Combinations

| Intent | Flags |
|--------|-------|
| Auto (default) | `--full-auto` |
| Safe read-only | `--sandbox read-only --ask-for-approval on-request` |
| CI read-only | `--sandbox read-only --ask-for-approval never` |
| Full autonomy | `--dangerously-bypass-approvals-and-sandbox` (alias: `--yolo`) |

### config.toml Configuration

```toml
approval_policy = "on-request"
sandbox_mode = "workspace-write"

[sandbox_workspace_write]
network_access = false

[profiles.full_auto]
approval_policy = "on-request"
sandbox_mode = "workspace-write"
```

### No Notification Hooks

Codex CLI **does not have notification hooks**. For long tasks:
1. Use `--full-auto` for known-safe operations
2. Use `--ask-for-approval never` with appropriate sandbox
3. Run in containers for dangerous operations

### Enterprise Managed Config

Admins can enforce requirements:
```toml
# /etc/codex/requirements.toml
allowed_approval_policies = ["on-request", "on-failure"]
allowed_sandbox_modes = ["read-only", "workspace-write"]
```

---

## Gemini CLI (Google)

### Trust-Based System

Gemini CLI uses a **folder trust** model (similar to VS Code):
- Trusted folders: Full functionality
- Untrusted folders: "Safe mode" restrictions

Enable in settings:
```json
{
  "security": {
    "folderTrust": {
      "enabled": true
    }
  }
}
```

### Untrusted Mode Restrictions

When untrusted:
- Workspace settings ignored
- `.env` files not loaded
- Extensions management restricted
- Tool auto-acceptance disabled
- MCP servers don't connect
- Custom commands not loaded

### Sandboxing

Gemini CLI has proper sandboxing:
```bash
# Enable with flag
gemini -s -p "analyze code"

# Or environment variable
export GEMINI_SANDBOX=true

# Or in settings.json
{"tools": {"sandbox": "docker"}}
```

Sandbox methods:
- macOS Seatbelt (`sandbox-exec`)
- Docker/Podman containers

### No Notification Hooks

Gemini CLI **does not have notification hooks**. For autonomous work:
1. Trust the folder
2. Enable sandboxing for safety
3. Use headless mode for CI/automation

---

## Comparison Summary

| Feature | Claude Code | OpenCode | Codex CLI | Gemini CLI |
|---------|-------------|----------|-----------|------------|
| **Permission Granularity** | High (pattern matching) | High (glob patterns) | Medium (modes) | Low (trust-based) |
| **Notification Hooks** | Yes (blocked + task complete) | Partial (via plugin) | No | No |
| **Sandboxing** | Optional | No | Built-in | Optional |
| **Full Auto Mode** | `bypassPermissions` | `"allow"` all | `--yolo` | Trust + sandbox |
| **Per-Pattern Rules** | Yes (prefix match) | Yes (glob) | No | No |
| **Session Memory** | Via hooks | `always` choice | No | No |

---

## Recommendations for Long Tasks

### Claude Code (Best for Autonomy)
1. Use notification hooks to alert when blocked
2. Pre-configure known-safe patterns in `allow` list
3. Consider `acceptEdits` mode for file operations
4. Use sandbox + `autoAllowBashIfSandboxed` for safe automation

### OpenCode
1. Configure generous `allow` patterns for common operations
2. Use `always` approval liberally during sessions
3. **Use plugin system** to subscribe to `session.idle` events for notifications
4. Watch PR #7672 for native notification hook support
5. Try community plugins: `opencode-message-notify`, `opencode-ntfy`

### Codex CLI
1. Use `--full-auto` for normal development
2. Use `--ask-for-approval never` with `workspace-write` sandbox for automation
3. Run long tasks in containers for safety

### Gemini CLI
1. Trust your development folders
2. Enable sandboxing for risky operations
3. Use headless mode for automation

---

## Key Insight

**Claude Code has the most mature notification system** with dedicated hooks for:
1. **Blocked alerts** (`permission_prompt`) - Know when agent needs approval
2. **Task complete alerts** (`idle_prompt`) - Know when agent finished and is ready for next task

**OpenCode is catching up** - the `session.idle` event exists and can be used via plugins. PR #7672 adds native `input_required` notification hooks. Community plugins already provide iOS and ntfy.sh integrations.

For Codex CLI and Gemini CLI, you still need:
- More permissive defaults (higher risk)
- Sandboxing (reduced capability)
- Being present during execution

A potential improvement for OpenCode would be to add a similar notification/hook system.
