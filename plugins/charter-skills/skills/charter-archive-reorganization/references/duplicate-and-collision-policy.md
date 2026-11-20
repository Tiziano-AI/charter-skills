# Duplicate, Version, And Collision Policy

## What equality establishes

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

## Classify the relationship first

- **Exact duplicate:** the complete file bytes have the same strong hash.
- **Hard link:** two directory entries refer to the same filesystem object; removing one name is
  not the same operation as deleting an independent copy.
- **Semantic duplicate:** different bytes appear to express the same content, often after metadata,
  compression, scanning, or format changes.
- **Version:** content changed over time and the sequence matters.
- **Derivative:** one file was exported, transcoded, resized, cropped, flattened, or previewed from
  another.
- **Replica:** redundancy is intentional for backup, distribution, or application behavior.

Only exact hashing establishes byte duplication. It does not establish which paths are dispensable.
Never delete a semantic duplicate, version, derivative, or replica through the exact-duplicate path.

## Hashing strategy

Group by size before full hashing to avoid unnecessary reads. Use a strong full-content digest for
the final grouping. On very large or remote collections, a sample hash may identify candidates but
must not authorize disposition. Re-read file identity before deletion because a file can change
between scan and action.

Treat packages, sparse files, symlinks, cloud placeholders, and application libraries according to
their owning filesystem or application semantics rather than blindly hashing their visible nodes.

## Survivor choice

Choose a survivor from the archive's retrieval and preservation needs. Prefer, in order relevant to
the collection:

1. a copy in the declared canonical collection rather than intake or temporary output;
2. a path with meaningful project, event, client, or record context;
3. intact provenance, metadata, permissions, extended attributes, or application relationships;
4. a stable, recognizable name;
5. an independently recoverable copy while the cleanup is still under review.

Modification time and shortest path are tie-breakers at most. Copying often rewrites timestamps,
and a shallow path may discard valuable context.

## Destination collisions

When a planned destination exists, classify the collision before proceeding:

- **same bytes:** retain the chosen canonical path and record the redundant candidate; do not
  silently delete it as part of a move;
- **different bytes, known versions or variants:** preserve both under explicit distinguishing
  names or a version/variant substructure;
- **different bytes, unresolved relationship:** move neither into the occupied destination; route
  both identities to review;
- **same filesystem object:** avoid a meaningless move or duplicate link operation;
- **invalid plan:** two unrelated sources map to one destination because the naming rule loses a
  discriminator; repair the rule and regenerate affected rows.

Never implement collision handling as overwrite-by-default or suffix guessing such as `(1)` unless
that suffix is an intentional, documented sequence.

## Removal

Duplicate discovery and duplicate removal are separate operations. Before removal, recheck the
survivor, hash, path identities, bundle relationships, backup posture, and current filesystem state.
Keep a removal record that maps every removed path to its surviving path and hash. If recovery
matters, use trash or a reversible holding area instead of permanent unlinking.
