# Coordinate a Multi-Surface Change

Write a map when several writers, agents or generators share one change and a
missed dependency would otherwise go unnoticed. A short direct change does not
need a separate artifact, and the map is not a registry to keep once the source
itself expresses the contract.

## What a useful map contains

Open with the public behavior that must work after the change, the owner of its
meaning, the public path that demonstrates it (command, API, screen or parser),
and any consumer outside the change that forces a staged transition. Then give
one row per carrier:

| Field | Purpose |
| --- | --- |
| identity and path | the exact source file or public surface |
| current meaning | old, new or mixed behavior, not a count of mentions |
| action | update, regenerate, remove, keep as external adapter, or defer |
| dependency | what must change first and why |
| result | what actually changed, or what remains open |

A fixture belongs in the map when it protects or regenerates the contract;
history does not become a carrier merely by containing an old name. For an
external adapter, name its current consumer, the direction it translates, its
owner and the condition for removing it. Add checks only for the schema,
generation or integration boundaries the change actually crosses.

## Resolve conflicts instead of parking them

A real open conflict may involve two plausible owners of the meaning, an
unknown vendor behavior, a generated output whose producer cannot be traced, or
a removal that would affect a consumer outside the task. Record the competing
meanings, what each choice would change, and the fact or the person's decision
that would settle it. Known implementation work is not an open conflict. When
the answer arrives, implement it or explicitly exclude it, and fold the
decision into its owner rather than leaving it in the map.
