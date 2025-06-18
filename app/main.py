import os
import sys
import subprocess
import datetime



def main():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    builtin_commands = ["exit", "echo", "type", "pwd", "cd"]
    path_env = os.getenv('PATH')  # Get path string

    while True:
        prompt_string = f"${os.getcwd()}                                                                                       {current_time} \n>> "
        sys.stdout.write(prompt_string)

        # Wait for user input
        command = input()

        # Base
        if command == "exit 0":
            break
        # Second base command
        elif command.startswith("echo ") and len(command)>len("echo "):
            print(command[len("echo "):])
        # If command starts with "type"
        elif command.startswith("type ") and len(command)>len("type "):
            builtin_found = False #Flag for builtin
            command_without_type = command[len("type "):] #Splice out 'type ' from the command
            for i in builtin_commands: # Loop through builtin_commands list
                is_builtin = command_without_type == i #Check whether command is builtin
                if is_builtin:
                    builtin_found = True #set flag
                    print(f"{command_without_type} is a shell builtin")
                    break
            if not builtin_found: #If not found command in builtin,
                if find_function_path(path_env, command_without_type) == "Not found":
                    print(f"{command_without_type}: not found")
                else:
                    print(f"{command_without_type} is " + find_function_path(path_env, command_without_type))


        elif command == "pwd":
            print(os.getcwd())
        elif command == "cd":
            os.chdir("/")
        elif command == "cd ..":
            os.chdir("..")
        elif command.startswith("cd ") and len(command)>len("cd "):
            try:
                os.chdir(command[len("cd "):])
            except FileNotFoundError:
                print("no such directory, please try again")
        else:  # Everything else, Base case
            parsed_args = []
            in_quote = False
            current_arg = []

            for part in command.split():
                if part.startswith('"') and not in_quote:
                    in_quote = True
                    current_arg.append(part[1:])  # Add content after the opening quote
                    if part.endswith('"'):  # Handle single-word quoted arguments e.g., "word"
                        in_quote = False
                        parsed_args.append(
                            " ".join(current_arg[:-1]) + " " + current_arg[-1][:-1] if len(current_arg) > 1 else
                            current_arg[0][:-1])
                        current_arg = []
                elif part.endswith('"') and in_quote:
                    in_quote = False
                    current_arg.append(part[:-1])  # Add content before the closing quote
                    parsed_args.append(" ".join(current_arg))
                    current_arg = []
                elif in_quote:
                    current_arg.append(part)
                else:
                    parsed_args.append(part)

            # If a quote was opened but not closed (malformed command), add the accumulated parts
            if in_quote:
                parsed_args.append(" ".join(current_arg))


            if not parsed_args:  # Handle empty input after parsing
                continue

            cmd = parsed_args[0]
            args = parsed_args[1:]

            full_function_path = find_function_path(path_env, cmd)
            if full_function_path != "Not found":
                # Pass the arguments directly to subprocess.run
                result = subprocess.run([full_function_path] + args, capture_output=True, text=True, check=False)
                if result.stdout:
                    sys.stdout.write(result.stdout)
                if result.stderr:  # Use 'if' to print both stdout and stderr if present
                    sys.stderr.write(result.stderr)
            else:
                print(f"{command}: command not found")


# Function to find valid path to method
def find_function_path(path, command):
    list_of_paths = path.split(":")
    path_found = False
    for i in list_of_paths:
        potential_path = os.path.join(i, command) #path join {Path}+command
        path_found = os.path.exists(potential_path) #Boolean to check if created path exists
        if path_found:
            return potential_path
    if not path_found:
        return "Not found"



if __name__ == "__main__":
    main()
