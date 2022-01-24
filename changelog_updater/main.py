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
    origin_branch_name: str = "main",
    prepend_at_line: int = None,
    prepend_this_to_commits: str = None,
) -> str:
    commits = get_all_commit_titles_until_origin_head(origin_branch_name)[:-1]

    if prepend_this_to_commits:
        commits = [prepend_this_to_commits + commit for commit in commits]

    if prepend_at_line:
        base_text_lines = base_text.split("\n")
        new_text = (
            base_text_lines[0 : prepend_at_line - 1]
            + commits
            + base_text_lines[prepend_at_line - 1 :]
        )
        return "\n".join(new_text)

    commit_titles_as_text = "\n".join(commits)

    return prepend_a_text_to_a_text(
        base_text=base_text, prepend_this=commit_titles_as_text
    )


def prepend_commit_titles_to_a_file(
    file_path: Union[Path, str],
    origin_branch_name: str = "main",
    prepend_at_line: int = None,
    prepend_this_to_commits: str = None,
):
    with open(file_path, "r") as f:
        file_content = f.read()

    final_text = prepend_commit_titles_to_a_text(
        file_content,
        origin_branch_name=origin_branch_name,
        prepend_at_line=prepend_at_line,
        prepend_this_to_commits=prepend_this_to_commits,
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
    parser.add_argument(
        "--prepend-at-line",
        help="Prepend commit messages at this line of the file",
        default="0",
    )
    parser.add_argument(
        "--prepend-this-to-commits",
        help="Prepend this to commit messages",
        default="",
    )
    args = parser.parse_args(argv)

    if not args.file:
        raise ValueError("You must specify the --file flag")

    prepend_commit_titles_to_a_file(
        args.file,
        args.origin_branch_name,
        int(args.prepend_at_line),
        args.prepend_this_to_commits,
    )

    return 0
