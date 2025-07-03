def _manual_split(command_string):
    """
    Manually splits a command string into arguments, respecting single and double quotes.
    This is a simplified version of what a real shell would do.
    """
    args = []
    current_arg = ''
    in_single_quote = False
    in_double_quote = False

    # We add a space at the end to make sure the last argument is processed.
    for char in command_string.strip() + ' ':
        if char.isspace() and not in_single_quote and not in_double_quote:
            if current_arg:
                args.append(current_arg)
                current_arg = ''
        elif char == "'" and not in_double_quote:
            in_single_quote = not in_single_quote
        elif char == '"' and not in_single_quote:
            in_double_quote = not in_double_quote
        else:
            current_arg += char
    return args

def parse_command(command):
    """
    Parses a full command line, including pipes and I/O redirection.
    """
    commands = []
    # First, split the command by the pipe operator
    for cmd_str in command.split('|'):
        # Manually split each sub-command into parts
        parts = _manual_split(cmd_str)
        
        i = 0
        command_and_args = []
        stdin_redir, stdout_redir, stdout_append_redir = None, None, None

        # Identify redirection operators and filenames
        while i < len(parts):
            if parts[i] == '<':
                if i + 1 < len(parts):
                    stdin_redir = parts[i+1]
                    i += 2
                else:
                    # Syntax error, but we'll just skip for now
                    i += 1
            elif parts[i] == '>':
                if i + 1 < len(parts):
                    stdout_redir = parts[i+1]
                    i += 2
                else:
                    i += 1
            elif parts[i] == '>>':
                if i + 1 < len(parts):
                    stdout_append_redir = parts[i+1]
                    i += 2
                else:
                    i += 1
            else:
                command_and_args.append(parts[i])
                i += 1
        
        # Only add if a valid command was found
        if command_and_args:
            commands.append({
                'command': command_and_args,
                'stdin': stdin_redir,
                'stdout': stdout_redir,
                'stdout_append': stdout_append_redir
            })

    return commands