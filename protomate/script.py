import getpass
from pprint import pprint
from github import Github
from loguru import logger

from protomate.cli_prompts import draw_ascii_banner, cli
from protomate.repo_auths import authentication, is_pass_saved, save_pass, retrieve_pass
from protomate.repo_actions import (
    create_local_repo,
    create_remote_repo,
    connect_local_to_remote,
)

import sys
import signal


sys.tracebacklimit = -10


# log
LOG_FILENAME = "logs/logfile.log"
logger.remove(0)
logger.add(
    LOG_FILENAME,
    format="-------------||time:{time}||level:{level}||-------------\n{message}\n",
    level="ERROR",
    backtrace=True,
    diagnose=False,
    enqueue=True,
    rotation="1 MB",
)


def main():
    """Main function
    """

    draw_ascii_banner()
    github_username, github_password, password_save, repo_name, repo_type, gitignore = (
        cli()
    )

    save_pass(password_save, github_username, github_password)
    print("Thanks for all your information, hang tight while we are at it...")

    g, user = authentication(github_username, github_password)
    create_local_repo(repo_name)
    create_remote_repo(g, github_username, repo_name, repo_type)
    connect_local_to_remote(repo_name, github_username, gitignore)


if __name__ == "__main__":
    main()
