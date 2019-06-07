import sys
import os
from github import Github
import subprocess
import getpass


def protomate():
    # extracting project path from bashrc
    try:
        project_path = os.environ["PROJECT_PATH"]

    except:
        print("project path not found")
        project_path = None

    # creating local directory
    if project_path:
        try:
            repo_name = str(input("repository_name :"))
            local_path = project_path + repo_name
            os.mkdir(local_path)

        except:
            print("local repository '{}' already exists".format(repo_name))
            local_path = None

    # creating remote repository and linking with local directory
    if local_path:
        github_username = str(input("github_username :"))
        github_password = str(getpass.getpass(prompt="github_password: "))

        user = Github(github_username, github_password).get_user()

        try:
            if user.login:
                print("login successful")
                try:
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
                    os.rmdir(local_path)

        except:
            print("incorrect username or password")
            os.rmdir(local_path)


if __name__ == "__main__":
    protomate()



