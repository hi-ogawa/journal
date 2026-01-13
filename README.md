# LLM Tasks

A collection of one-off tasks and experiments, each self-contained with its own planning, scripts, and outputs.

## Structure

```
tasks/
  YYYY-MM-DD-(title)/
    README.md            # Brief overview: what, why, key outputs
    plan.md              # Detailed planning and exploration
    notes/               # Research notes and references
    pyproject.toml       # Python dependencies (per-task)
    scripts/             # Task-specific scripts
    data/                # Generated outputs (often git-ignored)
    .gitignore           # Ignore build artifacts, data/html, .venv
```

## Workflow

1. Create `tasks/YYYY-MM-DD-(title)/` directory
2. Write `README.md` (brief: what, why, scope)
3. Write `plan.md` (detailed: problem, approach, progress)
4. Iterate on plan and scripting as needed

## Scripting

**Toolchain**: Python with `uv` for dependency management

Each task with scripts gets its own `pyproject.toml`:

```bash
cd tasks/YYYY-MM-DD-(title)/
uv sync                          # Install dependencies
uv run scripts/script_name.py    # Run a script
uv add package-name              # Add a dependency
```