# Recovering Across Commit Boundaries

An interrupted occurrence can have more progress than its local record admits
or less usable output than its status suggests. Recovery joins these views at
the product's real commit boundaries. Begin with the disagreement that changes
the next action; the occurrence model below is a diagnostic map, not a demand
to inventory every lifecycle object for a small repair.

## Identity determines what can be reconciled

Identify the product's actual lifecycle objects:

- user request or parent workflow;
- job, run, batch, or operation;
- attempt, delivery, worker lease, or retry;
- item, shard, page, offset, or checkpoint;
- provider request or external-effect identity;
- output, destination, and terminal record.

Do not assume a retry reuses the same identity. Some systems keep one job with many attempts; others
create a new job or provider request for each retry. Preserve that distinction so an old callback or
receipt cannot update the new occurrence accidentally.

## State authority differs from evidence of effects

Read the surface that owns legal state transitions: durable job row, provider operation, queue and
lease store, workflow engine, process supervisor, or transaction journal. Caches, dashboards,
filesystem artifacts, and logs may reveal effects but should not be allowed to invent the durable
state.

Capture the owner state with its update time, revision, lease or heartbeat, attempt, and terminal
reason. Classify it as precisely as the product permits:

- accepted or queued;
- acquired or running;
- waiting on a dependency, schedule, approval, or provider;
- completing or committing;
- succeeded;
- failed before effect, failed after partial effect, or outcome unknown;
- cancel requested, canceled, or cancellation lost;
- stale or lease expired;
- orphaned from a missing worker;
- superseded by a newer occurrence.

“No process is running” does not by itself mean the durable job failed, and “success” does not by
itself establish that every expected output is usable.

## Effects partition the unfinished work

Build an occurrence-specific map:

| Unit | Intended transition | Durable state | Effect identity | Output identity | Eligible next action |
| --- | --- | --- | --- | --- | --- |

Use the product's natural unit: item ID, input digest, database key, partition, message, file, page,
cursor range, deployment target, or transaction. Record separately:

- committed effects;
- effects accepted externally but not yet reflected locally;
- outputs written but not registered;
- reservations, locks, leases, or temporary objects still held;
- items never started;
- items whose outcome remains unknown;
- cancellations and timeouts that may race with late completion.

If the workflow has no durable per-unit identity, recovery may need to operate at a coarser boundary
or use compensation before replay.

## A checkpoint's meaning comes from commit ordering

A checkpoint is usable only when its meaning and commit ordering are known. Ask:

- Was the checkpoint written before or after the corresponding effect?
- Is it monotonic, transactional, or merely best-effort progress?
- Does it identify the last completed unit or the next unstarted unit?
- Can completed units be replayed idempotently?
- Did the input set or ordering change after the checkpoint?
- Is output append-only, replaceable, or dependent on prior sequence?

For paginated or streaming work, distinguish provider cursor, source offset, local item index, and
output commit position. They are interchangeable only when the workflow establishes that relation.

If source order can change, "resume at row 200" may skip newly inserted work or
repeat an earlier row. A stable item key or an immutable input revision gives
the offset meaning. If the workflow never established either, recover at the
coarser identity it actually owns rather than treating a convenient cursor as
a correctness guarantee.

## Recovery transitions solve different conditions

### Wait or reconnect

Use when the occurrence is still owned and making credible progress, or when an accepted and
queryable provider operation still has an outcome or effect that matters to the product. Reconnect
to the same identity rather than starting another occurrence.

Stop waiting once the owning surface establishes terminality and every consequential effect,
reservation, lock, lease, or late-event path is reconciled.

### Resume

Use when the same occurrence supports a durable checkpoint and remaining units are identifiable.
Resume from the first uncommitted unit, not merely the last log line.

### Retry

Use the lifecycle's explicit retry transition when the prior attempt is terminal and effect identity
or idempotency prevents duplication. Preserve attempt history and the reason the new attempt is
eligible.

### Restart from a verified boundary

Create a new occurrence when the old one cannot resume but completed effects can be excluded,
adopted, or safely repeated. Bind the new input set to the current source state.

### Adopt output

Use when the intended output already exists and can be associated completely with this occurrence.
Adoption should update the product through its supported transition rather than relabeling an
artifact or cache by hand.

### Compensate

Reverse or neutralize partial external effects when the product defines a compensation path and a
clean restart is preferable. Compensation is a new effect with its own possible failure, not
erasure of history.

### Abandon or quarantine

Use when outcome, identity, or preimage cannot be reconciled safely. Preserve enough state for later
classification and prevent automatic replay.

## A replacement must exclude the old writer

Before changing lifecycle state, check for:

- a newer occurrence for the same logical request;
- a worker whose lease or heartbeat is still current;
- a provider job still capable of completing;
- a late callback, queue redelivery, or retry timer;
- changed input, destination, or configuration;
- an operator action that already resolved the occurrence.

The first four can still write, so exclude them with compare-and-set revisions, fencing tokens,
unique effect identities or another product-owned mechanism before a replacement writes; the last two
change what the replacement should do at all. Canceling a local task does not necessarily cancel
provider work; keep listening for or explicitly reject late completion according to the lifecycle
contract.

## Recovery ends at a normal product transition

After the transition, read the same lifecycle owner and the affected durable units. Confirm that the
occurrence has one coherent state, completed effects have not duplicated, held resources changed as
expected, and the next normal transition—not a special recovery-only route—is now available.

When the workflow will be resumed again and its durable state does not already hold them, a compact
recovery note carries the occurrence identity, owner state and freshness, completed effects, first
unfinished unit, transition taken, late-event risk, and the condition that would permit another
retry.
