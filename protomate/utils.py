import functools
import logging
import os
import subprocess
import sys

import click

from protomate.settings import RUNTIME_ENVIRONMENT


def find_shell_path(shell_name):
    """Finds out system's bash interpreter path"""

    if not os.name == "nt":
        cmd = ["which", "-a", shell_name]
    else:
        cmd = ["where", shell_name]

    try:
        c = subprocess.run(
            cmd, universal_newlines=True, check=True, capture_output=True
        )
        output = c.stdout.split("\n")
        output = [_ for _ in output if _]

        _shell_paths = [f"/bin/{shell_name}", f"/usr/bin/{shell_name}"]

        for path in output:
            if path == _shell_paths[0]:
                return path
            elif path == _shell_paths[1]:
                return path

    except subprocess.CalledProcessError:
        click.echo(
            click.style(
                "Error: Bash not found. Install Bash to use Rush.", fg="magenta"
            )
        )
        sys.exit(1)


def run_task(use_shell, command, interactive=True, catch_error=True):
    std_out = sys.stdout if interactive else subprocess.PIPE
    std_in = sys.stdin if interactive else subprocess.PIPE

    res = subprocess.run(
        [use_shell, "-c", command],
        stdout=std_out,
        stdin=std_in,
        stderr=std_out,
        universal_newlines=True,
        check=catch_error,
        capture_output=False,
    )
    click.echo("")
