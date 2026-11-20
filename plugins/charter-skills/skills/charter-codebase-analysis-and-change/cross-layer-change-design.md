# Cross-Layer Change Design

A change that crosses layers changes an agreement. Schemas define it,
producers and mappers create and transform it, storage keeps it, consumers act
on it, and generators, fixtures and examples reproduce or teach it; each of
these is a carrier of the contract.

A local edit whose meaning stays inside one module needs none of this. If you
cannot yet identify the public path whose behavior will change, use
[repository assessment](repository-assessment.md) to trace it. If documents,
schemas, code or an external dependency disagree about what should survive,
resolve the [intended source contract](references/repo-evidence-policy.md)
before choosing the edit.

## Defaults

**Separate meanings across surviving interpretation boundaries.** When an
old reader, writer, stored row or queued message can survive the change, give
the changed meaning a distinct field or protocol identity. If `amount` changes
from integer cents to decimal currency units, a new field such as
`amount_decimal` prevents an old reader from silently reading the new value as
cents; required-field validation must still reject an absent old field rather
than substitute a misleading default. Do not reuse a removed key, enum value
or wire number while its old meaning can still arrive. If both facts remain
needed, they keep distinct identities. When every consumer and all state move
together, retain an appropriate domain name and replace its representation
without a compatibility path; a fully replaceable field needs no new name
solely because its encoding changed. A rename whose meaning is
unchanged is churn.

**Find every carrier first.** Beyond schema, producer and consumer,
carriers include serializers, migrations and stored rows, exhaustive switches,
registries, generated clients, fixtures, public examples, documentation that
teaches use, configuration defaults, and the access checks that scope who may
read the data; a new filter or read path needs the same ownership checks as
the old one. In typed code, a rename or deletion lets the compiler identify
references that still depend on the old symbol. Search for its wire spelling
(JSON key, column, flag, environment variable), which the compiler cannot see; follow generated
files back to their inputs; and look outside the repository for released
clients, other services, stored data and queued work. When several writers
share the change, a [source change map](references/replacement/source-change-map.md)
can show dependencies that none of them sees alone.

**Replace the owner and delete the old path in the same change.** When every
affected consumer, running job and retained record can move together, update
the owner and every carrier. Delete the displaced route, its generator input
and its fixtures together: no alias, shim,
fallback reader or deprecation period. Records still needed move with the
change, converted once or rebuilt when derived; where converting or losing them
is outside the change's authority, they are a population that cannot move at
once. Edit canonical inputs before derivatives and make the public path work
before deleting what it displaced; a compile failure along the way is editing
order, not a reason for migration machinery.

**Decide the fact where it is known.** If a result must mean "delivered"
rather than "accepted," the change belongs where delivery is known, not in the
label a client renders; a shared helper removes disagreement only if it
actually knows the fact. A serializer can own the encoding while the domain
owner decides the meaning; consumers receive the established value instead of
recomputing it. When the change adds lifecycle states, write each transition
as a conditional update from named source states, so a late or duplicated
writer cannot move a finished operation backwards.

## Stage only what cannot move at once

A transition is needed only for a population that cannot move with the change:
released clients, queued work, an independently deployed service, or
persisted data that live readers keep using while it converts. These boundaries
can exist before a product's first release. For those populations, expand,
migrate and contract: introduce compatible storage and readers before changed
writers, backfill only what existing evidence supports, then remove the old
shape. During the overlap, each reader must still obtain the facts it uses
from every writer whose output it can receive. Compatibility breaks when a
new writer drops information an old reader needs, or when a queued old value
arrives after its reader was removed.
Count the real populations, including caches, retries and delayed jobs; a
finished deploy does not mean old values are gone. Each kept adapter needs an
owner and a removal condition. Use the [worked staged replacement](references/replacement/replacement-workflow.md)
to check both directions when old and new readers, writers or records coexist;
one valid direction of translation does not establish the other.

## Finish the replacement

Running the public path a user drives shows that the new behavior works, not
that the old one cannot still win through an alias, a configuration default,
an enum member, a fixture, an example, a shell completion or a generated
member. Search finds candidates; each one's role decides whether it changes.
Changelogs, decision records and history stay as they are.

Failures point at what has not moved: generated drift at an unmoved generator
input, a mapper failure at two incompatible meanings, a public path reaching
the old default at an old path that still runs. Repair that dependency rather
than widening the rewrite. A failing old test may protect a retired contract
or a lost invariant: renaming a field retires the spelling assertion, not the
obligation to keep null, empty and partial results distinct.
`charter-test-design` covers reading a failing check before changing it.

The work is done when the public path shows the new behavior and no old path
can run or be regenerated, apart from a staged reader or adapter kept for a
named population until its removal condition holds.
