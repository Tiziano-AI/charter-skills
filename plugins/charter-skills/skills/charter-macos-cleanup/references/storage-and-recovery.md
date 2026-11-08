# Storage effects and custody

## What a plan binds

A scan is a saved, bounded observation. It records discovery coverage, excluded
boundaries, candidates, metadata preimages and reconstruction evidence. A plan
selects qualified candidates and binds the current helper bytes, scan, exact
object identities or native policy and destination scope. It is immutable:
changed helper bytes, inputs, ancestors, contents, command identities, observed
versions, endpoints, nodes or owner settings require inspection and planning
again before new execution. That stale-plan protection is distinct from admitting
a fresh installation through its supported operation contract.

Regular reconstruction evidence is hashed in streaming chunks, with file
identity, length and modification checks around the full read. Its size does
not require an indirect hash note. Metadata parsing has separate limits from
evidence hashing and discovery. Consumer coverage records the supplied roots,
overlap deduplication, entries visited and real metadata-binding omissions;
ordinary source files and directories do not consume that binding allowance.
Compacted outcomes retain coverage counts and disclose omitted root records,
not a claim that omitted diagnostics were saved in full.

The helper bounds saved scans, plans and operation growth so emitted reports
remain readable by their next consumer. A bounded inventory can carry explicit
incomplete coverage, findings and narrower inspection as the next step;
pagination alone does not establish a complete saved inventory. A selected plan
that cannot fit its required operation record is refused before execution.

The agent still determines whether material is authored, retained, reproducible
or source-linked. A typed reason is not a machine proof of those judgments.
Read unfamiliar output configuration and the owner guide before selecting it.
The helper never evaluates a repository's Python, shell, `.pth`, manifest
scripts or templates to decide what can be removed.

Filesystem snapshots stay on one device and do not follow symlinks. Removal
holds directory descriptors, verifies preimages, refuses newly added objects
and tests actual macOS guarded unlink behavior on its own disposable fixture.
If `AT_NODELETEBUSY`, no-follow and beneath semantics do not work on that host,
filesystem cleanup is unavailable: no weaker deletion fallback is offered.
The executable self-test controls admission on the actual host; a platform
label alone does not establish those semantics.

The open-file guard does not protect an open directory or a future consumer.
Stat and unlink are not one compare-and-delete syscall. Exclude active writers,
inspect lazy/source-linked consumers and stop the affected candidate on a
conflict. A tree can be partly removed before a new conflict appears; retain
the report and reconstruct only if use resumes. Hardlinked files are unlinked,
never truncated, so links outside the selected tree retain their contents.
Persistent lock names are retained. There is no quarantine or automatic restore;
recoverable inputs and the recorded reconstruction recipe are the recovery path.

An existing environment lock is opened read-only and held with nonblocking
exclusive `flock`; it is never written, recreated or replaced. Full preimage
and ancestor checks still apply. A `lock_changed` refusal names the changed
signature fields or ancestors; it does not establish that another process held
the lock.

## One attempt, shared resource claims

`clean` and `reclaim` create the requested operation file exclusively. Existing
files are status targets, not replay permission. Before each effect, the helper
also holds a durable resource claim in:

```text
<OS account home>/Library/Application Support/Charter Mac Cleanup
```

It resolves the account home through the OS account record, not an overridden
`HOME`, an agent's configuration root or package location. All installed copies
in that OS account therefore see overlapping resource claims. The private
directory is independent of the package's installation state. Admission locking
serializes claim decisions and outcome recording, waiting within a bounded
budget for contention on the same persistent lock. A `custody_busy` refusal
never replaces or steals that lock. Each foreground writer also holds an
attempt lease. A crash releases the live lease but leaves durable custody.
A new operation filename cannot evade it. Venv payload attempts claim their
environment conservatively while selecting only the inventoried files.

The operation file carries the plan, actions, lifecycle checkpoints, actual
outcomes and reconstruction recipes. The private claim carries enough intent
and outcome to retain custody if the caller moves or loses the report. Do not
delete or edit these records to clear a refusal. A changed or unreadable report
is a recovery problem, not authority to run again.

If custody cannot record or release a known action outcome, the helper still
attempts to save that outcome in the operation report. It stops the batch and
returns `custody_recovery_required: true` with `custody_finalize_failed`, the
failed phase and underlying error. The action's execution outcome remains
distinct from unfinished custody; even a single completed action leaves the
batch partial until custody is settled. Use status, not another cleanup call.
The caller-owned report alone cannot release a native claim: status still
requires the durable claim's terminal evidence or the original owner's readback.
If that readback differs from the saved receipt, status keeps the original as
`caller_reported_outcome` beside the trusted `outcome`. This report-only evidence
preserves measurements without authorizing claim release or overriding an
unresolved native result. Repeated status preserves that same receipt rather
than growing a chain of observations.

`status --operation <path>` reads one attempt. `status` discovers shared claims
without knowing its filename. Status may settle a dead writer's claim using
the original bound route's readback and persist the result. It performs no
cleanup, trim, restart or retry. A status read cannot settle a writer that still
holds its lease.

Readback must establish the original service/namespace and the command identity
needed to observe it. A replacement executable, changed route environment such
as `CONTAINER_ROOT`, or a same-named container in another service cannot settle
the original claim. A stopped or different incarnation proves termination only
on the original bound route. If that route cannot be established, keep the claim
unresolved; do not start services or connect to a remote replacement.

Identity drift before native submission releases custody as an unsubmitted
conflict; uncertainty after the durable submission checkpoint retains it.
A saved operation interrupted before its first action is incomplete work,
not successful cleanup merely because no resource claim remains.

| Result | Meaning and next action |
| --- | --- |
| `completed` / `no_change` | Execution ended. Read measurements before claiming space recovered. |
| `skipped` / `conflict` / `blocked` | Candidate was retained or admission refused. Read its reason; do not force through activity or missing evidence. |
| `partial` | Some effects may survive. Use the recorded paths and recipe; inspect survivors before selecting further work. |
| `execution_unresolved` | The native operation may still produce effects. Keep custody and use status; do not submit again. |
| attribution `unknown` with `execution_ended: true` | Execution is settled but exact bytes/effects cannot be attributed. Report uncertainty; the claim need not remain forever. |

Top-level JSON uses `schema_version`, `command`, `state`, `data` and `issues`.
Exit 0 means a completed read/plan or completed/no-change execution; 1 means a
conflict, skip, partial or unresolved operation; 2 means unusable arguments,
input or contract. A successful inspect can still have incomplete coverage or
refused native families: read `coverage`, `native_findings`, candidate issues
and `next_cursor`. A batch with both removals and skips is partial, never “all
removed.” Detailed reports remain in saved JSON rather than flooding the model
with every payload filename.

`request_coverage` preserves the requested-family dispositions through planning
and results, including unselected, retained and refused work. Its
`inspection_scope` distinguishes a root inventory from `requested_candidates`;
the latter covers only `requested_candidate_paths`, even when inspection is complete.
`result_scope: selected_plan` limits the execution outcome to selected actions.
Read status's `observation_state` and `custody_state` separately from the cleanup
outcome: completing a status read or settling an orphan claim does not turn a
partial or unstarted cleanup into success. Account for families outside the
saved scan as well when the user's request was broader. Neither zero claims nor
one successful exit code establishes whole-request completion.

## Measurement and package lifecycle

Logical size is file length. Allocated size is filesystem blocks attributed to
the observed unique inodes; hardlinks are deduplicated. Neither equals physical
space reclaimable from APFS clones or snapshots. Engine cache totals and guest
trim acknowledgements are another layer. Host `available_bytes` before/after
belongs to a named filesystem device and can include concurrent changes.
Do not sum these measures or label their difference exactly attributable to
this cleanup. Moving material to Trash on the same volume does not reclaim it.

This package has no daemon, queue, scheduler or background restart. A native
service request can nevertheless outlive its CLI, which is why custody exists.
Disabling or removing the skill stops its discovery, not accepted service work
or the account's shared claims. Package updates and removal must preserve those
claims and caller-owned reports. The current helper can read retained operation
metadata and custody after an update without executing a stale plan. Recovery
does not require exact historical release equality, but it still requires the
original bound service route for termination readback. If the helper is absent,
restore it through its owning installation route; do not hand-edit records or
infer that removing the skill ended an operation. Updating the package does not
change an already-running agent's loaded instructions.
