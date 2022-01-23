import argparse
import subprocess
from pathlib import Path
from typing import List, Optional, Union


def get_all_commit_titles_until_origin_head(
    origin_branch_name: str = "main",
) -> List[str]:
    try:
        commits = (
            subprocess.check_output(
                [
                    "git",
                    "log",
                    f"origin/{origin_branch_name}~1..HEAD",
                    "--pretty=format:%s",
                ],
                stderr=subprocess.STDOUT,
            )
            .decode("utf-8")
            .split("\n")
        )
    except subprocess.CalledProcessError:
        raise ValueError(
            "Make sure your local repo is connected to a remote repo. "
            "Try running 'git remote', "
            "if nothing is returned, then you are not using a remote repo. "
            "Otherwise, try setting the --origin-branch-name option. "
            "By default changelog-updater uses 'main'."
        )
    else:
        return commits


def prepend_a_text_to_a_text(*, base_text: str, prepend_this: str) -> str:
    return f"{prepend_this}\n{base_text}"


def prepend_commit_titles_to_a_text(
    base_text: str,
    *,
    prepend_this_to_commits: str = None,
    origin_branch_name: str = "main",
) -> str:
    commits = get_all_commit_titles_until_origin_head(origin_branch_name)[:-1]

    if prepend_this_to_commits:
        commits = [prepend_this_to_commits + commit for commit in commits]

    commit_titles_as_text = "\n".join(commits)

    return prepend_a_text_to_a_text(
        base_text=base_text, prepend_this=commit_titles_as_text
    )


def prepend_commit_titles_to_a_file(
    file_path: Union[Path, str], origin_branch_name: str = "main"
):
    with open(file_path, "r") as f:
        file_content = f.read()

    final_text = prepend_commit_titles_to_a_text(
        file_content, origin_branch_name=origin_branch_name
    )

    with open(file_path, "w") as f:
        f.write(final_text)


def main(argv: Optional[List[str]] = None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file",
        help="Path to file in which commit messages will be added",
    )
    parser.add_argument(
        "--origin-branch-name",
        help="The name of the origin branch",
        default="main",
    )
    args = parser.parse_args(argv)

    if not args.file:
        raise ValueError("You must specify the --file flag")

    prepend_commit_titles_to_a_file(args.file, args.origin_branch_name)

    return 0
