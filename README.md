# File Agent

This is a simple AI agent that runs from the command line. The project was created as an exercise in using a language model API and allowing the model to call additional functions.

The agent uses the OpenRouter API and can, for example:

- list files and directories,
- read file contents,
- write data to files,
- run Python files,
- use the example calculator in the `calculator` directory.

The model chooses the right tool based on the user's request. The program runs for a maximum of 20 iterations by default, but this limit can be changed with the `--limit` argument.

## Requirements

- Python 3.12 or newer,
- an OpenRouter account and API key,
- `uv` for installing dependencies and running the project.

## Installation

From the `agenty` directory, create the environment and install the dependencies:

```bash
uv sync
```

Next, create a `.env` file in the `agenty` directory and add the API key:

```env
OPENROUTER_API_KEY=your_api_key
```

The key is loaded by `python-dotenv`. The `.env` file should not be added to the repository.

## Running the agent

Run the command from the `agenty` directory:

```bash
uv run python main.py "Read the file calculator/README.md"
```

Extra information about token usage and function results can be enabled with `--verbose`:

```bash
uv run python main.py --verbose "What files are in the calculator directory?"
```

The iteration limit can also be set manually:

```bash
uv run python main.py --limit 5 "Run the calculator tests"
```

The agent communicates with the `openrouter/free` model. Before returning the final answer, the model can make several function calls if it needs more information.

## Project structure

```text
agenty/
├── main.py                    # starts the agent and handles CLI arguments
├── prompt.py                  # system instructions for the model
├── config.py                  # configuration constants
├── functions/                 # functions available to the agent
├── calculator/                # small project used for testing the agent
├── test_*.py                  # examples of calling the functions
└── pyproject.toml             # dependencies and tool configuration
```

The main functions in the `functions` directory are:

- `get_files_info` - lists files and directories in an allowed folder,
- `get_file_content` - reads a file,
- `write_file` - creates or overwrites a file,
- `run_python_file` - runs a Python file with optional arguments,
- `call_function` - selects and calls the function requested by the model.

File operations are limited to the working directory passed to the functions. File contents are also limited to 10,000 characters so that one large file does not use the entire model context.

## Tests

The calculator tests can be run with:

```bash
uv run python -m unittest calculator.tests
```

The `test_*.py` files also contain examples of calling the agent functions. For example:

```bash
uv run python test_get_files_info.py
```

## Code quality

The repository uses `ruff` and `pyright`. All pre-commit hooks can be run from the root directory of the repository:

```bash
pre-commit run --all-files
```
