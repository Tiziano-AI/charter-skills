# Storage effects and custody

## Qualify the candidates and their consumers

Start from the requested layer and the machine's owner guides. Use an existing
storage inventory where available to choose bounded roots;
do not repeatedly rescan the whole home. Read project instructions, manifests,
lockfiles and output configuration for the candidates, not every source file.
Use the helper's saved scan for subsequent inspection. Read its coverage and
findings before selecting: a native refusal does not invalidate usable filesystem
candidates, and an unsupported operation does not prove its data is unreclaimable.
Discovery recognizes metadata relationships; `--candidate-path` admits unfamiliar
output layouts for qualification, not deletion by name or a filter on discovery.
For known exact outputs, combine `--root <whole-owner>` with
`--candidate-path <output> --only-candidates`. This reads only the requested
payloads and fixed ownership metadata along their ancestors inside the root;
it does not enumerate unrelated siblings. Keep the root broad enough to observe
the real repository, manifest or declared owner: process matching still covers
that whole owner. Static consumer checks inspect the supplied `consumer_roots`;
include the relevant installed launcher and registration metadata there.
Coverage then describes the requested
candidates, not an inventory of the roots. Missing, unreadable or changed paths
and symlink, application, filesystem or environment boundaries remain findings;
they do not trigger a direct-snapshot fallback. To inspect a virtual environment,
request its root, not a child behind its inventory boundary. Application download
caches need their owner's redownload route; arbitrary `Library/Caches` trees are
not disposable just because of their location.

For projects without a recognized manifest or repository marker, declare the
project's actual consumer boundary with `inspect --project-root <project>`;
repeat it for separate projects within a broader scan. Establish that boundary
from the project's inputs and consumers, not just the presence of a guide.
`--candidate-path` selects an output, whereas `--project-root` identifies the
whole project that may consume it. Read each candidate's `owner_root` and
`owner_basis`: `scan_root` is a conservative fallback, not a discovered project.
A declaration cannot narrow an established manifest or repository owner. Guides
remain qualification evidence and do not silently change consumer boundaries.

A manifest and a lock identify inputs; they do not prove the installed state is
reproducible. Check local/source-built distributions, editable dependencies,
generated inputs and retained baselines. A mixed build tree must be split into
qualified children. Keep authored files and accepted test results even inside a
directory called `build`, `target` or `DerivedData`.

Before selecting a family, establish all three:

- **Reconstruction:** retained inputs, required toolchain/provider and the exact
  command or redownload route. Record missing setup instead of promising a
  rebuild that depends on unavailable sources or credentials.
- **Retention:** what the owner intends to keep. A guide is evidence about that
  intent, not permission to widen this cleanup.
- **Consumers:** running work and installed/source-linked users. A CLI launcher,
  editable Python install, app extension or service may load a checkout lazily
  without an open descriptor. Include relevant installed metadata directories
  or individual metadata files in `consumer_roots` (for example launcher and
  extension registration locations); explain why those scopes cover the selected
  operation's risks. An empty unrelated directory does not establish absence of
  consumers. Scope launcher and registration metadata, not unrelated evidence
  archives merely because they contain familiar metadata suffixes.

Consumer protection follows the operation. Exact filesystem removal needs fresh
checks for active writers and lazy/source-linked users. Native unused-entry
pruning can rely on established native reference and locking behavior, with
additional checks where it leaves a real consumer exposed. Establish generated
metadata's relevance from its content and references, not its filename.
Unrelated metadata need not veto another family; unknown executable hooks remain
unresolved where their behavior could matter. Never import or execute inspected
metadata to clear a finding. An external launcher referencing the project's
source can consume its dependencies lazily; a normal internal link to a retained
sibling is not by itself a consumer of the selected payload. Python
`direct_url.json` with recognized `archive_info`, `vcs_info` or non-editable
`dir_info` records installation provenance, not a runtime link to that origin.
An editable VCS install records its local clone with editable `dir_info`, not
`vcs_info`. Editable directory metadata still protects its source; separate
`.pth`, symlinks and launchers remain runtime links regardless of the origin
record. Ambiguous or malformed metadata and unknown executable hooks remain
unresolved. Static checks
exclude only metadata that the exact removal will discard: retained locks,
their ancestors and environment skeletons remain observable. Process checks
still cover the whole owner. Busy, changed or unreadable candidates are local
skips, not permission to stop work, kill applications, force locks or retry until
they disappear.

## Read the scan and bind the selection

`inspect` returns a default page and `next_cursor`; use `--scan`, `--cursor` and
`--limit` to read the rest without a new scan. Pagination limits the displayed
page, not discovery coverage. If a report budget leaves coverage incomplete,
inspect smaller exact candidates with `--only-candidates`, keeping their whole
owner root, rather than treating omitted material as checked. Read sizes from
`inspect` responses, where `measurement` holds them: a filesystem candidate in
the raw saved scan has no `measurement` and keeps its sizes under `snapshot`, so
a script that reads `measurement` from the file finds nothing and can report
zero. `--candidate` returns a selection template. Fill it with evidence and a
reconstruction recipe; several IDs may share one qualification where their
owner, inputs, retention and consumers are the same. Separate exceptions. The
selection format is:

```json
{
  "schema_version": 1,
  "groups": [{
    "ids": ["<candidate-id>"],
    "reason": "<why these exact objects are reconstructible and not retained or consumed>",
    "reconstruction": "<retained inputs and exact rebuild or redownload route>",
    "evidence_paths": ["<absolute guide, manifest, lock or owner evidence file>"],
    "consumer_roots": ["<absolute installed-consumer metadata directory or file>"]
  }]
}
```

Review the resulting exact paths, exclusions, recipes and native dynamic scopes
against the scope the user authorized. Resolve a consequential scope choice once
per family, not once per file. A confirmed digest binds the plan; it is not a
substitute for authority. `inspect`/`plan` do not remove target data; the plan
binds helper bytes, object preimages and reconstruction evidence. Changed inputs
need a fresh inspection and plan, not an edited digest.

Evidence files are hashed in bounded-memory chunks without a file-size cutoff;
bind a large retained input directly, not a separate note containing its hash.
Consumer traversal deduplicates overlapping roots and does not spend metadata
allowance on ordinary source files or directories. The separate allowance of
20,000 actual metadata bindings remains fail-closed: `consumer_coverage` reports
each supplied root, what was visited and any omitted metadata. Continue with a
relevant narrower scope when that check is incomplete; do not call it covered.

## Python environment payloads

For a Python virtual environment, the default candidate is its distribution
payload: packages, matching metadata and recorded entry points together.
Keep the environment root, interpreter links, activation skeleton, `pyvenv.cfg`,
bootstrap distributions and persistent locks. The helper inventories RECORDs,
rejects escapes and unknown/mixed payloads, checks supported lock versions, and
holds an existing cooperative `.lock` without replacing its inode. It never
imports the environment or runs its package tools.

An environment after payload removal **requires synchronization before use**.
Record the recipe; do not refill it immediately just to prove removal. Test a
representative reconstruction in a disposable copy when that uncertainty
changes qualification. Whole-environment retirement is a different owner
decision, not a fallback when payload qualification fails.

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
