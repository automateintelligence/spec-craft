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


def _claude_manifest():
    return json.load(open(os.path.join(ROOT, ".claude-plugin", "plugin.json")))


def _codex_manifest():
    return json.load(open(os.path.join(ROOT, ".codex-plugin", "plugin.json")))


# Fields codex-cli 0.155.0 actually READS from a plugin manifest, taken from
# codex-rs/core-plugins/src/manifest.rs at tag rust-v0.155.0
# (commit f0a1b8f0849d90960bc406b848f32e5a129b0457):
# - `RawPluginManifest` (lines 45-68), destructured exhaustively in
#   `resolve_raw_plugin_manifest` (lines 295-305). `rename_all = "camelCase"`
#   makes its `mcp_servers` field `mcpServers` in JSON.
# - `RawPluginCommandManifest` (lines 70-74), read by
#   `load_plugin_command_paths` (lines 202-219) for `commands`.
# Neither struct has `deny_unknown_fields`, so codex silently discards any
# other key.
CODEX_MANIFEST_FIELDS = {
    "name",
    "version",
    "description",
    "keywords",
    "skills",
    "mcpServers",
    "apps",
    "hooks",
    "interface",
    "commands",
}

# Kept in .codex-plugin/plugin.json only to mirror .claude-plugin/plugin.json.
# Codex discards it; listed separately so this suite never claims the host
# honours it.
CODEX_INERT_MIRROR_FIELDS = {"author"}


def test_codex_plugin_manifest_schema():
    data = _codex_manifest()
    assert data.get("name") == "spec-craft"
    assert re.match(r"^\d+\.\d+\.\d+$", data.get("version", "")), (
        "semver version required"
    )
    assert isinstance(data.get("author"), dict), "author must be an object"
    unknown = set(data) - CODEX_MANIFEST_FIELDS - CODEX_INERT_MIRROR_FIELDS
    assert not unknown, f"codex ignores unknown manifest fields; drop {sorted(unknown)}"


def test_codex_schema_does_not_claim_codex_reads_claude_only_fields():
    for field in ("author", "repository", "license", "homepage", "dependencies"):
        assert field not in CODEX_MANIFEST_FIELDS, (
            f"codex-cli 0.155.0 does not read {field!r}"
        )


def test_codex_manifest_does_not_claim_dependencies():
    # spec-craft is standalone on both hosts, and codex has no `dependencies`
    # counterpart: declaring one would assert something no install enforces.
    assert "dependencies" not in _codex_manifest()


def test_codex_and_claude_manifests_do_not_drift():
    claude = _claude_manifest()
    codex = _codex_manifest()
    for field in ("name", "version", "description"):
        assert codex.get(field) == claude.get(field), (
            f"{field} differs between .claude-plugin and .codex-plugin manifests; "
            "a version split ships a plugin one host cannot update"
        )


def test_codex_manifest_skills_pointer_resolves():
    skills = _codex_manifest().get("skills")
    # codex accepts a string or an array of strings (RawPluginManifestPaths,
    # manifest.rs lines 129-135) and requires the `./` prefix.
    pointers = [skills] if isinstance(skills, str) else skills
    assert isinstance(pointers, list) and pointers, "skills pointer required"
    expected = {"expectations", "executable-assertions"}
    for pointer in pointers:
        assert isinstance(pointer, str) and pointer.startswith("./"), pointer
        skills_dir = os.path.normpath(os.path.join(ROOT, pointer))
        assert os.path.isdir(skills_dir), f"{pointer} is not a directory"
        found = {
            name
            for name in os.listdir(skills_dir)
            if os.path.isfile(os.path.join(skills_dir, name, "SKILL.md"))
        }
        assert expected <= found, f"{pointer} is missing {sorted(expected - found)}"
