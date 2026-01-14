# Plan: LLM Tooling for Knowledge Work

## Problem Statement

Consumer chat interfaces (Claude.ai, ChatGPT) have good UX but produce worse results for deep inquiry compared to local agents with tool access. The goal is to find or build a better solution that combines:

- **Good conversational UX** (web chat-like)
- **Tool capabilities** (file access, web fetch, verification)
- **Persistent artifacts** (structured documents that survive sessions)

## Concrete Use Case

**Deep inquiry workflow** (exemplified by `tasks/2026-01-07-ableton-document/`):

1. **Exploration** - Ask questions about a new domain with personal context
2. **Verification** - Cross-reference LLM responses against authoritative sources
3. **Synthesis** - Build structured documents combining verified knowledge + personal context
4. **Iteration** - Refine and expand documents across multiple sessions

**Why local agents excel at this:**
- Can read/write files (persistent artifacts)
- Can fetch and verify against sources
- Can run scripts (e.g., convert documentation formats)
- Context accumulates in filesystem, not just conversation

**Why consumer chat falls short:**
- No filesystem access
- No web fetching (or limited)
- Artifacts are ephemeral (must copy-paste)
- Context resets between sessions (memory features are limited)

## Research Areas

### 1. Consumer Chat Capabilities Assessment

Evaluate what's actually possible with current consumer offerings:

- [ ] **Claude.ai Projects** - File upload, project context, artifacts
- [ ] **ChatGPT Canvas** - Document editing experience
- [ ] **Claude Artifacts** - Code/document generation and iteration
- [ ] **Memory features** - Cross-session context persistence
- [ ] **MCP in Claude Desktop** - Does this bridge the gap?

**Key question**: Can any combination of these features approximate the local agent workflow?

### 2. Web-Based Agent Interfaces

Survey alternatives that provide chat UX with agent capabilities:

- [ ] **Open WebUI** - Self-hosted, supports tools/functions
- [ ] **LibreChat** - Multi-provider, plugin support
- [ ] **LobeChat** - Modern UI, plugin ecosystem
- [ ] **Anything LLM** - Document-focused, RAG capabilities
- [ ] **Anthropic Claude API + custom UI** - Build something minimal

**Key question**: Do any of these support the tool access needed for verification/file workflows?

### 3. Hybrid Approaches

Explore workflows that combine chat + agent:

- [ ] **Chat for exploration, agent for execution** - Use chat to think, agent to do
- [ ] **Agent with web UI** - Run opencode/similar with a web frontend
- [ ] **Custom MCP servers** - Add capabilities to Claude Desktop

### 4. Other CLI Agents

Compare workflow support across CLI agents:

- [x] **Claude Code** - Plan mode, rewind, subagents (primary tool)
- [x] **opencode** - Plan/Build modes, undo/redo, agents/subagents (explored)
- [ ] **Codex CLI (OpenAI)** - Does it support plan mode? Rewind?
- [ ] **gemini-cli (Google)** - Does it support plan mode? Rewind?

**Key question**: Do these agents support the essential patterns (mode switching, rewinding, context hygiene)?

### 5. CI-like Autonomous Agents

Different pattern for defined tasks:

- [x] **GitHub Copilot agent** - Works well for pre-defined coding tasks
- [ ] **Could this pattern work for research?** - Pre-define scope, run autonomously, review output

**Key question**: When is autonomous execution better than interactive iteration?

### 6. Understanding What's Actually Needed

Document the minimal capabilities required:

- [x] **File read/write** - For persistent artifacts
- [x] **Web fetch** - For source verification
- [x] **Mode switching** - Plan (read-only) vs Build (full access)
- [x] **Chat rewinding** - Clean iteration, avoid context pollution
- [ ] **Session persistence** - Or filesystem as persistence layer
- [ ] **Structured output** - Markdown documents, not just chat

**Key question**: What's the simplest setup that provides these?

## Architecture Understanding (Background)

Understanding internals helps evaluate/build solutions:

### Already Documented
- `notes/llm-tools-api.md` - How function calling works at API level
- `notes/claude-code-skills.md` - Progressive disclosure and skill system

### To Explore (If Needed)
- System prompt patterns for agentic behavior
- Tool registration and execution flow
- Context management strategies
- Provider abstraction (for multi-provider solutions)

**Reference implementations:**
- [opencode](https://github.com/opencode-ai/opencode) - Open source Claude Code alternative
- [Vercel AI SDK](https://github.com/vercel/ai) - Tool schema translation

## Possible Outcomes

1. **Recommend existing solution** - Find a web-based tool that works
2. **Document a hybrid workflow** - Combine chat + agent effectively
3. **Document task-dependent patterns** - When to use interactive vs. autonomous
4. **Build minimal custom tooling** - If nothing exists, build it
5. **Create custom agents/commands** - For specific research workflows
6. **Accept the tradeoff** - Document when to use chat vs. agent

## Progress

### Session 1 (2026-01-13)

**Reframed the problem:**
- Original framing: "understand LLM tooling internals"
- Actual goal: "improve knowledge work with LLMs"
- Key insight: The question is about *interface and workflow*, not just understanding internals

**Identified the core tension:**
- Web chat = good UX, limited capabilities
- Local agents = powerful capabilities, terminal UX friction

**Meta-experiment:**
- This session itself is using opencode + Claude Opus 4.5 for research
- Started in Plan mode (read-only exploration), switched to Build mode for documentation
- Demonstrates the explore → capture workflow pattern
- See `notes/opencode-usage.md` for observations

**Opencode-specific exploration added:**
- Agents (Plan/Build) are the core abstraction, not just "modes"
- Full customization: custom agents, commands, permissions
- System-reminder injection for mid-conversation behavior changes

**Researched opencode documentation:**
- Agents can be primary (Tab to switch) or subagents (@mention)
- Custom agents via JSON config or markdown files
- Commands are prompt templates with argument support
- Rich permission system (ask/allow/deny per tool)

**Identified potential custom agents for knowledge work:**
1. **Research agent** - webfetch enabled, file write disabled
2. **Verify agent** - focused on source verification
3. **Synthesize agent** - organize verified info into documents

See `notes/opencode-usage.md` for detailed findings.

**Next steps:**
- Create and test custom agents for research workflows
- Research consumer chat capabilities (Claude Projects, MCP) for comparison
- Survey web-based agent interfaces
- Document friction points during continued use

### Session 1 Continued

**Explored opencode source directly:**
- Read prompt files at `packages/opencode/src/session/prompt/`
- Found base prompt (`anthropic.txt`), plan prompts, build-switch injection
- Understood the layered architecture: base + agent-specific + system-reminders

**Discovered real-world agent/command examples:**
- `.opencode/agent/docs.md` - Documentation writing agent
- `.opencode/agent/triage.md` - Hidden agent with restricted tools
- `.opencode/command/commit.md` - Commit with `subtask: true`
- `.opencode/command/rmslop.md` - Remove AI code patterns

**Experienced Plan mode permission blocking:**
- Tried to edit file in Plan mode → blocked by permission system
- Showed rules: `{"permission":"edit","pattern":"*","action":"deny"}`
- Exception for plan files: `.opencode/plan/*.md`
- This is exactly the safety mechanism for read-only exploration

**Key insight:** Local source is better than web docs for understanding internals. Agent's filesystem access makes this natural.

**Identified essential workflow patterns:**
1. **Mode switching (Plan/Build)** - Ergonomic, prevents premature changes
2. **Chat rewinding** - Essential for clean iteration, avoids context pollution
3. **Context hygiene** - Subtasks, subagents, knowing when to start fresh

**Expanded scope:**
- Other CLI agents to explore: Codex CLI (OpenAI), gemini-cli (Google)
- CI-like isolated usage: GitHub Copilot agent works well for defined tasks
- Task-dependent patterns: fuzzy exploration vs. defined coding tasks

See `notes/workflow-patterns.md` for detailed analysis.

**Compared Claude Code vs Opencode integration level:**
- Opencode: System prompt strongly coding-oriented ("best coding agent on the planet")
- Claude Code: More general feel, same "vibe" as web Claude
- Both work for non-coding, but Claude Code requires less steering
- Korean language project (5,000+ vocab cards) works well with Claude Code

**Project-level prompting pattern:**
- Build up guidance in project files (`prompts/requirements-*.md`)
- Reference via `@prompts/file.md` in conversation
- Works with any tool, version controlled, evolves with project

### Session 2 (2026-01-13) - Permission Systems Research

**Researched permission levels for autonomous long tasks:**

Core question: How do agents avoid blocking during long autonomous tasks?

**Findings by agent:**

1. **Claude Code** - Most sophisticated system:
   - Notification hooks: `permission_prompt`, `idle_prompt` events can trigger external alerts
   - Granular permissions: Pattern-based allow/deny rules per tool
   - Multiple modes: `default`, `plan`, `acceptEdits`, `dontAsk`, `bypassPermissions`
   - Optional sandboxing with `autoAllowBashIfSandboxed`
   - **Key advantage:** Only agent with notification hooks for alerting when blocked

2. **OpenCode** - Good but lacks notifications:
   - Three actions: `allow`, `ask`, `deny` per tool
   - Glob-pattern matching for bash commands (e.g., `"git *": "allow"`)
   - Per-agent permission overrides
   - `always` approval option during session (session-scoped memory)
   - **Missing:** No notification hook system - must watch terminal

3. **Codex CLI (OpenAI)** - Sandbox-focused approach:
   - Two layers: sandbox mode + approval policy
   - Sandbox modes: `read-only`, `workspace-write`, `danger-full-access`
   - `--full-auto` preset for normal development
   - `--yolo` (alias for `--dangerously-bypass-approvals-and-sandbox`)
   - **Missing:** No notification hooks

4. **Gemini CLI (Google)** - Trust-based model:
   - Folder trust system (trusted/untrusted)
   - Sandboxing via macOS Seatbelt or Docker/Podman
   - `/permissions` command to manage trust
   - **Missing:** No notification hooks

**Key insight:** Claude Code's notification hook (`Notification` event with `permission_prompt` matcher) is unique and critical for long-running tasks. Other agents require either:
- More permissive defaults (higher risk)
- Constant terminal monitoring
- Sandboxing (reduced capability)

**Update:** OpenCode already has `session.idle` event in its bus system! Plugins can subscribe to it. Active development:
- PR #7672 adds native `input_required` notification hooks
- Community plugins: `opencode-message-notify` (iOS/Bark), `opencode-ntfy` (cross-platform)

See `notes/agent-permissions.md` for detailed comparison.

---

### Session 3 (2026-01-14) - Directory-Backed Chat Options

**Core question:** Can we get a "Claude Chat Web" experience that binds conversations to local directories?

**Researched options:**

1. **Claude Desktop + MCP Filesystem Server**
   - Works: read/write/edit files in allowed directories
   - Gap: No "project" concept - conversation doesn't persist or bind to directory
   - Useful for ad-hoc file access, not for the workflow we want

2. **Claude Cowork (just announced Jan 12, 2026)**
   - Closest to what we want: chat UI + sandboxed folder access
   - Each session mounts specific folders (like Claude Code's working directory)
   - Sandboxed via Apple VZVirtualMachine
   - **Limitations:** macOS only, Max tier ($100-200/mo), local-only sessions
   - This is essentially "Claude Code with nicer UI for non-devs"

3. **Open WebUI + MCP**
   - Self-hosted, multi-provider chat UI
   - MCP support limited to HTTP transport (needs MCPO proxy for stdio servers)
   - Architecture is multi-tenant, not designed for single-user project workflows
   - Would require customization to get conversation-directory binding

4. **Custom solutions**
   - Claude Code web wrapper (shell out to cc, stream to browser)
   - Custom chat client with MCP (Anthropic SDK + filesystem MCP)
   - Maximum flexibility but significant dev effort

**Key insight:** Claude Cowork is basically what we're asking for - but macOS-only and Max-tier only. For Linux, the options are:
- Keep using Claude Code (terminal friction, but capabilities are right)
- Build custom tooling
- Wait for Cowork on other platforms

See `notes/directory-backed-chat.md` for detailed comparison.

---

## Follow-up Actions

- [x] **Explore Codex CLI (OpenAI)** - Permission system researched (sandbox + approval modes)
- [x] **Explore gemini-cli (Google)** - Folder trust system researched
- [x] **Research opencode notification system** - `session.idle` event exists, PR #7672 in progress
- [x] **Evaluate Claude Desktop + MCP** - Filesystem server works, but no project/session binding
- [x] **Survey web-based agent UIs** - Open WebUI: MCP via proxy, multi-tenant architecture
- [x] **Research Claude Cowork** - Closest to goal but macOS/Max-tier only
- [ ] **Test custom opencode agents** - Create research/verify/synthesize agents, test on new task
- [ ] **Document CI-like patterns** - When is autonomous execution better than interactive?
- [ ] **Try opencode notification plugin** - Test `opencode-ntfy` or create custom plugin
- [ ] **Explore Claude Code web wrappers** - Any mature open-source projects?
