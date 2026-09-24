import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_expectations_skill_contract_present():
    body = open(os.path.join(ROOT, "skills/expectations/SKILL.md")).read().lower()
    for needle in [
        "success scenarios",
        "failure scenarios",
        "must-nots",
        "definition-of-done gap",
        "do not write",
        "expectations section",
    ]:
        assert needle in body, needle
    assert "knowledge" not in body, "must be generalized (no product-specific coupling)"
    assert "conductor" not in body, "spec-craft must be conductor-agnostic"
    assert "level" not in body, "use 'kind', not conductor's 'level'"


def test_executable_assertions_skill_contract_present():
    body = (
        open(os.path.join(ROOT, "skills/executable-assertions/SKILL.md")).read().lower()
    )
    for needle in [
        "claim",
        "setup",
        "observation",
        "kind",
        "load-bearing",
        "do not write the test code",
        "must not contain",
        "example",
        "property",
        "contract",
        "red-team",
        "against a stub",
        "adapter",
    ]:
        assert needle in body, needle
    assert "knowledge" not in body and "tier" not in body  # generalized
    assert "conductor" not in body  # conductor-agnostic
    assert "level" not in body  # 4th part is 'kind', never 'level'


def test_skill_cross_references_are_host_neutral():
    # Claude Code invokes plugin skills as /plugin:skill, Codex as $plugin:skill.
    # Wherever one skill points the reader at the other, both forms must appear,
    # and the frontmatter `name:` both hosts key on must stay unqualified.
    pairs = {
        "expectations": "executable-assertions",
        "executable-assertions": "expectations",
    }
    for skill, other in pairs.items():
        body = open(os.path.join(ROOT, f"skills/{skill}/SKILL.md")).read()
        frontmatter = body.split("---")[1]
        assert f"\nname: {skill}\n" in frontmatter, skill
        for sigil in ("/", "$"):
            assert f"{sigil}spec-craft:{other}" in body, f"{skill}: {sigil}{other}"
        slash_refs = body.count("/spec-craft:")
        dollar_refs = body.count("$spec-craft:")
        assert slash_refs == dollar_refs, (
            f"{skill}: {slash_refs} Claude-form vs {dollar_refs} Codex-form references"
        )
