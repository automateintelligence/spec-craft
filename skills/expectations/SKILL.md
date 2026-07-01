---
name: expectations
description: Use when a spec's definition of done is implicit, or to refine a spec that already has an Expectations section. Adds or updates an Expectations section (success scenarios, failure scenarios, must-nots) in domain language, owned by whoever wanted the outcome. Reads a spec path and writes the section — creating it on a first run, or on a re-run diffing against the existing set to add only the genuinely missing gaps without duplicating what's already there. Pairs with /spec-craft:executable-assertions.
---

# /spec-craft:expectations

Read the spec at `$ARGUMENTS`. Add an **Expectations** section to it.

Background (so you make judgment calls, not template-fills): a spec blurs three things —
what the user wants, how it is built, and what counts as done. When "what counts as done"
is implicit, a coding agent fills the gap with its own interpretation. The Expectations
section closes that gap. It is the boundary of the work, owned by the person who wanted the
outcome, written in terms a user or domain expert would recognize — not implementation
language.

An Expectations section has three parts:

1. **Success scenarios.** The concrete conditions under which the result counts as done.
   Not "it works" but specific observable outcomes, stated so that whether each is met is a
   matter of fact, not opinion.
2. **Failure scenarios.** The specific ways this can produce a wrong result that looks
   right — where an agent would generate plausible code that violates intent. Think about
   what "confidently wrong" looks like for this feature.
3. **Must-nots.** Hard constraints the result must never violate, regardless of how done is
   otherwise defined — the load-bearing invariants. Across products these commonly concern
   access control, data exposure, money, data integrity, irreversible actions, and safety:
   anywhere a wrong result that looks right does real or unrecoverable damage.

Method:

- First read the spec and identify every place the definition of done is implicit, assumed,
  or left to interpretation. **List those gaps before writing anything** — they are the raw
  material for the section.
- Apply the **outsider test** to each candidate: would someone not in your head, reading
  only the spec, know whether this condition was met? If not, it is too vague — sharpen it
  until the answer is yes.
- Write in domain/user language, not implementation language. "Restricted results show the
  owner and access path, never the content" is an expectation; "the query returns a non-null
  permission label" is an implementation detail and does not belong here.
- **Surface ambiguities rather than resolving them silently.** Where the spec genuinely does
  not determine what done means, flag it as an open question — do not invent a boundary the
  author did not specify.

**Scope boundary (important):** produce the Expectations section only. **Do not write tests,
executable assertions, or any code**, and do not propose how to verify the expectations.
Encoding expectations as tests is a separate step (`/spec-craft:executable-assertions` → TDD).
If you reach for verification mechanics, stop and note it for the next step.

**Re-running on a spec that already has an `## Expectations` section.** When the spec already
carries an Expectations section (a prior run, or one the owner authored), the job changes from
*generating* a set to *diffing* against the one that exists — otherwise you re-derive a pile of
near-duplicates that bury the few real gaps. In that case:

- **Treat the existing set as input.** Read it first. Tag every gap you identify **`[COVERED]`**
  (already addressed by the existing set — cite which success/failure/must-not) or **`[NEW]`** (a
  genuine gap the existing set misses). The tagging forces a diff instead of regeneration.
- **Add only the `[NEW]` items.** Leave `[COVERED]` ones alone — do not reword or "improve" the
  owner's existing entries.
- **Preserve existing numbering.** If items are numbered, **append** new items with the next free
  number — never renumber, reorder, or insert into the existing sequence. Numbered items may be
  referenced by number (elsewhere in the spec, in existing assertion specs, or in code) and you
  usually can't see every reference, so treat any numbering as load-bearing: a rewrite that shifts
  the numbers silently breaks those cross-references.
- **Watch for over-generation.** If the `[NEW]` list is large relative to how much the existing set
  already covers, you are probably padding — re-check and cut to the ones that close a real gap.
  This is a nudge, not a quota; a genuinely under-specified spec can legitimately need many.
- **Show the restraint.** Output a short **"deliberately did not add"** list — candidates you
  considered and dropped, one line each (e.g. "covered by failure-3," "edges into verification
  mechanics," "would duplicate an existing entry — one home per decision"). Restraint shown beats
  padding to look thorough.

A first run (no existing section) is unchanged: everything is new, so skip the tagging and just
write the section.

**Output / action:**
1. Print the list of definition-of-done gaps you found — on a re-run, tagged `[COVERED]`/`[NEW]`
   plus the "deliberately did not add" list.
2. Write an `## Expectations` section (the three parts) into the spec file at `$ARGUMENTS`
   (append if absent; on a re-run, add only the `[NEW]` items in place — never regenerate or reword
   the existing set). Keep it surgical — expectations that restate the obvious add noise; keep the
   ones that close a real gap.
