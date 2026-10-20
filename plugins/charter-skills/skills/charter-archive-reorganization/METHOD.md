# Charter · Archive Reorganization

An archive is a retrieval system and a record of relationships. Rearrangement
is useful when future users can find and interpret material more readily
without reconstructing the cleanup author's decisions. A neat tree that loses
provenance or breaks linked media is a worse archive.

A handful of files in a folder the user already understands needs no method:
move or rename them and list the old and new paths in the reply. The method
matters when the collection is large or shared, when a name or date would have
to be guessed, when bundles, versions or sync clients are involved, or when a
move would be hard to undo.

## Start from what is there

Inventory depth follows what a move could lose: uncertain provenance, linked
bundles, broad renaming or difficulty retaining the relevant paths and
relationships call for a recorded inventory before choosing destinations.
File count alone does not decide that need. The read-only inventory below
records the tree's shape; inspect content or application metadata where the
relationships are not visible in paths. It writes a new report outside the
tree and changes nothing inside it. Resolve bundled scripts and templates from
the directory containing this loaded SKILL.md, not the archive or project
working directory. In these commands, replace `<skill-root>` with that absolute
package directory. The scripts use only the standard library and require an
existing Python 3.9 or newer interpreter:

```bash
python3 "<skill-root>/scripts/inventory_tree.py" /absolute/archive/root \
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

Then collect a few real retrieval questions: the signed agreement for a client,
the source of a delivered artifact, a tax record for a jurisdiction and period,
an original photograph from an event. Inspect content where it distinguishes
these placements.

## Let retrieval determine the axis

A primary axis works when it predicts where new material belongs and where a
future person will look. Entity, subject, time, source and lifecycle answer
different questions. Choose one within a genuine collection zone; secondary
access can come from names, metadata, search or an index. Copying material into
several editable subject trees creates divergence rather than better retrieval.

An intake area and a stable records archive may need different structures.
Application libraries, photo libraries and source repositories already have
owners for their internal relationships; they are not piles of loose files.
When path dependencies dominate, an index can improve discovery with less
disruption than movement.

Try the difficult cross-cutting items against the organizing idea. If most
require exceptions, the axis or granularity is wrong. A review queue is useful
for a specific missing decision; it is not a permanent substitute for a
taxonomy that fits the collection.

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

Full-content hashing finds byte-identical regular files at the time of reading.
It does not establish that a path is dispensable, that extended metadata is
equal, or that a recovery copy is independent. Intentional backups, application
links and delivery replicas can need their locations even when content matches.
Two names of one hard-linked file are one object: removing a name frees
nothing, which is why the duplicate report lists them as a hard-link set.

Choose disposition from the collection's preservation and retrieval needs.
Prefer meaningful canonical context and intact relationships over the shortest
path or newest timestamp. Similar-looking files with different bytes need
classification as versions, derivatives, variants or unresolved material; they
do not become deletion candidates by resemblance. Removing byte-identical
copies is a separate step for a tool that keeps them recoverable.

An occupied destination is information about the plan. Same bytes call for a
survivor decision, known variants need real discriminators, and an unexplained
collision calls for revising the placement or naming rule. Overwrite or
arbitrary suffixing hides the relationship the reorganization was meant to
clarify.

## Movement changes a live filesystem

The bundled scripts only observe; they do not move anything. Carry movement
through the owning application's relocation feature, an installed filesystem
tool or a small implementation fitted to the archive, which must handle the
actual volumes, links, bundles, sync clients and application dependencies.

For substantial movement, write the source-to-destination intent before the
batch and record each effect as it happens, outside the moved tree, so an
interruption leaves a usable account. Reconcile current sources and
destinations before each batch; a dry run cannot reserve paths. Within one
volume a move is a rename. Across volumes it is a copy followed by a delete:
verify content and required metadata at the destination against recorded source
preimages, then establish that the source has not changed before removing it.
If a writer cannot be excluded or the source changed, retain both and reconcile;
a successful copy does not authorize deleting a newer source.

Concurrent edits, sync or an interrupted cross-volume copy can leave both paths,
neither path or a changed object. After an interruption, classify those states
instead of reading a missing source as success or rerunning the old plan
wholesale. Rollback derives from successful effects and current identities, not
a reversed wish list; it may be blocked by later edits or occupied old paths,
and forward repair may preserve more work.

## Check the result by retrieval

Repeat the retrieval questions and open the high-value bundles and linked
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
