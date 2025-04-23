import os
from click.testing import CliRunner
from ai_yardstick.cli import cli


def test_version():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert result.output.startswith("cli, version ")

def test_cli_create():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["create", "myeval"])
        assert result.exit_code == 0
        # Check directories and files
        base = "myeval"
        assert os.path.isdir(base)
        assert os.path.isdir(os.path.join(base, ".ai-yardstick-cache"))
        assert os.path.isdir(os.path.join(base, "results"))
        # Config file
        cfg = os.path.join(base, "ai-yardstick-config.yaml")
        assert os.path.isfile(cfg)
        content = open(cfg, 'r').read()
        assert "name: myeval" in content
        assert "models: models.csv" in content
        # Template files
        assert os.path.isfile(os.path.join(base, "models.csv"))
        assert os.path.isfile(os.path.join(base, "prompts.csv"))
        assert os.path.isfile(os.path.join(base, "tests.csv"))
        assert os.path.isfile(os.path.join(base, "index.md"))
