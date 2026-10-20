---
name: charter-repository-assessment
description: 'Assess or catch up on a repository that is new to you or has changed:
  trace a real product path to what it supports, where behavior is owned and which
  gap decides the first useful work. Deploying or installing it is release engineering.'
metadata:
  content_version: charter-repository-assessment@2026.10.16.0
---
# Charter · Repository Assessment

A repository is a partial model of a product: it contains intentions,
implementations, generators and selected examples, but not necessarily the
installed state or the user's experience. A useful read reconstructs how a
meaningful input becomes a result, rather than describing the directory tree.

Choose a path that bears on the actual question: a command, API, screen, job,
document generator or package consumer. Following one vertical slice makes
ownership and missing joins visible. Add another path when it could change the
verdict—for example a background worker with a different persistence model—not
merely because another top-level folder exists.

When you are catching up on a repository you knew, start from what changed:
the log since the last commit you knew (`git log --oneline <commit>..HEAD`, or
`--since` a date), which branches landed and which are still open, and which
contract documents, schemas and entrypoints moved
(`git diff --stat <commit>..HEAD -- <paths>`). Then re-trace the product paths
those changes touch. A path whose code and dependencies did not change can
retain the earlier source assessment; changed configuration, data or runtime
conditions can still invalidate a claim about its observed behavior.

A question about one place, such as "where are retries configured?", needs the
location and any caveat that changes how it is used (the value is read only at
startup; a second default in the client overrides it), not a full assessment.

## Reconstruct the actual system

Find where the behavior is constructed, what controls it, and who consumes it.
Entrypoints reveal routing; schemas reveal accepted shapes; implementation
reveals transformations; tests reveal claimed invariants; runtime observations
reveal one occurrence. None substitutes for all the others.

Read the governing product contract and the complete relevant owners.
When docs and code disagree, separate intended behavior from implemented
behavior instead of automatically declaring either authoritative. The question
may be whether code satisfies an accepted promise, whether public docs became
stale, or whether the promise itself is still undecided. The same diff supports
different work under those three conditions.

Ownership follows construction and decisions. A generator may own a visible
file; a configuration resolver may own a surprising default; a queue worker
may own the effect an API only accepts. Tracing a constructor's callers or both
sides of serialization is often more revealing than searching every occurrence
of the public type name. The missing behavior may be at a join rather than in
the most obviously named module.

Build hypotheses while reading. For each consequential uncertainty, choose
the source or observation most likely to distinguish the live alternatives.
Do not let the nearest available test decide the question it was not built
to answer. If the hypothesis is that accepted jobs are never scheduled, a
request-schema test cannot discriminate it; the queue-to-worker connection
can. Read a test's inputs, assertion and doubles to learn which world it models.
An extensive suite using a permissive fake can miss one decisive host boundary.

## Turn understanding into a useful verdict

State what the path currently supports, the owner responsible, the material
gap and the best first work session. If representative use contradicts the
documented promise, lead with that mismatch. A source read can locate an
implementation and a missing piece, not show that the built artifact works
where it runs. When readiness is the question, one run of the public path in
a clean, isolated copy of the target environment (build the image and render
one real document; install the package and run the command) settles more than
further reading, and a green suite that mocks the host boundary does not.

Choose intervention scale from the mechanism. A local defect calls for a
local repair; recurring coupling may justify refactoring a boundary. If two
screens independently compute the same lifecycle incorrectly, centralizing
the decision may stop recurrence. If their timing or authority genuinely
differs, forcing one shared abstraction can create the defect instead.

A rewrite needs a credible architecture that removes the limiting mechanism
and a transition for valuable behavior and state. Compare hidden behavior,
transition cost, operating burden and likely future changes. Age, size or test
count alone says little: old code can encode a stable domain well, and small
new code can merely move complexity into operators' manual work.

[Quality lenses](references/quality-lenses.md) develops tracing techniques,
evidence that can falsify a conclusion, information loss across seams and the
ladder of intervention scales; open it when the path crosses several owners or
the evidence points in different directions.

## Git when it changes the verdict

Use ancestry and the actual change on each side to tell integrated, divergent
and parked work apart. A branch label does not establish relevance; a
remote-tracking ref shows what this clone last saw of the server; and a
squash-merged or rebased branch is not an ancestor of its target, so ancestry
alone calls it diverged. When branch state changes the verdict, run the
local-only helper, which never fetches or changes the repository. Resolve its
path from the directory containing the loaded `SKILL.md`, not the repository
being assessed or the shell's working directory. Substitute that observed
package path below:

```bash
bash "/absolute/path/to/loaded/charter-repository-assessment/scripts/git_snapshot.sh" --repo /absolute/path/to/repo --compare main --compare candidate
```

For each pair it reports what each side changed since the merge base and
whether one side's changes are already in the other, including by squash,
rebase or cherry-pick. Two cases still misread: a squash whose conflicts
were resolved by hand reads as diverged, and a squash or cherry-pick that the
target later reverted reads as integrated, because the evidence is the patch
in history rather than the current tree. The target's `git log` for those
files settles both.

Return what the product can do, where the gap that matters is owned, and the
first useful work. Stop reading when another file would not change the owner
or the recommendation. Carrying a known change through the code is
`charter-cross-layer-change-design`; deploying or installing it is
`charter-release-engineering`.
