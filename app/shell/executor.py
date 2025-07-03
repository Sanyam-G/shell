import os
import subprocess
import sys
from .analytics import show_analytics
from .logger import Logger


def execute_command(commands):
    if not commands:
        return

    # Handle built-in commands first
    cmd, *args = commands[0]['command']
    if cmd == "cd":
        try:
            os.chdir(args[0] if args else os.path.expanduser("~"))
        except FileNotFoundError:
            print(f"cd: no such file or directory: {args[0]}", file=sys.stderr)
        return

    if cmd == "pwd":
        print(os.getcwd())
        return

    if cmd == "analytics":
        logger = Logger()
        show_analytics(logger.log_file)
        return

    try:
        subprocess.run(commands[0]['command'], check=True)
    except FileNotFoundError:
        print(f"{cmd}: command not found", file=sys.stderr)
    except subprocess.CalledProcessError as e:
        print(f"{cmd}: command failed with exit code {e.returncode}", file=sys.stderr)