---
name: charter-session-status-coordination-and-wind-down
description: Report status or readiness across agent sessions or tasks this runtime
  can list, coordinate a real dependency or collision, or wind work down before a
  pause, handoff or restart. A status question does not authorize messaging sessions;
  preparing to stop does not restart, resume or move them.
metadata:
  content_version: charter-session-status-coordination-and-wind-down@2026.11.20.0
---
# Charter · Agent Session Status, Coordination & Wind-Down

“Can I quit?” asks what quitting would interrupt. Inspect the affected
work and answer; do not message a session to make the answer yes. “Get
these sessions ready to quit” asks for a stop at a coherent point, not
for the app to be closed. “Coordinate the two fixes” asks for intervention
only where the work interacts. The same two sessions may be visible in
all three cases; what you may do with them is different.

## Report what is usable, running or waiting

For a view across sessions, read [Session portfolio status](session-portfolio-status.md)
before deciding which work counts. A narrow question about one session
needs only its current evidence. List the requested population, including
relevant scheduled work; identify where a limit on history, account, host
or listing leaves a blind spot. Group by the result the person cares about,
not by similar session titles. A finished turn can leave a deployment in
flight. A session waiting for a decision can already have delivered a useful
artifact. Check a material completion claim where the result lives or
attribute it to the reporting session.

Report now rather than waiting for the picture to improve. State what is
ready, what still runs or needs a decision, and which observation is missing
if it would change the answer. Keep this read-only: no messages, steering,
interrupts, queued turns, repository edits or work resumed for the report.
If the issue is what agents repeatedly missed in past work, give
`charter-ai-evaluation-and-session-learning` the relevant records and
question rather than steering a live conversation.

## Coordinate work that really intersects

Read [Session coordination](session-coordination.md) before contacting a
writer. Name the shared object or missing result and say exactly how one
session changes the other's next valid action. The same checkout need not
mean a collision; different branches can still change the same live service
or define incompatible meanings for one field. Use the [dependency model](references/initiative-and-occurrence-model.md)
when it is unclear which session needs which result. If there is no
consequence for the other session, leave both alone.

Where scope can separate the work, separate it. Where two contributions must
be reconciled, choose one integration owner for that result, not a supervisor
over both sessions. Use [writer separation and handoff](references/collision-handoff-and-integration.md)
to transfer the actual artifact, its base, decisions, failures and remaining
rights to change it. Stop new competing effects only within the grant;
preserve useful work and unrelated directions. Check the actual recipient,
current activity and pending messages before delivering a change. A message
to an idle session may start it, and an after-turn message may arrive too late
to prevent a conflicting write. Use the supported route at the boundary needed;
if it is unavailable, provide the handoff for the person rather than assume
control elsewhere. Verify a material dependency by what the receiver does
with the contribution, not by a send receipt.

## Prepare an orderly stop

For readiness or an actual wind-down, read [Session wind-down](session-wind-down.md)
to determine what the proposed stop can strand **before** sending anything.
A client restart need not stop a remote job; a host restart may discard the
temporary files an idle session needs. Waiting for input or approval says
nothing about background work. Look for live effects, queued messages,
self-starting objectives and schedules; carry forward the person's unresolved
question, options and what depends on it. An ordinary disposable preview
needs a way back, not a completed project.

Only for a requested wind-down, direct affected active sessions to start
nothing new, finish useful in-flight work at a coherent point, preserve the
result and first safe next action, then wait. Do not wake a settled session
to ask it to stop. If an authorized preservation action is necessary in an
idle session, limit the turn to that action. A queue is not work to launch
just to drain it. Pause self-starting work through its authorized owner rather
than marking it complete; include scheduled work only within the requested
stop. A request sent is not a stop observed.

Use [the wind-down report](references/wind-down-report.md) when some
sessions are ready and others are draining, need the person or lack a
decisive observation. Say which work and effects survive the stop, where the
way back lives, and what still has an owner. Readiness is not permission to
restart, log out, switch accounts, transfer or resume. If a real interruption
has already left a send, deployment or other external effect uncertain, give
`charter-workflow-recovery` its exact operation identity; do not start
the work again to find out what happened.
