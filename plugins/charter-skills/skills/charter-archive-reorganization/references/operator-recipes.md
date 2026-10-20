# Archive reports and execution

The bundled scripts read a quiescent local tree and write new reports outside
it; an existing output path is never overwritten, and nothing in the archive is
moved or removed. Symlinks and special nodes are listed under
`excluded_nodes`, not followed. A directory or file the scan cannot read, such
as a folder protected by macOS privacy controls, is listed under `unreadable`
with its error, the scan continues, and the report says `"complete": false`.
A report is not an atomic snapshot, bundle inspection or deletion plan.
Hashing cloud placeholders may download them; use the storage owner's metadata
tools instead when that read would be inappropriate.

`inventory_tree.py`, `hash_duplicates.py` and `validate_reorg.py` are the entry
points. They share `archive_scan.py` (scanning and report paths) and use
`inventory_core.py`, `inventory_output.py`, `duplicate_core.py` and
`reorg_validation_core.py` from the same directory.

Resolve `<skill-root>` below to the absolute directory containing the loaded
SKILL.md. Use an existing Python 3.9 or newer interpreter. Neither the archive
root nor the caller's working directory is the package location.

## Observe the collection

```bash
python3 "<skill-root>/scripts/inventory_tree.py" /absolute/archive/root \
  --out-dir /absolute/work/new-inventory
```

`inventory.jsonl` holds one record per regular file; `summary.json` holds the
top-level shape, suffix and size counts, excluded and unreadable paths. Media
and opaque-name flags are heuristics: RAW originals count as media, and UUIDs,
long numbers, screenshot defaults and camera counters such as `IMG_1234` or
`DSC_0001` count as opaque. They locate candidates for review, not placement
decisions. Inspect bounded content or application metadata for unresolved
relationships.

## Discover equal content

```bash
python3 "<skill-root>/scripts/hash_duplicates.py" /absolute/archive/root \
  --out /absolute/work/new-duplicates.json
```

The report groups regular files by size and full SHA-256 and does not select a
survivor. Names that share one filesystem object are hashed once: the group
lists the object under one path with its other names in `hardlink_names`, and
`hardlink_sets` lists every such object, because removing one of its names
frees nothing and deletes no copy. A file that cannot be read, or that changes
while it is hashed, is recorded under `unreadable` and left out of the groups.
Equal bytes may still differ in permissions, extended metadata, link
dependencies or preservation role.

## Plan and perform admitted movement

Choose taxonomy, naming and bundle decisions before generating destinations.
`assets/taxonomy-spec-template.json` records those decisions, and
`assets/move-plan-template.jsonl` shows one row per intended operation with its
reason. Neither is read by the scripts; they are formats for the plan and its
review.

Select the application's relocation feature, an installed filesystem tool or a
bounded implementation appropriate to the archive. That path must handle
destination collisions, link boundaries, cross-volume behavior, current
preimages and partial completion. Keep the recovery record outside the moved
material and record intent and observed outcomes incrementally, so an
interrupted batch does not lose its completed prefix.

Across volumes, a move is a copy and a delete. Hash the source before copying
and verify the copy against that digest. Required extended attributes, ACLs,
resource forks and bundle relationships need their own preservation and
verification; equal file bytes do not cover them. On macOS, `ditto` can preserve
that metadata, subject to its options and the destination filesystem. Exclude
writers and recheck source preimages before removal; a changed source stays in
place for reconciliation rather than being deleted because an older copy
matched. A preimage read and deletion are not an atomic compare-and-delete.

Use smaller coherent batches where sync, application links or recovery cost
make broad movement inappropriate. Classify an unexpected collision or missing
source rather than guessing a suffix or replaying the original plan. Duplicate
removal is a separate survivor-and-recovery decision, best made through a tool
that moves copies to a recoverable location.

## Inspect the resulting collection

```bash
python3 "<skill-root>/scripts/validate_reorg.py" /absolute/archive/root \
  --config /absolute/work/validation-config.json --out /absolute/work/new-validation.json
```

Start the config from `assets/validation-config-template.json`. The command
exits 1 only when a top-level entry is outside `canonical_top_entries`, listed
in `remaining_noncanonical_top_entries`. Names are compared in Unicode NFC, so
a folder stored in decomposed form matches the composed spelling in the config,
and the report keeps the exact observed name.
A regular `.DS_Store` at the root is platform metadata, not a top-level entry;
a symlink or folder with that name is not. `absent_canonical_top_entries` lists
configured entries that do not exist yet.

`check_ds_store` and `check_exact_duplicates` add counts, never failures:
intentional replicas and platform metadata are acceptable in an archive.
Duplicate groups leave out `.DS_Store` files, which `check_ds_store` counts. A
disabled check reports `null`, which means unobserved, not zero. When
`complete` is false, the counts cover only the readable part of the tree.

A clean validation does not show that an application can relink its media or
that the taxonomy serves retrieval. Repeat the retrieval questions and inspect
affected high-value bundles. Keep exact duplicates that are intentional
replicas or unresolved decisions; a report count is not a mandate to delete.
