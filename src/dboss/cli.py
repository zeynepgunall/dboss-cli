import sys

import click

from dboss.auth_client import (
    AuthError,
    get_me,
)
from dboss.auth_client import (
    login as login_fn,
)
from dboss.auth_client import (
    register as register_fn,
)
from dboss.git_utils import GitError, get_staged_diff
from dboss.git_utils import commit as commit_fn
from dboss.ollama_client import OllamaError, generate, strip_code_fences
from dboss.prompts import build_commit_prompt
from dboss.token_store import clear_token, load_token, save_token


@click.group()
def main():
    """dboss — git commit message generator."""
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


@main.command()
def register():
    """Yeni hesap oluştur."""
    username = click.prompt("Kullanıcı adı")
    email = click.prompt("E-posta")
    password = click.prompt("Şifre", hide_input=True, confirmation_prompt=True)
    try:
        register_fn(username, email, password)
    except AuthError as e:
        raise click.ClickException(str(e)) from e
    click.echo(f"Hesap oluşturuldu: {username}. Şimdi giriş yapabilirsin.")


@main.command()
def login():
    """Hesabına giriş yap."""
    username = click.prompt("Kullanıcı adı")
    password = click.prompt("Şifre", hide_input=True)
    try:
        token = login_fn(username, password)
    except AuthError as e:
        raise click.ClickException(str(e)) from e
    save_token(token)
    click.echo(f"Logged in as {username}")


@main.command()
def logout():
    """Oturumu kapat."""
    clear_token()
    click.echo("Logged out.")


@main.command()
def whoami():
    """Giriş yapan kullanıcıyı göster."""
    token = load_token()
    if not token:
        click.echo("Not logged in.")
        return
    try:
        user = get_me(token)
    except AuthError as e:
        raise click.ClickException(str(e)) from e
    click.echo(f"Username : {user.get('username', '-')}")
    click.echo(f"Email    : {user.get('email', '-')}")


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
        raise click.ClickException(str(e)) from e

    if not diff:
        click.echo("No staged changes.")
        return

    prompt = build_commit_prompt(diff)

    while True:
        try:
            message = generate(prompt)
        except OllamaError as e:
            raise click.ClickException(str(e)) from e

        message = strip_code_fences(message)
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
                raise click.ClickException(str(e)) from e
            click.echo("Commit created.")
            break
        elif choice == "r":
            continue
        else:
            click.echo("Cancelled.")
            break
