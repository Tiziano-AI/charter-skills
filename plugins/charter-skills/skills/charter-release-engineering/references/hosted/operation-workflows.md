# Hosted Release Operations

Use this when a hosted release needs cutover, migration, mitigation, rollback, or mixed-version
sequencing beyond a direct deployment.

## Deploy and promote

1. Resolve the accepted source or immutable artifact and the exact target.
2. Read the currently routed revision; it is the recovery target and may not be the latest deploy.
3. Deploy or promote through the provider-supported path.
4. Exercise the consumer route as soon as it is eligible.
5. Retain the deployment or revision and traffic identity needed for recovery.

Prefer promotion of one immutable artifact when environments are intended to run identical bytes.
If the platform rebuilds per environment, record the resulting digest and configuration difference.

## Cutover patterns

- **rolling:** replace instances gradually; requires mixed-version compatibility and capacity
  during turnover.
- **blue/green:** prepare a parallel environment and switch traffic; requires state and migration
  compatibility plus a tested route reversal.
- **canary:** expose a small cohort or traffic share; requires release-correlated signals compared
  against a control cohort on the old version, and a window that covers the work the change
  touches. Keep unrelated changes out of a comparison when their effects cannot be separated;
  independent canaries with distinct consumers and attributable signals need not be serialized.
- **feature flag:** deploy the code with the behavior off and enable it by cohort; this separates
  exposure from deployment and gives a fast off-switch, but only for the path the flag actually
  gates.
- **phased channel:** publish to preview, beta, or update cohorts; requires channel identity,
  adoption visibility, and client compatibility.
- **instant replacement:** appropriate only when blast radius is small or the system is safely
  stateless and recovery is fast.

Set thresholds and abort behavior before increasing exposure. A direct low-consequence replacement
needs no canary protocol.

## Configuration changes

Treat runtime variables, domains, build/start commands, resources, networking, and service bindings
as part of the release when they change consumer behavior. Capture the current provider-visible
state, identify affected processes and restart semantics, apply through the owning provider path,
and observe the consumer behavior controlled by the setting.

Write-only values may not be readable after change; use provider metadata and a consuming behavior
for the aspects they can establish rather than assuming parity from operation acceptance.

## Schema and data migration

When all state is disposable and every consumer changes at once, replace the
shape outright. Otherwise, the sequence below preserves an interval in which
old and new consumers can coexist. Its ordering has a concrete reason:
changing writers before readers can accept their values creates incompatible
stored data; removing old support before delayed consumers disappear turns
rollback or queue replay into failure.

1. expand schema or data shape so old and new code can coexist;
2. deploy readers/writers that tolerate both shapes;
3. backfill or migrate with resumable identity and progress;
4. cut consumers to the new behavior;
5. contract the old shape only after incompatible consumers are absent.

An expansion that is never contracted leaves both shapes alive, and every later change pays for
them.

### Backfill progress is not write ordering

A resumable cursor says which records the job has visited. It does not keep a
late backfill write from replacing a newer application value. Suppose a copy
reads address A at source revision 7; a live request changes it to B at revision
8 and updates the new representation; the copy then writes A into that
representation and advances its cursor. Every record can be marked processed
while the consumer receives stale data. Repeating the same write safely after
a crash is not the same as ordering it correctly against other writers.

With writes quiesced, drain in-flight writers and delayed work that can mutate
the affected state, copy from the stable source, reconcile the result, and
switch the authoritative read/write path before admitting writes again. The
trade-off is the unavailable write interval, not a need for live replication.

With writes continuing, choose protection that covers both the application and
backfill paths. For example, store a source revision with each destination value
and atomically reject an older revision; a skipped stale copy then cannot undo
revision 8. Such protection still needs a way to carry every live change,
including deletes, to the new representation. Ordered change replay, coupled
writes with reconciliation, or a final bounded write pause can fit different
systems; none follows merely from having a cursor. Independent dual writes can
fail halfway, and an application-only guard does not constrain a legacy writer.

Cut over against a known boundary: account for changes through that boundary,
reconcile missing or divergent values at comparable revisions, and establish
which path owns subsequent writes. Retiring the old path also retires any old
writer that could reintroduce divergence. Row counts or a completed scan alone
cannot establish this. Choose the smallest mechanism matching the actual
concurrency and acceptable write interruption, not a replication architecture
for a migration that can safely run with writers stopped.

If this sequence is impossible, define downtime, snapshot, restore, and forward-repair behavior
explicitly. Code rollback does not automatically undo data changes.

Expand-and-contract is insufficient when the transformation loses
information, when an external client cannot upgrade, or when a historical
queue can reintroduce the old representation. Those conditions may require
versioned interpretation, a longer compatibility boundary or deliberate
downtime rather than another nominal migration step.

## Mitigate, then repair

Restore service before explaining the failure. Start with the cheapest reversible lever: turn the
flag off, halt the rollout, take the failing path out of service, reduce traffic to the new
revision.

Roll back when the previous artifact or revision is still compatible with current schema, data,
configuration, caches, clients, and external effects, and would not reintroduce a vulnerability
the release fixed. Reverse traffic or reinstall the prior artifact through the normal product path,
then observe that consumers actually select it; control-plane success alone is not route reversal.
When rollback is unsafe, keep exposure reduced and repair forward from the current state.

Restart only when the mechanism is process state, captured configuration, or a transient runtime
condition. A restart that clears symptoms without explaining recurrence is containment.

Once service is stable, classify the failure (build, startup, configuration, dependency, route,
capacity, data, or product), isolate the smallest changed owner, apply the repair to the pinned
target, and observe the target-linked and consumer consequences.
