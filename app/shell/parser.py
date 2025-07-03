import shlex

def parse_command(command):
    # This function will be expanded to handle pipes and redirection
    return [{'command': shlex.split(command), 'stdin': None, 'stdout': None, 'stdout_append': None}]
