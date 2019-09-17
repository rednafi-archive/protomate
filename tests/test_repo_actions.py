from protomate.repo_actions import create_local_repo,create_remote_repo

from protomate.repo_auths import authentication
from github import Github
import pytest

def test_create_remote_repo():
    username = 'deceptive-ai'
    password = 'creativepassword6969'
    repo_name = 'reddington'
    repo_type1 = 'public'
    repo_type2 = 'private'

    # logging into github with valid username and password
    g, user = authentication(username, password)



