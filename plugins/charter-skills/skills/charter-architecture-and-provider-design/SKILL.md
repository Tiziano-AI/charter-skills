---
name: charter-architecture-and-provider-design
description: Simplify an architecture with native or upstream primitives, or design
  support and fallback across providers, models and backends. Decide which local responsibilities
  can go without losing capability. Not a local bug fix, account setup or service
  restart.
metadata:
  content_version: charter-architecture-and-provider-design@2026.11.20.0
---
# Charter · Architecture & Provider Design

Take the behavior someone relies on and ask where it will be guaranteed in
the proposed design. If a platform primitive can take over the whole
responsibility, retire the local implementation. If it supplies a mechanism
but not the product rule, keep just that rule. Where several backends serve
the same operation, apply that comparison to the **selected path**: a provider
name or a shared method signature cannot tell you what happened to a request.

**When deciding what to build, keep or remove,** use
[Architecture simplification](architecture-simplification.md) before choosing
the replacement. Suppose two cashiers can claim the same seat. If both write
to the same database, a unique constraint on the performance and seat can
decide the winner at insert time. A separate lock service adds nothing for
that decision; the product still owns what a losing cashier sees. If the real
promise is an expiring hold followed by payment, uniqueness alone supplies
neither expiry nor reconciliation with the payment processor. Test the disputed
behavior, not just a successful reservation. The simpler design has fewer
responsibilities to coordinate, not necessarily fewer components. For a
workflow, contrast what ordinary control flow can express with the durability,
resumption or genuinely variable work that would justify an engine in
[Primitive fit and workflow choices](references/primitive-fit-and-workflows.md).

**When promising a capability on another provider, model or backend,** use
[Provider support design](provider-support-design.md) before settling what the
router should expose, adapt or refuse. Inspect the adopted version and
configuration, and enter through the actual default or override when
selection matters. Record what was requested and what ran. Validating a final
JSON object can satisfy a structured-result promise; it cannot supply valid
incremental fields to a streaming editor. That path is adapted for the former
and unsupported for the latter. A supported backend that's offline is
unavailable, not incapable; lack of evidence settles neither. When several
paths are exposed, use [Capability equivalence and routing](references/workflow.md)
to specify which promises hold on each. Use the [contrasting support cases](references/lane-example-patterns.md)
if the same failure would lead to different action for an explicit selection
and the default.

Fallback selects a different path; it does not make the first path work. An
equivalent substitution within accepted automatic routing need not interrupt
the user. A local-only transcription must not upload the recording because
the local engine is offline. Offer the change of destination *before* sending
anything. Price, quality, latency or reproducibility can distinguish otherwise
identical responses. If the first provider might already have received a job,
switching can incur a second charge or repeat a remote effect. Reconcile the
original by its identity or leave its outcome unknown; a timeout is not
permission to resubmit elsewhere. Use [Fallback and operation boundaries](references/fallback-ux-and-operation-boundaries.md)
when translating this decision into a choice, a refusal or a recovery action.

Carry an accepted ownership change to `charter-codebase-analysis-and-change`
if writers, readers or retained data must move with it. If an agent will
invoke the capability, give `charter-agent-tool-design` the supported
operation, limits and refusal meanings to expose. When equivalent interfaces
leave actual output quality in dispute, take representative work and its
quality criteria to `charter-ai-evaluation-and-session-learning`; model labels
or successful requests cannot settle that choice.
