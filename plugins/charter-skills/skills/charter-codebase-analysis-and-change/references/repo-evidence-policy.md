# Resolve the Intended Source Contract

Use this when implementation, documents, schemas or dependencies disagree
about the behavior that should remain.

## Distinguish intent, implementation and delivery

Repository conventions decide which documents govern product intent and
architecture. Public docs teach use; a plan proposes work; a historical record
explains what once happened. Do not give them equal current authority.

An executable schema defines accepted shape, but not necessarily intended
meaning. A test can preserve either a valuable invariant or a retired contract.
Generated output derives from its producer. Installed behavior is downstream
evidence at an exact version and location.

Classify the actual conflict:
- implementation does not yet satisfy current intent;
- documentation describes behavior the product no longer owns;
- two reachable sources define incompatible behavior;
- a derivative was not regenerated;
- an external contract constrains the proposed design;
- the product decision itself remains open.

Choose the owner from meaning and current constraints, not occurrence count or
a blanket preference for code over docs.

## Trace governing intent into the implementation

Extract the positive behavior, invariants and exclusions from the current
contract. Locate the entrypoint and decision owner, then the carriers required
to make that behavior real. If code is wrong, repair the implementation. If
the document is stale, correct its owner and the public copy that still teaches
the wrong path. If both are provisional, decide the product distinction first.

Do not turn a documentation alignment into a sweep of unrelated prose.
Update examples that users can still follow, and regenerate references from
their canonical producer where one exists.

## Respect the actual dependency contract

When SDK, API or host semantics constrain the change, use the exact adopted
version: installed source, lockfile-resolved package, headers or generated
client, then applicable official documentation/source. A newer vendor release
may be a migration option rather than the current runtime.

Read the relevant complete request, response, lifecycle or resolver owner.
Important differences include parameter presence versus defaulting, error and
retry semantics, cancellation, pagination, streaming terminality, hook timing
and configuration capture. Similar names do not prove interchangeable behavior.

Record the external fact and the source decision it forces. When the fact
cannot be established, leave that part of the design open and state what each
possible answer would change, rather than assuming compatibility.
