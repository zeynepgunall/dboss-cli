from pathlib import Path

_TOKEN_DIR = Path.home() / ".dboss"
_TOKEN_FILE = _TOKEN_DIR / "token"


def save_token(token: str) -> None:
    _TOKEN_DIR.mkdir(parents=True, exist_ok=True)
    _TOKEN_FILE.write_text(token, encoding="utf-8")


def load_token() -> str | None:
    if not _TOKEN_FILE.exists():
        return None
    text = _TOKEN_FILE.read_text(encoding="utf-8").strip()
    return text if text else None


def clear_token() -> None:
    if _TOKEN_FILE.exists():
        _TOKEN_FILE.unlink()
