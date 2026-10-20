---
name: charter-status-interface-design
description: Design or repair UI and CLI status when shown state can mislead action;
  align progress, freshness, outcomes, diagnostics, history and offered controls with
  real state. Recovering the stuck work is workflow recovery.
metadata:
  content_version: charter-status-interface-design@2026.09.26.1
---
# Charter · Status Interface Design

A status surface compresses system state into a decision: wait, continue,
intervene, retry, cancel or trust a result. Its quality depends on preserving
the distinctions that change that decision, not on displaying the most detail
or finding a green label. Trace the consequential label or action to the state
that actually makes it true.

Size the answer to the problem. When one label is wrong for a known reason, fix
its derivation or its words and stop there. A new status row for one job needs
its states, the next action each state allows, what it shows when refresh fails
and what it announces. Comparing several surfaces is worth doing only when they
read the same state and can disagree.

## A label is a projection, not the system

Local liveness, durable job outcome, provider acceptance, destination delivery
and setup answer different questions. "Ready" is meaningful only when its scope
is clear. One composite badge may conceal that a completed job has an offline
monitor, or that a running service cannot perform the requested remote action.

Keep independent dimensions in the model and expose the ones the person needs.
This avoids both a misleading universal health state and a Cartesian explosion
of public labels. A completed job does not become failed because monitoring
disconnected; a successful deployment can coexist with a route still serving an
older revision.

For the label that matters, ask which object it speaks about, which source
establishes it, how it is derived, when it was observed and what someone does
because of it. If the derivation is wrong, repair it there rather than teaching
each view a competing interpretation. Status reports the work; getting stuck
work moving again belongs to `charter-workflow-recovery`.

## Time changes the meaning of evidence

Event time, recording time and client observation time differ. Polling, cache,
clock skew, app suspension and disconnected clients can make old knowledge look
new. A stale heartbeat establishes stale observation; calling the worker stalled
requires a liveness contract that supports that conclusion.

Last-known information is often useful. Keep it distinguishable from current
state rather than erasing it after a failed refresh or silently renewing its
freshness. Choose the age signal from its consequence: an old completed report
may remain valid, whereas old capacity information may no longer support an
action. Clear the stale warning when current evidence arrives.

History and current status have different jobs. History preserves what happened
to an occurrence; a detail view can add later knowledge. A retry is another
attempt, not an opportunity to rewrite the earlier one as successful.

## Progress explains remaining work

A percentage needs a meaningful unit and scope. Exact completed counts do not
make an undiscovered denominator exact. When discovery expands the work, explain
the expansion instead of clamping the number into false monotonicity. Separate
phase progress from total completion and a new attempt from continuation.

Activity, elapsed time, phase, waiting reason and estimate can be more useful
than a percentage. Show the signal that helps someone decide whether to wait
or leave. Indeterminate animation acknowledges activity; on its own it cannot
distinguish healthy work from a frozen process. Time estimates are predictions,
not measured completion.

## Controls are claims about transitions

An enabled action promises that its prerequisites permit an attempt. The
execution path must recheck mutable state; a rendered button cannot lock the
world. If the state changed concurrently, explain the actual outcome with the
user's context intact.

Hide an irrelevant action; explain a temporary missing prerequisite when that
helps the person proceed. A disabled control should become usable when its
condition clears. A generic "Repair" button is not useful if it opens unrelated
diagnostics instead of the correction needed here.

Cancel requested, work stopped and effects retained are different states.
Completion may win a cancellation race. Retry must say what is repeated and
whether the earlier effect may exist. Correct labels and controls depend on
those execution contracts; a copy rewrite cannot repair an ambiguous mutation
protocol or a wrong configuration reader.

## Status reaches people who cannot see it change

A status change shown on screen must also reach a screen-reader user without
taking their focus. WCAG 2.2 success criterion 4.1.3, Status Messages (level
AA), covers results of an action, waiting, progress and errors. On the web, put
an empty live region in the initial markup and change its text. Use
`role="status"`, which is polite and waits for a pause in speech, for results
and progress; use `role="alert"`, which is assertive and interrupts, only for
what needs attention now, such as a failure that stops the work or a required
input. Announce the transitions that change a decision, such as started,
finished, failed or needs input, not every poll or percentage.

Colour never carries state alone (success criterion 1.4.1, Use of Color).
"Failed" and "Done" must also differ in words, an icon or a shape, which keeps
them legible to colour-blind readers and in a terminal without colour.

## Status in a CLI serves a person and a script

On an interactive terminal, a progress bar or spinner that redraws one line is
fine. When output goes to a pipe, a file or CI, print one complete line per
meaningful change instead, such as a phase starting, a count at intervals or
the terminal result, with no redraws, animation or colour. Keep data on stdout
and progress and log messages on stderr, so a pipe carries only the data; when
reporting state is the command's job, as in a `status` command or `--watch`,
that report is its data and goes to stdout.

The exit code is the status a script reads, and it must agree with the printed
words: a run that prints "3 of 5 uploads failed" and exits 0 tells automation it
succeeded. Decide whether the code reports the command's own success or the
state it observed, and say which in help. `gh run watch` exits 0 after watching
a failed run unless given `--exit-status`; `gh pr checks` reserves exit code 8
for checks still pending. A `--watch` mode prints each state change once, ends
with the terminal state and a code that reflects it, and when interrupted says
that watching stopped while the work continues, with the identifier needed to
watch again. The machine-output schema and exit-code taxonomy are protocol
design for `charter-agent-tool-design`; this package decides what they claim.

## Give the decision an intelligible surface

Use product-native words and stable subject identity across UI, CLI,
notifications and diagnostics. A compact row can show the state and useful next
action while details explain scope and freshness. Not every row needs an essay,
and not every transition deserves interruption.

Exercise the branches that can make this surface misleading: stale refresh,
partial result, completion racing cancellation, regained connectivity or an
enabled action that the executor refuses.

Open [state reasoning](references/workflow.md) when a state is derived from
several sources, freshness rules conflict, progress has a moving denominator,
cancel or retry can race completion, several surfaces such as a web row, a CLI
command and a notification must agree, or when you need live-region roles,
native announcements or terminal output detail.
