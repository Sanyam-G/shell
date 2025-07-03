import os
import subprocess
import sys
from .analytics import show_analytics
from .logger import Logger


def execute_command(commands):
    # If there are no commands, just return.
    if not commands:
        return

    # This is a list to keep track of all the processes we start.
    processes = []

    # We set the initial input to be the standard input of the shell.
    input_fd = sys.stdin.fileno()

    for i, cmd_info in enumerate(commands):
        command = cmd_info['command']
        
        # Check for built-in commands first.
        if command[0] == "cd":
            try:
                # If no directory is given, go to the home directory.
                path = command[1] if len(command) > 1 else os.path.expanduser("~")
                os.chdir(path)
            except FileNotFoundError:
                print(f"cd: no such file or directory: {path}", file=sys.stderr)
            # 'cd' is a special case, it doesn't create a new process.
            # So we can just continue to the next command if there is one (which is not typical).
            continue

        if command[0] == "pwd":
            print(os.getcwd())
            continue

        if command[0] == "analytics":
            logger = Logger()
            show_analytics(logger.log_file)
            continue

        # Set up the output for the current command.
        # If this is not the last command, the output goes to a new pipe.
        # Otherwise, it goes to the standard output.
        is_last_command = i == len(commands) - 1
        output_fd = sys.stdout.fileno()
        if not is_last_command:
            # Create a new pipe for the next command to read from.
            read_fd, write_fd = os.pipe()
            output_fd = write_fd

        # Set up I/O redirection.
        stdin_path = cmd_info['stdin']
        stdout_path = cmd_info['stdout']
        stdout_append_path = cmd_info['stdout_append']

        if stdin_path:
            input_fd = os.open(stdin_path, os.O_RDONLY)
        if stdout_path:
            output_fd = os.open(stdout_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
        if stdout_append_path:
            output_fd = os.open(stdout_append_path, os.O_WRONLY | os.O_CREAT | os.O_APPEND)

        try:
            # Create a new process for the command.
            proc = subprocess.Popen(
                command,
                stdin=input_fd if i == 0 else processes[-1].stdout,
                stdout=output_fd if is_last_command else subprocess.PIPE,
                stderr=sys.stderr,
            )
            processes.append(proc)

            # The input for the next command will be the output of this one.
            if not is_last_command:
                input_fd = proc.stdout

        except FileNotFoundError:
            print(f"{command[0]}: command not found", file=sys.stderr)
            break
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            break

    # Wait for all the processes to finish.
    for proc in processes:
        proc.wait()
