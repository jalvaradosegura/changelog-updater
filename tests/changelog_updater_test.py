from unittest.mock import patch

from changelog_updater.main import (
    get_all_commits_until_origin_head,
    prepend_a_text_to_text,
    prepend_commit_titles,
)


"""
This is an example of what you get by running the git command:
$ git log origin/main~1..HEAD --pretty=format:%s
test 3
test 2
test 1
Move tox to dev dependencies
"""
dummy_commit_titles = b"test 3\ntest 2\ntest 1\nMove tox to dev dependencies"


def test_prepend_a_line_to_text():
    text = "Some random text"
    result = prepend_a_text_to_text(base_text=text, prepend_this="Hi,")
    assert result == f"Hi,\n{text}"


@patch(
    "changelog_updater.main.subprocess.check_output",
    lambda *args, **kwargs: dummy_commit_titles,
)
def test_get_all_git_commits_title():
    result = get_all_commits_until_origin_head()

    assert "test 3" == result.pop(0)
    assert "test 2" == result.pop(0)
    assert "test 1" == result.pop(0)


@patch(
    "changelog_updater.main.subprocess.check_output",
    lambda *args, **kwargs: dummy_commit_titles,
)
def test_add_git_commit_titles_to_text():
    commits = get_all_commits_until_origin_head()
    file_content = "* 0.1.0\n" "some text\n" "some more text\n"
    expected_content = (
        f"{commits.pop(0)}\n"
        f"{commits.pop(0)}\n"
        f"{commits.pop(0)}\n"
        "* 0.1.0\n"
        "some text\n"
        "some more text\n"
    )

    result = prepend_commit_titles(file_content)

    assert result == expected_content
