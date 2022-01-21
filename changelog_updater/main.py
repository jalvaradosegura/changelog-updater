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
