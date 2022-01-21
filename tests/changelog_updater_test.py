from changelog_updater.main import (
    get_git_commits_title,
    prepend_a_line_to_text,
)


def test_prepend_a_line_to_text():
    text = "Some random text"
    result = prepend_a_line_to_text(text, "Hi,")
    assert result == f"Hi,\n{text}"


def test_get_git_commits_title():
    result = get_git_commits_title()
    assert "Create a function to prepend text" in result
    assert "Create the project" in result
    assert "Create a function to prepend text" == result[-2]
    assert "Create the project" == result[-1]
