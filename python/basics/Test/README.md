# Python Git Connection Test Project

A small CLI project for verifying Git repository connectivity with a richer output.

## Features

- Prints a structured environment report
- Simulates multiple steps to change output
- Supports JSON output for quick inspection
- Optional environment variable sampling

## Run

```bash
python main.py
```

## Examples

```bash
python main.py --iterations 5
python main.py --show-env
python main.py --json
python main.py --project-name "Git Connectivity Sandbox"
```

## Git Test Workflow

1. Add and commit: `git add . && git commit -m "Add Python test project"`
2. Push to remote: `git push origin main`
3. Verify on GitHub that the code has been synced
