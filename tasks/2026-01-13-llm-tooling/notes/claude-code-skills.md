# Claude Code Skills

## Overview

Skills are **model-invoked capabilities** that Claude automatically discovers and uses based on your request. Unlike slash commands (which require explicit `/command` invocation), Claude intelligently recognizes when a skill is relevant.

## How Skills Work

1. **Discovery** - Claude loads only skill names/descriptions at startup (minimal tokens)
2. **Activation** - When your request matches a skill's description, Claude asks permission
3. **Execution** - Claude follows the skill's instructions, loading referenced files as needed

## Creating Custom Skills

Skills live in `.claude/skills/` directories with a `SKILL.md` file:

```
~/.claude/skills/my-skill/
└── SKILL.md
```

### Basic Example

```yaml
---
name: explaining-code
description: Explains code with diagrams and analogies. Use when asking "how does this work?"
allowed-tools: Read, Grep
---

When explaining code:
1. Start with an analogy
2. Draw ASCII diagrams
3. Walk through step-by-step
```

### Skill Locations

| Location | Path | Scope |
|----------|------|-------|
| Personal | `~/.claude/skills/` | You, all projects |
| Project | `.claude/skills/` | Team members |

## Context Efficiency (Progressive Disclosure)

Skills use a **three-tier progressive disclosure** system to optimize context usage:

| Level | What's Loaded | When |
|-------|---------------|------|
| 1 | Skill name + description only | At startup (~50-100 tokens per skill) |
| 2 | Full `SKILL.md` content | When Claude determines skill is relevant |
| 3+ | Supporting files (`reference.md`, etc.) | On-demand during execution |

Key insight from Anthropic:
> "Agents with a filesystem and code execution tools don't need to read the entirety of a skill into their context window when working on a particular task. This means that the amount of context that can be bundled into a skill is effectively unbounded."

### Multi-file Structure

```
my-skill/
├── SKILL.md           # Always loaded when activated (~500 lines max)
├── reference.md       # Loaded ONLY when Claude needs it
├── examples.md        # Loaded ONLY when referenced
└── scripts/
    └── helper.py      # Executed, never loaded into context
```

In `SKILL.md`, reference supporting files:
```markdown
For API details, see [reference.md](reference.md)
```

Claude reads `reference.md` **only when the task requires it**.

## Skills vs Slash Commands

| Feature | Skills | Slash Commands |
|---------|--------|----------------|
| Invocation | Automatic (Claude decides) | Explicit (`/command`) |
| Structure | Directory + SKILL.md | Single .md file |
| Best for | Complex, auto-discovered workflows | Quick, frequently-used prompts |

## Configuration Options

| Option | Purpose |
|--------|---------|
| `name` | Required. Lowercase with hyphens (max 64 chars) |
| `description` | Required. Tells Claude when to use this skill (max 1024 chars) |
| `allowed-tools` | Restrict available tools (e.g., `Read, Grep, Bash(git:*)`) |
| `model` | Specify Claude model to use |

## Benefits

1. **Automatic discovery** - No need to remember commands
2. **Team standardization** - Commit to repo for shared workflows
3. **Complex workflows** - Include scripts, reference files, validation
4. **Context efficiency** - Progressive disclosure keeps context small
5. **Consistency** - Ensures practices applied uniformly

## Official Documentation

- [Agent Skills - Claude Code Docs](https://code.claude.com/docs/en/skills)
- [Agent Skills Overview - Claude Platform Docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) (Anthropic Engineering Blog - covers progressive disclosure)
- [Building Skills for Claude Code](https://claude.com/blog/building-skills-for-claude-code)
- [Using Agent Skills with the API](https://platform.claude.com/docs/en/build-with-claude/skills-guide)
