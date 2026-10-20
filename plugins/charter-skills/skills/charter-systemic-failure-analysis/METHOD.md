# Charter · Systemic Failure Analysis

Repeated failures often persist because each repair removes an instance while
leaving the mechanism that recreates it. Duplicate effects, stale decisions,
oscillation, backlog and false completion are particularly revealing: locally
reasonable components can produce a globally wrong result.

The explanatory target is a contrast, not a label. "Race condition" names a
family of failures; "a worker used lease version 4 after version 5 had become
authoritative, and the effect receiver accepted both" explains how this
failure occurred rather than the expected single write.

A failure already reproduced and localized to one component needs ordinary
debugging, and the answer is the fix with its one-line cause. This analysis
earns its place when the failure returns after instance repairs, appears only
when components interact, or nobody can yet say which part produces it.

## Start from the first divergence

Follow one representative failing occurrence before aggregating symptoms, and
compare it with one that succeeded. The first transition where they diverge
locates the mechanism better than frequency does. When the two runs differ in
version, configuration or input, bisection can isolate a cause if the contrast
is reproducible and the changed factors can be separated. Interacting factors
may require a combination to reproduce the failure; stochastic failures may
require comparing outcome distributions rather than seeking one deterministic
toggle. Correlate events by operation identity and causal milestones, not by
coincidence in wall-clock time.

Then choose the observation whose result would change the repair: the effect
persisted before or after its acknowledgement; the same logical operation
retried or a new one requested; fresh or stale state at the decision point;
one controller or two competing; the writer's ownership version current or
already superseded at the effect; arrival rate above or below the sustainable
service rate. [Occurrence investigation](references/investigation-workflow.md)
helps when the evidence is partial logs spread across processes, inspection may
be failing independently of its target, or an experiment must preserve the
condition it tests.

## The effective owner has information and control

An invariant can be enforced only where the required distinction is knowable
and the consequential action is controllable. A process-local lock cannot
protect an effect performed by another process. A dashboard can display
uncertainty, but cannot make an ambiguous provider operation complete. A review
step cannot catch a requirement its reviewer never sees.

This is why adding a lock, checking a lease earlier or deleting the extra
record can appear successful while leaving the failure possible. When the
recurrence is a duplicated or lost effect, enforcement belongs at the effect
boundary, keyed by the identity that separates a retry from a legitimate new
request: deduplicating payments by customer instead of by logical operation
would suppress real new payments. `charter-workflow-recovery` holds the
effect-identity, idempotency and fencing model in depth.

## Recurrence can come from structure, not a bad component

Retries increase arrival rate. If overload causes timeouts, and timeouts cause
retries, the loop amplifies its own trigger. Longer timeouts may reduce some
retries, but do not restore a sustainable arrival/service balance. Backpressure,
bounded retry budgets or capacity changes act on different edges of that loop.
Removing backlog is containment until the balance changes.

Delayed feedback can cause overshoot; two controllers can fight over the same
resource; a completion metric can reward a team for shifting unfinished work
downstream. The causal model should capture the relevant relationship, not
attribute these patterns to generic carelessness.

A happens-before graph reveals ordering, a state machine reveals stale
transition authority, a fault tree reveals alternative paths to a failure,
and a feedback model reveals amplification. Wall-clock proximity alone cannot
supply any of those relationships. [Causal modeling](references/causal-modeling.md)
develops each representation when the mechanism needs one written down.

## Latency has a critical path

When the failure is slowness, find where the time goes before changing
anything. End-to-end time accumulates along the critical path, the chain of
steps that each wait for the previous one; work on a parallel branch that
finishes early, or in the background, cannot shorten it however much it
improves. At each step on that path, separate time spent waiting in a queue,
pool or lock from service time spent doing the work. Queueing delay rises
steeply as utilization approaches capacity, so a saturated stage can dominate
response time while its service time is unchanged; there, added capacity,
admission limits, less arriving work or shorter service at the saturated stage
can help, whereas speeding an unrelated stage cannot remove that queue. Read
the distribution rather than the mean: the slow tail is often a different
population, such as a cold cache, a garbage-collection pause, a retry or one
slow shard, that an average hides. A request that waits for every parallel call
is held by the slowest: with 100 calls whose slow events are independent and
each have a 1% probability, about 63% of requests meet at least one slow call
(`1 - 0.99^100`). Shared queues, hosts or outages can correlate those events;
check for shared causes before applying the independence assumption. Measure
a slow occurrence with a trace or per-stage timestamps, and many occurrences
as percentiles at the same load, before choosing which stage to optimize.

## Repair depth follows the mechanism

Containment, such as draining a queue, disabling a path or isolating a corrupt
record, limits current harm; recurrence returns while the generating
conditions remain. A local repair changes the defective component. A boundary
repair changes the shared contract, such as acknowledgement semantics,
ordering or ownership transfer, because local correctness cannot enforce a
relationship another participant is free to violate. A feedback repair changes
delay, gain, thresholds or controller ownership. Redesign becomes appropriate
when the abstraction needs two authorities for one invariant. Higher-level is
not inherently more complete: the sufficient owner is the one that removes the
modeled route to recurrence without moving the defect elsewhere.

Familiar remedies often act on the wrong edge. Clearing a cache repairs one
stale view; changing invalidation or authority changes why stale views recur.
A longer timeout changes how long a client waits, not whether it can tell a
completed effect from a lost request. More retries help only when repetition is
safe and spare capacity exists. A new status label makes uncertainty visible
without resolving it. A regression check for one ordering shows that schedule
repaired while another legal schedule may still violate the invariant; the
question is which transitions are now impossible.

A repair keyed at the effect boundary can cover a lost acknowledgement and a
duplicated delivery without deciding which occurred; its success then does not
say which one did.

Every repair has costs at the boundary it changes. Deduplication with too
coarse an identity drops legitimate work, stricter ownership reduces
availability during partitions, and backpressure moves waiting toward
producers without removing service time. A repair can be correct and still
unacceptable for its use. The useful account connects the old mechanism, the
changed owner or contract, why the recurrence condition can no longer produce
the failure, and which of these costs appeared on the path that failed.
