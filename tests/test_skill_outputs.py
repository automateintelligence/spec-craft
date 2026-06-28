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
    ]:
        assert needle in body, needle
    assert "knowledge" not in body and "tier" not in body  # generalized
    assert "conductor" not in body  # conductor-agnostic
