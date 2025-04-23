import os
import yaml
import pandas as pd
import pytest

from ai_yardstick.cli import (
    load_models_from_csv,
    load_prompts_from_csv,
    load_models,
    load_prompts,
    load_config,
    _load_dataset as load_dataset,
)

def test_load_models_from_csv_with_header(tmp_path):
    f = tmp_path / "models.csv"
    f.write_text("model\nm1\nm2\n")
    models = load_models_from_csv(str(f))
    assert models == ["m1", "m2"]

def test_load_models_from_csv_without_header(tmp_path):
    f = tmp_path / "models.csv"
    f.write_text("m1\nm2\n")
    models = load_models_from_csv(str(f))
    assert models == ["m1", "m2"]

def test_load_prompts_from_csv_with_header(tmp_path):
    f = tmp_path / "prompts.csv"
    f.write_text("prompt\nhello {name}\nhi {name}\n")
    prompts = load_prompts_from_csv(str(f))
    assert prompts == ["hello {name}", "hi {name}"]

def test_load_prompts_from_csv_without_header(tmp_path):
    f = tmp_path / "prompts.csv"
    f.write_text("hello\nhi\n")
    prompts = load_prompts_from_csv(str(f))
    assert prompts == ["hello", "hi"]

def test_load_models_list_and_file(tmp_path):
    lst = ["a", "b"]
    assert load_models(lst) == lst
    f = tmp_path / "models.csv"
    f.write_text("model\na\nb\n")
    assert load_models(str(f)) == ["a", "b"]

def test_load_prompts_list_and_file(tmp_path):
    lst = ["x", "y"]
    assert load_prompts(lst) == lst
    f = tmp_path / "prompts.csv"
    f.write_text("prompt\nx\ny\n")
    assert load_prompts(str(f)) == ["x", "y"]

def test_load_config(tmp_path):
    f = tmp_path / "config.yaml"
    content = {"a": 1, "b": [2, 3]}
    f.write_text(yaml.safe_dump(content))
    config = load_config(str(f))
    assert config == content

def test_load_dataset(tmp_path):
    # Create a CSV with multiple input columns and expected_output
    f = tmp_path / "tests.csv"
    f.write_text("inp1,inp2,expected_output\nhello,world,yes\nfoo,bar,no\n")
    ds = load_dataset(str(f))
    cases = list(ds.cases)
    assert len(cases) == 2
    c0 = cases[0]
    assert c0.inputs == {'inp1': 'hello', 'inp2': 'world'}
    assert c0.expected_output == 'yes'