import getpass
import os
import subprocess
import sys
from pprint import pprint

from colorama import init
from github import Github
from termcolor import cprint

from github3 import login
from pyfiglet import figlet_format
from PyInquirer import Token, print_json, prompt, style_from_dict

init(strip=not sys.stdout.isatty())


def cli():

    text = "Protomate"
    ascii_banner = figlet_format(text, font="standard")
    cprint(ascii_banner, "green", attrs=["bold"])

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
        {"type": "input", "name": "repo_name", "message": "Repository Name:"},
        {"type": "input", "name": "github_username", "message": "GitHub Username:"},
        {"type": "password", "name": "github_password", "message": "GitHub Password:"},
        {
            "type": "list",
            "name": "repo_type",
            "message": "Repository Type:",
            "choices": ["Public", "Private"],
        },
    ]

    answers = prompt(questions, style=style)

    return answers


def create_local_repo(repo_name):

    try:
        os.mkdir(repo_name)
    except Exception:
        print("local repository '{}' already exists".format(repo_name))
        repo_name = None
        return repo_name


def create_remote_repo(repo_name, repo_type, github_username, github_password):

    g = Github(github_username, github_password)
    user = g.get_user()

    try:
        if user.login:
            print("login successful")

            try:
                if repo_type == "Public":
                    user.create_repo(repo_name, private=False)
                else:
                    user.create_repo(repo_name, private=True)

                cmd = """
                    cd {0}
                    git init
                    git remote add origin git@github.com:{1}/{0}.git
                    touch README.md
                    git add .
                    git commit -m "Initial commit"
                    git push -u origin master
                    code .
                    """.format(
                    repo_name, github_username
                )
                subprocess.check_output(cmd, shell=True)
                print("local and remote repository successfully created")

            except Exception:
                print("remote repository '{}' already exists".format(repo_name))
                os.rmdir(repo_name)

    except Exception:
        print("incorrect username or password")
        os.rmdir(repo_name)


if __name__ == "__main__":

    answers = cli()
    repo_name = answers.get("repo_name")
    repo_type = answers.get("repo_type")
    github_username = answers.get("github_username")
    github_password = answers.get("github_password")
    repo_name = create_local_repo(repo_name)
    if repo_name is not None:
        create_remote_repo(repo_name, repo_type, github_username, github_password)
