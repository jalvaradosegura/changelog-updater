from typing import List

import pytest

from changelog_updater.main import (
    get_all_commits_title,
    prepend_a_text_to_text,
    prepend_commits_title,
)


@pytest.fixture
def all_commits() -> List[str]:
    return get_all_commits_title()


def test_prepend_a_line_to_text():
    text = "Some random text"
    result = prepend_a_text_to_text(base_text=text, prepend_this="Hi,")
    assert result == f"Hi,\n{text}"


def test_get_all_git_commits_title(all_commits: List[str]):
    latest_commit = all_commits.pop(0)
    penultimate_commits = all_commits.pop(0)

    result = get_all_commits_title()

    assert latest_commit == result[0]
    assert penultimate_commits == result[1]


def test_add_git_commits_title_to_text(all_commits):
    latest_commit = all_commits.pop(0)
    penultimate_commits = all_commits.pop(0)
    file_content = "* 0.1.0\n" "some text\n" "some more text\n"
    expected_content = (
        f"{latest_commit}\n"
        f"{penultimate_commits}\n"
        "* 0.1.0\n"
        "some text\n"
        "some more text\n"
    )

    result = prepend_commits_title(file_content, commits_amount=2)

    assert result == expected_content
