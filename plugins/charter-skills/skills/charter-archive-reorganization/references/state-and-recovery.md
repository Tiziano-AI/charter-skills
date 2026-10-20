# Move State And Recovery

Archive movement must be resumable from recorded filesystem effects rather than from memory or the
original intention.

## Useful states

- **inventoried:** a current source inventory exists; nothing has moved.
- **classified:** taxonomy, naming, bundle, and review-queue decisions exist.
- **planned:** a root-relative move plan exists against a known inventory.
- **dry-run checked:** sources, destinations, root bounds, and collisions were evaluated without
  mutation.
- **partially applied:** some rows changed the filesystem before interruption or failure.
- **applied:** every reviewed row has a corresponding successful effect.
- **duplicate reviewed:** exact groups and survivors were decided; no removal is implied.
- **duplicate removed:** selected redundant paths were removed with a survivor mapping.
- **inspected:** structure, retrieval journeys, review queues, and affected dependencies were
  checked after movement.

Name the current state precisely. “Reorganization complete” is unsafe when the filesystem is only
inventoried or partially applied.

## Before movement

For a non-trivial batch retain:

- resolved root and exclusions;
- inventory and taxonomy version used to generate the plan;
- root-relative move plan;
- dry-run results and unresolved collisions;
- intended review queues;
- recovery location, snapshot, backup, or trash behavior if applicable.

A rollback is simplest when operations are one-to-one moves and no content was edited or deleted.

## Interrupted apply

Do not rerun the original plan wholesale. Reconcile each planned row against the current tree:

- `moved`: source absent and intended destination contains the expected object;
- `still_at_source`: source remains and destination is absent;
- `collision`: intended destination is occupied by another object;
- `both_present`: copy, manual action, or partial external operation occurred;
- `missing`: neither identity can be established;
- `changed`: source or destination exists but no longer matches the planned object;
- `unknown`: links, bundles, placeholders, or unavailable volumes prevent classification.

Build a continuation plan only from `still_at_source` rows that remain valid. Review every other
state. A stale plan can turn a formerly safe move into overwrite or misclassification.

## Rollback

Build the reverse operation from the successful apply records and current filesystem, not by
swapping every row in the original plan. Process in reverse order when parent directories or name
reuse make order significant. Stop if:

- the old source path is now occupied;
- the moved file was edited or replaced;
- a bundle acquired new linked members;
- an application or sync service changed identity or metadata;
- content was permanently deleted without a recoverable copy.

When the old taxonomy itself caused the retrieval failure, rollback may restore bytes safely while
restoring a poor organization. Decide whether forward repair is less disruptive.

## Review queue lifecycle

Each queued item keeps its original identity, unresolved decision, observed signals, and possible
destinations. Close it through one explicit outcome: place, rename, relate to another artifact,
retain in a deliberate unresolved collection, exclude from this archive, or remove through a
separate disposition.

Track queue size and age. Repeated ambiguity of the same kind is feedback that the taxonomy or
inventory signals need revision.

## Duplicate removal recovery

The removal record should identify hash, kept path, removed path, and recovery location if one
exists. Recheck the kept copy before removing another path and after the batch. If the survivor is
wrong or damaged, restore from trash, backup, replica, or holding area. When none exists, the loss is
not reconstructable merely because the files once shared a hash.
