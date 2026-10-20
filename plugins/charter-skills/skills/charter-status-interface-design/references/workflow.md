# Reasoning about a state surface

Visible state is a projection of evidence into decisions. Tracing the one label
or action whose mistake would matter gives the repair a narrower target than
"make the dashboard accurate."

## A source can answer only its own question

Consider a document export with a worker, durable job row, object store and
download route. A live worker does not establish that this job is running. A
completed job row may establish successful generation while the download route
still fails. A recent object can belong to an earlier attempt.

The useful public state depends on the promised action. "Generated; download
temporarily unavailable" preserves two important facts. A universal "failed"
may invite regenerating a valid artifact; "complete" with a dead download button
may leave the person unable to finish. If the job promise includes delivery,
model that phase explicitly rather than broadening a convenient source label.

Carry subject and occurrence identity through derivation. A later attempt can
succeed while an earlier one failed. Aggregating by the document alone may turn
the failed attempt green or offer cancellation for the wrong work.

## Public vocabulary is smaller than internal state

Keep meaningful differences without exposing every implementation phase.
Queued, waiting for input, processing, partial success, failed and canceled
suggest different behavior. Setup missing, denied, unsupported and temporarily
unavailable may all prevent an action, but the remedy differs.

A state machine governs transitions and terminality; independent dimensions
such as connectivity and freshness qualify what is known. Combining every
dimension into one enum creates brittle transitions and unreadable labels.
Conversely, leaving them unmodeled makes views invent conflicting meanings.

Several surfaces can use different detail without contradiction. A compact row
might say "3 files failed"; a detail view can list successes and failures. A
notification records the result at its event time; reopening it can lead to a
current view with later knowledge.

## Freshness belongs to the claim

A stale threshold has a reason only in relation to the decision. A heartbeat
expected frequently can lose its ability to establish liveness after missed
updates. A completed immutable report need not become suspect because it has
not been polled today. Source age and result age are not interchangeable.

Model poll delay, cache age, disconnected clients, sleeping apps and clock skew
where they affect interpretation. If refresh fails, preserve useful last-known
state with its time; mark currentness unknown rather than silently restarting
the age. If a fresh response arrives for an obsolete target, it must not renew
the current target's freshness.

When sources disagree, derive the state the person's decision needs rather than
choosing the greenest source:

- service alive, provider unknown: the local service is ready and remote action
  availability is unknown;
- job says running, heartbeat stale: last-known running, current liveness
  unknown; call it stalled only when the product's liveness contract
  establishes that;
- deployment complete, routed revision old: deployed but not live on the route;
- outbox retryable, earlier provider outcome ambiguous: retry blocked, or
  offered as an explicit choice that names the duplicate risk.

A product may deliberately choose when to draw attention to stale data. That
choice should reflect consequence and expected cadence, not an arbitrary
universal interval.

## Progress needs units with a stable meaning

Suppose an import has discovered 100 files and processed 42. "42 of 100
discovered files" is accurate while discovery continues; "42% complete" may not
be. A later denominator of 160 represents new scope, not necessarily lost work.
A new attempt starts another progress identity rather than inheriting a
cosmetically pleasing counter.

Weighted stages can be useful when their costs are understood. Equal weighting
of upload, processing and delivery is misleading if processing dominates and
varies wildly. When remaining work cannot be estimated, show current phase,
latest completed unit, elapsed time or waiting reason. An estimate can still
help if it is presented as an estimate and revised when its basis changes.

## Actions and state must use the same contract

For an action, connect eligible states, additional prerequisites, actual
consequence, immediate acknowledgement and eventual outcome. Visibility is a
product choice; eligibility is an execution contract. The executor rechecks
mutable prerequisites because the world can change after rendering.

A cancellation race illustrates the distinction:

- Clicking Cancel sends a request; acknowledgement can mean only that the
  request was accepted, not that work stopped.
- If work stops, completed effects may remain.
- If completion wins, show completion rather than inventing a canceled result.
- If the request outcome is unknown, preserve that uncertainty and use the
  occurrence's readback rather than treating another click as harmless.

Retry requires knowing whether it repeats failed units, the whole job or an
external effect that may already exist. "Try again" without that scope can
create duplicates. A known missing account should lead to account correction
with context retained, not a generic retry loop.

## When several surfaces share one state

A web row, a CLI command, a notification and a history entry can each derive
the same job's state on their own and drift apart. To find where, write down
each underlying source once: its owner, the occurrence it describes, its raw
states, when it was observed, when it stops supporting a claim, how it becomes
product state and what happens when it cannot be read. Then each surface: the
sources it reads, the state it derives, its label, detail, age, and empty, unknown and error
copy,
how it refreshes and which actions it offers. Then each action: the states that
allow it, other prerequisites, its consequence, whether it asks for
confirmation, whether it is shown, disabled or hidden, its immediate acknowledgement and the resulting state on success,
failure, cancellation and an unknown outcome, and the recovery it offers. Use the product's own state names
and keep only the entries where surfaces could disagree.

For a single export job it reads like this. The source is the job record in the
job store, identified by job id, raw state running, with an observation time.
When the heartbeat is late, the product state becomes last-known running with
current liveness unknown, and a failed refresh keeps that state with its time.
The web row reads the record and shows "Processing", "42 of 100 items" and the
age of the update; when refresh fails it says "Current progress is unavailable.
Last update: 14:02." and offers Cancel. Cancel is allowed while the job is
queued or running and the current occurrence is known; remaining items stop and
completed items remain. Clicking it shows Canceling. The result is Canceled when
cancellation wins and Completed when the commit already won. A failed request
leaves the last-known state with the error; an unknown outcome stays Cancel
requested until the exact occurrence is read again, which also comes before any
second attempt.

Surfaces may differ in detail but must not give the same current state
contradictory meanings. The comparison is a coordination aid: keep the real
state and copy in their existing owners rather than in a second registry.

## Accessible status

Assistive technologies announce changes to a live region they already know
about. Put the empty region in the initial markup, or insert it and change its
text in a later task; a region created together with its message may stay
silent. Choose the role by urgency and shape:

- `role="status"`: advisory results and progress; polite, so it waits for the
  current sentence or a pause in typing. It should not receive focus when it
  changes.
- `role="alert"`: important, usually time-sensitive information; assertive, so
  it interrupts. Reserve it for failures and required input.
- `role="log"`: an ordered sequence such as a job's event history; polite, with
  new entries read in order.
- `role="progressbar"` with `aria-valuenow`, `aria-valuemin` and
  `aria-valuemax` kept in step with the visible bar; omit `aria-valuenow` while
  the amount is indeterminate.

A change of context, such as moving the person to the finished result, is not a
status message and needs no announcement.

On Apple platforms, `AccessibilityNotification.Announcement(_:).post()` from the
Accessibility framework announces a change without moving focus. Its attributed
string's `accessibilitySpeechAnnouncementPriority` sets urgency: `.low` queues
behind current speech, the polite equivalent for results and progress;
`.default` interrupts current speech but can itself be interrupted; `.high`
interrupts and cannot be interrupted, for a failure or required input. Set
`.low` explicitly for routine status.

## Status in a terminal

Animate only when output goes to an interactive terminal. In CI logs, pipes and
files, a redrawn line turns into pages of fragments: print one complete line per
phase change, a count at a modest interval and the terminal result, with a
timestamp when the log will be read later. Redrawn lines and spinners are also
hard for speech synthesizers and braille displays to follow and can bother
people with motion sensitivity, so offer a text-only progress mode even on a
terminal; the GitHub CLI's `spinner disabled` setting is one example. Drop
colour when the stream is not a terminal, when `NO_COLOR` is set to a non-empty
value, when `TERM` is `dumb` or when the user passes `--no-color`; the state
words must read correctly without it.

Print the state and choose the exit code from the same derivation, so the two
cannot drift. Distinct non-zero codes help when a script must tell failure,
partial success and still pending apart. A watcher polls, but its output should
change only when the state does, and on interruption it should give the command
that resumes watching the same occurrence.

## Read the surface as a person

Copy should make the state, relevant reason and useful action intelligible.
Scope or age belongs beside the label when omitting it changes the decision;
technical derivation can remain in detail. Do not force a fixed five-part
message into every badge.

Exercise the branch capable of contradicting the new model: an old response
after navigation, a lost monitor after success, completion during cancellation,
or setup becoming available while a button stays disabled.
