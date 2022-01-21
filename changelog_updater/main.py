import subprocess
from typing import List


def get_git_commits_title() -> List[str]:
    result = (
        subprocess.check_output(
            ["git", "log", "--pretty=format:%s"], stderr=subprocess.STDOUT
        )
        .decode("utf-8")
        .split("\n")
    )
    return result


def prepend_a_line_to_text(text: str, line: str) -> str:
    return f"{line}\n{text}"


def prepend_git_commits_title(text: str) -> str:
    commits_title = get_git_commits_title()
    commits_title_as_text = "\n".join(commits_title)
    return prepend_a_line_to_text(text, commits_title_as_text)
