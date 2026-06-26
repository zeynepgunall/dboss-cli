# dboss-cli

> AI-powered CLI that generates [Conventional Commits](https://www.conventionalcommits.org/) messages from your staged git changes, using a locally-run language model via [Ollama](https://ollama.com/).

No data leaves your machine — the model runs locally.

## Features

- Reads your staged git diff and drafts a clear, conventionally-formatted commit message
- Runs entirely on a local LLM through Ollama (no API keys, no cloud calls)
- Interactive flow: accept, regenerate, or cancel each suggestion before committing
- Configurable model via a single environment variable
- Tested with a mocked git/HTTP test suite and a GitHub Actions CI/CD pipeline

## Requirements

- Python 3.12+
- [Ollama](https://ollama.com/) installed and running
- A pulled model (default: `qwen2.5-coder:3b`)

```bash
ollama pull qwen2.5-coder:3b
```

## Installation

```bash
pip install dboss-cli
```

## Usage

Stage the changes you want to commit, then run:

```bash
git add .
dboss commit
```

`dboss` will read your staged diff, send it to your local model, and suggest a commit message. You can then:

- **`y`** — accept and commit
- **`r`** — regenerate a new suggestion
- **`n`** — cancel without committing

Example:

```
$ dboss commit

Suggested commit message:

  feat: add user authentication flow

[y] accept  [r] regenerate  [n] cancel [y]:
```

## Configuration

By default, `dboss` uses the `qwen2.5-coder:3b` model. To use a different Ollama model, set the `DBOSS_MODEL` environment variable:

```bash
# macOS / Linux
export DBOSS_MODEL="llama3.2:3b"

# Windows (PowerShell)
$env:DBOSS_MODEL = "llama3.2:3b"
```

## Development

Clone the repository and install with development dependencies:

```bash
git clone https://github.com/zeynepgunall/dboss-cli.git
cd dboss-cli
python -m venv .venv
# Activate the virtual environment, then:
pip install -e ".[dev]"
```

Run the test suite:

```bash
pytest
```

## How it works

1. `dboss commit` runs `git diff --staged` to capture your staged changes.
2. The diff is wrapped in a prompt instructing the model to produce a single Conventional Commits message.
3. The prompt is sent to the local Ollama server (`http://localhost:11434`).
4. The response is cleaned (stray code fences removed) and shown for your approval.
5. On accept, `dboss` runs `git commit` with the generated message.

## Temp

## License
MIT

