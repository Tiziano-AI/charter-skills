---
name: charter-test-design
description: 'Software tests: adding tests, fixing a flaky one, or finding why a test
  passes or fails; choose expected values, boundaries and mocks that catch the real
  bug, and drop tests that protect nothing.'
metadata:
  content_version: charter-test-design@2026.11.20.0
---
# Charter · Software Test Design

Name one relevant wrong behavior, one acceptable one and the observation
that distinguishes them. A green result can mean the test never exercised
the seam, observed the wrong thing, or accepted the same mistake. For a
clear rule, a hand-worked example at its public boundary can be enough.
Use the deeper methods for a missed bug, a flaky result, suspect mocks or a
suite whose protection is no longer clear.

## Ground the expected result outside the suspected mistake

The oracle is the basis for the expected result. It can come from a public
contract, a hand-checked example, an invariant, an independent implementation or
a valid relation between executions. Computing an expected answer with the
same faulty helper as the implementation confirms agreement, not correctness.
The same trap appears when a test is written by reading the code: copying what
the code does now into the assertion makes the test pass on the bug. When no
specification exists, as in legacy code, pinning current output is legitimate
if the test says so: a characterization test detects change, not correctness.

Independence is specific to the failure under examination. Sharing a parser
may be harmless in a test of scheduling and fatal in a test of parsing.
An independent implementation can share the same mistaken specification.
A round trip can prove mutual consistency while both directions violate the
external format. Choose the oracle for the claim, not for the label
"independent."

Exact expected values work well for controlled examples. Invariants and
metamorphic relations help when the full answer is expensive to specify, but
their preconditions matter. Reordering input should preserve a result only if
order is irrelevant to the contract. A property that every constant function
satisfies is usually too weak to protect the useful behavior by itself.

## Put the real failure inside the test boundary

The boundary determines which mistakes can be seen. A unit test can isolate a
decision rule. An integration test can expose serialization, identity,
transaction or lifecycle mismatches between components. A contract test can
check conformance to an external interface. A consumer-path test can reveal
that otherwise-correct parts are not connected. These are different claims,
not a ladder in which the broadest test makes the rest redundant.

A double is appropriate when it controls a dependency outside the behavior
being investigated. It is dangerous when it replaces the seam likely to fail.
Mocking a database commit makes it possible to test handling a commit error;
it cannot establish that the actual transaction is atomic. Returning a canned
SDK response can test product mapping but not prove that the adopted SDK emits
that shape.

A fake repository backed by a dictionary may omit uniqueness, isolation and
ordering semantics. Keep it honest by running one set of contract tests against
both the fake and the real implementation, so a divergence fails in one place.
More detail in the fake is useful only where it changes the test's validity; a
miniature database can become a second unreliable product. Use the real
component in an isolated environment when its own semantics are the live
question.

## Choose failures that discriminate

Design examples around distinctions a plausible implementation can get wrong:
absent versus empty, accepted versus durable, requested cancellation versus
stopped execution, same subject versus same display name. Boundary values,
interleavings and negative cases earn their place through these mechanisms:
put the tie, the limit or the concurrent writer exactly where the defect bites.

For asynchronous code, control the event or scheduling point that enables the
race instead of hoping repeated runs encounter it. For stateful code, a sequence
may reveal what a single call cannot: retry after a partial effect, reconnect
after terminal state, or two clients competing for one transition. Assertions
should observe the property the product needs, including relevant absence of
side effects, rather than only which internal helper was called. When a class
of defect passes silently, such as a template rendering a missing variable as
empty text, a strict mode that makes it fail protects every instance where a
test protects one.

A flaky test is one whose result changes without a code change. Find the
cause before touching it: run it alone and in a different order to expose
state shared with other tests, then look for a sleep standing in for an event,
real time or time zones, unordered collections, and ports, files or services
shared across parallel runs. Each cause has its own fix; a retry only hides
the cause and any real race behind it.

White-box observations can be right when internal order is the contract:
authorization must precede a protected mutation, and an acknowledgement may
have to follow durable persistence. The defect is freezing incidental structure,
not observing internals at all.

When sensitivity to the relevant defect is uncertain, observing failure can
settle it: run a regression test against the unfixed code, or break the
relevant lines by hand (flip a comparison, drop the tie-breaker, remove the
lock) and check that the assertion notices. A known failing occurrence is
particularly useful for showing that a regression check catches that bug.
Where several fields or clauses jointly determine one result, a failing old
implementation does not show every part is protected. Vary one at a time so
each independently meaningful distinction can change the outcome.
[Mutation examples](references/oracles-seams-and-failures.md#isolating-each-part) explain when a case isolates a part and when it cannot.

There is no need to manufacture another red result when existing evidence
already establishes the protection. Coverage alone shows which lines ran,
not whether any assertion would notice them being wrong.

## Remove redundancy by protection, not appearance

Two tests with similar assertions can protect different seams. A pure rule test
can cover many cases while one public-path test establishes that the rule is
actually used. Conversely, many tests can all compute their expectations with
the same helper and miss the same defect.

When deciding what to retain, ask which plausible regression becomes invisible
if the check disappears, considering the surviving checks. Keep distinct
protection. Replace assertions on incidental call sequences, giant unreviewed
snapshots or duplicated wiring where a smaller semantic observation carries the
same protection. A failing test may expose an obsolete expectation, a product
defect, a broken validator or a different environment; read its input,
assertion and fixture to tell which. Changing it to match current output
without resolving that destroys its value.

[Oracles, seams and failure cases](references/oracles-seams-and-failures.md)
develops these choices; open it for the kinds of oracle and their blind spots,
concurrency and cancellation tests, a flaky test whose cause is not obvious,
and mutation tools. When the question is quality across model outputs rather than a deterministic
invariant, take representative and hard cases to `charter-ai-evaluation-and-session-learning`.
For a failure only visible after import, use `charter-document-fidelity` to
observe it in the recipient's application and make that result the test's oracle.
Perceptual quality likewise needs its own observation; green tests cannot stand in.
