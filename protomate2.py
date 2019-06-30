import getpass
import os
import shutil
import subprocess
import sys
from pprint import pprint

from colorama import init
from github import Github
from pyfiglet import figlet_format
from PyInquirer import Token, print_json, prompt, style_from_dict
from termcolor import cprint
import languages

init(strip=not sys.stdout.isatty())


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
        {"type" : "input", "name" : "gitignore", "message" : "(Optional) Please enter language name to create .gitignore file, press enter if you don't want."}
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
        auth = True

    except Exception:
        print("authError: Username or password is incorrect")
        auth = False

    return (auth, g, user)


def create_local_repo(repo_name):

    try:
        os.mkdir(repo_name)
        local_exists = False

    except Exception:
        print(
            "localExistsError: Local repository '{}' already exists".format(repo_name)
        )
        local_exists = True

    return local_exists


def check_existing_repo(g, github_username, repo_name):
    try:
        repo = g.get_repo("{}/{}".format(github_username, repo_name))
        print(
            "remoteExistsError: Remote repository '{}' already exists".format(repo_name)
        )
        remote_exists = True

    except Exception:
        remote_exists = False

    return remote_exists


def create_remote_repo(g, github_username, repo_name, repo_type):

    user = g.get_user()

    try:
        remote_created = True
        if repo_type == "Private":
            user.create_repo(repo_name, private=True)

        else:
            user.create_repo(repo_name, private=False)
    except Exception:
        remote_created = False
        print(
            "remoteCreateError: Cannot create remote repository '{}'".format(repo_name)
        )

    return remote_created


def connect_local_to_remote(repo_name, github_username, gitignore):

    try:
        if gitignore is not '' and gitignore.lower() in languages.PROGRAMMING_LANGUAGES:
            cmd = """
                cd {repo_name}
                git init
                git remote add origin git@github.com:{github_username}/{repo_name}.git
                touch README.md
                curl -X GET https://www.gitignore.io/api/{gitignore} > .gitignore
                git add .
                git commit -m "Initial commit"
                git push -u origin master
                code .
                """.format(
                repo_name=repo_name, github_username=github_username, gitignore=gitignore 
            )
        else:
            cmd = """
                cd {repo_name}
                git init
                git remote add origin git@github.com:{github_username}/{repo_name}.git
                touch README.md
                git add .
                git commit -m "Initial commit"
                git push -u origin master
                code .
                """.format(
                repo_name=repo_name, github_username=github_username
            )
        subprocess.check_output(cmd, shell=True)
        print("Local and remote repository successfully created")
        connected = True

    except Exception:
        print("Local and remote repo can't be connected")
        connected = False

    return connected


def main():
    github_username, github_password, repo_name, repo_type, gitignore = cli()
    print("Thanks for all your information, hang tight while we are at it")

    auth, g, user = authentication(github_username, github_password)

    if auth:
        local_exists = create_local_repo(repo_name)

        if not local_exists:
            remote_exists = check_existing_repo(g, github_username, repo_name)

            if not remote_exists:
                remote_created = create_remote_repo(
                    g, github_username, repo_name, repo_type
                )

                if remote_created:
                    connected = connect_local_to_remote(repo_name, github_username, gitignore)


if __name__ == "__main__":
    main()
