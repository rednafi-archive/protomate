from __future__ import unicode_literals
import os
import subprocess
import sys

import art
import click
from github import Github
from github.GithubException import BadCredentialsException, GithubException
from sty import fg, rs
from termcolor import cprint

from protomate.languages import PROGRAMMING_LANGUAGES
from protomate.utils import logfunc
from protomate.settings import RUNTIME_ENVIRONMENT


def _do_github_auth(github_username, github_password):
    """Trying to log into github
    """

    g = Github(github_username, github_password)
    user = g.get_user()

    try:
        user.login

    except BadCredentialsException:
        sys.exit("AuthError: Username or password is incorrect 😣")

    return (g, user)


def _create_local_repo(repo_name):
    try:
        os.mkdir(repo_name)

    except FileExistsError:
        sys.exit(f"LocalExistsError: Local repository '{repo_name}' already exists 😣")


def _create_remote_repo(g, github_username, repo_name, is_private):

    user = g.get_user()
    try:
        if is_private.lower() in ("yes", "y"):
            user.create_repo(repo_name, private=True)

        else:
            user.create_repo(repo_name, private=False)

    except GithubException:
        sys.exit(
            f"RemoteCreationError: Remote repository '{repo_name}' already exists 😣"
        )


def _connect_local_remote(repo_name, github_username, gitignore):

    cmd = f"""
        cd {repo_name}
        git init
        git remote add origin git@github.com:{github_username}/{repo_name}.git
        touch README.md
        git add .
        git commit -m "Initial commit"
        git push -u origin master
        code .
            """

    cmd_gitignore = f"""
        cd {repo_name}
        git init
        git remote add origin git@github.com:{github_username}/{repo_name}.git
        touch README.md
        curl -X GET https://www.gitignore.io/api/{gitignore} >.gitignore
        git add .
        git commit -m "Initial commit"
        git push -u origin master
        code .
        """

    try:
        if gitignore.lower() in PROGRAMMING_LANGUAGES:
            cmd_gitignore
            subprocess.check_output(cmd_gitignore, shell=True)

        elif gitignore.lower() not in PROGRAMMING_LANGUAGES:
            print("Language not supported:\n Creating repository without .gitignore 😣")
            cmd
            subprocess.check_output(cmd, shell=True)

        else:
            cmd
            subprocess.check_output(cmd, shell=True)

        print("Local and remote repository successfully created")

    except Exception:
        sys.exit("Local and remote repository cannot be connected 😣")


g, user = _do_github_auth("deceptive-ai", "creativepassword6969")

_create_local_repo("anyth")
_create_remote_repo(g, "deceptive-ai", "anyth", "y")
_connect_local_remote('ayth','deceptive-ai', "python")
