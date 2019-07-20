import getpass
import os
import shutil
import subprocess
import sys
from pprint import pprint

import colorama
import questionary
from github import Github
from loguru import logger
from prompt_toolkit.styles import Style
from pyfiglet import figlet_format
from termcolor import cprint

import protomate.languages as languages

colorama.init(strip=not sys.stdout.isatty())

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


class Protomate(object):
    def __init__(self):
        pass

    def cli(self):
        """CLI function that shows a list of questions regarding github credentials and other functionalities.

        Returns
        -------
        github_username : str
        github_password : str
        repo_name : str
        repo_type : str
        gitigore : str
            Question regarding whether to add a gitignore file or not. If yes, then asks for the name of the gitignore language.

        """

        self.text = "protomate"
        self.ascii_banner = figlet_format(self.text, font="standard")
        cprint(self.ascii_banner, "cyan", attrs=["bold"])

        self.style = Style(
            [
                ("qmark", "fg:#E91E63 bold"),
                ("answer", "fg:#fac731 bold"),
                ("instruction", "fg:#ef8a62"),
                ("separator", "fg:#cc5454"),
                ("selected", "fg:#7fc97f"),
                ("pointer", "fg:#fdc086"),
                ("question", ""),
            ]
        )

        self.questions = [
            {"type": "text", "name": "github_username", "message": "GitHub Username:"},
            {
                "type": "password",
                "name": "github_password",
                "message": "GitHub Password:",
            },
            {"type": "text", "name": "repo_name", "message": "Repository Name:"},
            {
                "type": "select",
                "name": "repo_type",
                "message": "Repository Type:",
                "choices": ["Public", "Private"],
            },
            {
                "type": "text",
                "name": "gitignore",
                "message": "(Optional) Please enter language name to create .gitignore file,\n press enter if you don't want to:",
            },
        ]

        self.answers = questionary.prompt(self.questions, style=self.style)

        self.github_username = self.answers["github_username"]
        self.github_password = self.answers["github_password"]
        self.repo_name = self.answers["repo_name"]
        self.repo_type = self.answers["repo_type"]
        self.gitignore = self.answers["gitignore"]

        return (
            self.github_username,
            self.github_password,
            self.repo_name,
            self.repo_type,
            self.gitignore,
        )

    def authentication(self, github_username, github_password):
        """Function for github authentication

        Parameters
        ----------
        github_username : str
        github_password : str

        Returns
        -------
        g : github.MainClass.Github
        user : github.AuthenticatedUser.AuthenticatedUser
        """

        self.g = Github(github_username, github_password)
        self.user = self.g.get_user()

        try:
            self.user.login

        except Exception as e:
            logger.exception(e)
            sys.exit("AuthError: Username or password is incorrect")

        return (self.g, self.user)

    def create_local_repo(self, repo_name):
        """Creates a local directory

        Parameters
        ----------
        repo_name : str
            Takes in the name of the local directory
        """

        try:
            os.mkdir(repo_name)

        except Exception as e:
            logger.error(e)
            sys.exit(f"LocalExistsError: Local repository '{repo_name}' already exists")

    def create_remote_repo(self, g, github_username, repo_name, repo_type):
        """Function that creates remote repository.

        Parameters
        ----------
        g : github.MainClass.Github
        github_username : str
        repo_name : str
        repo_type : str
        """

        self.user = g.get_user()

        try:
            if repo_type == "Private":
                self.user.create_repo(repo_name, private=True)

            else:
                self.user.create_repo(repo_name, private=False)

        except Exception as e:
            logger.exception(e)
            sys.exit(
                f"RemoteCreationError: Remote repository '{repo_name}' already exists "
            )

    def connect_local_to_remote(self, repo_name, github_username, gitignore):
        """Function that connects remote and local repositories.

        Parameters
        ----------
        repo_name : str
        github_username : str
        gitignore : str

        """

        self.cmd = f"""
                cd {repo_name}
                git init
                git remote add origin git@github.com:{github_username}/{repo_name}.git
                touch README.md
                git add .
                git commit -m "Initial commit"
                git push -u origin master
                code .
                    """

        self.cmd_gitignore = f"""
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

        try:
            if gitignore != "" and gitignore.lower() in languages.PROGRAMMING_LANGUAGES:
                self.cmd_gitignore
                subprocess.check_output(self.cmd_gitignore, shell=True)

            elif (
                gitignore != ""
                and gitignore.lower() not in languages.PROGRAMMING_LANGUAGES
            ):
                print(
                    "Language not supported:\n Creating repository without .gitignore"
                )
                self.cmd
                subprocess.check_output(self.cmd, shell=True)

            else:
                self.cmd
                subprocess.check_output(self.cmd, shell=True)

            print("Local and remote repository successfully created")

        except Exception as e:
            logger.exception(e)
            sys.exit("Local and remote repository cannot be connected")


def main():

    protomate = Protomate()
    github_username, github_password, repo_name, repo_type, gitignore = protomate.cli()

    print("")
    print("Thanks for all your information, hang tight while we are at it...")

    g, user = protomate.authentication(github_username, github_password)
    protomate.create_local_repo(repo_name)
    protomate.create_remote_repo(g, github_username, repo_name, repo_type)
    protomate.connect_local_to_remote(repo_name, github_username, gitignore)


if __name__ == "__main__":
    main()
