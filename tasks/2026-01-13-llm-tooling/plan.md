# Plan: Understanding LLM Tooling Internals

## Problem Statement

Claude Code is a powerful agentic coding assistant, but its internals are closed. To build mental models of how such systems work - and potentially build custom tooling - we need to study open implementations.

**Key questions:**
1. How are system prompts structured for agentic behavior?
2. How are tools defined, registered, and executed?
3. How do subagents work (spawning, context passing, coordination)?
4. How is context managed across multi-step interactions?
5. What patterns are common vs. implementation-specific?

## Reference Implementation

**opencode** - https://github.com/opencode-ai/opencode

An open-source AI-powered coding CLI written in Go. Chosen because:
- Fully open source (can read everything)
- Similar feature set to Claude Code
- Active development
- Clean codebase

## Exploration Areas

### 1. System Prompt Architecture
- [ ] Locate and analyze the main system prompt
- [ ] Identify how tool descriptions are injected
- [ ] Study prompt structure (persona, rules, capabilities)
- [ ] Compare with Claude Code's observable behavior

### 2. Tool Implementation
- [ ] Map out all built-in tools (Read, Write, Bash, etc.)
- [ ] Understand tool registration/discovery mechanism
- [ ] Study tool execution flow (validation, execution, result handling)
- [ ] Analyze error handling and retry patterns

### 3. Subagent Architecture
- [ ] Identify how/when subagents are spawned
- [ ] Study context passing between agents
- [ ] Understand agent coordination patterns
- [ ] Analyze resource/token management across agents

### 4. Context Management
- [ ] Study conversation history handling
- [ ] Understand summarization strategies (if any)
- [ ] Analyze file/codebase context injection
- [ ] Study how large contexts are managed

### 5. Provider Abstraction
- [ ] How multiple LLM providers are supported
- [ ] Tool schema translation between providers
- [ ] Streaming implementation
- [ ] Rate limiting and error handling

## Outputs

- Annotated notes on each exploration area
- Architecture diagrams where helpful
- Comparison notes: opencode vs. Claude Code (observed)
- Potentially: small experimental scripts testing specific patterns

## Resources

- [opencode source](https://github.com/opencode-ai/opencode)
- [Vercel AI SDK](https://github.com/vercel/ai) - tool schema translation layer
- [Anthropic Tool Use docs](https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview)
- [OpenAI Function Calling docs](https://platform.openai.com/docs/guides/function-calling)

## Progress

_To be updated as exploration proceeds._
