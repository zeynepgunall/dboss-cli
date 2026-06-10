import subprocess


class GitError(Exception):
    pass


def get_staged_diff() -> str:
    try:
        subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            capture_output=True,
            check=True,
        )
    except FileNotFoundError:
        raise GitError("git komutu bulunamadı. Git kurulu mu?")
    except subprocess.CalledProcessError:
        raise GitError("Bu dizin bir git reposu değil.")

    try:
        result = subprocess.run(
            ["git", "diff", "--staged"],
            capture_output=True,
            encoding="utf-8",
            check=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise GitError(f"git diff başarısız: {e.stderr.strip()}")


def commit(message: str) -> None:
    try:
        subprocess.run(
            ["git", "commit", "-m", message],
            capture_output=True,
            encoding="utf-8",
            check=True,
        )
    except subprocess.CalledProcessError as e:
        raise GitError(f"git commit başarısız: {e.stderr.strip()}")
