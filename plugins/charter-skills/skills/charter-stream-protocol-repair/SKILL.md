---
name: charter-stream-protocol-repair
description: Repair streaming protocols when event semantics corrupt outcomes; fix
  framing, ordering, partial output, callbacks, cancellation, reconnect, replay or
  competing terminal signals at the responsible seam. Ordinary command waiting and
  recovery of one durable job are separate work.
metadata:
  content_version: charter-stream-protocol-repair@2026.10.12.0
---
# Charter · Stream Protocol Repair

A stream gives the consumer observations over time, not an automatically agreed
outcome. Producer, transport, decoder and consumer each have their own state.
Missing finals, duplicate callbacks, partial-result loss and unsafe reconnect
usually arise when one layer's transition is treated as another's: socket
closure becomes success, waiter cancellation becomes remote cancellation, or
replayed bytes become new work.

SSE, WebSocket, JSONL, PTY and subprocess protocols and realtime callbacks
share this class of problem, not one universal state machine. Ordinary command
waiting belongs to its process lifecycle. Durable-job reconciliation belongs to
`charter-workflow-recovery`; presentation of established state belongs to
`charter-status-interface-design`.

A defect with a reproducing input at one layer, such as a record split across
reads or a missing flush, needs the fix at that layer and a check with the
failing input; it does not need a state model of the whole protocol.

## Find the boundary that decides completion

Trace one affected sequence through producer, transport, decoder, consumer
and durable result. These can finish at different times. A clean transport
close may mean success, truncation or loss of observation depending on the
protocol. Process exit is authoritative for that process, not automatically
for remote work it started.

The transport's own rules often decide the bug, and they are easy to get wrong
from memory. EventSource reconnects after the server ends the response body,
so a finished operation can be requested again; an LLM provider reports a
failure as an event after HTTP 200; WebSocket close codes 1005 and 1006 are
never sent by a peer but reported locally; a PTY ends its output with EIO on
Linux and can lose unread output on macOS when the parent waits for exit
first. [Protocol facts](references/protocol-facts.md) gives these rules for
SSE, WebSocket, LLM provider streams and PTYs with their sources; read the
section for the transport in front of you before deciding what a close, an end
of input or an error event means.

Identify the logical operation, attempt, connection and event. Reconnect
usually changes the connection without necessarily creating another
operation; retry may create another attempt or effect. A timestamp alone
rarely establishes order across independent producers. Sequence numbers work
only within their defined ordering scope; two shards can both correctly emit
event 12 without those events being duplicates or globally ordered.

Define the consumer's allowed transitions and the event that commits each
outcome. Recognize completion only from events the protocol defines as
terminal. Skip an unknown event only when the protocol's extension rules
permit ignoring it; an unfamiliar required data or control event cannot be
silently discarded. Where the protocol defines a terminal event, treat end of
input without it as truncation. Distinguish “this attempt failed” from
“the operation did not happen.” The latter requires effect evidence,
especially after a timeout.

An application failure followed by a normal transport close remains an
application failure. Conversely, a committed success followed by a broken
connection need not invalidate the result. Decide which signal owns the
outcome and preserve it across cleanup; last-callback-wins logic confuses
arrival order with authority.

## Preserve the meaning of partial output

Determine whether chunks are append-only deltas, replacement snapshots,
independently committed items or speculative material. Assembly and replay must
follow that choice. Applying a snapshot as a delta duplicates content; replacing
a newer snapshot with an old replay loses progress.

Transport reads need not coincide with application messages. Decode at the
protocol's framing boundary, preserve incomplete multibyte text or records
across reads, and reject malformed complete units according to the public
contract. Data, diagnostics, progress and control can share a transport only
with an unambiguous grammar.

For example, a UTF-8 code point or JSONL record split across reads is incomplete,
not malformed. Buffer until the framing boundary before parsing. But buffering
forever after a complete malformed frame hides an error and may consume
unbounded memory. Framing, size bounds and error semantics need to agree.

Retain partial material when it has useful meaning, but do not relabel it a
complete result. A consumer may stop rendering after terminality while a
separate reconciliation path records a late external effect. That is not a
second final for the same consumer attempt.

## Resolve races, flow and resumption

Cancellation is a request that can race with commit. Define which transition
wins and what remains if cancellation arrives too late. Idempotent cancellation
does not imply that all completed effects can be undone.

Bound queues and decide how slow consumers affect producers. Dropping a
replaceable progress update is different from dropping a data delta. Avoid
unbounded per-event tasks that turn backpressure into hidden memory growth or
reorder callbacks. Distinguish connection, first-event, idle, total-operation
and shutdown timeouts where those states require different recovery.

Backpressure relocates waiting rather than eliminating it. Pausing reads can
bound memory but may violate a provider's idle deadline; coalescing progress
reduces load only when newer progress supersedes older progress. Data that
cannot be dropped may require producer flow control, durable buffering or an
explicit overload failure. Choose from the protocol's retention promise.

A resumable protocol needs a cursor meaning, retention window, gap behavior
and duplicate handling. Advance the durable cursor consistently with applying
the event; otherwise a crash can either lose data or apply it twice. Fence
superseded connections when they can still write. If resumption is unavailable,
a fresh connection must not silently replay a non-idempotent operation.

[Stream semantics](references/workflow.md) develops the partial-output replay
laws, channel authority, liveness timers, cancellation and reconnect races, the
scenarios worth contrasting, and how to write a state model when branches make
prose ambiguous.

## Repair the layer that owns the wrong transition

Change the producer, decoder, adapter or consumer that owns the wrong
transition. A parser fix addresses split records; it cannot fix two writers
committing conflicting terminal states. A state-machine fix resolves that race;
it cannot reconstruct an event a provider never retained.

The useful feedback is the sequence at the consumer boundary, including retained
output and final state. Contrast a split valid record with a malformed complete
one, a duplicate with a new event, cancellation before commit with cancellation
after it, or a reconnect replay with a genuine gap as the defect requires.
Repairing one branch does not establish the others. Report what became
terminal, what output or effects survived and what can safely happen next.
