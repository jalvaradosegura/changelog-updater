from pathlib import Path
from unittest.mock import patch

import pytest

from changelog_updater.main import (
    get_all_commit_titles_until_origin_head,
    main,
    prepend_a_text_to_a_text,
    prepend_commit_titles_to_a_text,
)


"""
This is an example of what you get by running the git command:
$ git log origin/main~1..HEAD --pretty=format:%s
test 3
test 2
test 1
"""
dummy_commit_titles = b"test 3\ntest 2\ntest 1\n"


def test_prepend_a_line_to_text():
    text = "Some random text"
    result = prepend_a_text_to_a_text(base_text=text, prepend_this="Hi,")
    assert result == f"Hi,\n{text}"


def test_get_all_git_commits_title_no_remote_repo():
    with pytest.raises(ValueError):
        get_all_commit_titles_until_origin_head()


@patch(
    "changelog_updater.main.subprocess.check_output",
    lambda *args, **kwargs: dummy_commit_titles,
)
def test_get_all_git_commits_title():
    result = get_all_commit_titles_until_origin_head()

    assert "test 3" == result.pop(0)
    assert "test 2" == result.pop(0)
    assert "test 1" == result.pop(0)


@patch(
    "changelog_updater.main.subprocess.check_output",
    lambda *args, **kwargs: dummy_commit_titles,
)
def test_add_git_commit_titles_to_text():
    commits = get_all_commit_titles_until_origin_head()
    file_content = "* 0.1.0\n" "some text\n" "some more text\n"
    expected_content = (
        f"{commits.pop(0)}\n"
        f"{commits.pop(0)}\n"
        f"{commits.pop(0)}\n"
        "* 0.1.0\n"
        "some text\n"
        "some more text\n"
    )

    result = prepend_commit_titles_to_a_text(file_content)

    assert result == expected_content


@patch(
    "changelog_updater.main.subprocess.check_output",
    lambda *args, **kwargs: dummy_commit_titles,
)
def test_add_commit_titles_with_some_format_to_a_text():
    commits = get_all_commit_titles_until_origin_head()
    file_content = "* 0.1.0\n" "some text\n" "some more text\n"
    expected_content = (
        f"\t* {commits.pop(0)}\n"
        f"\t* {commits.pop(0)}\n"
        f"\t* {commits.pop(0)}\n"
        "* 0.1.0\n"
        "some text\n"
        "some more text\n"
    )

    result = prepend_commit_titles_to_a_text(
        file_content, prepend_this_to_commits="\t* "
    )

    assert result == expected_content


@patch(
    "changelog_updater.main.subprocess.check_output",
    lambda *args, **kwargs: dummy_commit_titles,
)
def test_cmd_prepend_commits_to_a_file(tmp_file_path: Path):
    with open(tmp_file_path, "w") as f:
        f.write("* 0.1.0\nsome text\nsome more text\n")

    response = main(["--file", str(tmp_file_path)])
    with open(tmp_file_path, "r") as f:
        content = f.read()

    assert response == 0
    assert "test 3" in content


def test_cmd_prepend_commits_to_a_file_and_it_doesnt_exist():
    with pytest.raises(FileNotFoundError):
        main(["--file", "some-file-123!.hello"])


def test_cmd_prepend_commits_to_a_file_empty_file_parameter():
    with pytest.raises(ValueError):
        main([])


@patch(
    "changelog_updater.main.subprocess.check_output",
    lambda *args, **kwargs: dummy_commit_titles,
)
def test_cmd_prepend_commits_to_a_file_at_certain_line(tmp_file_path: Path):
    with open(tmp_file_path, "w") as f:
        f.write("CHANGELOG\n\n* line 1\n * line 2\n* line 3")

    response = main(["--file", str(tmp_file_path), "--prepend-at-line", "3"])
    with open(tmp_file_path, "r") as f:
        content = f.read()

    assert response == 0
    assert (
        content == "CHANGELOG\n\ntest 3\ntest 2\ntest 1\n* line 1\n * line 2\n* line 3"
    )


@patch(
    "changelog_updater.main.subprocess.check_output",
    lambda *args, **kwargs: dummy_commit_titles,
)
def test_cmd_prepend_commits_to_a_file_at_certain_line_with_certain_format(
    tmp_file_path: Path,
):
    with open(tmp_file_path, "w") as f:
        f.write("CHANGELOG\n\n* line 1\n * line 2\n* line 3")

    response = main(
        [
            "--file",
            str(tmp_file_path),
            "--prepend-at-line",
            "3",
            "--prepend-this-to-commits",
            "\t* ",
        ]
    )
    with open(tmp_file_path, "r") as f:
        content = f.read()

    assert response == 0
    assert content == (
        "CHANGELOG\n\n\t* test 3\n\t* test 2\n\t* test 1\n* line 1\n * line 2\n* line 3"
    )
