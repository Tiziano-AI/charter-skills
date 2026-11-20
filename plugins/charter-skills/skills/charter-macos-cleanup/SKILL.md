---
name: charter-macos-cleanup
description: 'Mac disk cleanup: remove rebuildable caches, dependencies and build
  outputs without breaking active or source-linked consumers; reclaim already-free
  container storage. Not duplicates, models, histories, installed tools or data retirement.'
metadata:
  content_version: charter-macos-cleanup@2026.11.20.0
---
# Charter · macOS Cleanup

Reclaim disk space from redownloadable caches or rebuildable development
outputs. If a prior removal or prune lost its receipt, inspect the original
operation with `status`; do not resubmit. For new work distinguish exact
filesystem removal, native pruning (the owner selects entries under its policy)
and reclaim of already-free container blocks. These are different effects.

Keep source code, Git/worktrees, installed apps/tools/runtimes, models, agent
histories, correspondence, databases, recovery material and retained test or
release evidence. Duplicates need a survivor and recovery decision; installed
tools have their own retirement route. Cache cleanup does not retire images,
containers, volumes, virtual machines or environments.

## Establish what can actually be discarded

Start from the requested families, their actual owners and existing bounded
inventory. A name like `DerivedData` says nothing about an accepted baseline
inside it. A lockfile identifies inputs but does not prove local or editable
dependencies can be rebuilt. Before selecting anything, establish:

- **Reconstruction:** the retained inputs, required toolchain and exact
  rebuild or redownload route. Split mixed trees; keep authored files and
  retained evidence.
- **Retention:** the owner's intent for these exact objects, within the
  cleanup requested. A guide does not widen that scope.
- **Consumers:** inspect the whole owner for active writers and relevant
  installed metadata for lazy consumers: an idle launcher can still depend
  on the checkout. An empty unrelated metadata root proves nothing. Never
  execute inspected hooks to resolve ambiguity. A busy, changed, unreadable
  or insufficiently covered candidate is a local skip, not grounds to kill
  work or force a lock.

Before choosing inspection roots, read [candidate qualification](references/storage-and-recovery.md#qualify-the-candidates-and-their-consumers):
it distinguishes exact outputs from whole project and consumer boundaries,
provenance records from runtime links, and payloads from retained locks.
Use a saved scan rather than repeatedly traversing the home. Keep incomplete
coverage visible; an omitted path was not checked.

If the pressure is on unified memory or thermals rather than disk, give the
symptom to `charter-system-and-mac-diagnosis`; nothing has qualified for
removal. When the problem is finding material the owner intends to keep,
`charter-archive-reorganization` starts with retrieval and provenance.

## Use the packaged helper

Resolve `scripts/macos_cleanup.py` from this SKILL.md. Run
`python3 -I <absolute-script-path>` with an existing interpreter outside the
candidates. The standard-library helper checks interpreter support, writes no
bytecode and installs nothing. Read command help for syntax; other results
are JSON only on stdout. There is no force or raw-command fallback.

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

Read [the scan and selection contract](references/storage-and-recovery.md#read-the-scan-and-bind-the-selection)
before preparing a plan. A page is not a scan; inspect the remaining pages
through the saved cursor. Sizes in `inspect` results and raw snapshots occupy
different fields. Use the candidate's template to record the exact IDs, why
they qualify, the reconstruction route, evidence paths and consumer roots.
Review exact paths, exclusions, qualifications and any dynamic native scope
against the commission. A confirmed digest binds helper bytes, preimages and
evidence; it never grants authority. Changed inputs need fresh inspection
and planning, not an edited digest.

For a native store read [owner routes](references/owner-routes.md) **before
selection**: uv prune can remove environments, and pnpm reaches three
destinations even when a target names one store. Do not remove native stores
through a filesystem plan. Unsupported operations remain findings for their
family; never downgrade a tool, edit a plan or guess a raw command.

## Preserve environments, act on payloads

Before qualifying a virtual environment, read the [payload rules](references/storage-and-recovery.md#python-environment-payloads).
Select distributions, their metadata and recorded entry points together,
keeping the root, interpreter, activation skeleton, bootstrap distributions
and persistent locks. The environment requires synchronization before use:
record the recipe rather than immediately refilling it. Whole-environment
retirement is not a fallback for failed qualification.

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

For a separately requested container reclaim, [qualify the owner's actual
mount scope](references/owner-routes.md#reclaim-and-uncertain-execution);
Apple Container trim is not file cleanup and OrbStack observation is not a
compaction command.

Account for the entire request with `request_coverage`; a
`result_scope: selected_plan` result covers only selected objects. Distinguish
removed, retained, skipped, unsupported, partial and unresolved families;
give reasons and recipes to resume use. A refusal is not retention, and
finished status or zero open claims does not prove success.

Keep logical size, inode-deduplicated allocation, owner-reported cache bytes and
host free-space changes distinct. APFS clones, snapshots and concurrent work
prevent exact attribution from a simple delta. Do not claim host recovery from
a guest trim acknowledgement alone.
