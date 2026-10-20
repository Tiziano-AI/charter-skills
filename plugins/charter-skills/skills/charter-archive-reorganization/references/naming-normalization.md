# Naming Normalization

Normalize names to improve recognition and sorting without erasing provenance or inventing
semantics. Folder and filename rules may differ, and an archive does not need to imitate a source
code style guide.

## Build a name from useful discriminators

Common components are:

- trustworthy date or period;
- client, project, event, account, person, property, or jurisdiction;
- document or media kind;
- sequence, language, version, variant, or lifecycle state;
- stable source identifier when it aids traceability;
- original extension.

Choose an order that matches how the collection sorts. Examples:

```text
2026-07-31_acme_signed-agreement.pdf
2024_tax-return_it.pdf
fieldmark_launch-interview_003.wav
portrait-session_014_select-color.tif
```

These are patterns, not a mandate to lowercase or transliterate every archive.

## Dates

Use a date only when its meaning is known: capture, issue, signing, service period, delivery, or
another domain event. Prefer sortable `YYYY-MM-DD` or `YYYY-MM` forms when chronological browsing
matters. Do not promote download or copy modification time into a document date.

When several dates matter, name the dominant retrieval date and retain the others in metadata or an
index. Leave an uncertain date out or mark the item for review rather than inventing precision.

## Language, characters, and case

Preserve native-language characters when they carry names or meaning and the destination ecosystem
supports them. Transliteration may help interoperability but should be a deliberate collection
choice, not an automatic loss. Normalize Unicode consistently if mixed normalization forms cause
duplicate-looking names.

Use separators and case for scanability and destination compatibility. Avoid trailing spaces,
control characters, ambiguous path separators, and names forbidden by target filesystems. Do not
rewrite established identifiers whose case or punctuation is significant.

## Versions and variants

Replace vague names such as `final2` only when the relationship is known. Use discriminators such as:

- `v03` for an actual ordered version sequence;
- `draft`, `reviewed`, `signed`, or `delivered` for established lifecycle states;
- `en`, `it`, `print`, `web`, `square`, or `captioned` for explicit variants;
- `source`, `edit`, `proxy`, and `export` for media roles.

Do not label a file `final`, `signed`, or `approved` from appearance alone.

## Opaque and generated names

UUIDs, camera counters, scanner timestamps, screenshot defaults, export IDs, and message-attachment
names may be valuable source identifiers. When semantics are clear, add a readable prefix or place
the item in a meaningful context while retaining the identifier. When semantics are unclear, keep
the original name in a review queue.

## Mapping and collisions

For broad renames, retain an old-path to new-path mapping and generate all candidates before any
move. Inspect case-only changes, Unicode-equivalent names, extension changes, reserved names, path
length, and multiple sources that normalize to the same target. Repair the naming rule instead of
resolving collisions ad hoc during apply.
