# Charter · Mac Cleanup

Recover Mac storage from redownloadable caches and rebuildable development
material. Remove what qualifies and retain what does not; a report that skips
everything has not achieved a cleanup. The package supplies one inventory,
exact plans, guarded removal, native owner routes and shared operation custody.
Your contribution is establishing reconstructibility, retention and consumers.

The two ordinary layers are download/tool caches and repository dependencies or
outputs. Container reclaim is a separate operation on already-free guest blocks.
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
Use the helper's saved scan for subsequent inspection. Discovery recognizes
metadata relationships; `--candidate-path` admits unfamiliar output layouts for
qualification, not deletion by name. Application download caches need their
owner's redownload route; arbitrary `Library/Caches` trees are not disposable
just because of their location.

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
  extension registration locations); explain why those scopes cover this family.
  An empty unrelated directory does not establish absence of consumers.

The helper checks process arguments, working directories, descriptors and those
bounded static consumer scopes freshly before each candidate. It reports
incomplete visibility or executable metadata instead of evaluating it. Busy,
changed or unreadable candidates are local skips, not permission to stop work,
kill applications, force locks or retry until they disappear.

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
`--limit` to read the rest without a new scan. `--candidate` returns a selection
template. Fill it with evidence and a reconstruction recipe; several IDs may
share one qualification where their owner, inputs, retention and consumers are
the same. Separate exceptions. The selection format is:

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

Native stores use `inspect --owner <owner> [--target <exact-target>] --output
<scan.json>`. **Read [owner routes](references/owner-routes.md) before a native
selection**: a native prune binds a store and policy, not a frozen file list.
In particular, pnpm reaches three stores even when `--target` selects one.

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

Report removed, retained/skipped, partial and unresolved families with the
recipe needed to resume use. Keep logical size, inode-deduplicated allocation,
owner-reported cache bytes and host free-space changes distinct. APFS clones,
snapshots and concurrent work prevent exact attribution from a simple delta.
Do not claim host recovery from a guest trim acknowledgement alone.
