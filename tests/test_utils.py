import pytest
import pandas as pd

from ai_yardstick.cli import (
    hash_arg,
    expand_dict_columns,
    calculate_aggregates,
    parse_boolean,
)


def test_hash_arg_simple_and_length():
    h1 = hash_arg(1)
    h2 = hash_arg(1)
    assert isinstance(h1, str)
    assert len(h1) == 8
    assert h1 == h2


def test_hash_arg_list_order_diff():
    # Order of list elements should affect hash
    assert hash_arg([1, 2]) != hash_arg([2, 1])


def test_hash_arg_dict_order_same():
    # Order of dict keys should not affect hash
    d1 = {"a": 1, "b": 2}
    d2 = {"b": 2, "a": 1}
    assert hash_arg(d1) == hash_arg(d2)


def test_parse_boolean_true():
    assert parse_boolean("YES") is True
    assert parse_boolean("some yes text") is True


def test_parse_boolean_false():
    assert parse_boolean("NO") is False
    assert parse_boolean("no way") is False


def test_parse_boolean_ambiguous_raises():
    with pytest.raises(ValueError):
        parse_boolean("YES and NO")


def test_parse_boolean_invalid_raises():
    with pytest.raises(ValueError):
        parse_boolean("maybe")


def test_expand_dict_columns_basic():
    df = pd.DataFrame({"id": [1, 2], "data": [{"a": 10, "b": 20}, {"a": 30, "b": 40}]})
    expanded = expand_dict_columns(df, ["data"])
    # Check new columns and values
    assert "data.a" in expanded.columns
    assert "data.b" in expanded.columns
    assert list(expanded["data.a"]) == [10, 30]
    assert list(expanded["data.b"]) == [20, 40]
    # Original column dropped, and id preserved
    assert "data" not in expanded.columns
    assert "id" in expanded.columns
    # Column order: id, data.a, data.b
    assert list(expanded.columns) == ["id", "data.a", "data.b"]


def test_expand_dict_columns_with_missing_keys():
    df = pd.DataFrame({"id": [1, 2], "data": [{"a": 100}, {"b": 200}]})
    expanded = expand_dict_columns(df, ["data"])
    # Missing keys should result in NaN (null) values
    vals_a = expanded["data.a"].tolist()
    assert vals_a[0] == 100
    assert pd.isna(vals_a[1])
    vals_b = expanded["data.b"].tolist()
    assert pd.isna(vals_b[0])
    assert vals_b[1] == 200


def test_calculate_aggregates():
    df = pd.DataFrame(
        {
            "attributes.model": ["m1", "m1", "m1", "m2"],
            "attributes.prompt": ["p1", "p1", "p2", "p1"],
            "assertion.EqualsExpected": [True, False, True, False],
        }
    )
    result = calculate_aggregates(df).reset_index()
    # Check aggregation for m1, p1
    r1 = result[
        (result["attributes.model"] == "m1") & (result["attributes.prompt"] == "p1")
    ]
    count1 = r1["count"].iloc[0]
    correct1 = r1["is_correct"].iloc[0]
    share1 = r1["share_correct"].iloc[0]
    assert count1 == 2
    assert correct1 == 1
    assert pytest.approx(share1) == 0.5
    # Check aggregation for m1, p2
    r2 = result[
        (result["attributes.model"] == "m1") & (result["attributes.prompt"] == "p2")
    ]
    count2 = r2["count"].iloc[0]
    correct2 = r2["is_correct"].iloc[0]
    share2 = r2["share_correct"].iloc[0]
    assert count2 == 1
    assert correct2 == 1
    assert pytest.approx(share2) == 1.0
    # Check aggregation for m2, p1
    r3 = result[
        (result["attributes.model"] == "m2") & (result["attributes.prompt"] == "p1")
    ]
    count3 = r3["count"].iloc[0]
    correct3 = r3["is_correct"].iloc[0]
    share3 = r3["share_correct"].iloc[0]
    assert count3 == 1
    assert correct3 == 0
    assert pytest.approx(share3) == 0.0
