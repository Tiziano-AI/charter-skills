# Writer separation and useful handoff

## A collision needs a consequence

The workspace label does not decide a collision; the object and the
consequence do. For a suspected collision, identify what each writer may
change, any effect already in flight, who produces each contribution and who
integrates the result. Then ask: if both continue, what can be overwritten,
duplicated or made inconsistent? Without that consequence there is not yet an
actionable collision.

## Choose between settling and interruption

Stopping new overlapping work keeps the collision from growing. An action
already in flight can still yield a useful contained result, so letting it
settle may preserve more than cancelling it. Interrupt when continuing creates
the collision itself, or cost, destruction, credentialed effects or exposure
others can see.

Keep produced artifacts and complete failure output whichever you choose. A
session that loses integration ownership has not lost the value of its
contribution. Starting a new worker to reproduce a result that exists, or that
a running session will still deliver, creates another dependency instead of
removing one.

## A handoff changes who can act

The receiving owner needs enough to integrate correctly:

- the shared outcome and the decisions already settled;
- exact artifacts, paths, revisions or evidence;
- assumptions and unknowns that could change integration;
- effects already spent and effects still possible;
- complete relevant errors or failed checks;
- what the receiver may change, what stays out of scope, and the next action.

These are the contents that carry decisions, not a required format. The
artifact can stay where it is while the receiver gets its exact location. The
transfer has to reach the session that performs the dependent action;
acceptance into its queue is not incorporation. Check uptake only as far as
that next decision requires.

## Integration reconciles meaning, not just patches

The integration owner picks the version that stays by the desired outcome,
adapts the other contributions to concurrent work and resolves differences in
meaning. A patch that applies cleanly can still carry the wrong contract.
Resolve that contract from the task, evidence and settled decisions; for a
research conclusion or a passage of copy, this may be the whole collision.
When a code interaction remains uncertain and execution can decide it, use an
isolated trial merge with the build or tests that exercise that interaction.
A conflict-free merge alone cannot settle behavior, and green checks cannot
decide which meaning the product should have.

Common failures show which link needs repair:

| Symptom | Broken relationship |
| --- | --- |
| "Done" arrives without artifact or evidence | A status report replaced the contribution |
| Two sessions reconcile the same target | Integration still has two owners |
| Repeated requests for another cycle | The useful result never transferred |
| Clean transplant breaks the destination contract | Integration ignored a change in meaning |
| A contributor retires while a late effect or the only evidence remains | Nobody owns that effect or evidence any more |
| An accepted message is treated as an incorporated change | Delivery was mistaken for integration |

Repair the failed relationship rather than adding another status summary.
Release a contributor when its remaining result or effects no longer change
the work, not merely because a handoff message was sent.
