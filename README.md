# ai-yardstick

[![PyPI](https://img.shields.io/pypi/v/ai-yardstick.svg)](https://pypi.org/project/ai-yardstick/)
[![Changelog](https://img.shields.io/github/v/release/kevinschaul/ai-yardstick?include_prereleases&label=changelog)](https://github.com/kevinschaul/ai-yardstick/releases)
[![Tests](https://github.com/kevinschaul/ai-yardstick/actions/workflows/test.yml/badge.svg)](https://github.com/kevinschaul/ai-yardstick/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/kevinschaul/ai-yardstick/blob/master/LICENSE)

A CLI tool for running and managing LLM evaluations

See [my own evals](https://github.com/kevinschaul/llm-evals/)

## Installation

Install this tool using `pip`:
```bash
pip install ai-yardstick
```
## Usage

Create a new eval with:
```bash
ai-yardstick create EVAL_NAME
```

Then edit prompts.csv, models.csv and tests.csv with your test cases.

Run an eval with:
```bash
ai-yardstick run path/to/config.yaml
```

## Configuration File

A configuration file (YAML) defines your evaluation settings. Keys include:

- `name`: Identifier for the evaluation.
- `description`: Brief description of the evaluation.
- `models`: Path to your `models.csv` file (relative to the config file).
- `prompts`: Path to your `prompts.csv` file (relative to the config file).
- `tests`: Path to your `tests.csv` file (relative to the config file).
- `cache_dir`: (Optional) Directory to store LLM response cache. Defaults to `.ai-yardstick-cache`.
- `output_dir`: (Optional) Directory for results. Defaults to `results`.
- `results_file`: (Optional) Filename for detailed results CSV. Defaults to `results.csv`.
- `aggregate_file`: (Optional) Filename for aggregate results CSV. Defaults to `aggregate.csv`.
- `transform_func`: (Optional) Post-process LLM output. Can be:
  - A built-in name, e.g. `parse_boolean`.
  - A path to a Python file defining a function named `transform_output`.
  - A dict spec `{file: "path.py", function: "func_name"}`.

Example `ai-yardstick-config.yaml`:
```yaml
# Configuration for my evaluation
name: myeval
description: "Translate sentences to French"

# Input files (CSV format)
models: models.csv
prompts: prompts.csv
tests: tests.csv

# Optional settings
cache_dir: .ai-yardstick-cache
output_dir: results
results_file: detailed.csv
aggregate_file: summary.csv

# Optional transform function (convert YES/NO to boolean)
transform_func: parse_boolean
```

## CSV File Formats

ai-yardstick relies on three CSV inputs. All CSVs support an optional header row.

### models.csv
List of model identifiers, one per line. Header `model` is recommended but not required.

Each model must be a valid [`llm` model](https://llm.datasette.io/) that is installed and set up on your system.
```csv
model
openai/gpt-4o-mini
claude-3.7-sonnet
gemini-1.5-flash-latest
```

### prompts.csv
Prompt templates with placeholders matching test input column names. Header `prompt` is recommended.
```csv
prompt
"Translate '{sentence}' to French"
"Summarize: {paragraph}"
```

### tests.csv
Test cases as rows. Each column (except `expected_output`) becomes an input variable in your prompt templates.
The `expected_output` column holds the ground-truth for evaluation.
```csv
# Example with one input variable
sentence,expected_output
"Hello, world","Bonjour le monde"

# Example with multiple inputs
text,language,expected_output
"Good morning","Spanish","Buenos días"
```

For help, run:
```bash
ai-yardstick --help
```
You can also use:
```bash
python -m llm_evals_cli --help
```
## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:
```bash
cd ai-yardstick
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
To run the tests and linters:
```bash
just
```
To fix linter issues:
```bash
just fix
```
