# Worked Replacement: Accepted Is Not Completed

This illustrative asynchronous publishing service has released v1 clients and
queued v1 work that cannot all change at once. Its request handler returns
`success: true` when a job is durably queued. A dashboard interprets that as
"published" and unlocks a dependent action before the worker has published
anything. Renaming the response field cannot supply the missing fact.

The replacement invariant is precise: `completed` means the intended result
has been established at the publication target and its identifying receipt is
durably recorded. Queue acceptance means only `accepted`. The worker and
target readback can establish completion; the request handler cannot.

## Carry the fact through the whole path

| Carrier | Meaning after the change |
| --- | --- |
| Request producer | Persist the operation identity and enqueue obligation before acknowledging acceptance; a recoverable dispatch mechanism handles a crash between persistence and queue delivery. Return the operation ID, not a completion claim. |
| Worker | Publish under that operation identity and record the target receipt before exposing completion. Duplicate queue delivery resolves the same operation rather than creating a second publication. |
| Persistence | Retain acceptance, execution state and terminal receipt separately. Order transitions so a delayed acceptance write cannot regress a completed operation. A publication attempt with an unresolved target outcome remains distinguishable from a definite failure. |
| Mapper | Derive the public lifecycle from those records. A legacy acknowledgement is evidence of acceptance, never a substitute completion receipt. Preserve operation identity and result reference through serialization. |
| Consumer | Show accepted work as pending; unlock the dependent action only on `completed` with the required result. Use a read or completion event for the same operation, not another submission, to await it. |
| Recovery | Resolve a lost acknowledgement or interrupted worker against that operation's persisted and target state. An unresolved possible publication does not become a safe new attempt merely because no local receipt exists. |

The receipt here identifies the target result; a local log saying "worker
started" would not meet the invariant. If publication is a remote effect,
atomic local storage cannot close the remote-effect/local-receipt gap by itself.
Target-supported deduplication or authoritative lookup can resolve that gap;
without either, the unresolved outcome must remain visible rather than being
converted into completed or automatically retried.

## Coexistence exposes asymmetric compatibility

In this example the v1 wire contract promises acknowledgement, despite the
dashboard's incorrect interpretation. Keep the v1 serializer at the boundary
for released acknowledgement-only clients; new internal callers use the
explicit lifecycle. Its owner is the API boundary, its direction is new
operation state to the old acknowledgement response, and its removal condition
is retirement of those clients and any persisted inputs that still require it.

| Pair | What is actually possible |
| --- | --- |
| New reader, old record | `success: true` can establish accepted work if that old record denotes durable queue acceptance. Completion is unknown unless a separately attributable target receipt can establish it. |
| New reader, new record | It can distinguish accepted, running, completed, definite failure and unresolved outcome, retaining the receipt and operation identity. |
| Old acknowledgement-only client, new producer | A v1 response can still acknowledge acceptance. It cannot expose all lifecycle distinctions. |
| Old completion-dependent client, either producer | The existing interpretation is unsafe. A serializer cannot repair it while still returning at acceptance; upgrade or contain that workflow rather than call it compatible. |

Map historical rows from what they prove, not what their labels imply. Do not
backfill `completed` from `success: true`, nor resubmit every historical row
without a receipt. A target lookup joined to the exact operation may recover
completion evidence; otherwise preserve the limitation.

Translation can be lossy but parseable. Collapsing running, completed and
unresolved-outcome operations into the same v1 `success: true` response is valid
only as acknowledgement of their earlier acceptance. Mapping that value back
cannot recover their lifecycle. It may serve an old acknowledgement display,
but it cannot drive completion-dependent actions or retry decisions. Both
parsers accepting the payload does not make the translation bidirectional.

## Sequence the transition around actual writers

First add storage and readers that preserve these distinctions without
reinterpreting old rows. Then deploy the lifecycle-producing worker and mapper.
During the overlap, legacy workers may finish their already-owned jobs, but
their `success` writes do not populate the new completion receipt. New workers
must not steal possibly active legacy attempts merely to obtain the new shape.
Drain or fence those owners before handing over execution; reconcile uncertain
attempts at the target instead of replaying them.

Move the dashboard and dependent action to the explicit lifecycle when the
producing path supports it. Completion events must follow durable terminal
state, and a delayed accepted event must not regress the consumer view. Carry
the contract through the schema, client generator, fixtures and public example:
an example that submits twice to "check completion" teaches a duplicate-effect
path even if the new API is correct.

Retire the internal boolean mapper once no internal consumer needs it. Keep
only the externally required v1 boundary until its stated removal condition is
met, including delayed messages and recovery readers. An old binary that
cannot preserve the new lifecycle is not a safe rollback writer just because
it can parse the expanded table. Constrain it to a compatible role or repair
forward. If every consumer and all state instead move atomically, this overlap
machinery has no purpose: make the coherent source replacement directly.

## Let failures locate the missing change

A public-path example can submit once, observe pending, finish the worker, and
then observe completed with its result. Interrupted-worker and delayed-event
cases exercise the distinct recovery and ordering obligations; they do not
establish a real provider's deduplication behavior without provider evidence.

Each failure points at the carrier that has not moved:
- a dashboard becoming complete at enqueue reveals an unmoved consumer or mapper;
- a schema rejecting the completion receipt means the schema and the worker
  disagree about the contract;
- a regenerated client restoring the boolean reveals an unmoved generator input;
- a test requiring immediate publication may be stale, while a test preventing
  duplicate publication still protects an invariant.
