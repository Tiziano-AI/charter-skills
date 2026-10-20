---
name: charter-test-design
description: 'Software tests: adding tests, fixing a flaky one, or finding why a test
  passes or fails; choose expected values, boundaries and mocks that catch the real
  bug, and drop tests that protect nothing.'
metadata:
  content_version: charter-test-design@2026.10.08.0
---
# Charter · Test Design

A useful software test distinguishes a relevant wrong behavior from an
acceptable one. The measuring instrument has three connected parts: the
behavior it exercises, the observation it makes and the basis for deciding
whether that observation is correct. Weakness in any one can make a green
result uninformative.

An ordinary test for a clear behavior needs no elaborate analysis: take the
expected value from the requirement or a hand-worked example and exercise the
behavior at the boundary the test protects. The rest of this skill is for tests
whose protection is in doubt: a green suite that missed a bug, a flaky test, mocks
that may hide the failing seam, or a suite that needs pruning.

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
and mutation tools. Software tests do not settle whether a model, prompt or
agent produces good results (`charter-ai-evaluation`), whether a document
renders faithfully at its destination (`charter-document-fidelity`), or
perceptual quality; those jobs keep their own observation methods.
