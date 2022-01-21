import subprocess
from typing import List


def get_all_commits_until_origin_head() -> List[str]:
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


def prepend_commit_titles(base_text: str) -> str:
    commits = get_all_commits_until_origin_head()[:-1]
    commit_titles_as_text = "\n".join(commits)
    return prepend_a_text_to_text(
        base_text=base_text, prepend_this=commit_titles_as_text
    )
