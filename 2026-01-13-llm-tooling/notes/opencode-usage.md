# Opencode Usage Notes

Observations from using opencode for this research task itself (meta-experiment).

## Setup

- **Tool**: opencode
- **Model**: Claude Opus 4.5 (via GitHub Copilot)
- **Task**: Research on LLM tooling for knowledge work

## Agents: The Core Abstraction

Opencode uses **agents** as its primary customization mechanism. What we called "modes" are actually different agents.

### Agent Types

1. **Primary agents** - Main assistants you interact with directly
   - Switch between them with **Tab** key
   - Have full conversation context

2. **Subagents** - Specialized assistants invoked for specific tasks
   - Called via `@mention` or automatically by primary agents
   - Run as child sessions

### Built-in Agents

| Agent | Type | Purpose |
|-------|------|---------|
| **Build** | Primary | Full development with all tools enabled |
| **Plan** | Primary | Read-only analysis and planning (file edits and bash set to "ask") |
| **General** | Subagent | Multi-step research and complex tasks |
| **Explore** | Subagent | Fast codebase exploration |

### Observed Workflow
1. Started in **Plan** agent - explored task files, discussed direction
2. When ready to capture findings, switched to **Build** agent
3. Agent then wrote/updated documentation files

**Insight**: This mirrors the explore → capture pattern from knowledge work. Plan for thinking, Build for doing.

## System Prompt Architecture (From Source)

Explored `~/code/others/opencode` source code.

### Prompt Files Location

`packages/opencode/src/session/prompt/`:

| File | Purpose |
|------|---------|
| `anthropic.txt` | Base system prompt for Anthropic models |
| `plan.txt` | Plan mode reminder (injected as `<system-reminder>`) |
| `plan-reminder-anthropic.txt` | Extended plan mode with phases and plan file |
| `build-switch.txt` | Injected when switching from Plan to Build |
| `codex.txt` | System prompt for Codex models |
| `gemini.txt`, `qwen.txt` | Model-specific prompts |

### How Agents Work

1. **Base prompt** (`anthropic.txt`) - Always present, defines core behavior
2. **Custom agent prompt** - Appended from agent config (markdown body)
3. **System reminders** - Injected per-message via `<system-reminder>` tags

### Plan Mode Implementation

The `plan.txt` file shows the actual Plan mode prompt:

```
CRITICAL: Plan mode ACTIVE - you are in READ-ONLY phase. STRICTLY FORBIDDEN:
ANY file edits, modifications, or system changes...

Your current responsibility is to think, read, search, and delegate explore
agents to construct a well-formed plan...
```

The `plan-reminder-anthropic.txt` is more sophisticated with phases:
1. Initial Understanding (parallel Explore agents)
2. Planning (Plan subagent)
3. Synthesis (ask user questions)
4. Final Plan (write plan file)
5. ExitPlanMode

### Build Switch

When switching Plan → Build, `build-switch.txt` is injected:

```xml
<system-reminder>
Your operational mode has changed from plan to build.
You are no longer in read-only mode.
You are permitted to make file changes, run shell commands...
</system-reminder>
```

### Permission System in Action

When I tried to edit a file in Plan mode, the system blocked it:

```
Error: The user has specified a rule which prevents you from using this specific tool call.
Rules: [{"permission":"edit","pattern":"*","action":"deny"},
        {"permission":"edit","pattern":".opencode/plan/*.md","action":"allow"}]
```

This shows:
- Plan mode denies `edit` for all files (`*`)
- Exception: `.opencode/plan/*.md` files can still be edited
- Matches behavior described in `plan-reminder-anthropic.txt`

### Example Agents (From Opencode Repo)

Located in `.opencode/agent/`:

**docs.md** - Primary agent for documentation:
```markdown
---
description: ALWAYS use this when writing docs
color: "#38A3EE"
---
You are an expert technical documentation writer
You are not verbose
Use a relaxed and friendly tone
...
```

**triage.md** - Hidden agent for GitHub issues:
```markdown
---
mode: primary
hidden: true
model: opencode/claude-haiku-4-5
tools:
  "*": false
  "github-triage": true
---
You are a triage agent responsible for triaging github issues.
...
```

**Key patterns:**
- `hidden: true` - Agent exists but not shown in Tab cycling
- `tools: {"*": false}` - Disable all tools, then enable specific ones
- Custom MCP tools (`github-triage`, `github-pr-search`)

### Example Commands (From Opencode Repo)

Located in `.opencode/command/`:

**commit.md** - Commit workflow:
```markdown
---
description: git commit and push
model: opencode/glm-4.6
subtask: true  # Runs as subagent to avoid polluting context
---
commit and push
make sure it includes a prefix like docs: tui: core: ci:
...
```

**rmslop.md** - Remove AI-generated code patterns:
```markdown
---
description: Remove AI code slop
---
Check the diff against dev, and remove all AI generated slop...
- Extra comments that a human wouldn't add
- Extra defensive checks or try/catch blocks
- Casts to any to get around type issues
...
```

**issues.md** - Search GitHub issues:
```markdown
---
description: "find issue(s) on github"
model: opencode/claude-haiku-4-5
---
Search through existing issues using the gh cli to find issues matching:
$ARGUMENTS
...
```

## Custom Agents

Agents can be defined in two ways:

### 1. JSON Configuration (opencode.json)

```json
{
  "agent": {
    "research": {
      "description": "Research and verify information from sources",
      "mode": "primary",
      "model": "anthropic/claude-sonnet-4-20250514",
      "tools": {
        "write": false,
        "edit": false,
        "bash": false,
        "webfetch": true
      },
      "prompt": "You are a research assistant. Focus on gathering and verifying information."
    }
  }
}
```

### 2. Markdown Files

Place in `~/.config/opencode/agent/` (global) or `.opencode/agent/` (per-project):

```markdown
---
description: Research and verify information
mode: primary
tools:
  write: false
  edit: false
  webfetch: true
permission:
  bash: deny
---

You are a research assistant focused on gathering and verifying information.
When making claims, cite sources. Be skeptical of unverified information.
```

### Agent Options

| Option | Purpose |
|--------|---------|
| `description` | When to use this agent (shown in UI, used by model) |
| `mode` | `primary`, `subagent`, or `all` |
| `model` | Override the default model |
| `tools` | Enable/disable specific tools |
| `permission` | Fine-grained control (`ask`, `allow`, `deny`) |
| `prompt` | Custom system prompt |
| `temperature` | Control creativity (0.0-1.0) |
| `maxSteps` | Limit agentic iterations |

## Custom Commands

Commands are prompt templates triggered by `/command`:

### Example: Research Command

`.opencode/command/research.md`:
```markdown
---
description: Research a topic with source verification
agent: plan
---

Research the following topic: $ARGUMENTS

Focus on:
1. Finding authoritative sources
2. Verifying claims against documentation
3. Noting any uncertainties or conflicts

Structure findings as markdown notes.
```

Usage:
```
/research reverb parameters in audio production
```

### Command Features

- **Arguments**: `$ARGUMENTS`, `$1`, `$2`, etc.
- **Shell output**: `` !`git log --oneline -5` `` injects command output
- **File references**: `@src/file.ts` includes file content
- **Agent override**: Run command with specific agent
- **Subtask mode**: Run as subagent to avoid polluting context

## Potential Custom Agents for Knowledge Work

Based on our research patterns, these agents could be useful:

### 1. Research Agent (Primary)

```markdown
---
description: Gather information and verify against sources
mode: primary
tools:
  write: false
  edit: false
  webfetch: true
permission:
  bash: deny
---

You are a research assistant. Your job is to gather information and verify claims.

Guidelines:
- Always cite sources when making factual claims
- Use webfetch to verify information against official documentation
- Be explicit about uncertainty
- Structure findings clearly for later synthesis
```

### 2. Verify Agent (Subagent)

```markdown
---
description: Verify claims against authoritative sources
mode: subagent
tools:
  write: false
  edit: false
  webfetch: true
---

Verify the following claims against authoritative sources.
For each claim, indicate:
- VERIFIED: Found in official documentation
- UNVERIFIED: Could not find authoritative source
- CONTRADICTED: Official docs say something different
```

### 3. Synthesize Agent (Primary)

```markdown
---
description: Synthesize research into structured documents
mode: primary
tools:
  write: true
  edit: true
  webfetch: false
permission:
  bash: deny
---

You are synthesizing research into structured documentation.
Focus on clarity, organization, and actionable information.
Do not make new claims - only organize and present verified information.
```

## Things That Worked Well

1. **Filesystem as context** - Could read task files, previous notes, example outputs
2. **Iterative refinement** - Updated README, plan.md, created new notes
3. **Agent switching** - Natural transition from exploration to documentation
4. **Conversation flow** - Felt like chat, but with file artifacts
5. **Webfetch for verification** - Could check documentation during research

## Friction Points

- Terminal scrolling for long outputs (e.g., reading the 900-line bass-tone.md)
- Navigation between related files during exploration
- TODO: Continue documenting friction during use

## Meta-Observations from This Session

### Plan/Build Workflow in Practice

The session demonstrated the Plan → Build workflow naturally:

1. **Started in Plan mode** - Explored task files, discussed problem framing
2. **Switched to Build** - Captured findings in documentation
3. **Switched back to Plan** - Continued exploration (reading opencode source)
4. **Permission denied** - Tried to edit file in Plan mode, system blocked it
5. **Switched to Build** - Documented the permission system observation

This is exactly the explore → capture pattern we identified for knowledge work.

### Local Source as Documentation

Instead of fetching docs from the web, we read the opencode source directly:
- `~/code/others/opencode/.opencode/agent/` - Real-world agent examples
- `~/code/others/opencode/packages/opencode/src/session/prompt/` - Actual prompts
- `~/code/others/opencode/packages/web/src/content/docs/` - Website documentation source

This is more authoritative than web docs and demonstrates a key agent capability: direct filesystem access to arbitrary local resources.

### The `/rmslop` Command

The opencode team has a command to "remove AI code slop" - patterns like:
- Extra comments a human wouldn't add
- Unnecessary defensive checks
- Type casts to `any`
- Style inconsistencies

This acknowledges that AI-generated code has recognizable patterns that need cleanup. Worth noting for our own workflows.

## Next Steps

1. **Create custom agents** for research workflows
2. **Create custom commands** for common research tasks (e.g., `/verify`, `/synthesize`)
3. **Test the workflow** with a new research task
4. **Compare UX** with consumer chat for similar tasks
