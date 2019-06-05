import sys
import os
from github import Github
import subprocess

# extracting project path, github username and password from bashrc
try:
    username = os.environ["GITHUB_USERNAME"]
    password = os.environ["GITHUB_PASSWORD"]
    path = os.environ["PROJECT_PATH"]

except:
    print("bashrc variables are not found")

# repository name
repo_name = str(sys.argv[1])
full_path = path + repo_name

# checking if the local repository already exists
if os.path.exists(full_path):
    print("local repository '{}' exists".format(repo_name))

# creation of local and remote repository
elif not os.path.exists(full_path):
    os.mkdir(full_path)
    try:
        user = Github(username, password).get_user()
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
            full_path, username, repo_name
        )
        subprocess.check_output(cmd, shell=True)

        print("local and remote repository successfully created")

    except:
        print("remote repository '{}' already exists".format(repo_name))

else:
    pass

