# Post-Reorganization Inspection

Inspect both structural conformance and practical retrieval after each applied batch.

## Filesystem accounting

- Every successful move has the expected source absence and destination identity.
- Skipped, failed, collided, missing, and manually changed rows remain visible.
- No destination was created outside the approved root or through an unintended symlink boundary.
- File and byte counts reconcile with moves, deliberate additions, and recorded removals.
- Empty source directories are retained or removed deliberately; they are not mistaken for lost
  content.
- Review queues contain the ambiguous items assigned to them and no unrelated material.

Ambient metadata such as regular `.DS_Store` files may be tolerated and preserved. Treat it as a
collection-specific choice rather than a universal failure. Symlinks, special nodes, application
libraries, cloud placeholders, and hidden files need their own semantics before movement.

## Taxonomy behavior

- Top-level entries follow the chosen primary axis.
- Peer folders answer the same kind of question; lifecycle, subject, time, source, and geography are
  not mixed arbitrarily.
- New intake has an obvious destination and promotion path.
- Version, derivative, original, delivered, and review states remain distinguishable.
- Names sort and scan as intended without losing important language, identifiers, or provenance.

## Retrieval journeys

Repeat the prompts used to select the taxonomy. Ask another likely user, when available, to locate
high-value items without being taught the move plan. Inspect:

- number of decisions needed to reach the item;
- whether likely search terms match names or metadata;
- whether the canonical artifact is distinguishable from drafts and derivatives;
- whether chronology, entity, subject, or lifecycle context is still understandable;
- whether review queues explain why an item remains unresolved.

## Content and dependency sampling

Open representative high-value files, bundles, and linked projects. Check application libraries,
relative links, aliases, shared links, sync status, permissions, backup selection, and automation
affected by path changes. Hash equality can support identity but cannot show that an application can
still locate its media or that a user remembers the new route.

## Duplicate state

Re-run exact-duplicate discovery only when duplicate handling was part of the batch. Remaining exact
groups are acceptable when they are intentional replicas, pending survivor review, or excluded by
scope. Verify that every removal maps to an intact survivor and any promised recovery location.

## Feedback

Concentrated misclassification, large or aging review queues, repeated collision patterns, and
difficult retrieval journeys indicate a taxonomy or naming rule that should change before the next
batch. Repair the rule and regenerate remaining destinations rather than accumulating exceptions.
