import subprocess
from subprocess import CalledProcessError
from unittest.mock import MagicMock

import pytest

from dboss.git_utils import GitError, commit, get_staged_diff


# --- get_staged_diff ---


def test_get_staged_diff_returns_diff(mocker):
    mocker.patch(
        "subprocess.run",
        side_effect=[
            MagicMock(),
            MagicMock(stdout="diff --git a/foo.py b/foo.py\n+print('hello')\n"),
        ],
    )
    result = get_staged_diff()
    assert "diff" in result


def test_get_staged_diff_empty(mocker):
    mocker.patch(
        "subprocess.run",
        side_effect=[
            MagicMock(),
            MagicMock(stdout=""),
        ],
    )
    assert get_staged_diff() == ""


def test_get_staged_diff_git_not_found(mocker):
    mocker.patch("subprocess.run", side_effect=FileNotFoundError)
    with pytest.raises(GitError, match="git komutu bulunamadı"):
        get_staged_diff()


def test_get_staged_diff_not_a_repo(mocker):
    mocker.patch("subprocess.run", side_effect=CalledProcessError(128, "git"))
    with pytest.raises(GitError, match="git reposu değil"):
        get_staged_diff()


# --- commit ---


def test_commit_success(mocker):
    mocker.patch("subprocess.run", return_value=MagicMock())
    commit("feat: add login")  # exception çıkmamalı


def test_commit_failure(mocker):
    err = CalledProcessError(1, "git")
    err.stderr = "nothing to commit"
    mocker.patch("subprocess.run", side_effect=err)
    with pytest.raises(GitError, match="git commit başarısız"):
        commit("feat: add login")
