# LLM Tooling for Knowledge Work

Exploring how to improve LLM-assisted knowledge work - specifically, deep inquiry and documentation workflows that go beyond simple Q&A.

## The Problem

**Observation**: Local agents with tool access (Claude Code, opencode) produce significantly better results for deep inquiry than consumer chat interfaces - even for non-coding tasks like researching audio production workflows.

**Example**: The `tasks/2026-01-07-ableton-document/` task used a "coding assistant" to:
- Research Ableton Live workflows with personal context (Linux background, specific gear)
- Verify LLM claims against official documentation
- Build structured, verified reference documents
- Iterate and refine across multiple sessions

This would be difficult or impossible with consumer chat:
- Context evaporates between sessions
- No tool access for source verification
- Output is ephemeral (buried in chat history)
- Can't iterate on structured documents

**The tension**: Web chat has better UX for conversation, but local agents have the capabilities needed for deep work.

## Questions to Answer

1. **Can consumer chat apps be made to work?** What features exist (Projects, Artifacts, Memory)? What's fundamentally missing?

2. **If local agents are necessary, can the interface be improved?** Terminal UX is inferior for extended reading/writing. What alternatives exist?

3. **What's the minimal viable setup?** What capabilities are actually required vs. nice-to-have for these workflows?

## Approach

1. Document what makes local agents effective for knowledge work
2. Survey consumer chat capabilities and gaps
3. Explore web-based agent interfaces (Open WebUI, LibreChat, etc.)
4. Evaluate hybrid approaches

## Notes

- `notes/llm-tools-api.md` - How function calling works at the API level
- `notes/claude-code-skills.md` - Claude Code's skill system and progressive disclosure
- `notes/knowledge-work-patterns.md` - What makes local agents effective for deep inquiry
- `notes/opencode-usage.md` - Observations from using opencode for this research (meta-experiment)
- `notes/workflow-patterns.md` - Essential patterns: mode switching, rewinding, context hygiene
- `notes/opencode-compaction.md` - How opencode manages context window limits (two-tier: pruning + summarization)
