---
name: executable-assertions
description: Use after /spec-craft:expectations, when a spec's load-bearing expectations need to become machine-checkable. Selects the load-bearing ones, produces 4-part assertion specs (claim, setup, observation, kind), and persists them to <spec>.assertions.md for review. Specs only, no test code — feeds any downstream test runner.
---

# /spec-craft:executable-assertions

Read the spec at `$ARGUMENTS`, including its Expectations section. Turn the **load-bearing**
expectations into **executable assertions**. Read this whole framing first — the selection
judgment matters more than the mechanics.

An expectation is prose; prose is re-interpreted slightly differently each run, so the same
expectation can produce different code under different models. An executable assertion
removes the interpretation: a machine check that passes or fails on an exit code, never "it
depends." The expectation says what must be true; the assertion is the runtime proof that it
is true in this build.

**Not every expectation becomes an assertion. Select first:**

- An expectation is **load-bearing** if it would be expensive, dangerous, or silent to get
  wrong. The clearest cases across products are security/access, data exposure, money, data
  integrity, and irreversible actions: anything where a wrong result looks correct but
  leaks data, corrupts state, charges wrongly, or can't be undone. Encode those first.
- A **must-not** is almost always load-bearing. A **failure scenario** usually is. A
  **success scenario** sometimes is — only when "done" is objectively checkable rather than
  a matter of judgment or feel.
- **Skip** expectations whose truth needs a human eye (visual polish, tone, subjective
  quality). Note them out of scope rather than forcing a brittle check.
- When in doubt, prefer **fewer, sharper** assertions over broad coverage.

For each selected expectation, define the assertion in plain terms (the 4-part spec):

- **Claim.** The single Boolean fact this proves, as one true/false sentence — nothing
  softer. If you can't reduce it to one Boolean, it's two assertions or not assertable yet;
  say which.
- **Setup.** What state must exist for the check to be meaningful: inputs, fixtures,
  preconditions. Concrete about conditions, not code.
- **Observation.** What the assertion inspects to decide pass/fail, and what specifically
  counts as fail. For exposure/security rules name what the result **must contain** and,
  just as explicitly, what it **must not contain** — the dangerous failure is usually the
  presence of something that should be absent.
- **Kind.** The logical form: `example` (one concrete input/output case), `property` (must
  hold across all inputs of a kind), or `contract` (a function's pre/postconditions). Prefer
  `property` when the invariant is meant to hold universally — a single case can pass while
  the invariant is broken.

Method/scope:

- Work only from expectations in the spec. Do not invent new ones; if writing an assertion
  exposes a missing expectation, **flag it** rather than quietly adding it.
- Call out expectations that look checkable but aren't, and vague prose that actually
  reduces to a hard Boolean.
- **Do not write the test code** — produce the assertion specs first, so the claims and
  kinds can be confirmed before implementation.

**Output, in order:** (1) expectations judged load-bearing enough to encode, each with a
one-line reason; (2) expectations deliberately not encoded, each with a one-line reason
(unprovable by machine / not load-bearing / subjective); (3) for each encoded one, the 4-part
spec (claim; setup; observation with explicit must-contain and must-not-contain where
exposure is involved; kind). Keep it surgical — specs only.

**Persist the output — do not just print it.** The 4-part specs are a review-before-implementation
artifact; they must survive the session, not evaporate when it ends. Write the full output (the two
selection lists as a header, then the specs) to **`<spec>.assertions.md`** — a *sibling* of the
spec, **not** inside `spec.md` (assertions are pre-test artifacts, not spec prose). Report the path
you wrote. Always write the file — it is the durable artifact a downstream test-writing / TDD step
reads to implement the tests; do not skip it.
