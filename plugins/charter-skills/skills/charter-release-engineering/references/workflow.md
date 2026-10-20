# Installed Release Path

Use this when a change must reach a package, command, app, plugin, feed, materialized directory, or
other installed consumer. The symptom is usually the same, the consumer still behaves the old way,
and each cause has its own repair.

## Where installed delivery fails

- **No release contains the change.** A fix merged to the default branch is not what a Homebrew
  tap, registry, feed, or plugin marketplace serves; the channel still points at the previous tag
  or version. Cut a release that contains the change, update the channel to it, and check that the
  channel's metadata (formula URL and checksum, feed entry, marketplace version) names the new
  artifact.
- **The artifact lacks what the source tree supplied.** A launcher imports the checkout, a
  template, schema, migration, or certificate is read relative to the working directory, a
  generated member is stale, or an executable the command calls is undeclared. Include resources
  through the runtime's packaging mechanism, resolve them relative to the installed package or an
  explicit data root, and exercise from a clean shell (below).
- **Another copy is selected.** `PATH` order (`~/.local/bin` ahead of a package manager's bin), a
  second app bundle, a plugin cache, an older marketplace entry, or an update channel can resolve
  an older copy. List every candidate the consumer can resolve (`which -a <tool>`, the path the
  loader reports), identify the intended install for this consumer and repair its selection.
  Deliberately separate versions or profiles need not be removed. Remove or deprioritize an
  unintended shadow only when that change is in scope.
- **The running process predates the install.** A daemon, LaunchAgent, app, or host session keeps
  the code and definitions it loaded at start until it restarts or reloads. Restart that exact
  process and confirm the new process identity.
- **The platform rejects the right bytes.** Signing, notarization, permissions, or ownership changed
  by the installer can block or alter a correct artifact.
- **The version is already spent.** Registries keep published versions immutable. npm never lets a
  `package@version` be used again, even after unpublishing, and PyPI rejects a filename it has seen
  before. Repair by publishing a new version; mark the bad one with `npm deprecate`, or yank it on
  PyPI so installers ignore it unless a specifier pins exactly that version.

Prefer an already accepted immutable artifact when it has the right source, configuration,
platform, and channel eligibility; build when the candidate does not exist or a material input
changed. Keep unrelated worktree state out of the candidate.

## Choose an install shape

Common shapes are a single native binary, a package-manager-installed executable, an isolated
Python application environment, a repository-local command for a repo-owned tool, an app bundle
with a command-line bridge, and a container image for environment-dependent operation. Choose from
startup latency, dependency size, platform support, upgrade needs, signing, filesystem access, and
how callers discover the command. A stable operator command should not require a global development
toolchain unless developers are its actual audience.

Installation can change shell lookup, file ownership, signatures, permissions, service lifecycle,
and upgrade channels. A command that works only through a repository wrapper is a development
surface; call it that rather than presenting it as installed.

## Exercise from a clean shell

From outside the source checkout and without inherited development-path shortcuts:

```bash
which -a <tool>
<tool> --version
<tool> --help
```

Then run the smallest representative operation that reads each required resource class, offline,
on a fixture, or locally where the product allows it. Use the product's actual diagnostic
semantics: a command named `doctor` that starts a service or contacts a provider has those effects
in a smoke sequence too. This exposes source-tree imports, missing packaged resources, undeclared
executables, wrong `PATH` precedence, and configuration resolved against the repository.

## Upgrade and removal

Define how an upgrade treats configuration, caches, durable jobs, plugins, database schemas, and
running services, and separate forward-compatible state migration from replacing the executable. A
failed upgrade should leave either the prior working install or a clear recovery state, not a mixed
set of launcher and libraries.

Removal distinguishes the executable from user configuration, caches, logs, credential references,
and durable product data. Uninstalling does not silently delete user-owned state.

## Record what recovery needs

For one direct release, the source or artifact identity, the exact destination, the consumer
result, and the recovery target are enough. The recovery target names the previous version or
artifact, the mechanism that returns consumers to it (reinstall, channel reversal, disablement,
configuration or data restore), and which schema, data, cache, configuration, credential, client,
or external state will not revert with the code. Release notes, examples, help, and update metadata
change with the release when they are how the consumer finds the changed behavior: the user-visible
change, any compatibility or migration step, and known limitations.

When several artifacts, channels, or targets make identity hard to keep, use the
[lineage chain](lineage-chain.md).
