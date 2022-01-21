import subprocess
from typing import List


def get_all_commits_title() -> List[str]:
    result = (
        subprocess.check_output(
            ["git", "log", "--pretty=format:%s"], stderr=subprocess.STDOUT
        )
        .decode("utf-8")
        .split("\n")
    )
    return result


def prepend_a_text_to_text(*, base_text: str, prepend_this: str) -> str:
    return f"{prepend_this}\n{base_text}"


def prepend_commits_title(base_text: str, *, commits_amount: int) -> str:
    commits_title = get_all_commits_title()[0:commits_amount]
    commits_title_as_text = "\n".join(commits_title)
    return prepend_a_text_to_text(
        base_text=base_text, prepend_this=commits_title_as_text
    )
