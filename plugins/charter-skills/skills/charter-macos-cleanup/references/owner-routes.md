# Native owner routes

Open this before selecting a native store or engine. The helper performs local,
non-bootstrapping discovery, then revalidates the operation before submission.
Upstream owns native entry selection, locking and prune implementation; the
helper binds authorized scope, command and destination identity, submission
custody and results. Native stores are never edited through filesystem fallbacks.

Admission depends on supported options, effective configuration, required
semantic output and bounded effect scope. Additive output fields need not change
that contract; missing or ambiguous safety-critical fields can. Release numbers
are observations, with version conditions only for evidenced feature or
incompatibility boundaries. Documentation, source where semantics are
undocumented, and real-owner integration establish the adapter's behavior during
development. Help text alone cannot establish destructive semantics, but ordinary
cleanup does not require a fresh source audit. A refusal must identify the
unsupported capability, output, target or scope rather than a release mismatch.

Inspect-to-execute checks are separate from compatibility admission. They bind
the observed version, executable/interpreter/wrapper identities, configuration,
environment, endpoints, destinations, nodes and policy. npm also depends on its
installed implementation modules and package configuration, not just its small
launcher and Node interpreter. Read the recorded identity checks accurately;
path/stat identity is not a universal byte-hash guarantee. Retain public
invocation spelling: the Homebrew Container wrapper supplies an installation
root, and OrbStack's Docker multicall entrypoint dispatches by its invocation
name. Calling only a resolved binary can change the operation.

`inspect --owner <owner> [--target <target>] --output <new-scan.json>` returns a
dynamic operation candidate, including every destination it can affect. Use
the ordinary selection/plan process, qualifying consumers against the native
protection actually available. The helper does not install an owner, start an
engine or connect to a remote endpoint. Expected failures remain inspectable
findings alongside usable candidates.

| Owner | Target and effect |
| --- | --- |
| `npm` | Optional cache directory; otherwise resolved effective cache. Removes its entire `_cacache`, preserving `_npx` and installed tools. Native `--force` is npm's required confirmation, not a helper bypass. |
| `uv` | Optional persistent cache directory; otherwise its effective cache. Prune can include centralized project and temporary build environments, not only unused downloads. Excluded environment removal must be prevented by a supported selector or reported as a scope conflict. |
| `pnpm` | Optional store directory on macOS. Sequential operation covers expired dlx cache, the selected package store, then abandoned private package-manager/runtime installs in the effective engine store. |
| `apple-buildkit` | Exact running container ID; defaults to `buildkit`. Uses the bound local guest Unix endpoint and unused private-cache policy. |
| `orbstack-buildx` | Exact existing builder name; defaults to `orbstack`. Every node must already run on an identified local OrbStack engine. Prunes unused private cache across those nodes. |
| `apple-container` | Required exact running container ID. Reclaim: trim writable root and every writable block/volume mount, including named volumes. Skips read-only and VirtioFS mounts. |
| `orbstack` | Observation-only reclaim of automatic sparse recovery; no compaction, trim, restart or reset command. |

## Package caches

npm `cache verify` performs garbage collection, and `cache clean --force`
does not honor dry-run as a nonmutating preview. Resolve effective configuration
and any explicit cache override without either. Clean has no cooperative in-use
lock, so targeted activity and source/cache-linked consumer checks matter.
`_npx` is a separate executable cache with its own consumer/retention problem;
this route does not remove it.

uv's cache is versioned native storage. Its exclusive prune lock coordinates
participating uv commands, not arbitrary Python consumers of source or symlinked
cache paths. The native environment-removal scope cannot silently become
authority to retire environments, installed tools or Python runtimes. A cache
directory override alone does not narrow prune to downloads. Never substitute
whole-cache removal, raw bucket deletion or forced locks.

`UV_NO_CACHE` can override even an explicit directory and cause temporary-cache
creation. With caching disabled and no exact persistent target, report the
configuration without calling `cache dir`. An explicit persistent target needs
a bound child-only environment that really selects it; do not change workstation
configuration. The route does not pass `--ci`; the helper's `CI=1` does not select
that different prune policy. A project dry-run may also create cache material
and is not a machine-wide read-only preview.

pnpm's `store prune` covers expired dlx entries, the package store and abandoned
private package-manager/runtime installs, in that order. Its store override
bounds only the middle phase; there is no supported per-phase selector or
nonmutating dry-run for this route. Resolve every destination from pnpm's actual
configuration precedence and native layout, not npm's configuration or remembered
private paths. If authority covers only the package store, retain the wider
candidate. Private-install in-use locking and package reference protection do
not establish that an expired dlx entry is idle: keep live-dlx checks. A later
phase failure may leave earlier effects; report partial work rather than replay.
The passive reader still reports static references into the store. Positively
missing targets are recorded as dangling references, not consumers of existing
payloads; access errors do not establish absence. Existing references, process
activity and incomplete visibility remain blocking. Do not delete or repair
installed wrappers as part of cache cleanup.

## Private BuildKit cache

Private means not shared with other engine resources; it does **not** mean
owned by one project. Describe an engine-wide unused-private-cache request as
such. These adapters do not prune images, containers or volumes, and they do
not use disk-pressure flags that can trigger a build RPC during inspection.
The native policy may select different unused records between inspection and
execution; the engine applies that policy under its own concurrency semantics.

For Apple Container, bind the already-running API/runtime route and exact
container creation/start incarnation, not just the host CLI version. `system
version` can fall back to CLI-only information; that does not identify the
server. Guest buildctl's client version is separate from the BuildKit daemon's
Info. DU's JSON array and prune's per-record NDJSON are different output
contracts. A measurement parse failure does not undo established completion.

Buildx locality is established for every node from local builder/context
metadata before daemon-facing reads. `buildx ls` can probe unrelated remote
builders and is not used for discovery. Bind the actual plugin, endpoints and
server/node identities. A client dependency tag is not a server version, and a
Docker-driver display can derive a BuildKit value from Docker Engine rather
than daemon Info. Preserve the `private=""` selector, no `--all`, and no
disk-pressure flags. Native confirmation suppression does not bypass reference
protection. The helper offers a bounded policy, not cache-record-ID deletion.

## Reclaim and uncertain execution

Apple `clean` frees already-unused guest blocks; it does not remove files.
There is no per-mount selection. Qualify every writable block mount, not just
the root filesystem. Its acknowledgement does not contain reclaimed byte
counts. The helper reports available host backing information separately;
root backing allocation may be unavailable through the public inspect output.

Apple and Buildx calls can lose their response after submission. A dead CLI
process or a smaller disk image does not establish that a service request ended.
Use the original route's readback and retain custody until it proves termination;
see [storage and recovery](storage-and-recovery.md). Do not restart an engine to
manufacture this evidence.

OrbStack sparse recovery is measurement, not admission to a destructive command.
It needs the actual vendor-owned backing location and permitted access, not
equality with an examined release. Identify that location from the installed
owner's storage contract; a web example's filename is not a substitute. Respect
OS access denial. OrbStack shares a VM among engines and machines, so its large
sparse logical size is neither host allocation nor one engine's reclaimable
bytes. Unchanged allocation does not justify guest `fstrim`, compaction,
backing-file editing, restart or reset.

## Owner documentation

- [npm cache contract](https://docs.npmjs.com/cli/v11/commands/npm-cache/)
- [uv cache semantics](https://docs.astral.sh/uv/concepts/cache/)
- [OrbStack sparse storage](https://docs.orbstack.dev/faq#why-is-there-an-8-tb-data-file) and [shared VM](https://docs.orbstack.dev/architecture)
