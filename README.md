# spec-craft

**Make a spec's definition of done explicit and machine-checkable.** Two Claude Code
skills that turn a vague spec into a checkable one: first a definition of done in plain
language, then precise assertion specs a test runner can grade.

spec-craft is standalone. It writes specs and assertion specs, never test code, and it
knows nothing about any particular test runner or orchestrator. (Conductor consumes it;
spec-craft never depends on conductor.)

---

## Why

A spec blurs three different things: what the user wants, how it gets built, and what
counts as done. When "what counts as done" is left implicit, a coding agent fills the gap
with its own interpretation, and you find out at the worst possible time that its idea of
done was not yours.

spec-craft fixes the "done" part.

- **Stop "confidently wrong" output.** Prose gets re-interpreted a little differently every
  run. An executable assertion removes the interpretation: a check that passes or fails on
  an exit code, never "it depends." The expectation says what must be true; the assertion is
  the runtime proof that it is true in this build.
- **A definition of done a machine can grade.** Expectations become 4-part assertion specs
  any test runner can implement. That gate is what lets an autonomous agent know it is
  actually finished, instead of guessing.
- **Owned by the person who wanted the outcome.** Expectations are written in domain
  language (what a user or domain expert would recognize), not implementation language, so
  the boundary of the work belongs to the human, not the agent.
- **It surfaces ambiguity instead of papering over it.** Where the spec genuinely does not
  determine what done means, the skill flags it as an open question rather than inventing a
  boundary you never specified.
- **Standalone and portable.** The output is plain prose and 4-part specs that feed any
  downstream test runner. Nothing about it is tied to a specific tool.

---

## Install

spec-craft is a Claude Code plugin. The runtime artifact is just two `SKILL.md` files plus
a manifest — there is no service to run. (Python 3.12 in this repo is only for the
plugin's own structural tests, not a dependency for using it.)

### As a plugin (shared)

Once published to a marketplace (a `.claude-plugin/marketplace.json` that lists
`spec-craft`):

```
/plugin marketplace add automateintelligence/spec-craft
/plugin install spec-craft@<marketplace-name>
```

> **Note:** this repo does not ship a `marketplace.json` yet, so the one-command install
> above is not wired up today. Use the local method below until it is.

### Locally (works today)

```bash
git clone https://github.com/automateintelligence/spec-craft
claude --plugin-dir ./spec-craft
```

Verify with `claude plugin list` (look for `spec-craft`). The skills are then available as
`/spec-craft:expectations` and `/spec-craft:executable-assertions`.

If you use [conductor](https://github.com/automateintelligence/conductor), installing it
pulls in spec-craft automatically — conductor declares it as a dependency.

---

## Use

Two skills, run in sequence on the same spec file. The first writes a definition of done
into the spec; the second derives machine-checkable assertions from it.

### 1. Add expectations

```
/spec-craft:expectations path/to/spec.md
```

Reads the spec, lists every place the definition of done is implicit, then writes an
`## Expectations` section back into the file. The section has three parts:

- **Success scenarios** — the concrete, observable conditions under which the result counts
  as done. Stated so that whether each is met is a matter of fact, not opinion.
- **Failure scenarios** — the specific ways this can produce a wrong result that looks
  right. What "confidently wrong" looks like for this feature.
- **Must-nots** — hard constraints the result must never violate. The load-bearing
  invariants: access control, data exposure, money, data integrity, irreversible actions,
  safety.

It applies the **outsider test** to every condition: would someone not in your head,
reading only the spec, know whether this was met? If not, it sharpens the wording until the
answer is yes. It writes expectations only — no tests, no code.

### 2. Derive executable assertions

```
/spec-craft:executable-assertions path/to/spec.md
```

Reads the spec including its Expectations, selects the **load-bearing** ones (an expectation
is load-bearing if it would be expensive, dangerous, or silent to get wrong), and produces a
4-part spec for each. It deliberately skips expectations whose truth needs a human eye
(visual polish, tone, subjective quality) and prefers fewer, sharper assertions over broad
coverage. Output, in order: what it chose to encode and why, what it skipped and why, then
the specs.

Each assertion spec has four parts:

- **Claim** — the single Boolean fact this proves, as one true/false sentence.
- **Setup** — the state that must exist for the check to be meaningful: inputs, fixtures,
  preconditions.
- **Observation** — what the check inspects to decide pass/fail. For exposure/security rules,
  what the result **must contain** and, just as explicitly, what it **must not contain** (the
  dangerous failure is usually the presence of something that should be absent).
- **Kind** — the logical form: `example` (one concrete case), `property` (holds across all
  inputs of a kind), or `contract` (a function's pre/postconditions).

It produces specs only, never the test code, so the claims and kinds can be confirmed before
anyone implements them.

---

## The model: expectation vs assertion

An **expectation** is prose a human owns. An **executable assertion** is the runtime proof
of that expectation, reducible to an exit code. spec-craft is the bridge between them, and
it stops at the spec: it hands off 4-part specs for a downstream test runner to implement.

One naming rule matters. The fourth part of an assertion is its **`kind`**
(`example` / `property` / `contract`) — the logical form of the check. It is deliberately
**not** called `level`. `level` is a downstream gate-tier concept (conductor's), and the two
must not collide. spec-craft stays a neutral producer of assertion specs; how a runner maps
`kind` onto its own tiers is entirely the runner's business.

---

## What it does not do

- It does not write test code. Encoding assertions as runnable tests is a separate,
  downstream step.
- It does not resolve ambiguity silently. Genuine gaps in the spec are flagged as open
  questions, not invented.
- It does not depend on conductor or any other tool. The output feeds any test runner.
