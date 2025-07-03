# Advanced Python Shell

This project is a custom shell built with Python, designed to be both powerful and user-friendly. It supports essential shell features and includes a unique analytics tool to help you understand your command usage.

## Features

*   **Interactive Shell:** A familiar command-line interface.
*   **Command Execution:** Runs built-in and external commands.
*   **Pipes (`|`):** Chain multiple commands together.
*   **I/O Redirection (`>`, `>>`, `<`):** Redirect input and output streams.
*   **Command History:** Persists command history across sessions.
*   **Usage Analytics:** Provides insights into your command patterns.

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
*   `analytics`: Display command usage analytics.

### Analytics

The `analytics` command shows your top 10 most used commands and a bar chart visualization.

## Testing

To run the unit tests, use:

```bash
python -m unittest discover tests
```
