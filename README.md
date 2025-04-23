# llm-evals-cli

[![PyPI](https://img.shields.io/pypi/v/llm-evals-cli.svg)](https://pypi.org/project/llm-evals-cli/)
[![Changelog](https://img.shields.io/github/v/release/kevinschaul/llm-evals-cli?include_prereleases&label=changelog)](https://github.com/kevinschaul/llm-evals-cli/releases)
[![Tests](https://github.com/kevinschaul/llm-evals-cli/actions/workflows/test.yml/badge.svg)](https://github.com/kevinschaul/llm-evals-cli/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/kevinschaul/llm-evals-cli/blob/master/LICENSE)

A CLI tool for running and managing LLM evaluations

## Installation

Install this tool using `pip`:
```bash
pip install llm-evals-cli
```
## Usage

For help, run:
```bash
llm-evals-cli --help
```
You can also use:
```bash
python -m llm_evals_cli --help
```
## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:
```bash
cd llm-evals-cli
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
