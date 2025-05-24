import os
import sys
import subprocess


def main():
    builtin_commands = ["exit", "echo", "type"]
    path_env = os.getenv('PATH')  # Get path string

    while True:
        sys.stdout.write("$ ")

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


        else: # Everything else, Base case
            parts_of_command = command.split()
            cmd = parts_of_command[0]
            args = parts_of_command[1:]
            full_function_path = find_function_path(path_env, cmd)
            if full_function_path != "Not found":
                full_function_call = [full_function_path] + args
                function_executable = [cmd] + args
                result = subprocess.run(function_executable, executable=full_function_path, capture_output=True, text=True, check=False)
                if result.stdout:
                    sys.stdout.write(result.stdout)  # Use sys.stdout.write to print exactly what the command outputted

                    # Print the actual stderr from the command
                elif result.stderr:
                    sys.stderr.write(result.stderr)  # Use sys.stderr.write for error output
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
