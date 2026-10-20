# Oracles, seams and failure cases

## Choose an oracle for the claim

| Oracle | Useful claim | Common blind spot |
| --- | --- | --- |
| Contract example or hand calculation | A controlled case has the required result | A mistaken or ambiguous contract, or unrepresentative input |
| Invariant | Every admitted execution preserves a necessary property | Many useless implementations can preserve that property |
| Metamorphic relation | A defined input transformation induces a defined output relationship | The transformation's preconditions may not hold |
| Differential implementation | Implementations disagree on an input | Both may share the same error; disagreement alone does not identify the correct answer |
| Golden output | A reviewed artifact retains meaningful behavior | The original may be wrong; bulk updates can erase the review |
| Model of state transitions | Sequences follow an independently specified lifecycle | A model copied from implementation shares its omissions |
| Implicit (crash, hang, sanitizer report, uncaught exception) | Any input, including generated ones, can be judged without an expected value | Silent wrong results pass |
| Current behavior (characterization) | Legacy output did not change | Existing bugs are pinned as expected |

For a money calculation, an explicit example using independently worked
arithmetic can protect rounding at the chosen precision. Calling the production
rounding helper to compute the expectation does not test that helper. The same
helper can legitimately prepare fixtures in a test concerned solely with access
control; independence is relative to the disputed behavior.

For serialization, `decode(encode(x)) == x` is valuable but insufficient to
establish compatibility with another implementation. A pair that consistently
uses the wrong field name passes. A known external-format example or a real
consumer catches a different defect. Keep both when both promises matter.

For sorting, permutation invariance and ordered output still allow an
implementation that drops values. Add conservation of the input multiset and
examples for any tie-breaking contract. For ranking, by contrast, reordering
input can legitimately change equal-score output when stable order is promised.
The property comes from the domain, not from a generic testing recipe.

## A double can preserve or remove the disputed seam

Suppose an application marks a message delivered when its provider adapter
returns `accepted`. A mock configured to return `delivered` lets the test pass
without exposing the semantic mismatch. A useful adapter test uses an observed
or documented provider response and checks the mapped state. A product-path
test then checks that the recipient-visible state distinguishes acceptance from
delivery. Neither test alone proves actual reception by a person.

A contract fixture needs a credible owner and version. Hand-authored fixtures
can exercise rare errors, but merely resembling a provider response does not
establish that the real provider produces it. When the live uncertainty is SDK
compatibility, use that SDK or a verified contract at the boundary; when it is
the application's response to a timeout, a fault-injecting double may give
better control than a live service.

A stub supplies selected outputs; a spy records interactions; a fake implements
a simplified dependency. Each can answer a useful question. Their names do not
grant fidelity. An interaction assertion such as "audit was called once" is
insufficient if the requirement is that a durable record survives a restart.
Conversely, asserting that a denied request never reaches the mutation boundary
can directly protect an authorization invariant.

## Make concurrency failures reachable

Consider a completion counter intended to acknowledge only durable writes.
Two writes begin, the first is held before persistence, and the second advances
the counter. A test that waits for both to finish misses whether the first was
acknowledged too early. A useful test controls the first persistence boundary,
allows the second to progress and observes whether acknowledgement is withheld
until the required write is durable.

Control the relevant ordering with explicit barriers, a deterministic scheduler
or fault injection available at that seam. A broad sleep guesses at scheduling
and often turns a race into a flaky test. A fake clock helps with deadline
logic but does not model disk durability or network ordering by itself.

Cancellation has similarly different contracts: asking to cancel, stopping
local callbacks and stopping the external operation. Exercise the state where
the defect can occur, such as a suspended operation rather than an already
completed one. Checking that a cancellation method was invoked is only enough
when invocation itself is the promised behavior.

## Flaky tests by cause

Reproduce before fixing. A test that fails only in the full suite, in parallel
or on CI is telling you which cause to look for.

| Cause | How to expose it | Fix at the cause |
| --- | --- | --- |
| Waiting on time instead of an event | Slow the dependency or run under load | Wait on the completion signal, or poll a condition with a deadline |
| Interleaving of concurrent work | Hold one side at a barrier | Control the order with barriers or a deterministic scheduler |
| State left by other tests | Run the test alone, then in reverse or random order | Give each test its own state, or reset shared state before each test |
| Real time, dates and time zones | Run in another time zone, or near midnight or a daylight-saving change | Inject the clock and pin the time zone |
| Unordered collections | Vary the hash seed or insertion order | Compare as a set or multiset, or sort, when order is not in the contract |
| Ports, files or services shared across parallel runs | Run the suite in parallel | Allocate unique resources per test and release them |
| Network and live services | Run offline | Fake at the boundary; keep a separate check against the real service |

If a test must leave the gate before its cause is fixed, quarantine it with
the cause recorded, so it is not mistaken for coverage.

## Test the requested product rather than a guessed evaluator

A test suite can reward shallow success: existence of a file rather than its
contents, a counter rather than completed work, or one supported input rather
than the required family. It can also create unnecessary behavior when code
adds speculative aliases and fallbacks for hypothetical assertions.

The remedy is to connect the disputed check to the actual product contract.
If its failure would matter only to an imagined evaluator, it is a poor reason
to expand the public API. If a required case is missing from the suite, that
absence does not remove the requirement. A targeted new check can protect the
missing behavior without inventing a broader validation program.

## Mutation tools

A mutation tool limited to the changed lines automates breaking the code by
hand to watch a new test fail. A campaign over the whole codebase rarely pays
for one change, and its score means something only for the kinds of fault its
mutants imitate. A surviving mutant is either a missing assertion or an
equivalent change that alters no observable behavior; only the first needs a
test.

## Determinism and claim limits

Fixing random seeds and controlling clocks can make a regression reproducible.
It does not show that the selected seed represents the input distribution.
Property-based generation can explore a larger domain, while shrinking helps
explain a failure; its generators and assumptions still define what it can see.

For a nondeterministic dependency, test deterministic surrounding contracts
directly: invalid outputs are rejected, required identities survive mapping,
and partial results do not become completed work. Statistical quality or agent
behavior needs a different observation design. A mock that always emits ideal
content cannot supply that evidence, and an exact snapshot of one model answer
can freeze wording while missing the relevant quality variation.

## Retiring a check

Suppose every internal refactor breaks a snapshot of an entire response, even
though consumers rely only on identifiers, ordering and a small set of values.
Replacing that snapshot with assertions on those semantics can preserve
protection and reduce irrelevant failures. If consumers actually require the
exact serialized bytes, the snapshot may be the appropriate contract check.

Similar-looking unit and integration tests deserve separate consideration. The
unit test can expose calculation edge cases; the integration test can expose
that the endpoint never uses the calculation. Remove either only when the
surviving checks cover its relevant failure or that behavior no longer belongs
to the product. Counts, layers and naming conventions do not settle redundancy.
