"""Performance regressions for app boot and workspace git badges."""
import re
from pathlib import Path
from unittest.mock import patch


REPO = Path(__file__).resolve().parents[1]


def test_boot_does_not_block_on_model_dropdown():
    """A slow /api/models call must not block session restore or first paint."""
    src = (REPO / "static" / "boot.js").read_text(encoding="utf-8")

    assert "await populateModelDropdown();" not in src
    assert "const modelDropdownReady=populateModelDropdown()" in src


def test_external_stylesheets_do_not_block_first_paint():
    """Slow CDN CSS should load async instead of blocking the chat shell."""
    html = (REPO / "static" / "index.html").read_text(encoding="utf-8")
    active_head = re.sub(r"<noscript>.*?</noscript>", "", html, flags=re.DOTALL)

    assert 'rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex' not in active_head
    assert 'rel="stylesheet" href="https://cdn.jsdelivr.net/npm/prismjs' not in active_head
    assert 'rel="preload" as="style" href="https://cdn.jsdelivr.net/npm/katex' in html
    assert 'rel="preload" as="style" href="https://cdn.jsdelivr.net/npm/prismjs' in html


def test_git_info_uses_single_fast_status_call(tmp_path):
    """The workspace git badge should avoid multiple git subprocesses per refresh."""
    from api.workspace import git_info_for_workspace

    (tmp_path / ".git").mkdir()
    status = "\n".join([
        "## main...origin/main [ahead 1, behind 1956]",
        " M api/workspace.py",
        "M  static/workspace.js",
    ])

    with patch("api.workspace._run_git", return_value=status) as run_git:
        info = git_info_for_workspace(tmp_path)

    assert run_git.call_count == 1
    assert run_git.call_args.args[0] == [
        "status",
        "--short",
        "--branch",
        "--untracked-files=no",
    ]
    assert info == {
        "branch": "main",
        "dirty": 2,
        "modified": 2,
        "untracked": 0,
        "ahead": 1,
        "behind": 1956,
        "is_git": True,
    }


def test_git_info_is_cached_briefly(tmp_path):
    """Repeated badge refreshes for the same workspace should not rerun git."""
    from api.workspace import git_info_for_workspace

    (tmp_path / ".git").mkdir()
    with patch("api.workspace._run_git", return_value="## main") as run_git:
        first = git_info_for_workspace(tmp_path)
        second = git_info_for_workspace(tmp_path)

    assert first == second
    assert run_git.call_count == 1
