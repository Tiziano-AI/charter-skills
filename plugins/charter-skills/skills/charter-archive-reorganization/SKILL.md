---
name: charter-archive-reorganization
description: 'Reorganize file collections so people can find and interpret what they
  keep: choose names and structure, preserve bundles, versions and provenance, and
  plan recoverable moves. Not duplicate removal or disk reclamation.'
metadata:
  content_version: charter-archive-reorganization@2026.11.20.0
---
# Charter · Archive Reorganization

Start with something the owner must be able to find and interpret: a signed
agreement, the source of a delivered artifact, a tax record for a particular
period or an original photo. A tidy tree that breaks linked media is worse.
For a few files in a familiar folder, make the requested moves and report
the old and new paths. For an inventory alone, move nothing.

## Start from what is there

Record the inventory before planning broad renames, moving bundles or risking
provenance; file count alone does not decide this. The read-only helper
writes a new report outside the tree. Resolve scripts and templates from the
directory holding this SKILL.md, not the archive or current working directory.
With an existing Python 3.9+ interpreter (standard library only), run:

```bash
python3 "<absolute-skill-root>/scripts/inventory_tree.py" /absolute/archive/root \
  --out-dir /absolute/work/new-inventory
```

The summary shows the top-level shape, suffixes, sizes, media and opaque names,
the symlinks and special nodes it did not follow, and the paths it could not
read. The scripts do not recognise application bundles or repositories: rows
inside a `.photoslibrary`, `.app`, `.fcpbundle` or `.git` are that owner's
internals, not loose material or duplicate candidates. `"complete": false` means some directories or files were unreadable: the
report covers the rest, and conclusions about the whole collection wait until
those paths are named or opened.
[Operator recipes](references/operator-recipes.md) covers all three scripts and
their reports.

Inspect content or application metadata when it distinguishes placements.

## Let retrieval determine the axis

Choose the axis that predicts both where a new item goes and where a person
would seek it. Client, time, source and lifecycle serve different questions.
Test hard cross-cutting items before moving anything; if links or application
ownership make moves disruptive, an index may solve retrieval without them.
Use [taxonomy selection](references/taxonomy-selection.md) when competing axes
or recurring exceptions would change the structure.

## Preserve the relationships that give a file meaning

A version, derivative, component, replica and variant can look similar while
serving different purposes. RAW plus sidecar, project plus linked media, source
plus export, original plus translation and the exact delivered copy all carry
relationships worth retaining. “Final” in a filename establishes none of them.

Confidence attaches to a decision. Project placement may be clear while the
date or lifecycle state remains unknown. Keep useful source identifiers, such
as camera counters and export IDs, and native-language names rather than
inventing a precise semantic filename. Modification time may record copying or
downloading, not the event the document describes.

Names should supply the discriminators needed for retrieval and sorting. Date
meaning, version order, language, audience and source identifier can matter
more than uniform casing. Normalization can collapse distinct names through
case or Unicode equivalence, so generate every destination of a broad rename
and compare them as a set before any move.

## Equal bytes do not choose a survivor

The same bytes can be a needed delivery replica, an intentional backup or two
hard links to one inode. Neither path lengths nor timestamps decide which
location matters. If a plan collides or suggests removing an identical copy,
read [duplicates and collisions](references/duplicate-and-collision-policy.md):
identify the relationship before choosing a survivor. Removal is separate
work. For a separate Mac disk-space request, only identified rebuildable
candidates belong with `charter-macos-cleanup`, not the archive by default.

## Movement changes a live filesystem

The bundled scripts only observe; they do not move anything. Carry movement
through the owning application's relocation feature, an installed filesystem
tool or a small implementation fitted to the archive, which must handle the
actual volumes, links, bundles, sync clients and application dependencies.

For substantial moves record intent and actual effects outside the moved tree.
Read [move state and recovery](references/state-and-recovery.md) before the
batch or a rollback. A same-volume rename is not a cross-volume copy and
delete: verify the destination's bytes and needed metadata against the
source preimage, then check the source is still that object before removal.
Retain both if it changed or a competing writer cannot be excluded. Never
replay a batch or reverse a wish list to find out what already moved.

## Check the result by retrieval

If conversion is requested too, use `charter-document-fidelity` on the actual
target format before replacing anything; the moved package must still open,
calculate or extract as needed. Repeat the retrieval questions and open the high-value bundles and linked
projects. `scripts/validate_reorg.py` checks the top-level entries against the
configured list: it fails only when an entry is outside that list, comparing
names in Unicode NFC so a decomposed `café` matches the composed one. It
reports `.DS_Store` files and exact-duplicate groups as observations when asked,
because intentional replicas and platform metadata are acceptable. Concentrated
misclassification, repeated collisions or aging review queues call for a better
rule before further movement.

## References by problem

- [Archive model](references/archive-model.md): open when a root mixes intake,
  working, record, media or backup material: collection states, canonical
  placement, bundles, provenance and version relationships.
- [Taxonomy selection](references/taxonomy-selection.md) and
  [profiles](references/taxonomy-profiles.md): open when choosing the primary
  axis and adapting it to intake, household, client, media, research or
  project collections.
- [Naming](references/naming-normalization.md): open before a broad rename:
  dates, identifiers, language, versions and collision checks.
- [Confidence and review](references/confidence-and-quarantine-rules.md): open
  when items cannot be placed or named with confidence.
- [Duplicates and collisions](references/duplicate-and-collision-policy.md):
  open before choosing a survivor or resolving an occupied destination.
- [Operator recipes](references/operator-recipes.md): the inventory, duplicate
  and validation scripts, their reports, and choosing a movement path.
- [State and recovery](references/state-and-recovery.md): open when movement
  was interrupted or needs rollback.
- [Post-reorganization inspection](references/validation-checklist.md):
  structural accounting, taxonomy behavior and retrieval journeys after a
  batch.

Scripts: [inventory_tree.py](scripts/inventory_tree.py),
[hash_duplicates.py](scripts/hash_duplicates.py) and
[validate_reorg.py](scripts/validate_reorg.py), with their shared modules
`archive_scan.py`, `inventory_core.py`, `inventory_output.py`,
`duplicate_core.py` and `reorg_validation_core.py` in the same directory.
Optional formats: [taxonomy spec](assets/taxonomy-spec-template.json),
[move plan](assets/move-plan-template.jsonl),
[review queues](assets/review-buckets-template.md) and
[validation config](assets/validation-config-template.json).
