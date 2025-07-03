import os
import sys
from .parser import parse_command
from .executor import execute_command
from .history import History
from .logger import Logger

def main():
    history = History()
    logger = Logger()

    while True:
        try:
            prompt_string = f"{os.getcwd()} >> "
            sys.stdout.write(prompt_string)
            sys.stdout.flush()

            command = input()

            if not command:
                continue

            history.add(command)
            logger.log(command)

            if command.lower() == "exit":
                break

            parsed_commands = parse_command(command)
            execute_command(parsed_commands)

        except (KeyboardInterrupt, EOFError):
            print("\nExiting shell.")
            break
        except Exception as e:
            print(f"An error occurred: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
