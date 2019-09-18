import os
import sys

from protomate.repo_auths import (
    authentication,
    is_pass_saved,
    save_pass,
    retrieve_pass,
    delete_pass,
)

import keyring
from github import Github
from github.GithubException import BadCredentialsException
import pytest


def test_authentication():
    correct_user = "deceptive-ai"
    correct_pass = "creativepassword6969"
    incorrect_user = "absfdf"
    incorrect_pass = "sfsfe"

    # when username and password is correct
    __, github_auth_user = authentication(correct_user, correct_pass)
    assert github_auth_user.login == correct_user

    # when username or password is incorrect
    with pytest.raises(SystemExit):
        assert authentication(incorrect_user, incorrect_pass)


def test_is_pass_saved():
    appname = "protomate"
    username_exists = "deceptive-ai"
    password_exists = "creativepassword6969"

    username_doesnot_exist = "habijabi"

    # saving the pass for checking
    keyring.set_password(appname, username_exists, password_exists)
    password_exists = keyring.get_password(appname, username_exists)

    # when username and password exists
    flag = is_pass_saved(username_exists)
    assert flag == True

    # when username or password do not exist
    flag = is_pass_saved(username_doesnot_exist)
    assert flag == False


def test_save_pass():
    appname = "protomate"
    username = "bankok"
    password = "shanghai"
    password_save = "Yes"

    save_pass(password_save, username, password)
    assert keyring.get_password(appname, username) == password


def test_retrieve_pass():
    appname = "protomate"
    username = "bankok"
    password = "shanghai"

    keyring.set_password(appname, username, password)
    assert retrieve_pass(username) == password


def test_delete_pass():
    appname = "protomate"
    username = "bankok"
    password = "shanghai"

    keyring.set_password(appname, username, password)
    delete_pass(username)
    assert keyring.get_password(appname, username) is None
