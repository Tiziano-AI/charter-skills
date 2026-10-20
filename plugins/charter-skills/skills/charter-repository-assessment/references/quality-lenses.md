# Reading a Repository as a Product

Use these lenses when the repository question depends on architecture,
information fidelity, readiness or intervention scale. They are alternate
ways to resolve a question, not report sections to fill.

## Trace a vertical slice

Start with an externally meaningful input and follow its result:
entrypoint, validation, decision, state transition, output and consumer.
At each seam ask what owns the meaning and what merely transports it.

A vertical slice is a sampling strategy. It reveals the joins required for one
product result, not the coverage of the entire product. A second slice earns
its reading cost when it crosses a different decision owner, persistence model
or consumer boundary. Reading five similar endpoints may teach less than
reading the one background job that completes all five.

Useful techniques include following a stable request or object ID, tracing
callers of the constructor rather than every mention of a type, reading both
sides of serialization, and locating the scheduler or worker behind an
asynchronous acknowledgement. Follow a generator back to its inputs before
judging its output as hand-maintained source.

A command that prints a receipt may own acceptance while a worker owns
completion. A UI can render cached state while a background process decides
actions. A public schema may accept a value that the effective resolver never
selects. These distinctions often explain documented-versus-real capability.

## Evaluate evidence by what it could falsify

Product contracts explain intent. Code explains reachable implementation.
Tests protect selected examples and invariants. Observed use establishes one
result at one destination. Ask what would contradict the current conclusion
and whether the available evidence reaches that layer.

Test and validation machinery becomes a problem when it stands in for a
missing product path or only restates its own declarations. This is not a
judgment against test quantity: a small parser may need extensive edge tests;
a large dashboard may still measure no useful outcome. Preserve checks that
protect real invariants.

When a failing check bears on the verdict, `charter-test-design` covers telling
a product defect from a stale expectation, a broken validator or a different
environment.

## Follow information across seams

For a product that records, summarizes, filters or transports information,
follow one real input through each transformation to the receiver that uses it.
At each seam, tell apart content the product must not pass to this receiver
(redaction, permissions), a deliberate narrowing that keeps the full record
reachable, meaning lost or changed before the receiver can use it, and
information the source never supplied. Losses concentrate in ordering,
identity, partial results, encoding, repeated records and concurrent updates,
so compare difficult examples of those at the seam. A sample can expose a loss;
it cannot prove there is none across all inputs.

## Choose intervention scale

Prefer local repair when one owner can restore the behavior. Harden a boundary
when failure detection or recovery is missing. Refactor when recurring coupling
makes local changes unstable. Replace a public contract when its shape itself
prevents the required behavior. Superficially similar workflows with different
authority or timing may deserve separate owners rather than one shared one.
