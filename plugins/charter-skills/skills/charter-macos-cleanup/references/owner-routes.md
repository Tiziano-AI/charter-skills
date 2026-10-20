# Native owner routes

Open this before selecting a native store or engine. The helper performs only
non-bootstrapping reads during discovery, then repeats identity/configuration
checks before submitting an effect. It binds actual executables, qualified
contracts, effective destinations and relevant environment settings. The
helper owns compatibility admission; an unsupported contract needs
source-qualified adapter maintenance, not a guessed command or an edited plan.
Native stores are never edited through filesystem fallbacks.

The qualified Homebrew Container wrapper binds its interpreter, native
executable and installation root while retaining the public invocation.
OrbStack's Docker multicall entrypoint likewise retains its invocation name
while binding the resolved executable; calling the resolved binary by another
name would select a different operation.

`inspect --owner <owner> [--target <target>] --output <new-scan.json>` returns a
dynamic operation candidate, including every destination it can affect. Use
the ordinary selection/plan process; package caches also require bounded
installed-consumer metadata scopes and a fresh activity check. The helper
does not install an owner, start an engine or connect to a remote endpoint.

| Owner | Target and effect |
| --- | --- |
| `npm` | Optional cache directory; otherwise resolved effective cache. Removes its entire `_cacache`, preserving `_npx` and installed tools. Native `--force` is npm's required confirmation, not a helper bypass. |
| `uv` | Optional cache directory; otherwise `uv cache dir`. Prunes unused entries with native in-use protection; never passes force. |
| `pnpm` | Optional store directory on macOS. Sequential operation covers expired dlx cache, the selected package store, then abandoned private package-manager/runtime installs in the effective engine store. |
| `apple-buildkit` | Exact running container ID; defaults to `buildkit`. Uses the bound local guest Unix endpoint and unused private-cache policy. |
| `orbstack-buildx` | Exact existing builder name; defaults to `orbstack`. Every node must already run on an identified local OrbStack engine. Prunes unused private cache across those nodes. |
| `apple-container` | Required exact running container ID. Reclaim: trim writable root and every writable block/volume mount, including named volumes. Skips read-only and VirtioFS mounts. |
| `orbstack` | Observation-only reclaim of automatic sparse recovery; no compaction, trim, restart or reset command. |

## Package caches

npm `cache verify` performs garbage collection, and `cache clean --force`
does not honor dry-run as a nonmutating preview. The helper discovers
configuration without either. `_npx` is a separate executable cache with its
own consumer/retention problem; this route does not remove it.

uv's cache is versioned native storage. Native prune owns its locks and entry
semantics. Do not walk its internals with a raw removal plan. A project dry-run
may still create temporary cache material; it is not a machine-wide read-only
test. A venv's advisory lock coordinates participating installers, not every
Python runtime, and failure to acquire that lock is not a way around consumers.

pnpm's `store prune` has no qualified per-phase selector or dry-run. Its store
override bounds only the middle phase, not dlx or private engine installation
cleanup. If authority covers only the package store, retain this candidate
rather than invoking the wider operation. A failed command may already have
completed an earlier phase. The plan shows all effective paths.

## Private BuildKit cache

Private means not shared with other engine resources; it does **not** mean
owned by one project. Describe an engine-wide unused-private-cache request as
such. These adapters do not prune images, containers or volumes, and they do
not use disk-pressure flags that can trigger a build RPC during inspection.
The native policy may select different unused records between inspection and
execution; the engine applies that policy under its own concurrency semantics.

Buildx locality is established from local builder/context metadata before
daemon-facing reads. `buildx ls` can probe unrelated remote builders and is not
used for that discovery. A client dependency tag is not a measured server
version. The adapter records actual reported node/engine identity and preserves
the qualified filter spelling. The helper offers a bounded policy, not
individual cache-record-ID deletion.

## Reclaim and uncertain execution

Apple `clean` frees already-unused guest blocks; it does not remove files.
There is no per-mount selection. Qualify every writable block mount, not just
the root filesystem. Its acknowledgement does not contain reclaimed byte
counts. The helper reports available host backing information separately;
root backing allocation may be unavailable through the public inspect output.

Apple and Buildx calls can lose their response after submission. A dead CLI
process or a smaller disk image does not establish that a service request has
ended. The claim remains until a route-specific readback proves termination;
where available, the original runtime/container incarnation ending provides
that boundary. Do not restart an engine to manufacture this evidence.

OrbStack shares a VM among engines and machines. Its large sparse logical size
is not host allocation. The observation route never treats an unchanged
allocation as permission for raw guest `fstrim`, backing-file editing or a reset.
The installed owner's `data/README.txt` identifies the current backing file as
`~/Library/Group Containers/HUAQ24HBR6.dev.orbstack/data/data.img.raw`;
the web FAQ's shorter `data.img` name does not override that local contract.

## Contract sources

- [npm cache implementation](https://github.com/npm/cli/blob/v11.19.0/lib/commands/cache.js)
- [uv cache semantics](https://docs.astral.sh/uv/concepts/cache/) and [sync lock behavior](https://github.com/astral-sh/uv/blob/0.12.23/crates/uv/src/commands/project/sync.rs)
- [pnpm prune phases](https://github.com/pnpm/pnpm/blob/v12.9.1/pnpm/crates/cli/src/cli_args/store.rs) and [engine store](https://github.com/pnpm/pnpm/blob/v12.9.1/pnpm/crates/cli/src/engine_pm/install.rs)
- [Buildx prune](https://github.com/docker/buildx/blob/v0.33.0/commands/prune.go), [BuildKit prune](https://github.com/moby/buildkit/blob/v0.26.2/cmd/buildctl/prune.go)
- [Container clean command](https://github.com/apple/container/blob/1.5.0/Sources/ContainerCommands/Container/ContainerClean.swift) and [runtime trim](https://github.com/apple/container/blob/1.5.0/Sources/Services/RuntimeLinux/Server/RuntimeService.swift)
- [OrbStack sparse storage](https://docs.orbstack.dev/faq#why-is-there-an-8-tb-data-file) and [shared VM](https://docs.orbstack.dev/architecture)
