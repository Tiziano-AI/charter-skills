# Classification Confidence And Review Queues

Confidence is decision-specific. A file may have high-confidence project placement, uncertain date,
and no safe basis for renaming or deletion. Do not collapse these into one score.

## Signals

Use the least invasive signals that distinguish the decision:

- current path and neighboring items;
- filename and extension;
- embedded author, capture, creation, subject, or application metadata;
- visible title page, thumbnail, or bounded content inspection;
- application bundle or sidecar relationships;
- recurring client, project, event, account, or date patterns;
- source export records or an existing index;
- an archive owner's classification.

File modification time, generated names, and inferred entities are weak signals unless the source
system gives them a known meaning.

## Confidence by action

### Placement

- **High:** independent signals agree on the same destination and no bundle relationship is broken.
- **Medium:** the correct branch is clear but a deeper subject or lifecycle position is uncertain.
- **Low:** plausible destinations compete, source context is missing, or the item may belong to an
  application-managed bundle.

### Naming

- **High:** the subject and discriminating date, sequence, or version are explicit.
- **Medium:** the item can receive a stable generic name while preserving its original identifier.
- **Low:** a semantic rename would invent people, dates, status, or relationships.

### Duplicate disposition

- **High for byte identity:** size and a strong full-content hash agree.
- **Still undecided for deletion:** even byte-identical paths may be intentional replicas, bundle
  members, or linked locations. Placement and recovery context decide the survivor.
- **Low:** similar names, thumbnails, or extracted text differ in bytes or provenance.

## Review queues

Use named queues that describe the unresolved decision, for example:

- `needs-placement`;
- `needs-date-or-subject`;
- `bundle-or-link-review`;
- `same-subject-different-bytes`;
- `duplicate-survivor-review`;
- `unreadable-or-corrupt`.

A review record should keep the original path, proposed destination if any, signals observed,
competing interpretations, and the smallest human decision that resolves it. Preserve the original
name until a stronger name is established.

## Review queue health

Sample queues after classification. If most material lands there, the taxonomy is too specific,
the signals are insufficient, or the root should be split by archive state. A queue is working when
items can leave through a small number of clear decisions: place, rename, retain, relate, exclude,
or deliberately remove.
