# Plan

## Methodology Questions

- [x] What is the "Ralph method"? → See `notes/ralph-method.md`
- [ ] Which Ralph variant to try first? (original, snarktank, frankbria)
- [ ] How to structure PROMPT.md for this type of project?
- [ ] What metrics/logs to capture during the experiment?
- [ ] When to intervene vs let the loop run?
- [x] How to isolate the agent environment? → See `notes/isolation.md`
  - Docker Sandbox recommended (zero config, full permissions by default)

## Test Project Questions

- [x] Best framework for VST3 development? → See `notes/test-project.md`
  - **NIH-plug** (Rust): already familiar, `cargo xtask bundle`, minimal deps
- [x] Which LV2 plugin to port?
  - **Guitarix Faust plugins** - Faust compiles to Rust automatically
  - Start with `tremolo.dsp` (48 lines) or `distortion.dsp` (137 lines)
  - No manual DSP translation needed
- [x] Licensing? MIT/ISC preferred, GPL okay for experiment

## Action Items

### Phase 0: Research (this repo - `llm-tasks`)

- [x] Research agent-driven methodologies
- [x] Research isolation options
- [x] Research target framework (NIH-plug)
- [x] Research source plugins (Guitarix Faust)
- [x] Curate references for agent context
- [ ] Finalize PROMPT.md draft
- [ ] Decide which plugin to port first

### Phase 1: Setup (new dedicated repo)

- [ ] Create new repo for the plugin project
- [ ] Set up Docker Sandbox or isolated environment
- [ ] Copy reference code (or clone fresh)
- [ ] Set up Ralph loop script
- [ ] Place PROMPT.md in repo root

### Phase 2: Run Experiment

- [ ] Start Ralph loop, let it run AFK
- [ ] Observe and log (periodically check progress)
- [ ] Document intervention points
- [ ] Iterate on PROMPT.md based on learnings

### Phase 3: Evaluate

- [ ] Analyze git history - what worked, what failed
- [ ] Write up methodology learnings (back to this repo)
- [ ] Test plugin in DAW - does it work?

## Experiment Design

### What to Observe

- Tasks agents handle autonomously vs need help
- Common failure modes and recovery patterns
- Prompt refinements that improved outcomes
- Time/cost vs equivalent manual work

### Success Criteria

**Methodology**: Develop clear mental model of when/how to use Ralph effectively

**Test project**: Plugin builds on Windows, loads in DAW, produces correct audio

## Progress

### 2026-01-17

- Created task from idea in bass-tone research
- Researched Ralph method - wrote `notes/ralph-method.md`
  - Core: infinite loop, state in files/git, fresh context each iteration
  - frankbria/ralph-claude-code looks promising for Claude Code
- Researched isolation options - wrote `notes/isolation.md`
  - Docker Sandbox (`docker sandbox run claude-code`) is simplest
  - Runs with `--dangerously-skip-permissions` by default
  - Full container isolation, zero config
- Researched test project options - wrote `notes/test-project.md`
  - Framework: NIH-plug (Rust, already familiar, minimal deps)
  - Key insight: source complexity doesn't matter (large input → small output)
  - Build verification: `cargo build && cargo xtask bundle`
- Curated Linux plugin references - wrote `notes/references.md`
  - Source: Arch pro-audio group packages with upstream GitHub links
  - NIH-plug ecosystem: lamb-rs, elysiera, cyma (patterns to follow)
  - Clone commands for local refs (agent reads local, no web roundtrips)
- Cloned key repos to `refs/`:
  - `nih-plug` - framework + examples
  - `guitarix` - 100+ Faust DSP files at `trunk/src/LV2/faust/`
  - `lamb-rs` - production nih-plug + Faust + VIZIA example
  - `rust-faust` - Faust→Rust build tooling
- **Key discovery**: Guitarix uses Faust DSP
  - Faust compiles directly to Rust via `faust-build` crate
  - Agent task = copy .dsp + write NIH-plug wrapper (no DSP translation)
  - lamb-rs shows the exact pattern in `build.rs` and `lib.rs`
