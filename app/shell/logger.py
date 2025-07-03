import os
import datetime

class Logger:
    def __init__(self, log_file='.shell_log.csv'):
        self.log_file = os.path.join(os.path.expanduser("~"), log_file)
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w') as f:
                f.write('timestamp,command\n')

    def log(self, command):
        with open(self.log_file, 'a') as f:
            timestamp = datetime.datetime.now().isoformat()
            f.write(f'{timestamp},{command}\n')

