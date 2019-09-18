from protomate.repo_actions import (
    create_local_repo,
    create_remote_repo,
    connect_local_to_remote,
)

from protomate.repo_auths import authentication
from github import Github
from github.GithubException import UnknownObjectException
import pytest


def delete_repo(g, username, repo_name_public, repo_name_private):

    # delete public repo
    try:
        repo = g.get_repo(username + "/" + repo_name_public)
        repo.delete()
    except UnknownObjectException:
        pass

    # delete private repo
    try:
        repo = g.get_repo(username + "/" + repo_name_private)
        repo.delete()
    except UnknownObjectException:
        pass


def test_create_remote_repo():
    username = "deceptive-ai"
    password = "creativepassword6969"
    repo_name_public = "reddington"
    repo_name_private = "raymond"
    repo_type_public = "Public"
    repo_type_private = "Private"

    # log into github with valid username and password
    g = Github(username, password)

    # delete existing repo
    delete_repo(g, username, repo_name_public, repo_name_private)

    # create public remote repo
    create_remote_repo(g, username, repo_name_public, repo_type_public)

    # create private remote repo
    create_remote_repo(g, username, repo_name_private, repo_type_private)

    # check public repo
    try:
        repo = g.get_repo(username + "/" + repo_name_public)

        if not repo.private:
            flag_public = True

    except UnknownObjectException:
        flag_public = False

    assert flag_public == True

    # check private repo
    try:
        repo = g.get_repo(username + "/" + repo_name_private)

        if repo.private:
            flag_private = True

    except UnknownObjectException:
        flag_private = False

    assert flag_private == True

    # check systemExit
    with pytest.raises(SystemExit):
        g = Github("deceptive-ai", "creativepassword696")

        assert create_remote_repo(g, "fake-username", "fake-repo", "Private")


def test_connect_local_to_remote():
    pass
