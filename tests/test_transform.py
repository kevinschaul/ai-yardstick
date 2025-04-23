import pytest

from ai_yardstick.cli import (
    load_function_from_file,
    get_transform_function,
    parse_boolean,
)

def test_load_function_from_file(tmp_path):
    file = tmp_path / "mod.py"
    file.write_text(
        "def transform_output(x):\n"
        "    return x + '!'"
    )
    fn = load_function_from_file(str(file), "transform_output")
    assert callable(fn)
    assert fn("hello") == "hello!"

def test_get_transform_function_builtin():
    fn = get_transform_function("parse_boolean")
    assert fn is parse_boolean

def test_get_transform_function_file(tmp_path):
    file = tmp_path / "mod.py"
    file.write_text(
        "def transform_output(x):\n"
        "    return x.upper()"
    )
    fn = get_transform_function(str(file))
    assert fn("aBc") == "ABC"

def test_get_transform_function_dict(tmp_path):
    file = tmp_path / "mod2.py"
    file.write_text(
        "def my_transform(x):\n"
        "    return x.lower()"
    )
    spec = {"file": str(file), "function": "my_transform"}
    fn = get_transform_function(spec)
    assert fn("ABC") == "abc"

def test_get_transform_function_invalid():
    with pytest.raises(ValueError):
        get_transform_function("unknown_function")