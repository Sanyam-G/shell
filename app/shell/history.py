import os

class History:
    def __init__(self, history_file='.shell_history'):
        self.history_file = os.path.join(os.path.expanduser("~"), history_file)

    def add(self, command):
        with open(self.history_file, 'a') as f:
            f.write(command + '\n')

    def get(self):
        try:
            with open(self.history_file, 'r') as f:
                return f.readlines()
        except FileNotFoundError:
            return []
