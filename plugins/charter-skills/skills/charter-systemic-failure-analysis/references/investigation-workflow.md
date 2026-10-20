# Investigate a Recurrent Occurrence

Leave source records where they are and build a synthesized timeline only as a
map for navigating them; the timeline is an interpretation, the records are the
evidence.

## Reconstruct the material edges

Identify the actor/resource and logical operation, then the deliveries,
attempts, versions and ownership changes that can explain it. Join durable
state and external effects to acknowledgements, retries, cancellation and
recovery. Logs may show an attempt without an effect, or disappear while the
effect remains.

Read only the relevant window, but do not omit inconvenient terminal or late
events: a late callback or a second terminal record is often the mechanism.

A comparison with another occurrence is worth its cost when it can reveal the
first divergent transition, a missing handoff, stale authority, an
invalidation gap or a feedback condition.

## Separate the target from its observer

When attribution is still open, distinguish the target's operation from the
observer's capture, parsing and reporting. An inspector, exporter or telemetry
collector can fail while its target continues; a surviving process alone does
not establish correct operation. Apparently different probes can share the
same parser or capture service, so agreement between them need not be
independent evidence about the target. Trace that shared path when it changes
which observation can distinguish the possible causes.

A reduced case that still fails identifies a triggering condition, not by
itself which participant violates its contract. Attributing the defect needs
evidence about the input at the failing boundary and the contract there.
A compatible workaround can restore useful operation without establishing a
target defect or repairing the observer.

## Experiments must preserve the tested condition

An observation may come from an existing record or from a bounded repair
itself. When an experiment is needed, it has to reproduce the condition under
test: dropping an acknowledgement while preserving the effect tests something
different from preventing the request entirely.

Inject ordering, delay, partition or stale reads in isolated fixtures or in an
environment whose effects are contained and recoverable. An injection against
live dependencies performs real effects, whatever the experiment is called, so
define those effects and their recovery before running it.
