import getpass
import os
import shutil
import subprocess
import sys
from pprint import pprint

import colorama
from github import Github
from pyfiglet import figlet_format
from PyInquirer import Token, print_json, prompt, style_from_dict
from termcolor import cprint

import languages

colorama.init(strip=not sys.stdout.isatty())


def cli():

    text = "Protomate"
    ascii_banner = figlet_format(text, font="standard")
    cprint(ascii_banner, "cyan", attrs=["bold"])

    style = style_from_dict(
        {
            Token.QuestionMark: "#E91E63 bold",
            Token.Answer: "#fac731 bold",
            Token.Instruction: "#ef8a62",
            Token.Separator: "#cc5454",
            Token.Selected: "#7fc97f",
            Token.Pointer: "#fdc086",
            Token.Question: "",
        }
    )

    questions = [
        {"type": "input", "name": "github_username", "message": "GitHub Username:"},
        {"type": "password", "name": "github_password", "message": "GitHub Password:"},
        {"type": "input", "name": "repo_name", "message": "Repository Name:"},
        {
            "type": "list",
            "name": "repo_type",
            "message": "Repository Type:",
            "choices": ["Public", "Private"],
        },
        {
            "type": "input",
            "name": "gitignore",
            "message": "(Optional) Please enter language name to create .gitignore file, press enter if you don't want.",
        },
    ]

    answers = prompt(questions, style=style)

    github_username = answers["github_username"]
    github_password = answers["github_password"]
    repo_name = answers["repo_name"]
    repo_type = answers["repo_type"]
    gitignore = answers["gitignore"]

    return github_username, github_password, repo_name, repo_type, gitignore


def authentication(github_username, github_password):

    g = Github(github_username, github_password)
    user = g.get_user()

    try:
        user.login

    except Exception:
        sys.exit("AuthError: Username or password is incorrect")

    return (g, user)


def create_local_repo(repo_name):

    try:
        os.mkdir(repo_name)

    except Exception:
        sys.exit(f"LocalExistsError: Local repository '{repo_name}' already exists")


def create_remote_repo(g, github_username, repo_name, repo_type):

    user = g.get_user()

    try:
        if repo_type == "Private":
            user.create_repo(repo_name, private=True)

        else:
            user.create_repo(repo_name, private=False)
    except Exception:

        sys.exit(
            f"RemoteCreationError: Remote repository '{repo_name}' already exists "
        )


def connect_local_to_remote(repo_name, github_username, gitignore):

    try:
        if gitignore != "" and gitignore.lower() in languages.PROGRAMMING_LANGUAGES:
            cmd = f"""
                cd {repo_name}
                git init
                git remote add origin git@github.com:{github_username}/{repo_name}.git
                touch README.md
                curl -X GET https://www.gitignore.io/api/{gitignore} > .gitignore
                git add .
                git commit -m "Initial commit"
                git push -u origin master
                code .
                """

        else:
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
        subprocess.check_output(cmd, shell=True)
        print("Local and remote repository successfully created")

    except Exception:
        sys.exit("Local and remote repository cannot be connected")


def main():
    github_username, github_password, repo_name, repo_type, gitignore = cli()
    print("Thanks for all your information, hang tight while we are at it")

    g, user = authentication(github_username, github_password)

    create_local_repo(repo_name)

    create_remote_repo(g, github_username, repo_name, repo_type)

    connect_local_to_remote(repo_name, github_username, gitignore)


if __name__ == "__main__":
    main()
