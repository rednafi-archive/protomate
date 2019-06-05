import sys
import os
from subprocess import call
from github import Github
import subprocess

# extracting project path, github username and password from bashrc

username = os.environ["GITHUB_USERNAME"]
password = os.environ["GITHUB_PASSWORD"]
path = os.environ["PROJECT_PATH"]

# repository name
repo_name = str(sys.argv[1])

# creation of local repository
if not os.path.exists(path + repo_name):
    os.mkdir(path + repo_name)
    user = Github(username, password).get_user()
    repo = user.create_repo(repo_name)

    cmd = """
        cd {0}{1}
        git init
        git remote add origin git@github.com:{2}/{3}.git
        touch README.md
        git add .
        git commit -m "Initial commit"
        git push -u origin master
        code.
        """.format(
        path, repo_name, username, repo_name
    )
    subprocess.check_output(cmd, shell=False)

    print("succesfully created repository {}".format(repo_name))

else:
    print("local repository already exists")

