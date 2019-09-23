from github import Github
import sys
import os
from protomate.languages import PROGRAMMING_LANGUAGES
import subprocess
from github.GithubException import GithubException
from protomate.utils import logfunc


@logfunc
def create_local_repo(repo_name):
    """Creates a local directory

    Parameters
    ----------
    repo_name : str
        Desired repository name.
    """

    try:
        os.mkdir(repo_name)

    except FileExistsError:
        sys.exit(f"LocalExistsError: Local repository '{repo_name}' already exists")


@logfunc
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

    try:
        if repo_type == "Private":
            user.create_repo(repo_name, private=True)

        else:
            user.create_repo(repo_name, private=False)

    except GithubException:
        sys.exit(
            f"RemoteCreationError: Remote repository '{repo_name}' already exists "
        )


@logfunc
def connect_local_to_remote(repo_name, github_username, gitignore):
    """Function that connects remote and local repositories.

    Parameters
    ----------
    repo_name : str
        Desired repository name.
    github_username : str
        Github user name where the repository will be created.
    gitignore : str
        Empty string or gitignore language.

    """

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
        if gitignore != "" and gitignore.lower() in PROGRAMMING_LANGUAGES:
            cmd_gitignore
            subprocess.check_output(cmd_gitignore, shell=True)

        elif gitignore != "" and gitignore.lower() not in PROGRAMMING_LANGUAGES:
            print("Language not supported:\n Creating repository without .gitignore")
            cmd
            subprocess.check_output(cmd, shell=True)

        else:
            cmd
            subprocess.check_output(cmd, shell=True)

        print("Local and remote repository successfully created")

    except Exception:
        sys.exit("Local and remote repository cannot be connected")
