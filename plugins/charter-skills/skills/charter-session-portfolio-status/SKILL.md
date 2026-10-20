---
name: charter-session-portfolio-status
description: 'Status across the agent sessions or tasks this runtime can list: explain
  from current evidence what is usable, running or waiting and where a decision matters,
  without continuing the work. Inspecting one session, coordination and stopping sessions
  are separate jobs.'
metadata:
  content_version: charter-session-portfolio-status@2026.10.01.1
---
# Charter · Session Portfolio Status

A useful portfolio view explains what is now true of the user's outcomes and
where attention changes the next action. Session activity is evidence for that
picture, not the picture itself. A finished turn can leave an initiative
unfinished; a running support session can coexist with a usable result. A
narrow question gets a narrow answer: "is anything still running on the
billing work?" needs the live sessions for that work and a line each, not a
portfolio.

This is observational work. Do not message, steer, fork, interrupt, archive or
continue sessions, or change repositories, to improve the report. Use ordinary
inspection for one session, `charter-session-wind-down` to stop or pause
sessions and `charter-session-coordination` for a requested intervention.

## Coverage and relevance solve different problems

The listing this runtime offers defines the visible population, and a listing
can be bounded. One that returns pinned and recently updated sessions, with no
way to page further back, leaves out a session that went quiet before that
window: it is absent from the list, not finished. State the bound as part of
the coverage, and read a session you already know about by its exact ID.
Sessions the listing cannot reach, such as another account's, profile's or
harness's, and hosts or sources it reports as unreachable, are blind spots, not
empty. A remembered subset cannot establish the absence of other active work
either.

Scheduled work is part of what is running: include the active automations,
scheduled tasks or loops that target the sessions or projects in scope, with
their target, schedule and latest run, as a layer of their own, and read them
without changing them. When the question is what is scheduled, list the paused
ones too, marked paused.

Within that population, group by established outcome, not title similarity.
One repository may contain several initiatives; one initiative may cross
repositories. Keep live or attention-needing sessions unclassified when their
purpose is unknown rather than silently dropping them.

Keep a session in the account when its work, unresolved effect, waiting
decision or recent result changes the account. Completed sessions often hold
the decisive result or qualify an active claim. Pins, recency and dirty
checkouts do not by themselves establish activity.

## Reconcile statements about the same outcome

Start with the session carrying the user's result or current coordination. Add
sessions whose evidence can change that account. A newer failure displaces an
older success only when it concerns the same outcome, required claim,
dependency or effect. Chronology alone cannot settle the conflict.

A session's final message is that session's own account of its work, and such
accounts lean toward "done". When a line of the report depends on something
being complete, such as merged, released or deployed, check it where that fact
lives: the branch and commits in the repository, or the version actually
deployed. Otherwise report it as the session's claim. Session, repository and
deployment are different layers; do not promote one into another.

The account needs the intended result, the latest material achievement and the
layer that supports it, the current running or waiting state, the next useful
action or human decision, and any missing observation that changes use.

Refresh live state when its age matters, but do not wait for work to finish in
order to report it. A self-starting objective, a queue or a delegated agent
earns inspection when it changes the account. Where the listing does not
show delegates, services or external effects, leave that layer unobserved.

## Organize the result around attention

Lead with material change and where attention matters, not a message or commit
chronology. A project name or established outcome can label a row. When naming
a session, keep its source title and tell duplicate titles apart by exact
session ID.

A compact comparison can show current result, running or waiting state,
decisive evidence and its freshness, next action and attention. Avoid empty
"in progress" cells that hide what remains. "Nothing needs your attention" is
a valid answer.

Recommend an order when a shared dependency, conflicting demand or material
consequence supports it; otherwise say the work is independent. Priorities the
user has not stated are theirs to set rather than yours to invent.

State coverage and consequential blind spots once. If no materially active
work is observed, say so within the inspected scope instead of turning old
sessions into current activity.
