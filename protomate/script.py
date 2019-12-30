from __future__ import unicode_literals

import os
import sys

import art
import click
from github import Github
from github.GithubException import BadCredentialsException, GithubException
from sty import fg
from termcolor import cprint

from protomate.languages import PROGRAMMING_LANGUAGES
from protomate.settings import RUNTIME_ENVIRONMENT
from protomate.utils import find_shell_path, run_task

if RUNTIME_ENVIRONMENT == "production":
    sys.tracebacklimit = -100


use_shell = find_shell_path("bash")


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
    SUCCESS = "\u001b[1m" + "\u001b[38;5;192m"  # bold + lemonish


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
        if not isinstance(is_private, str) or is_private.lower() not in (
            "yes",
            "y",
            "no",
            "n",
        ):
            click.secho("\nWrong Input: Please type yes(y) or no(n)\n", fg="magenta")
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
        click.secho("AuthError: Username or password is incorrect 😣", fg="magenta")
        sys.exit(1)

    return (g, user)


def _create_local_repo(repo_name):
    try:
        os.mkdir(repo_name)

    except FileExistsError:
        click.secho(
            f"LocalExistsError: Local repository '{repo_name}' already exists 😣",
            fg="magenta",
        )
        sys.exit(1)


def _create_remote_repo(g, github_username, repo_name, is_private):

    user = g.get_user()
    try:
        if isinstance(is_private, str) and is_private.lower() in ("yes", "y"):
            user.create_repo(repo_name, private=False)

        elif isinstance(is_private, str) and is_private.lower() in ("no", "n"):
            user.create_repo(repo_name, private=True)

    except GithubException:
        click.secho(
            f"RemoteCreationError: Remote repository '{repo_name}' already exists 😣",
            fg="magenta",
        )
        sys.exit(1)


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
        if isinstance(gitignore, str) and gitignore.lower() in PROGRAMMING_LANGUAGES:
            run_task(use_shell, cmd_gitignore)

        elif (
            isinstance(gitignore, str)
            and gitignore.lower() not in PROGRAMMING_LANGUAGES
        ):
            click.secho(
                "Warning: Unsupported language. Creating repository without .gitignore 🙃",
                fg="yellow",
            )
            run_task(use_shell, cmd)

        else:
            run_task(use_shell, cmd)
        click.secho("Local and remote repository successfully created 🎉", fg="green")

    except Exception:
        click.secho("Local and remote repository cannot be connected 😣", fg="magenta")
        sys.exit(1)


def main():
    _ascii_flare()

    try:
        github_username, github_password = _prompt_auth_info()
        repo_name, is_private = _prompt_repo_info()
        gitignore_langugage = _prompt_gitignore_language()

    except click.exceptions.Abort:
        click.secho("Operation Aborted ⚠️", fg="magenta")
        sys.exit(1)

    click.secho(
        "Thanks for all of your information, hang tight while we are at it..⏳",
        fg="green",
    )

    try:
        g, user = _do_github_auth(github_username, github_password)
        _create_local_repo(repo_name)
        _create_remote_repo(g, github_username, repo_name, is_private)
        _connect_local_remote(repo_name, github_username, gitignore_langugage)

    except KeyboardInterrupt:
        click.secho("Operation Aborted ⚠️", fg="magenta")
        sys.exit(1)


if __name__ == "__main__":
    main()
