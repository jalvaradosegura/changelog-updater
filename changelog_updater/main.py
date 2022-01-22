import argparse
import subprocess
from pathlib import Path
from typing import List, Optional, Union


def get_all_commit_titles_until_origin_head() -> List[str]:
    commits = (
        subprocess.check_output(
            ["git", "log", "--pretty=format:%s"], stderr=subprocess.STDOUT
        )
        .decode("utf-8")
        .split("\n")
    )
    return commits


def prepend_a_text_to_a_text(*, base_text: str, prepend_this: str) -> str:
    return f"{prepend_this}\n{base_text}"


def prepend_commit_titles_to_a_text(
    base_text: str, *, prepend_this_to_commits: str = None
) -> str:
    commits = get_all_commit_titles_until_origin_head()[:-1]

    if prepend_this_to_commits:
        commits = [prepend_this_to_commits + commit for commit in commits]

    commit_titles_as_text = "\n".join(commits)

    return prepend_a_text_to_a_text(
        base_text=base_text, prepend_this=commit_titles_as_text
    )


def prepend_commit_titles_to_a_file(file_path: Union[Path, str]):
    with open(file_path, "r") as f:
        file_content = f.read()

    final_text = prepend_commit_titles_to_a_text(file_content)

    with open(file_path, "w") as f:
        f.write(final_text)


def main(argv: Optional[List[str]] = None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file",
        help="Path to file in which commit messages will be added",
    )
    args = parser.parse_args(argv)

    if not args.file:
        raise ValueError("You must specify the --file flag")

    prepend_commit_titles_to_a_file(args.file)

    return 0
