# Python Shell

This project is a custom command-line shell implemented in Python.

## Features

*   **Interactive Prompt:** Provides a command-line interface for user interaction.
*   **Command Execution:** Supports running both built-in commands and external programs.
*   **Pipes (`|`):** Allows chaining commands, directing the output of one command as input to another.
*   **I/O Redirection (`>`, `>>`, `<`):** Enables redirecting command input from files and output to files.
*   **Command History:** Stores a history of executed commands.
*   **Usage Analytics:** Provides basic statistics on command usage.

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-username/shell.git
    cd shell
    ```

2.  Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To start the shell, run:

```bash
python -m app.main
```

### Built-in Commands

*   `cd <directory>`: Change the current directory.
*   `pwd`: Print the current working directory.
*   `exit`: Exit the shell.
*   `analytics`: Display command usage statistics.

## Testing

To run the unit tests, use:

```bash
python -m unittest discover tests
```