---
name: charter-codebase-analysis-and-change
description: Assess an unfamiliar or changed repository, or carry a contract change
  across schemas, writers, readers and stored data. Trace what the product can do
  and where its behavior is decided. A known one-module fix needs no system assessment.
metadata:
  content_version: charter-codebase-analysis-and-change@2026.11.26.0
---
# Charter · Codebase Analysis & Change

Follow one input someone actually cares about to the result they use. Find
where the decisive fact first becomes knowable. In an asynchronous export,
the request handler may know that work was queued; only the worker or a read
of the destination can establish that the file is ready. Editing the button
label cannot make the file exist. For an assessment, explain what the path
supports and where it falls short; do not refactor it. For a requested change,
start at the owner of that fact and follow its meaning out to the last reader.

**To get up to speed,** use [Repository assessment](repository-assessment.md)
before drawing a conclusion from a tree, a diff or a passing test. If you knew
an earlier revision, start with the meaningful changes since then and retrace
the paths they affect. Follow a request ID across a queue, a constructor to
its callers or a generated client back to its schema; another endpoint that
uses the same path teaches less than the worker that actually finishes it.
Distinguish the promised result, reachable implementation and observed
behavior at the destination. Report the gap that changes what to do first.
If the question was just where the export directory is set, give the effective
setting and any override that matters, not a tour. When accounts of the same
path conflict, use the [quality lenses](references/quality-lenses.md) to
choose an observation that would discriminate between them. If the question
is what *should* survive a disagreement between docs, schema and code, use
[owner and evidence resolution](references/repo-evidence-policy.md) instead.

**To change what a value means,** use [Cross-layer change design](cross-layer-change-design.md)
before choosing the field, editing its consumer or planning a migration.
Trace both the typed symbol and its spelling on the wire. A schema, worker,
serializer, permission filter, generated client or public example can keep
the old behavior alive even if the main screen works. Update the inputs that
generate it, not just the generated files. Test the case where the meanings
differ: an export is in the queue and nobody can download it yet. If several
teams or generators share the change, use the [source change map](references/replacement/source-change-map.md)
to identify their dependencies before dividing the edits.

The compatibility question is who or what can still interpret the old
meaning. Look beyond repository callers to released clients, independently
deployed services, queued retries and records people still need. If all can
move together, replace the contract outright, convert needed data once or
rebuild it, and remove the displaced path. If some cannot, read the
[worked replacement](references/replacement/replacement-workflow.md) before
designing the overlap. Preserve each needed direction of translation: a new
service can still acknowledge enqueue to an old client; the old
acknowledgement cannot establish completion for a new reader. Nor did a client
that unlocks downloads on enqueue ever have the fact it needed. Upgrade or
contain that client rather than promise that a parseable response is safe.
Name the population each temporary reader serves and how to tell when it can go.

If the unresolved question is *which component should own this*, take the
required behavior to `charter-architecture-and-provider-design` and bring the
chosen owner back to the source change. If tests accept both meanings, take
the counterexample to `charter-test-design`. If versions must coexist in
service, give `charter-release-and-configuration-diagnosis` the live readers,
writers, data and compatible ordering; a coherent source change is not a
completed rollout.
