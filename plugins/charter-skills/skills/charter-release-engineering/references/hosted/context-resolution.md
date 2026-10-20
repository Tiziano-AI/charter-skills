# Hosted Target Resolution

Resolve the hosted target before selecting a deploy, promotion, cutover, migration, restart, or
rollback command.

## Target tuple

Identify the fields the provider uses to route an operation:

```text
provider -> account or organization -> project -> service or resource
-> environment or stage -> deployment/revision -> route or consumer
```

Depending on the platform, include region, cluster, namespace, database, bucket, domain, traffic
group, branch, or channel.

## Resolution order

1. Start from the user's explicit provider URL, resource ID, deployment receipt, or named target.
2. Parse stable IDs and use a current provider read to recover mutable labels.
3. List the narrow containing scope only when an ID is absent.
4. Compare resolved remote identity with local project links, config, shell environment, and CLI
   defaults.
5. Pin the operation to stable IDs or an unambiguous provider-supported selector.
6. Identify the current consumer route and revision before planning change.

Stable resource IDs normally outrank friendly names, recent dashboard tabs, working-directory
links, cached CLI contexts, and default accounts. A local link is useful evidence about intent only
when it agrees with the requested remote target.

## Consumer and dependency context

Consumers and coupled resources determine exposure and transition order. Follow
the relationships the changed behavior can affect:

- public domains, internal routes, queues, cron jobs, workers, or mobile clients;
- databases, migrations, buckets, caches, secrets, and variable sets;
- upstream and downstream services;
- traffic allocation and mixed-version clients;
- update channels or regional replicas.

These relationships determine cutover order, blast radius, rollback, and observation.

## Ambiguity matters at the operation it can misdirect

- more than one account, project, environment, service, or database matches;
- a stable ID and local ambient context point to different targets;
- production and preview labels are reused across projects;
- the deployed revision is known but the routed revision is not;
- a migration target or traffic group is implicit;
- current consumers or rollback target cannot be identified for a consequential change.

Resolve target ambiguity with a provider read or the target owner rather than
choosing the most recent or familiar resource. Not every missing field blocks
every operation: an isolated preview deployment can be valid before a public
route exists, while traffic cutover needs that route resolved. Unknown consumers
matter when a migration, deletion or incompatible change could break them; they
do not require an organization-wide dependency inventory for a local asset fix.

Provider URL shapes, CLI flags, authentication, and API payloads remain provider-specific. Use the
current provider tool or official documentation once the target tuple is known.
