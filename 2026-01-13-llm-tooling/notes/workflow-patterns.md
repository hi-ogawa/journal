# Agent Workflow Patterns

Observations on effective patterns for working with LLM agents, based on experience with Claude Code and opencode.

## Claude Code vs Opencode: Integration Level

A key difference in how these tools position themselves:

### Opencode: Project/Task-Oriented Prompting

Opencode's system prompts are **heavily geared toward coding tasks**:
- "You are OpenCode, the best coding agent on the planet"
- "You are an interactive CLI tool that helps users with software engineering tasks"
- Strong emphasis on TodoWrite, code references, file operations

The base prompt assumes a coding context. Non-coding tasks require user-level prompting to steer it differently.

### Claude Code: General-Purpose Feel

Claude Code's integration feels more like **Claude on the web with tool access**:
- Same conversational "vibe" as web Claude
- Works naturally for non-coding tasks
- Example: Korean language learning project with 5,000+ vocabulary cards, etymology generation, Anki integration

**Evidence**: The `~/code/personal/misc/korean/` project uses Claude Code for:
- Generating Korean etymology (Hanja, Japanese cognates, compounds)
- Creating example sentences
- Processing Anki cards
- Writing data processing scripts

The project works by building up **project-level prompt files** that guide behavior:
- `prompts/requirements-etymology.md` - Detailed etymology generation standards
- `prompts/guide-script.md` - Script writing principles
- `prompts/koreantopik2/generate-examples.md` - Workflow-specific prompts

### Implication

| Tool | System Prompt Focus | Non-Coding Tasks |
|------|---------------------|------------------|
| **Opencode** | Strongly coding-oriented | Requires more steering via user prompts |
| **Claude Code** | More general | Works naturally, same vibe as web Claude |

Both work for non-coding tasks, but Claude Code requires less "fighting against" the system prompt. Opencode's strength is its configurability - you can define custom agents with different prompts.

## Essential Workflow Features

### 1. Explicit Mode Switching (Plan/Build)

Both Claude Code and opencode support explicit Plan mode:

| Feature | Benefit |
|---------|---------|
| **Read-only exploration** | Think before acting, avoid premature changes |
| **Permission enforcement** | System prevents accidental modifications |
| **Clear mental model** | User knows what the agent can/cannot do |
| **Natural workflow** | Mirrors how humans work: research → plan → execute |

**Usage pattern:**
1. Start in Plan mode for exploration and discussion
2. Switch to Build when ready to make changes
3. Switch back to Plan for further exploration

### 2. Chat Rewinding / Undo

**Essential for iteration quality.** Both Claude Code and opencode support this.

**Why it matters:**
- Bad iterations pollute context (model sees failed attempts)
- Context pollution leads to worse subsequent responses
- Clean context = better model performance

**Pattern:**
1. Try an approach
2. If it goes wrong, rewind/undo
3. Rephrase and try again with clean context

**Without rewind:** Each failed attempt stays in context, model may repeat mistakes or get confused by contradictory history.

### 3. Context Hygiene

Related to rewinding, but broader:

- **Subtask mode** (`subtask: true` in opencode) - Run commands in isolated context
- **Subagents** - Delegate tasks without polluting main conversation
- **Session management** - Know when to start fresh vs. continue

### 4. Project-Level Prompting

Instead of fighting tool-level system prompts, build up **project-level guidance**:

**Example from Korean project:**
```
korean/prompts/
├── requirements-etymology.md    # 147 lines of etymology standards
├── requirements-example.md      # Example sentence requirements
├── guide-script.md              # Script writing principles (270 lines)
└── koreantopik2/
    ├── generate-examples.md     # Workflow-specific prompts
    └── generate-notes.md
```

**Pattern:**
1. Create detailed requirement docs in the project
2. Reference them via `@prompts/requirements-etymology.md` in conversation
3. Agent follows project standards without modifying tool config

**Benefits:**
- Works with any agent (Claude Code, opencode, etc.)
- Version controlled with project
- Evolves with project needs
- No tool configuration required

This is essentially **user-level steering** that accumulates as project documentation.

## Agent Landscape

### Local CLI Agents

| Agent | Provider | Status |
|-------|----------|--------|
| **Claude Code** | Anthropic | Primary tool, closed source |
| **opencode** | Open source | Explored, good Claude Code alternative |
| **Codex CLI** | OpenAI | TODO: Explore |
| **gemini-cli** | Google | TODO: Explore |

**Questions to answer:**
- Do Codex/gemini-cli support Plan mode equivalent?
- Do they support chat rewinding?
- How do they handle context management?

### CI-like Isolated Agent Usage

Different pattern: **pre-defined scope, autonomous execution**

**GitHub Copilot (agent mode in CI):**
- Works well for coding tasks with clear scope
- Isolated execution (no context pollution from previous runs)
- Good for: PRs, issue fixes, defined features

**Characteristics:**
- Task defined upfront (issue, PR description)
- No interactive iteration needed
- Success/failure is clear
- Context is fresh each run

### Interactive vs Autonomous

| Aspect | Interactive (Chat) | Autonomous (CI-like) |
|--------|-------------------|---------------------|
| **Scope** | Fuzzy, evolving | Pre-defined, clear |
| **Iteration** | Fast back-and-forth | Single run |
| **Context** | Accumulates, needs hygiene | Fresh each time |
| **Best for** | Exploration, research | Defined coding tasks |
| **Key feature** | Rewind, mode switching | Isolation, clear spec |

## Task-Dependent Patterns

### Fuzzy Iterative Exploration (e.g., research, learning)

**Needs:**
- Fast interaction loop
- Easy rewinding
- Mode switching (read-only exploration → capture)
- Good context management

**Best tools:** Claude Code, opencode with Plan/Build modes

### Defined Coding Tasks (e.g., fix bug, add feature)

**Needs:**
- Clear task specification
- Autonomous execution
- Isolated context
- Verification (tests, build)

**Best tools:** GitHub Copilot agent, CI-integrated agents

### Knowledge Synthesis (e.g., documentation, learning notes)

**Needs:**
- Web fetching for verification
- File system for persistent artifacts
- Iterative refinement
- Source cross-referencing

**Best tools:** Local agents with tool access (Claude Code, opencode)

## Open Questions

1. **Do other CLI agents (Codex, gemini-cli) support these patterns?**
   - Plan mode equivalent?
   - Chat rewinding?
   - Subagent/subtask isolation?

2. **Can CI-like patterns work for research tasks?**
   - Pre-define research scope in issue/spec
   - Run agent autonomously
   - Review output, iterate on spec

3. **Hybrid approaches?**
   - Interactive planning → autonomous execution
   - Use chat to define scope, then hand off to CI agent

4. **Consumer chat improvements?**
   - Could Claude.ai add rewind?
   - Could Projects add tool access?
   - Would MCP bridge the gap?
