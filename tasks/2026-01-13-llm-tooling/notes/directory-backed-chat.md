# Directory-Backed Chat: Current Options

> **See also:** [prd-knowledge-work-agent.md](prd-knowledge-work-agent.md) - the pragmatic approach we landed on (use existing coding agents + conventions)

The goal: A chat interface where each conversation corresponds to a local directory, enabling persistent research, accumulated notes, and continued work across sessions.

This is essentially what Claude Code provides (conversation ↔ working directory), but with a chat-first UX rather than terminal UX.

## Option 1: Claude Desktop + MCP Filesystem Server

**What it is:** Claude Desktop can connect to local MCP servers, including the official filesystem server that provides read/write access to specified directories.

**Setup:**
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/path/to/allowed/directory"
      ]
    }
  }
}
```

**Tools provided:** `read_file`, `write_file`, `edit_file`, `create_directory`, `list_directory`, `move_file`, `search_files`, `get_file_info`

**Pros:**
- Official Anthropic product
- Desktop extensions make setup easier (2025)
- Per-operation approval keeps control with user
- Can connect to multiple MCP servers (filesystem, web fetch, etc.)

**Cons:**
- No built-in conversation-to-directory association
- Conversation context doesn't persist (memory features are limited)
- Manual permission prompts for each file operation
- Must configure which directories are accessible upfront

**Gap for our use case:** The tool access is there, but there's no "project" concept that binds a conversation to a directory with accumulated context.

**References:**
- [Claude Help Center - MCP Setup](https://support.claude.com/en/articles/10949351-getting-started-with-local-mcp-servers-on-claude-desktop)
- [MCP Filesystem Server](https://modelcontextprotocol.io/docs/develop/connect-local-servers)

---

## Option 2: Claude Cowork (Research Preview, Jan 2026)

**What it is:** "Claude Code for the rest of your work" - a desktop agent that operates on local files through a sandboxed Linux VM. Accessed via a new "Cowork" tab in Claude Desktop.

**Key features:**
- Mount folders into a containerized sandbox
- Full file operations (read, create, edit, organize)
- Browser integration (Chrome extension for web tasks)
- Built-in sandboxing via Apple's VZVirtualMachine
- "Skills" for document/presentation creation

**Pros:**
- Closest to "chat web with directory access" vision
- Less intimidating than Claude Code for non-developers
- Sandboxing provides security isolation
- Sessions are tied to mounted folders (like Claude Code)

**Cons:**
- macOS only (Windows "planned")
- Claude Max tier only ($100-$200/month)
- Sessions don't sync across devices (local only)
- Still a "research preview" - may have rough edges
- Not Linux

**Gap for our use case:** This is actually very close to what we want. The main friction:
1. Cost (Max tier required)
2. Platform (macOS only for now)
3. Local-only sessions (can't pick up on another machine)

**References:**
- [Anthropic Blog - Cowork Research Preview](https://claude.com/blog/cowork-research-preview)
- [Simon Willison's first impressions](https://simonwillison.net/2026/Jan/12/claude-cowork/)
- [TechCrunch coverage](https://techcrunch.com/2026/01/12/anthropics-new-cowork-tool-offers-claude-code-without-the-code/)

---

## Option 3: Open WebUI + MCP

**What it is:** Self-hosted web UI that supports multiple LLM providers, with MCP integration via HTTP transport or the MCPO proxy.

**Architecture:**
- Open WebUI is web-based and multi-tenant
- Native MCP only supports Streamable HTTP (not stdio)
- For stdio-based servers (like filesystem), use MCPO proxy to convert to OpenAPI

**Pros:**
- Self-hosted (your data stays local)
- Multi-provider (Claude, GPT, local models)
- Web-based chat UX
- Extensible via MCP/OpenAPI tools

**Cons:**
- More complex setup (Docker, proxies, etc.)
- Filesystem access requires MCPO proxy bridge
- Security implications of exposing filesystem via HTTP
- Multi-tenant design not optimized for single-user "project" workflow

**Gap for our use case:** The infrastructure is there, but it's designed for shared/multi-tenant use. Would need customization to get the "conversation = directory" binding.

**References:**
- [Open WebUI MCP Docs](https://docs.openwebui.com/features/mcp/)
- [MCPO Proxy](https://github.com/open-webui/mcpo)

---

## Option 4: Custom Solutions

### 4a: Claude Code wrapper with web UI

Build a web frontend that shells out to Claude Code:

**Approach:**
- Web UI that manages sessions
- Each session = a working directory
- Claude Code runs in the background
- UI streams stdout/stderr to browser

**Examples (not fully researched):**
- Various "Claude Code web" projects on GitHub
- Anthropic's agentic-starter kits

**Pros:**
- Leverages Claude Code's mature tooling
- Can customize UI to taste
- Directory-conversation binding is natural

**Cons:**
- DIY maintenance burden
- Need to handle auth, security, etc.

### 4b: Custom chat client with MCP

Build a minimal chat interface that:
1. Talks directly to Claude API
2. Connects to MCP servers (filesystem, web fetch, etc.)
3. Persists conversations in the project directory

**Libraries:**
- Anthropic SDK (chat completions with tools)
- MCP SDK (for server connections)
- Any web framework for UI

**Pros:**
- Maximum flexibility
- Can design exactly the workflow you want
- Conversation history stored in project directory

**Cons:**
- Significant development effort
- Need to implement all the agent behaviors yourself

---

## Comparison Matrix

| Feature | Desktop+MCP | Cowork | Open WebUI | Custom |
|---------|-------------|--------|------------|--------|
| Directory access | ✓ | ✓ | ✓ (via proxy) | ✓ |
| Chat UX | ✓ | ✓ | ✓ | ✓ |
| Session = Directory | ✗ | ✓ | ✗ | ✓ |
| Cross-device | ✗ | ✗ | ✓ | depends |
| Linux support | ✓ | ✗ | ✓ | ✓ |
| No subscription | ✗ | ✗ | ✓ | ✓ |
| Setup effort | Medium | Low | High | Very High |

---

## Recommendations

**For macOS + Max subscriber:** Claude Cowork is the obvious choice. It's essentially what we're asking for.

**For Linux/other platforms now:**

1. **Short term:** Continue using Claude Code directly. The terminal UX is friction, but the capabilities are right.

2. **Medium term:** Watch for:
   - Cowork on Linux/Windows
   - Open WebUI native MCP improvements
   - Community Claude Code web wrappers

3. **If you want to build:** A minimal custom chat client with MCP filesystem server is probably the cleanest path. The Anthropic SDK + MCP SDK combination is well-documented.

---

## Open Questions

1. Does Cowork support the same `CLAUDE.md` / `AGENTS.md` pattern as Claude Code? (project-level instructions)
2. Can Cowork sessions be exported/imported to continue on another machine?
3. Are there good open-source "Claude Code web UI" projects worth evaluating?
