# Expression Evaluator

A web-based mathematical expression evaluator with support for variable assignments and file input processing.

## Prerequisites

Make sure to install `uv` on your device:
```bash
pip install uv
```

**Alternative (if you don't want to use uv):** You can also use pip directly with the requirements file.

### Setup

1. Clone or extract the project files
2. Navigate to the project directory
3. Install dependencies:

**Option 1 - Using uv (recommended):**
```bash
uv sync
```

**Option 2 - Using pip:**
```bash
pip install -r requirements.txt
```

## Running the Application

### Web Interface

**If using uv:**
```bash
uv run main.py
```

**If using pip:**
```bash
python main.py
```

Then open your browser and navigate to: `http://localhost:5000`

### Running Tests

**If using uv:**
```bash
uv run pytest tests
```

**If using pip:**
```bash
pytest tests
```

## Sample Input File

You can create a `.in` file with multiple expressions to test the file input functionality. Here's an example:

**sample.in:**
```
a = 5
b = a + 2
c = b * 3
result = (a + b + c) / 3
x = 10
y = x % 3
final = y + result
```

This file can be loaded using the "Load File" button in the web interface to process all expressions at once.

## Architecture

The expression evaluator follows a classic interpreter design:

1. **Lexical Analysis** (`lexer.py`): Converts input text into tokens
2. **Parsing** (`parser.py`): Builds Abstract Syntax Tree (AST) from tokens
3. **Evaluation** (`evaluator.py`): Executes the AST and manages symbol table

## Development

### Pre-commit Setup (Optional)

For development with code quality checks:
```bash
# If venv not sourced
uv run pre-commit install

# If venv sourced
pre-commit install
```