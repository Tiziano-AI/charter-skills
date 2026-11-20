# FSEvents Branch

Load this reference when `fseventsd`, `deleted`, `backupd`, a file-watcher
client, or FSEvents drop/rescan signals are part of the incident. It prevents a
common misdiagnosis: naming the dropped client or most recent disk-heavy app as
the producer without establishing the event chain.

## Actors

- `fseventsd` brokers filesystem event streams and may perform work separately
  for many clients.
- A watcher client chooses roots, lifetime, latency, and teardown behavior. Many
  short-lived clients or repeated root reconfiguration can multiply daemon work.
- `deleted` owns CacheDelete and purgeable-space work. It can be an FSEvents
  client that falls behind rather than the original producer.
- `backupd`, snapshots, cleanup tools, mounted volumes, and disk pressure can
  create work or amplify backlog, but none owns the incident merely by being
  present.

## Investigation branch

1. Capture CPU, resident memory, CPU time, thread count, and PID for `fseventsd`.
   Capture the same fields for suspected clients and controllers.
2. Constrain unified logs to the onset. Find client additions, roots, PIDs,
   dropped/rescan markers, teardown, purge failures, backup transitions, and the
   time heavy work stops.
3. Resolve each short-lived PID to an executable and parent at the event time.
   Do not map an old PID from current process state alone.
4. Group repeated daemon work by client, thread, time block, and root. Similar
   blocks following separate registrations support per-client replicated drain;
   they do not by themselves prove journal corruption.
5. Compare current filesystem event rate with daemon CPU. Low current churn plus
   high daemon work supports historical drain, replay, recovery, or client churn
   over a live producer storm.
6. Only if that distinction remains decision-relevant, create a short, bounded
   fresh FSEvents stream for narrow roots. Record event IDs, flags, rates, and
   timestamps; stop it when the window ends.

## Interpret carefully

- A user-space dropped/rescan signal describes a client buffer failure. The
  client receiving it may be slow, may be collateral damage, or may have joined
  an already degraded state; it is not automatically the producer.
- A fresh stream receiving degraded-state markers while current event rate is
  low is evidence against “too many files are changing right now.” It does not
  by itself identify the client or library that created the backlog.
- Repeated group-resolution or client-loop log messages can correlate with new
  stream creation. A diagnostic probe also creates a client and can therefore
  generate the message under investigation.
- CPU returning to idle while resident memory remains high separates completed
  drain from retained allocation. Restarting may release the residue but says
  nothing about the recurrence owner.
- Purge, teardown, or registration failures in a client library matter only when
  their timing and multiplicity explain the daemon work. One real bug need not be
  sufficient for the observed incident; backlog size, root churn, or an internal
  threshold can still be necessary.

## Discriminators

Use the smallest observation that separates the live explanations:

| Competing explanations | Observation that separates them |
| --- | --- |
| Active producer storm vs historical drain | Short current event-rate capture alongside daemon CPU-time growth |
| One slow client vs global degraded state | Bounded fresh stream plus contemporaneous client logs |
| One backlog vs per-client replication | Registration timeline aligned with repeated daemon work blocks |
| Active work vs retained memory | Repeated CPU time, RSS, state, and thread samples after the burn ends |
| Trigger vs amplifier | Onset order and a user-authorized before/after change to the suspected controller |

A custom Swift watcher is an observer, not a neutral fact source. Keep roots and
duration bounded, include event IDs and flags when those change the conclusion,
and account for its own client registration in later log analysis.

## Recovery and repair

Do not manually delete `.fseventsd`, purge the per-volume event database, unmount
volumes, restart the daemon, or disable backup merely to see whether CPU falls.
Those actions erase or change the state being diagnosed and require explicit
authority.

When evidence points to client churn, the structural repair belongs in the
watcher or its library: deduplicate roots, register them coherently, avoid
rebuilding the entire stream for every path change, and eliminate invalid or
unnecessary teardown work. Closing the client or rebooting the Mac can contain
or recover an incident, but does not establish that repair.

Report storage pressure, Time Machine, cleanup tools, and other background work
as triggers or amplifiers unless the onset and counterfactual establish them as
the recurrence owner.
