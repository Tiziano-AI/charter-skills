# Release Lineage Chain

Use a lineage chain when several build, package, promotion, install, or deployment stages make it
hard to know which source a consumer is running.

## Core relationships

```text
source revision
  -> build invocation and inputs
  -> immutable artifact
  -> channel, registry, feed, or environment
  -> installed target or hosted revision
  -> selected runtime
  -> consumer observation
  -> rollback or forward-recovery target
```

Each arrow needs an identity relationship, not necessarily a large evidence packet.

Identity depth follows ambiguity. For one local artifact copied directly into
a known consumer, a content digest and selected path may settle the relationship.
For a registry tag that can move while several regions roll out independently,
the tag alone cannot join an observation to its source. Retain the immutable
artifact and route allocation at the relevant time. More logs of the mutable
tag do not repair the missing relationship.

## Source node

Record repository or owner, revision or content digest, version source, relevant generated inputs,
and whether the candidate intentionally includes uncommitted source. A tag without the revision it
resolves to is mutable lineage.

## Build node

Record the build command or workflow run, material toolchain and dependency versions, platform and
architecture, configuration or feature set, and build invocation identity. Distinguish a rebuild
from promotion of an existing artifact.

## Artifact node

Record artifact ID, kind, version, digest, signature or provenance, and storage locator. Common
kinds include package archives, wheels, containers, app bundles, installers, update metadata,
plugins, generated prompts or roles, and static web bundles.

An artifact digest connects bytes; it does not establish that a consumer selected them.

## Distribution node

Record registry, channel, update feed, marketplace, environment, bucket, or package repository and
the immutable artifact identity it exposes. Mutable labels such as `latest`, `production`, and
friendly release names should resolve to an immutable digest or revision at the time of operation.

## Target and runtime node

For installed releases, identify install root, selected executable or app bundle, plugin loader,
service wrapper, user scope, and version/digest readback. For hosted releases, identify account,
project, service, environment, deployment/revision, route, and traffic allocation.

The installed file and the running process can differ; the deployed revision and routed revision
can differ. Record both when selection is part of the incident or release.

## Consumer observation

Tie each important observation to a target and release identity:

- command or app version plus the public job exercised;
- request, trace, log, or metric carrying deployment/revision identity;
- browser or client path routed to the intended release;
- update adoption or mixed-version state;
- product outcome and material regression signals.

Do not infer feature behavior from a generic health check.

## Recovery node

Record the previous known artifact or deployment, the mechanism that returns consumers to it, and
state that may not roll back with code: schema and data migrations, cache format, external effects,
configuration, credentials, and client updates. When rollback is unsafe, identify the forward
repair path and containment option.

## Drift patterns

Investigate when:

- the build claims one revision but the artifact metadata or digest differs;
- registry or feed labels point at unexpected bytes;
- installation succeeded but PATH, app selection, or plugin cache resolves an older target;
- a deployment exists but traffic still routes elsewhere;
- release notes or examples describe behavior absent from the selected target;
- rollback restores code but not schema, data, cache, or external effects.

For several artifacts or targets, keep one short record per artifact (identity, digest, channel)
and per target (identity, selected runtime, traffic or adoption, consumer observation), plus the
recovery node. For one linear release, the textual chain above is clearer.
