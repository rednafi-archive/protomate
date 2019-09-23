from github import Github
from loguru import logger
import sys
import os
from protomate.languages import PROGRAMMING_LANGUAGES
import subprocess


def create_remote_repo(g, github_username, repo_name, repo_type):
    """Function that creates remote repository.

    Parameters
    ----------
    g : github.MainClass.Github
        Github object from PyGithub package.
    github_username : str
        Github user name where the repository will be created.
    repo_name : str
        Desired repository name.
    repo_type : str
        Whether the repository will be public or private.

    """

    user = g.get_user()

    if repo_type == "Private":
        user.create_repo(repo_name, private=True)

    else:
        user.create_repo(repo_name, private=False)


g = Github("deceptive-ai", "creativepassword6969")
print(create_remote_repo(g, 'deceptive-ai', 'reddington', "d"))