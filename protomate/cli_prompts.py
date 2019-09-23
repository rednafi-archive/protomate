import questionary
from prompt_toolkit.styles import Style
import sys
from protomate.repo_auths import is_pass_saved, save_pass, retrieve_pass
import art
from sty import fg, rs
from termcolor import cprint
import colorama
from protomate.utils import logfunc

colorama.init(strip=not sys.stdout.isatty())


@logfunc
def draw_ascii_banner():
    """
    Draw Protomate banner !!!
    """
    text = "ProtomatE"
    ascii_banner = art.text2art(text, font="glenyn-large")
    ascii_banner = fg(255, 213, 128) + ascii_banner + fg.rs

    cprint(ascii_banner, attrs=["bold"])


@logfunc
def cli():
    """CLI function that shows a list of questions regarding
    github credentials and other functionalities.

    Returns
    -------
    github_username : str
        Github user name where the repository will be created.
    github_password : str
        Github password.
    repo_name : str
        Desired repository name.
    repo_type : str
        Whether the repository will be public or private.
    gitignore : str
        Question regarding whether to add a gitignore file or not.
        If yes then asks for the name of the gitignore language.

    """

    style = Style(
        [
            ("qmark", "fg:#e91e63 bold"),
            ("answer", "fg:#fac731"),
            ("instruction", "fg:#f06292"),
            ("separator", "fg:#cc5454"),
            ("selected", "fg:#7fc97f"),
            ("pointer", "fg:#fdc086"),
            ("question", "fg:#d3d7cF"),
        ]
    )

    github_username = questionary.text("GitHub Username:", style=style).ask()

    PASS_SAVED = is_pass_saved(github_username)
    if not PASS_SAVED:
        github_password = (
            questionary.password("GitHub Password:", style=style)
            .skip_if(PASS_SAVED, default=False)
            .ask()
        )
    else:
        github_password = retrieve_pass(github_username)

    password_save = (
        questionary.select(
            "Do you want to save your password?", choices=["Yes", "No"], style=style
        )
        .skip_if(PASS_SAVED, default=False)
        .ask()
    )

    repo_name = questionary.text("Repository Name:", style=style).ask()
    repo_type = questionary.select(
        "Repository Type:", choices=["Public", "Private"], style=style
    ).ask()

    gitignore = questionary.text(
        """Gitignore(Optional):
            Please enter the desired language name to create
            .gitignore file, press enter if you don't want to:
            """,
        style=style,
    ).ask()

    return (
        github_username,
        github_password,
        password_save,
        repo_name,
        repo_type,
        gitignore,
    )
