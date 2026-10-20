# Stream Semantics at the Consumer Boundary

The consumer assembles output and commits an outcome from events delivered by
other owners. Diagnose the event distinction that is being lost: framing,
identity, ordering, retention, terminal authority or continuation. The sections
below describe interacting contracts; a framing defect does not require a new
reconnect subsystem or a complete state-model artifact.

## Outcome ownership

Name the transport, public operation, stream and attempt identity, and the consumer that decides
completion. Then draw allowed states and transitions, for example:

```text
idle -> connecting -> open -> receiving -> finalizing -> succeeded
                    |        |             |-> failed
                    |        |-> canceling -> canceled
                    |        |-> disconnected -> reconnecting -> receiving
                    |        |                         |-> failed
                    |        |-> failed
                    |-> failed
```

Use names from the product protocol rather than forcing this example onto it.

## Event identity and order

For each event or frame define:

- type and payload schema;
- stream, request, attempt, and event ID;
- sequence or monotonicity rule;
- states in which it is permitted;
- whether it is data, progress, diagnostic, control, or terminal;
- duplicate and late-event behavior.

SSE `event:` fields, WebSocket message types, callback names, and JSONL row types are part of the
contract when consumers use them. When a transport has both an envelope type and a payload type,
such as SSE `event:` and a `data.type` field, state whether they must agree. A generic sentinel is
valid only if the protocol explicitly defines it.

The protocol's extension policy decides whether an unknown type can be ignored.
An optional progress event may be safely skipped; an unfamiliar required data
operation followed by a known terminal event would instead produce silent loss.
Follow the contract's must-understand, rejection or version-negotiation rule
where ignoring is not permitted. Recognize termination only from defined
terminal events, never from an unknown type. An error event that arrives after
partial output ends the attempt as failed, and the retained partial output
keeps its own label rather than becoming the result.

## Partial output is an algebra, not just text

Decide whether partial output is:

- append-only deltas;
- cumulative replacement snapshots;
- independently committed items;
- speculative output that must be discarded;
- retained after failure or cancellation;
- replayed after reconnect.

The consumer needs an unambiguous way to assemble, display, store, and recover it.
Appending a delta, replacing a snapshot and committing an independent item are
different operations. Their replay laws differ: an append needs deduplication,
a snapshot needs freshness comparison, and an independently committed item
needs its durable item identity. Byte equality alone is not a universal rule;
two identical text deltas may both be legitimate new content.

## Channels carry different authority

Map the channels the implementation actually exposes: response headers, SSE or WebSocket frames,
callbacks, stdout, stderr, and process exit or close codes. State which one is authoritative for each
outcome when they disagree. A channel promised as JSONL or NDJSON carries only that grammar; prose,
tracebacks, or progress mixed with human diagnostics in it break every downstream parser. Process
exit and transport closure remain separate from application success unless the protocol defines
that mapping. The stdout, stderr and exit contract of a command-line tool is designed with
`charter-agent-tool-design`.

## Flow control and liveness

Separate connection or header timeout, time to first byte, idle between events, total operation,
callback deadline, and graceful shutdown. Model producer and consumer backpressure, bounded queues,
buffer growth, slow readers, and downstream pipe closure.

Timeouts should lead to an explicit state and partial-output policy rather than a generic exception
that leaves the consumer unsure whether work continues.

A heartbeat can establish connection liveness without establishing useful
progress. If it resets the only timeout, a stalled operation can live forever.
Conversely, a long computation may legitimately have no data events. Keep
transport heartbeat, progress expectation and total-operation policy separate
where the product needs to distinguish those cases.

## Cancellation and reconnect are racing protocols

For cancellation, trace request, acknowledgement, producer stop, downstream stop, retained effects,
terminal event, and transport close. Define the race with commit: completed work may win before
cancellation takes effect. Make repeated cancellation idempotent, not a promise to undo effects.

For reconnect, define resume token or cursor, replay window, event deduplication, gap behavior,
server retention, and how the old connection is fenced. Coordinate event application with the
durable cursor so a crash cannot silently skip or duplicate a committed unit. Distinguish opening
a new connection from resuming an operation; do not replay effects when safe continuation is absent.

## Contrast the sequences that can falsify the repair

Choose the reachable scenarios whose outcomes can change the protocol repair or claim. Candidates
include:

- normal and empty success;
- producer failure before and after partial output;
- malformed request, frame, or callback;
- duplicate, missing, late, or out-of-order event;
- no first byte and idle mid-stream;
- slow consumer or downstream close;
- cancellation during connect, receive, and finalization;
- reconnect with replay, gap, and concurrent old connection;
- duplicate terminal event or data after terminality.

For each selected scenario, write the expected event sequence, what happens to retained output, and
the final state; capture the actual sequence at the consumer boundary and compare. Repair the
producer, adapter, or consumer that owns the invalid transition.

## Invariants worth encoding

- exactly one consumer terminal result per attempt, separate from any later effect reconciliation;
- no late data or progress reopens a terminal consumer attempt;
- event order is monotonic or explicitly reorderable;
- replayed events can be identified and deduplicated;
- partial output has one assembly and retention rule;
- a racing completion follows the documented winner rule and is not mislabeled as canceled;
- transport close cannot erase an already emitted application failure;
- final callbacks correlate to the correct attempt.

## A written state model, when prose gets ambiguous

When a stream has enough event types, channels, terminal branches or consumers that prose becomes
ambiguous, write the model down with the product's own state and event names. Each real state
records its meaning, entry events and allowed prior states, events accepted while active, output or
effects retained, timeout and cancellation behavior, allowed next states, whether it is terminal,
and its relation to close codes, final callbacks or process exit. Each event records the fields
listed under event identity above. Leave out states and axes the protocol does not have.

## The useful protocol account

State the changed event sequence and only the partial-output, terminal, cancellation, reconnect,
channel, or timeout behavior needed to understand or use the repair.
