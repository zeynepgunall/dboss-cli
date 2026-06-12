from dboss.prompts import build_commit_prompt

DIFF = "diff --git a/foo.py b/foo.py\n+print('hello')"


def test_contains_diff():
    assert DIFF in build_commit_prompt(DIFF)


def test_conventional_commits_instruction():
    assert "Conventional Commits" in build_commit_prompt(DIFF)


def test_no_code_fences_instruction():
    assert "code fences" in build_commit_prompt(DIFF)


def test_raw_text_only_instruction():
    assert "raw text only" in build_commit_prompt(DIFF)
