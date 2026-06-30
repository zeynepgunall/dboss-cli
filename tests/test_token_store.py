import pytest

import dboss.token_store as ts


@pytest.fixture(autouse=True)
def patch_token_paths(tmp_path, monkeypatch):
    """Redirect token storage to a temp directory for every test."""
    token_dir = tmp_path / ".dboss"
    token_file = token_dir / "token"
    monkeypatch.setattr(ts, "_TOKEN_DIR", token_dir)
    monkeypatch.setattr(ts, "_TOKEN_FILE", token_file)


def test_save_and_load_token():
    ts.save_token("tok_abc123")
    assert ts.load_token() == "tok_abc123"


def test_load_token_returns_none_when_missing():
    assert ts.load_token() is None


def test_clear_token():
    ts.save_token("tok_abc123")
    ts.clear_token()
    assert ts.load_token() is None


def test_clear_token_no_file_is_safe():
    ts.clear_token()  # dosya yokken çağırmak hata vermemeli


def test_save_token_creates_directory(tmp_path, monkeypatch):
    nested_dir = tmp_path / "a" / "b" / ".dboss"
    nested_file = nested_dir / "token"
    monkeypatch.setattr(ts, "_TOKEN_DIR", nested_dir)
    monkeypatch.setattr(ts, "_TOKEN_FILE", nested_file)

    ts.save_token("tok_xyz")
    assert nested_file.exists()
    assert nested_file.read_text(encoding="utf-8") == "tok_xyz"


def test_load_token_strips_whitespace(tmp_path, monkeypatch):
    token_dir = tmp_path / ".dboss"
    token_file = token_dir / "token"
    monkeypatch.setattr(ts, "_TOKEN_DIR", token_dir)
    monkeypatch.setattr(ts, "_TOKEN_FILE", token_file)

    token_dir.mkdir()
    token_file.write_text("  tok_abc123\n", encoding="utf-8")
    assert ts.load_token() == "tok_abc123"
