# LLM Tooling

Understanding how agentic LLM applications work under the hood - system prompts, tool wiring, subagent architecture, and the orchestration layer between raw LLM APIs and useful agents.

## Motivation

**Local agents with tool access are fundamentally more capable than consumer chat interfaces** - even for non-coding tasks. The combination of filesystem access, arbitrary tool execution, and agentic loops enables knowledge work that chat UIs cannot match. This repository itself demonstrates the pattern: using a "coding assistant" for research, documentation, and planning tasks.

Understanding the internals helps us:
1. Use these tools more effectively
2. Build custom tooling for specific workflows
3. Recognize what's possible vs. what's implementation-specific

As a heavy Claude Code user, the internals remain opaque (closed source). [opencode](https://github.com/opencode-ai/opencode) provides a fully open-source alternative, making it possible to study:

- System prompt construction
- Tool/function calling implementation
- Subagent spawning and coordination
- Context management strategies
- The full request-response lifecycle

## Approach

Use opencode as a reference implementation to reverse-engineer patterns applicable to any agentic LLM system, then validate understanding against Claude Code's observable behavior.

## Notes

- `notes/llm-tools-api.md` - How function calling works at the API level
- `notes/claude-code-skills.md` - Claude Code's skill system and progressive disclosure
