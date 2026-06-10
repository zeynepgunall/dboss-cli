import sys

import click

from dboss.git_utils import GitError, commit as commit_fn, get_staged_diff
from dboss.ollama_client import OllamaError, generate
from dboss.prompts import build_commit_prompt


@click.group()
def main():
    """dboss — git commit message generator."""
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


@main.command()
def hello():
    """Smoke test: verify the CLI is installed correctly."""
    click.echo("hello from dboss")


@main.command()
def commit():
    """Generate a commit message for staged changes and commit."""
    try:
        diff = get_staged_diff()
    except GitError as e:
        raise click.ClickException(str(e))

    if not diff:
        click.echo("No staged changes.")
        return

    prompt = build_commit_prompt(diff)

    while True:
        try:
            message = generate(prompt)
        except OllamaError as e:
            raise click.ClickException(str(e))

        click.echo(f"\nSuggested commit message:\n\n  {message}\n")
        choice = click.prompt(
            "[y] accept  [r] regenerate  [n] cancel",
            type=click.Choice(["y", "r", "n"]),
            default="y",
            show_choices=False,
        )

        if choice == "y":
            try:
                commit_fn(message)
            except GitError as e:
                raise click.ClickException(str(e))
            click.echo("Commit created.")
            break
        elif choice == "r":
            continue
        else:
            click.echo("Cancelled.")
            break
