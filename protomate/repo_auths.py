from github import Github
import sys
import keyring
from github.GithubException import BadCredentialsException
from protomate.utils import logfunc


@logfunc
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

    except BadCredentialsException:
        sys.exit("AuthError: Username or password is incorrect")

    return (g, user)


@logfunc
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

        except BadCredentialsException:
            is_saved = False
            print("\nWrong password saved. Enter your password again.\n")
    else:
        is_saved = False
    return is_saved


@logfunc
def save_pass(password_save, github_username, password):
    appname = "protomate"
    username = github_username
    if password_save == "Yes":
        keyring.set_password(appname, username, password)


@logfunc
def retrieve_pass(github_username):
    appname = "protomate"
    username = github_username
    password = keyring.get_password(appname, username)
    return password


@logfunc
def delete_pass(github_username):
    appname = "protomate"
    username = github_username
    keyring.delete_password(appname, username)
