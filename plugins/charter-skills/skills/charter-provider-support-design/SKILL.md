---
name: charter-provider-support-design
description: Design capability support across providers, models or backends; decide
  selection, adaptation, degradation and fallback across transports and platforms
  without losing the user's requested behavior or constraints. Account setup and runtime
  operations belong to the owning integration.
metadata:
  content_version: charter-provider-support-design@2026.10.16.0
---
# Charter · Provider Support Design

Support is the relationship between a user-visible promise and a particular
execution path. A provider name is too coarse: one model may support images but
not structured output, or one transport may omit a feature its sibling exposes.
Describe the capability and the dimensions that can change it—provider/model or
backend, version, host/transport, region or account tier, and selection mode.

The central design question is equivalence: which differences leave the user's
job intact, which require a narrower promise, and which change the choice the
user made? A common interface can normalize syntax. It cannot by itself make
latency, quality, privacy, cancellation or effect guarantees equivalent.

Start by naming the capability the user asked for, the path that ran or will
run, and whether the two are the same. When one path is exposed and implements
the capability directly, that statement and the one branch that could break it,
such as an override, a quota failure or an unsupported input, are the whole
answer. The support states below, and a per-lane record, earn their place when
several paths are exposed or a substitution is disputed.

## Separate selection from capability

A configured default, an explicit override, a router's choice and the path that
actually ran may differ. Selection is part of the feature, not setup around it:
forcing a model directly bypasses the default router whose behavior may be
wrong. Keep the request and effective path together so a successful substitute
cannot be mistaken for support on the requested path.

Classify the useful behavior:
- native support implements the promise directly;
- adaptation preserves it through a known transformation;
- degradation offers a narrower result;
- unsupported means the capability is absent;
- unavailable means a supported path cannot run now;
- unknown means evidence has not settled it.

These states predict different interventions. An unavailable local model may
need startup, not a new adapter; an unsupported modality needs another path or
a narrower promise, not retry. Unknown is an evidence gap, not a failure or
automatic prohibition. Source inspection or a bounded admitted probe can settle
it where consequences permit. Catalog presence alone does not settle it.

## Distinguish client guarantees from provider premises

Controlled crashes, failed writes and concurrent calls can expose client
recovery and concurrency defects. A synthetic timeout can reveal duplicate
submission by retry logic; provider-side deduplication instead depends on the
adopted idempotency contract and its scope. Ground modeled provider response
shapes, event ordering and effect guarantees in the adopted specification,
SDK or source, or authorized observations of that path.

When actual behavior contradicts the fixture, correct the mistaken wire
mapping or capability assumption, or expose a genuine provider incompatibility.
Extending the fixture to accept an invented protocol preserves the mismatch
instead of repairing integration.

## Design substitution deliberately

Fallback changes the path; adaptation changes representation on a path.
An adapter that translates a lossless enum mapping preserves meaning. An
adapter that silently drops an unsupported document image does not; it has
degraded the capability even if the request succeeds. Compare semantics,
quality, cost, latency, privacy, residency, attribution and repeatability.

A transport change can leave capability selection unchanged, or activate a
different route. Verify the actual selector rather than inferring one from
a configuration flag. Preserve logical settings separately from provider wire
representations where native mapping is intentional.

Automatic fallback is suitable when the product promise already includes that
substitution and its consequences. It is unsuitable when a named local model
expresses a no-upload choice, or an explicitly selected provider is part of
the result's reproducibility. A visible label after upload cannot repair that
breach. Deny or ask for the real choice before substitution in those cases.

Show users the changed capability or consequence and any choice they need to
make. An equivalent substitution within accepted product-managed routing need
not expose backend selection as a new task; retain requested and effective
paths in diagnostics, and name them in the primary surface when the user's
selection or the consequence makes those identities relevant.

Timing changes the problem. Before transmission, fallback is a routing choice.
After possible transmission, switching providers can duplicate effects or cost;
reconcile the first operation or preserve its unknown outcome before deciding
whether a distinct attempt is permissible. Provider B cannot deduplicate an
unknown operation at provider A merely by receiving the same request text.
Which risk applies depends on who performs the effect. When the model returns
text, or a tool call the caller executes after the response, a repeat risks
duplicate cost and a different answer. A provider that performs an effect
itself, such as a submitted video job, a sent message, a stored file or a
provider-hosted tool call (remote MCP, code execution) made during the
request, can perform it twice.

[Support design](references/workflow.md) develops the lane, its states,
selection intent and substitution, and the per-lane record when several paths
must stay coherent. [Worked patterns](references/lane-example-patterns.md)
contrast default, override, adapted, degraded and unavailable cases.
[Fallback UX](references/fallback-ux-and-operation-boundaries.md) turns the
decision into copy, user control, diagnostics and owners of the operations.

Carry the choice into the router, diagnostics and public promise, using the
owning product integration for operations. Useful feedback observes the branch
whose meaning is disputed: an exposed override, quota failure, degraded input
or fallback decision, not a quota of provider calls. A syntactically valid
response with missing capability is evidence against the support promise.
A successful default run does not certify every model, region, account or
override.
