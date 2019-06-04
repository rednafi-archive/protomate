import sys
import os
from github import Github

path = "./"
username = os.environ["GITHUB_USERNAME"]
password = os.environ["GITHUB_PASSWORD"]  


def create():
    folder_name = str(sys.argv[1])
    os.makedirs(path + folder_name))
    user = Github(username, password).get_user()
    repo = user.create_repo(sys.argv[1])
    print("Succesfully created repository {}".format(sys.argv[1]))


if __name__ == "__main__":
    create()
print(username, password)