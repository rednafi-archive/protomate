from github import Github
from loguru import logger
import sys
import keyring


def authentication(github_username, github_password):
    """Function for github authentication

    Parameters
    ----------
    github_username : str
        Github user name where the repository will be created.
    github_password : str
        Github password.

    Returns
    -------
    g : github.MainClass.Github
        Github object from PyGithub package.
    user : github.AuthenticatedUser.AuthenticatedUser
        Authenticated user object from PyGithub package.
    """

    g = Github(github_username, github_password)
    user = g.get_user()

    try:
        user.login

    except Exception as e:
        logger.exception(e)
        sys.exit("AuthError: Username or password is incorrect")

    return (g, user)


def is_pass_saved(github_username):
    appname = "protomate"
    username = github_username
    password = keyring.get_password(appname, username)
    if password is not None:
        
        g = Github(username, password)
        user = g.get_user()
        try:
            user.login
            is_saved = True
        except Exception as e:
            is_saved = False
            print("\nWrong password saved. Enter your password again.\n")
    else:
        is_saved = False
    return is_saved


def save_pass(password_save, github_username, password):
    appname = "protomate"
    username = github_username
    if password_save == "Yes":
        keyring.set_password(appname, username, password)


def retrieve_pass(github_username):
    appname = "protomate"
    username = github_username
    password = keyring.get_password(appname, username)
    return password


def delete_pass(github_username):
    appname = "protomate"
    username = github_username
    keyring.delete_password(appname, username)
