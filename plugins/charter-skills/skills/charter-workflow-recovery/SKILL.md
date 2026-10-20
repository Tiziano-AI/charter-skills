---
name: charter-workflow-recovery
description: Recover interrupted workflows with uncertain surviving effects; reconcile
  operation state and durable output to find the first safe continuation without duplicating
  work. Healthy processes, ordinary waits and broken protocol design need different
  treatment.
metadata:
  content_version: charter-workflow-recovery@2026.10.16.0
---
# Charter · Workflow Recovery

## When a plain relaunch is enough

Relaunch directly when the interrupted step is known to be repeatable, no
effect it may have started is uncertain, and the prior writer cannot race the
relaunch. Idempotency means repeating the same intended operation adds no
consequence beyond its first successful application. A rebuild of disposable
output from fixed inputs can qualify; a keyed upsert that increments a value
or fires a notification on every update does not. Overwriting a download is
repeatable only when replacing that target is intended and the source
identity still fits the request. The command's name alone proves none of this.

No uncertain effect means nothing was sent, charged, published, deleted or
handed to a provider whose acceptance you cannot see. When these conditions
are already established, the relaunch is the recovery and its result is the
check; no additional state inventory or manual correction needs to come
first. A healthy process that only needs waiting, or a task whose resume
point is already known, needs no recovery work either.

Recovery work starts when one of these fails: rerunning could repeat an effect
that may already have happened, the relaunch would resume from a checkpoint
that may claim work that never committed, or the interrupted run may still be
writing.

## Recover the operation, not the last log line

Recovery reconstructs the legal next action from effects that already exist.
An interrupted job is not a blank slate: its local status, worker, checkpoint
and provider may disagree because they commit at different times. Restarting
from the last visible line can lose work or repeat effects that the line never
recorded. This applies to jobs, batches, migrations, exports and external
operations; a broken transport contract belongs to
`charter-stream-protocol-repair` instead.

Resolve the product's logical operation, attempt, worker or lease, natural
unit of progress and external-effect identity. Find the owner that can
transition that occurrence. Logs and files can establish effects missing from
a job row; a dashboard cannot authorize a new lifecycle state by itself.

Keep status and consequences distinct. A failed run may have committed useful
items. A successful run may have missing output. A vanished process may have
left a provider working.

The natural recovery unit is the smallest unit whose identity and effect can
be reconciled. That may be one message in a batch, one file in an export or an
entire indivisible provider operation. Finer-looking log offsets do not create
finer recovery. When ten batch items are known complete and one is unknown,
restarting all eleven discards the strongest evidence available.

## Establish the commit boundary

For the affected units, distinguish never started, committed, externally
accepted but not locally recorded, written but unregistered, and unknown.
Use the workflow's natural identity—item key, input digest, partition, file,
transaction or provider operation—rather than inventing a parallel ledger.

A checkpoint is meaningful only with its write ordering:
- checkpoint before effect can skip work after a crash;
- checkpoint after effect can repeat work after a crash;
- a transactional effect/checkpoint or effective deduplication can close the
  corresponding gap.

For example, a payment can be accepted remotely before the local row is marked
complete. Replaying from the local row can charge again; looking up the same
provider operation can reconcile the gap. If the provider cannot look up or
deduplicate that operation, a local retry wrapper cannot manufacture the missing
guarantee. The unknown unit remains a separate recovery decision.

Determine whether a cursor identifies the last completed or next unstarted
unit and whether the input ordering still matches it. Provider pagination,
source offset and output commit position are not interchangeable by
convention. Recompute a plan if its source or destination changed since the
plan was made.

## Choose the transition that preserves useful work

Resume the same occurrence when its owner provides a valid boundary. Adopt
already-produced output through the product's supported transition when its
identity and completeness match. Retry or restart only at a boundary where
completed effects are excluded, repeatable or deliberately compensated.
[Lifecycle recovery](references/lifecycle-recovery-workflow.md) lists the
state classes to tell apart and when each transition (wait, resume, retry,
restart, adopt, compensate, quarantine) applies; open it when the choice
between them is not obvious.

An idempotency key helps only within the provider's actual scope, retention
and payload contract. A new key does not deduplicate an earlier unknown
effect; an expired key may not either. Compensation is a new operation that
can itself fail, not erasure of history.

Wait or reconnect when the existing occurrence can still resolve a material
outcome. Waiting is useful when a queryable provider job is progressing; it is
not useful when no remaining observer can resolve the uncertainty. If safe
continuation remains unavailable, isolate the uncertain units and advance
independent work when the product permits it.

## Prevent the old owner from racing recovery

Lease expiry means the lease is expired, not necessarily that its process
stopped. A paused worker may wake after its replacement begins. A fencing
generation works by making the effect owner reject the older generation; a
token checked only inside the replacement does not fence the old writer.
Compare-and-set revisions can protect local state, while a provider-side
idempotency key may be needed to protect the external effect. Each guard covers
its actual boundary, not the whole workflow by association.

An old callback or retry timer also carries an occurrence identity. Correlate it
to the attempt it describes rather than allowing it to mark the newest attempt
complete. A late effect may require reconciliation without reopening a terminal
consumer result.

The decisive feedback is that the same lifecycle owner now permits the next
normal action and the affected units agree with it. A changed dashboard label
alone is not recovery. What comes back is the recovered or safely concluded
workflow, with any unit whose outcome is still unknown named as such.
