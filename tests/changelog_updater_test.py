from changelog_updater.main import (
    get_git_commits_title,
    prepend_a_line_to_text,
    prepend_git_commits_title,
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


def test_add_git_commits_title_to_text():
    file_content = "* 0.1.0\n" "some text\n" "some more text\n"
    expected_content = (
        "Create a function to read git logs\n"
        "Create a function to prepend text\n"
        "Create the project\n"
        "* 0.1.0\n"
        "some text\n"
        "some more text\n"
    )

    result = prepend_git_commits_title(file_content)

    assert result == expected_content
