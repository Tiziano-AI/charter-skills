---
name: charter-release-engineering
description: Release, deploy or install an exact change so the installed or hosted
  consumer actually runs it; resolve artifact and target identity, runtime selection,
  compatibility, cutover and recovery. Source readiness alone is not delivery.
metadata:
  content_version: charter-release-engineering@2026.10.16.0
---
# Charter · Release Engineering

A release changes which behavior a consumer receives. Building bytes, making
them eligible for selection and the consumer actually selecting them are
separate steps; the release is done when the intended user action runs the
change at its destination. Start from that action.

## Defaults

**Confirm which copy the consumer selects before reinstalling anything.** Read
what the consumer actually resolves: `which -a <tool>` and `<tool> --version`,
the path a plugin loader or launcher reports, the revision a route serves. When
another copy shadows the intended one, repair selection for this consumer.
Keep deliberately separate versions, accounts or profiles separate; remove or
deprioritize an unintended shadow only within the release's authority.
Upgrading or reinstalling the shadowing copy from source leaves two live
installs and can ship unreleased code.

**Stage only what cannot move with the change.** When state is disposable and
every consumer changes together, as in an unreleased product with recreatable
stores, replace the old shape outright. When a population cannot move at once
(released clients, persisted rows, queued work, a rollback target that must
read new data), expand before you contract as
`charter-cross-layer-change-design` stages it, and remove the old shape once
nothing still needs it.

**Mitigate before you roll back.** When a release misbehaves, first stop the
harm with the cheapest reversible lever: turn the feature flag off, halt the
rollout, take the failing path out of service. Roll back when the previous
version still reads current data, serves current clients and does not
reintroduce a vulnerability the release fixed; diagnose after service is
restored. When state has moved on, contain the failing path and repair
forward.

When the only consumer runs straight from the source tree, such as a
LaunchAgent that starts `uv run --project <checkout>`, and the change needs no
build, generated artifact or state transition, there is no package to publish.
Reload or restart that exact consumer if it captures the changed code, confirm
the new process or reload, and exercise the changed behavior. A source-backed
launcher does not by itself make persistent state disposable or eliminate
other consumers.

## Bytes, selection and state

Three questions often diverge:
- Which source and build inputs produced the artifact?
- Which artifact does this installer, route or runtime select?
- Which state and other versions must remain compatible with it?

This model localizes failures. If candidate bytes are absent from the package,
repair packaging. If they are installed but a launcher resolves another path,
repair selection. If the intended process is running but rejects existing data,
repair compatibility. Rebuilding addresses only the first class and can
introduce new dependency variation while leaving the others intact. Promoting
an accepted immutable artifact is not rebuilding, and is usually the better
move.

The same symptom, "the consumer still behaves the old way", has several
causes: a merged fix that no release contains while the channel still serves
the previous version, an installed file that differs from an already-running
process, a healthy deployment that receives no traffic, a plugin cache or
update channel that selects an older release.

Resolve the exact account, project, environment, install root, executable or
route before a live transition. Friendly names and ambient context are weak
substitutes when several targets exist.

## Compatibility decides order and recovery

Use the product-owned build, package, install, materialize or deploy
mechanism, and move canonical inputs before generated targets. An atomic local
replacement may be simple; a rolling deployment has old and new readers and
writers at once. Ask which reader can consume which writer's output. An
overlap of old and new shapes does not make a destructive normalization
reversible.

Data migrations, queued messages, cache formats and clients can prevent
rollback even when the old binary is available. If new code has emitted values
the old version cannot interpret, route reversal may intensify the failure.

Exposure strategy trades the cost of discovering a defect against the cost of
operating mixed versions. A canary helps when a small cohort gives an early,
release-correlated signal against a control group on the old version, and
reversal is possible. It teaches little for a rare weekly job before that job
runs, and it can create incompatibility that a brief atomic replacement would
avoid. Choose the observation window from the failure mechanism and ordinary
traffic, not a ceremonial soak time.

Infrastructure health detects process and dependency failures; a
representative consumer action detects whether the changed capability survived
selection, configuration and data. Run that action as soon as it is reachable,
and read intermediate states when they explain a mismatch.

## Depth

- [Installed release path](references/workflow.md) when a change must reach a
  package, command, app, plugin or feed: where installed delivery fails, install
  shape, clean-shell exercise, upgrade and removal, published versions.
- [Lineage](references/lineage-chain.md) when several artifacts, channels or
  targets make it unclear which source a consumer runs.
- [Hosted targets](references/hosted/context-resolution.md) before a deploy
  whose account, service or route is not pinned.
- [Hosted diagnostics](references/hosted/evidence-and-diagnostics.md) for a
  release-correlated failure at a hosted target.
- [Hosted operations](references/hosted/operation-workflows.md) for cutover
  patterns, schema migration, quiesced versus live-write backfills, mitigation
  and rollback.

A failed consumer action outweighs a successful deployment receipt for
readiness; it does not erase the deployment effect that recovery must now
handle.
