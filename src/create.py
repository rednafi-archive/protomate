import sys
import os
from github import Github
import subprocess
import getpass

# prompting for credentials
try:
    github_username = str(input("github_username :"))
    github_password = str(getpass.getpass(prompt="github_password: "))

except:
    print("username or password is incorrect")

# extracting project path from bashrc
try:
    project_path = os.environ["PROJECT_PATH"]

except:
    print("project path not found")

# prompting for repository name
repo_name = str(input("repository_name :"))
local_path = project_path + repo_name

# checking if the local repository already exists
if os.path.exists(local_path):
    print("local repository '{}' exists".format(repo_name))

# creation of local and remote repository
else:
    os.mkdir(local_path)
    try:
        user = Github(github_username, github_password).get_user()
        repo = user.create_repo(repo_name)
        cmd = """
            cd {0}
            git init
            git remote add origin git@github.com:{1}/{2}.git
            touch README.md
            git add .
            git commit -m "Initial commit"
            git push -u origin master
            code {0}
            """.format(
            local_path, github_username, repo_name
        )
        subprocess.check_output(cmd, shell=True)

        print("local and remote repository successfully created")

    except:
        print("remote repository '{}' already exists".format(repo_name))

