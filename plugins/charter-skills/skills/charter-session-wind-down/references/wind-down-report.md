# Reporting a stop across several sessions

A useful report lets the user decide whether to go ahead with the stop, and
lets each session later resume without replaying completed effects. It is not
a transcript, and it is not a form whose empty fields call for more work. For
one session, or when nothing is mid-work, a sentence or two is the whole
report.

## Comparing sessions

When several affected sessions are mid-work, a compact table shows which ones
hold the stop back:

| Session | Where it is now | Way back | Stop consequence |
| --- | --- | --- | --- |
| Exact title and session ID | Running turn, delivered or queued wind-down, or the question waiting for the user | Last message, handoff or ledger; first safe action | Ready, draining, needs you, or the one missing observation |

Add freshness, host and coverage only when they change the decision. A
projectless session can be affected; a visible remote session may not be. Link
an existing handoff instead of copying it, and do not reconstruct intermediate
checks to lengthen the record.

## Similar-looking states can require different actions

A wind-down queued behind a running turn may not have reached it yet. A
completed turn can still have queued or scheduled successors. A stopped local
command can leave an external operation active. Each difference can change
whether the stop strands work, so read the state that matters rather than
inferring it from another layer.

When unresolved work matters, say what can still produce an effect, who can
control it, whether the way back survives the stop and which decision remains
with the user. Not having seen a process does not show that it is active, and
not having seen a pause take effect does not show that it did.
