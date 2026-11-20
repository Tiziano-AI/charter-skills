---
name: charter-release-and-configuration-diagnosis
description: Ship a release to the consumer that should run it, or find why a configuration
  change has no effect. Trace the selected build or effective setting in the actual
  app, service, command or request. Diagnosing selection does not require a deploy.
metadata:
  content_version: charter-release-and-configuration-diagnosis@2026.11.20.0
---
# Charter · Release Engineering & Configuration Diagnosis

Start with the action that still behaves the old way. Which executable,
process or routed revision performs it? Which value did that reader select,
and when? A desktop app can start its bundled executable while your shell
starts the updated one. A service can run exactly the right executable with
an override that your shell never receives. Reinstalling is the wrong fix
for both. The reader's own report of the selected path, value or source may
answer the question without changing anything.

## When a setting did not take effect

Read [Configuration diagnosis](configuration-diagnosis.md) before choosing
which input to change. Work backwards from the disputed request or running
process, not forwards from the file you edited. Compare what each launcher
supplies, how the reader combines or normalizes those inputs, and whether
it captures the value at build, startup or request time. Use readback for
the setting in question, not a dump of the environment. A status command
that rereads today's file cannot establish what yesterday's process holds.

Use the [reader and precedence contrasts](references/configuration-diagnosis-workflow.md)
when two plausible sources predict different outcomes. An explicit zero
lost to a fallback is a resolver defect; a documented alias displayed under
its canonical name is not. If the launcher sets the wrong value, restarting
will capture the wrong value again. If the input is right but the process
retains an older value, identify the reload that consumer needs. Give a
diagnosis as the winning source, capture point and observation that showed
it; when a fix is requested, change the responsible input through its owner
and repeat the original contrast. Deliberate differences between profiles
are not defects.

## When the change must reach a consumer

Read [Release engineering](release-engineering.md) before choosing a
delivery mechanism. Separate three failures: the change is absent from the
artifact; the artifact is present but not selected; or the right version is
selected but cannot use the current state. Follow only the links in the
[release lineage](references/lineage-chain.md) needed to tell them apart.
Use the project's release path and the exact target named by the grant.
Building, installing, publishing and shifting traffic have different effects.
Prefer promoting the accepted bytes to rebuilding them. A source-backed
service may have no package to publish.

For an [installed command, app or plugin](references/release-engineering-workflow.md),
check the path its normal launcher selects outside the checkout. For a
[hosted target](references/hosted/context-resolution.md), resolve the account,
service, environment and route before acting: the latest deployed revision
need not be the one receiving traffic. Exercise the changed action through
that consumer; distinguish what the deployment record shows from what the
action demonstrated.

Plan [cutover and recovery](references/hosted/operation-workflows.md) around
the readers and writers that cannot move together. If an old worker or
rollback binary cannot read what the new writer emits, take that fact to
`charter-codebase-analysis-and-change` for a compatible transition. Where
all consumers move together and state is disposable, an old path need not
survive. If a rollout fails, limit exposure within the release mandate;
reverse it only if the previous version still works with today's state and
clients and does not reopen the defect that made it unsafe.

A missing deployment acknowledgement is not a reason to deploy again.
Give `charter-workflow-recovery` the operation and target identities to
establish what happened. When the intended revision and configuration are
selected but service has degraded, use [target-linked diagnostics](references/hosted/evidence-and-diagnostics.md);
take the failing request, revision and observations to
`charter-system-and-mac-diagnosis` if the mechanism is still unclear.
