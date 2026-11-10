# Charter · Session Coordination

Two agent sessions or tasks need coordination when one can change whether the
other's next action is valid, possible or safe: one needs the other's result,
both may write the same thing, or both are settling the same behavior
differently. They may run in one harness or in different harnesses working on
the same checkout. Running at the same time or sharing a repository is not
enough. When they share no object or result, they are independent: say so and
leave them running.

Use `charter-session-portfolio-status` to report where sessions stand,
`charter-session-wind-down` to stop or pause one or more sessions, including
before a restart, and `charter-workflow-recovery` for one interrupted run whose
effects are uncertain. Ordinary delegation needs none of this.

## Dependencies run through objects and consequences

Resolve each session's exact identity and current purpose where it lives,
with the tools this runtime offers for reading and messaging sessions. When
the other session is beyond what these tools can reach, in another harness,
account or profile, write the transfer as a message for the user to deliver,
with the contents listed under the handoff below. Then name the relationship:

| Relationship | What makes it actionable | Useful intervention |
| --- | --- | --- |
| Prerequisite | B needs A's result for a valid next action | Wait for that result, transfer it, or give B a valid path that does not need it |
| Write collision | Both may change the same object or destination | Separate the scope or give it one writer |
| Semantic collision | Both choose different truths for one behavior | Give integration to one owner, who picks the version that stays |
| Missing contribution | A holds an artifact or evidence B needs | Transfer that exact contribution |
| Live activity | B's next decision depends on something A still runs or controls: a late effect, a watcher, a delegate | Observe or control it through A, or leave it bounded with A |
| Supersession | A's remaining work would duplicate or invalidate B's | Stop A's new competing effects |

A completed session can still hold the decisive artifact. Different checkouts
can contend for the same deployment or product contract, while two sessions in
one directory may touch nothing in common. If you cannot name the shared object
or the consequence, find that out before steering either session.

A semantic collision is the one a clean merge can hide. First identify the
contested meaning and the task, evidence or settled decision that governs it.
Conflicting research conclusions, copy or product decisions may be resolved
there. For code, an isolated trial merge is useful when executing the combined
contributions can reveal an interaction that would change the choice: apply
them in a throwaway worktree and run the relevant build or tests, then remove
the worktree. Passing checks on each branch alone do not establish that the
combination works; passing combined checks do not choose the intended contract.

[The dependency model](references/initiative-and-occurrence-model.md) helps
when it is unclear which sessions belong to the problem or which way a
dependency runs.

## Production and integration are different responsibilities

Production creates a contribution; integration decides how contributions fit
together in the shared result. Give each shared result one integration owner,
chosen as the session best placed to judge the desired outcome, not by who
wrote more, which session was opened first or which touched it last. That owner
gets the shared result, not control over the contributors' unrelated work, and
independent artifacts can keep different owners.

When overlap is real, stop new competing changes. An action already running in
a contained way may be worth letting finish, because it produces evidence or an
artifact; interrupt it when continuing is itself the collision or exposure.
Cancelling a session only to tidy the session list loses work without
resolving the dependency.

Transfer the decisive artifact, the exact base it was built on, complete
relevant failure output, the decisions already settled and what the receiver
may change. A status paraphrase does not replace the contribution. After the
transfer the producer stops building a competing version; a bounded follow-up
can still help integration.
[Writer separation and handoff](references/collision-handoff-and-integration.md)
covers what the receiving owner needs and the symptoms that show which link
broke.

## Control only what resolves the interaction

An existing result is better than a second session recreating it. A scope
change is enough when writers can be independent; ownership transfer is needed
when they cannot. Waiting helps when the prerequisite is already being produced
and nothing else can supply it. Stopping or interrupting a session helps when
its continued execution is itself the problem.

Resolve coupled decisions together, but do not force independent work into one
serial order. A small graph may clarify dependencies; it should not become a
tracker to maintain.

## Deliver a change while it can still govern the work

A correction to current work, a withdrawn premise or an answer that unblocks
the active turn belongs in that turn through the runtime's supported steering
route. An independent later task belongs in its queue. When the recipient is
idle and continuation is authorized, start the useful next turn rather than
wait for a reporting tick. A pause or intake-only hold still forbids that
continuation; coordination does not enlarge anyone's authority.

Steering can interrupt tools. Compare the effect of interrupting the action
already in flight with the effect of delaying the correction. Let a valid,
contained write reach a supported safe boundary when that preserves the work.
Do not leave an invalidation behind an action that would now be unauthorized
or harmful: use an authorized containment route, or bring the missing authority
to the person who can decide. Neither "always queue" nor "never steer during a
gate" makes that trade-off. A delivery choice supplies no permission to bypass
the gate, force-stop a process or restart a session.

Pending directions are separate by contribution or dependency, not merely by
recipient. Where a later direction replaces an earlier one from the same sender,
keep one coherent current instruction with its surviving requirements. Use the
runtime's supported edit, cancellation or promotion of the existing message
when available, after reading fresh queue state. Replace only wholly owned,
still-queued material actually superseded by this change. Preserve independent
questions, unrelated content, mixed-ownership messages and other senders'
directions, including the person's. If consumption races an edit, establish
what reached the recipient and reconcile that state rather than send the same
effect again.

Accepted, queued, steered, understood and acted on are different observations.
For a material dependency, inspect the receiver's next relevant action or
result: did it stop using the withdrawn premise or produce the corrected
contribution? A delivery receipt cannot answer that. An informational update
that changes no dependent action needs no acknowledgement ritual. An external
reviewer sends its critique to the integration owner; a delivery route does
not give it control of that owner's workers.

## Continue through the actual dependency

A contributor's result, failure or blocker changes the next action when it
arrives, not at the next reporting slot. Advance independent authorized work,
integrate what arrived, or use the prerequisite's supported lifecycle wait.
Reporting samples and explains the work; it is not the clock that dispatches
it. Keep the person's account coherent rather than have several jobs announce
the same event as independently new.

When waiting, identify the execution that still carries the dependency. A
newer cancelled run does not establish that an older active run ended. A
completed turn can still leave delegated or background work that matters;
wait for that settlement when it is the prerequisite, not just the last
assistant message. Follow the actual completion/wake contract of an entrusted
delegate. For a peer session, use the supported wait for the relevant run or
an authorized return message; do not assume the delegate's wake contract covers
it. A recorded duty, thread owner or activation condition is not itself an
operating route that resumes the work. No polling loop, watcher or scheduled
job is needed merely to make responsibility look active.

The coordination is done when the dependency is resolved or safely bounded and
each piece of useful work has one owner that no other session competes with.
Report the relationship or owner that changed, what can still alter the result
and the next step; independent sessions do not need to finish first. Then
judge the integrated result against the person's purpose. A settled queue and
finished contributions do not make a missing or unusable product complete.
