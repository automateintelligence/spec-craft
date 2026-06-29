import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_plugin_manifest_schema():
    data = json.load(open(os.path.join(ROOT, ".claude-plugin", "plugin.json")))
    assert data.get("name") == "spec-craft"
    assert re.match(r"^\d+\.\d+\.\d+$", data.get("version", "")), (
        "semver version required"
    )
    assert "dependencies" not in data, "spec-craft must be conductor-agnostic (no deps)"
    assert set(data) <= {
        "name",
        "version",
        "description",
        "author",
        "displayName",
        "homepage",
        "repository",
        "license",
    }
