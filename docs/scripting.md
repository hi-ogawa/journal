## Scripting

**Toolchain**: Python with `uv` for dependency management

Each task with scripts gets its own `pyproject.toml`:

```bash
uv sync                          # Install dependencies
uv run scripts/script_name.py    # Run a script
uv add package-name              # Add a dependency
```
