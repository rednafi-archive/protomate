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

if RUNTIME_ENVIRONMENT == "production":
    sys.tracebacklimit = -100


class bcolors:
    """Class for creating bold colored text

    # generate ascii terminal colors with this script
    import sys
    for i in range(0, 16):
        for j in range(0, 16):
            code = str(i * 16 + j)
            sys.stdout.write(u"\u001b[38;5;" + code + "m " + code.ljust(4))
        print (u"\u001b[0m")

    """

    USERNAME = "\u001b[1m" + "\u001b[38;5;209m"  # bold + orangish
    PASSWORD = "\u001b[1m" + "\u001b[38;5;112m"  # bold + greenish
    REPO_NAME = "\u001b[1m" + "\u001b[38;5;176m"  # bold + pinkish
    REPO_TYPE = "\u001b[1m" + "\u001b[38;5;81m"  # bold + skybluish
    GITIGNORE = "\u001b[1m" + "\u001b[38;5;180m"  # bold + brownish


def _ascii_flare():
    """
    Draw Pr0t0mate banner !!!
    """
    text = "protomate"
    ascii_color = fg(123, 239, 178)
    ascii_style = art.text2art(text, font="glenyn-large")
    ascii_banner = ascii_color + ascii_style + fg.rs
    cprint(ascii_banner, attrs=["bold"])


def _prompt_auth_info():
    username_color = bcolors.USERNAME + "Github Username"
    username_style = click.style(username_color)
    github_username = click.prompt(username_style, type=str)

    password_color = bcolors.PASSWORD + "Github Password"
    password_style = click.style(password_color)
    github_password = click.prompt(password_style, hide_input=True)

    return github_username, github_password


def _prompt_repo_info():
    repo_color = bcolors.REPO_NAME + "Repository Name"
    repo_style = click.style(repo_color)
    repo_name = click.prompt(repo_style, type=str)

    is_private_color = (
        bcolors.REPO_TYPE + "Do you want your repository to be public? (y/n)"
    )
    is_private_style = click.style(is_private_color)

    while True:
        is_private = click.prompt(
            is_private_style,
            click.Choice(["Yes", "Y", "No", "N"], case_sensitive=False),
            show_default=False,
        )
        if is_private.lower() not in ("yes", "y", "no", "n"):
            print("\nWrong Input: Please type yes(y) or no(n)\n")

        else:
            break

    return repo_name, is_private


def _prompt_gitignore_language():
    gitignore_color = (
        bcolors.GITIGNORE
        + """Please enter the desired language name to create gitignore file,
press enter if you don't want to"""
    )
    gitignore_style = click.style(gitignore_color)
    gitignore_language = click.prompt(
        gitignore_style,
        click.Choice(PROGRAMMING_LANGUAGES, case_sensitive=False),
        show_default=False,
    )
    return gitignore_language


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
        if gitignore is not None and gitignore.lower() in PROGRAMMING_LANGUAGES:
            cmd_gitignore
            subprocess.check_output(cmd_gitignore, shell=True)

        elif gitignore is not None and gitignore.lower() not in PROGRAMMING_LANGUAGES:
            print("Language not supported:\n Creating repository without .gitignore 🙃")
            cmd
            subprocess.check_output(cmd, shell=True)

        else:
            cmd
            subprocess.check_output(cmd, shell=True)

        print("Local and remote repository successfully created")

    except Exception:
        sys.exit("Local and remote repository cannot be connected 😣")


def main():
    try:
        _ascii_flare()
    except KeyboardInterrupt:
        sys.exit("Operation Aborted ⚠️")

    try:
        github_username, github_password = _prompt_auth_info()
    except click.exceptions.Abort:
        sys.exit("Operation Aborted ⚠️")

    try:
        repo_name, is_private = _prompt_repo_info()
    except click.exceptions.Abort:
        sys.exit("Operation Aborted ⚠️")

    try:
        gitignore_langugage = _prompt_gitignore_language()
    except click.exceptions.Abort:
        sys.exit("Operation Aborted ⚠️")

    print("Thanks for all of your information, hang tight while we are at it..⏳")

    # auth
    try:
        g, user = _do_github_auth(github_username, github_password)
    except KeyboardInterrupt:
        sys.exit("Operation Aborted ⚠️")

    try:
        _create_local_repo(repo_name)
    except KeyboardInterrupt:
        sys.exit("Operation Aborted ⚠️")

    try:
        _create_remote_repo(g, github_username, repo_name, is_private)
    except KeyboardInterrupt:
        sys.exit("Operation Aborted ⚠️")

    try:
        _connect_local_remote(repo_name, github_username, gitignore_langugage)
    except KeyboardInterrupt:
        sys.exit("Operation Aborted ⚠️")


if __name__ == "__main__":
    main()
