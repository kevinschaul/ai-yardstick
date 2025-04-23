import json
from ai_yardstick.cli import cache


def test_cache_decorator(tmp_path):
    # Use a dedicated cache directory
    cache_dir = tmp_path / "cache"

    @cache(cache_dir=str(cache_dir))
    def inc(x, y=0):
        return x + y + 1

    # First call: should compute and cache
    result1 = inc(5, y=2)
    assert result1 == 8
    # Cache file created
    files = list(cache_dir.glob("inc-*.json"))
    assert len(files) == 1
    # Check cached content
    with open(files[0], "r") as f:
        data = json.load(f)
    assert data["result"] == 8

    # Modify underlying function to a different behavior
    inc.__wrapped__ = lambda x, y=0: 999
    # Second call with same args: should return cached result, not new
    result2 = inc(5, y=2)
    assert result2 == 8

    # Call with different args: new cache entry
    result3 = inc(3)
    assert result3 == 4
    files = list(cache_dir.glob("inc-*.json"))
    assert len(files) == 2
