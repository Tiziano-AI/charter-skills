# Charter · Mac Cleanup

Recover Mac storage from redownloadable caches and rebuildable development
material, preserving active and retained work. The helper owns bounded discovery,
exact plans, guarded filesystem removal, native cache operations and shared
operation custody. Establish reconstructibility, retention and consumers, then
report what happened across the requested families, not just the selected batch.

The two ordinary layers are download/tool caches and repository dependencies or
outputs. Filesystem removal selects exact payloads; a native prune selects a
store and policy whose entries the owner chooses at execution. Container reclaim
is a separate operation on already-free guest blocks.
Source code, Git/worktrees, installed apps/tools/runtimes, models, agent histories,
correspondence, databases, recovery material and retained test/release evidence
are outside this package. Duplicate selection needs its own byte-identity,
survivor and recovery decisions; installed-tool retirement follows that tool's
own operating guide. Do not use cache cleanup to retire images, containers,
volumes, virtual machines or environments.

## Establish what can actually be discarded

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

## Use the packaged helper

Resolve `scripts/macos_cleanup.py` relative to this SKILL.md. Run it with an
existing Python interpreter outside the candidates, using
`python3 -I <absolute-script-path>`. The helper checks interpreter support and
reports an unmet requirement before admitting an operation. It uses only the
standard library, writes no bytecode and installs nothing. `--help` and each
command's `--help` describe the protocol. All results except help are JSON;
stdout never mixes diagnostics with a result. There is no `--force` or
raw-command route.

Store scan, selection, plan and operation files in an existing private working
directory outside the cleanup targets. Paths must be absolute and canonical;
on macOS `/tmp` is a symlink, so use its real `/private/tmp` destination when
working with disposable fixtures. Output files are create-new, mode 0600.

```text
python3 -I <script> inspect --root <repository-parent> --include-caches --output <scan.json>
python3 -I <script> inspect --scan <scan.json> --candidate <candidate-id>
python3 -I <script> plan --scan <scan.json> --selection <selection.json> --output <plan.json>
python3 -I <script> clean --plan <plan.json> --confirm-digest <digest> --operation <operation.json>
python3 -I <script> status --operation <operation.json>
```

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

Native stores use `inspect --owner <owner> [--target <exact-target>] --output
<scan.json>`. Repeat `--owner` for several families; `--target` requires a single
owner. Expected refusals remain visible in `native_findings`, not selectable as
cleanup candidates. **Read [owner routes](references/owner-routes.md) before a
native selection**: uv prune can remove environments, and pnpm reaches three
destinations even when `--target` selects one store. Keep native stores out of
filesystem removal plans.

Native compatibility depends on the operation's capabilities, effective scope
and interpretable output, not equality with one examined release. The observed
version and command identities still belong to the plan: a change after
inspection requires fresh inspection and planning. A genuine unsupported
capability or scope remains a finding for that family while other authorized
work continues; do not downgrade tools, edit a plan or guess a raw command.

## Preserve environments, act on payloads

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

## Interpret effects and recover

Read [storage and recovery](references/storage-and-recovery.md) before executing
or recovering a batch. Filesystem removal requires a successful disposable test
of the running macOS kernel's guarded unlink behavior. It does not downgrade to
ordinary recursive deletion on an unsupported system. Open regular files are
protected at unlink; directory handles and future lazy consumers are not.
Preimage checking and unlink are separate syscalls, so do not claim an atomic
transaction or safety against a hostile concurrent writer.

Keep the operation report. On interruption or an uncertain native result, run
`status`, without a path if necessary to discover shared retained claims.
Changing the operation filename or invoking another materialized package copy
does not bypass custody. `execution_unresolved` means further effects may still
occur: never replay. Unknown byte attribution after established completion does
not keep the resource blocked. Status can persist an owner's completion
readback; it never submits cleanup again.

For requested reclaim, inspect the exact owner separately, use `plan --kind
reclaim`, then `reclaim` with its own digest and operation file. Cleanup does not
imply authority to trim every writable container mount. Apple Container trim is
online and does not start stopped containers. OrbStack's route observes its
automatic sparse recovery and sends no unsupported compaction command.

Use `request_coverage` to account for requested families, including unselected,
retained and refused work. A result marked `result_scope: selected_plan` covers
that selection, not the entire request. Report removed, genuinely retained,
skipped, unsupported, partial and unresolved families, with reasons and any
recipe needed to resume use. An unsupported family remains a tool limitation,
not a retention decision. A completed status observation or zero open claims is
not evidence that cleanup succeeded.

Keep logical size, inode-deduplicated allocation, owner-reported cache bytes and
host free-space changes distinct. APFS clones, snapshots and concurrent work
prevent exact attribution from a simple delta. Do not claim host recovery from
a guest trim acknowledgement alone.
