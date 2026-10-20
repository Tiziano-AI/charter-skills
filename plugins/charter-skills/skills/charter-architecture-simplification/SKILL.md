---
name: charter-architecture-simplification
description: 'Architecture simplification before building or refactoring: use suitable
  native, standard or upstream primitives to remove unnecessary responsibilities and
  custom layers while preserving required capability.'
metadata:
  content_version: charter-architecture-simplification@2026.10.12.0
---
# Charter · Architecture Simplification

Architecture is simpler when fewer responsibilities require custom ownership
and fewer independent states must agree. Fewer files, fewer components or a
shorter diagram can conceal more coordination, a lost capability or an upstream
dependency whose behavior the product still has to repair.

Before building, this lens can avoid responsibilities the product never needs
to acquire. During refactoring, it can return ordinary machinery to a suitable
native, standard or upstream owner. In both cases the comparison is between
actual ways to deliver the required behavior, not between a complex present and
an imagined primitive that works perfectly.

## Compare capabilities at their consequential seams

A name such as "workflow engine," "agent SDK" or "transaction" does not specify
the relevant contract. Inspect the candidate's actual supported behavior at the
adopted version and configuration. Match the product's meaningful operations,
states and failure modes to that contract. A declaration in documentation, a
source path and a demonstrated integration answer different uncertainties; use
the one that resolves the live fit question.

The decisive seam is often outside the happy path: whether cancellation stops
remote work or only local waiting, which failures can be retried, whether a
stream retains partial output, how credentials are selected, or what remains
after a process restart. Inspect such semantics where the product depends on
them rather than expanding every review into a universal checklist.

Native ownership is useful evidence about where responsibility can live, not a
guarantee of fit. A primitive may be excellent at request execution and offer
no way to reconcile an uncertain external effect. A small retained component
for that gap can be simpler than replacing the primitive or pretending the gap
does not matter.

## Separate removal, transfer and residual work

For each consequential responsibility, distinguish what disappears, what moves
to a capable owner, and what the product must still do. This distinction exposes
false simplification. Removing a database may transfer durable state to a
service; replacing it with an in-memory map may instead remove recovery.

A useful custom boundary expresses the residual domain decision. For example,
it may choose an account, enforce a business transition or translate a provider
result into a product concept. It need not reimplement ordinary transport,
stream parsing or retry behavior that an existing library already owns. A thin
wrapper can still be expensive if it creates a second state machine or erases
information every caller later needs.

Keep a layer when it earns its responsibility: a stable external contract,
meaningful provider differences, a security boundary or independent release
needs may justify it. "It makes mocking easy" is insufficient if the wrapper
changes no product semantics and its tests bypass the real failing seam.
Equally, a mature adapter used by actual consumers is not disposable merely
because direct calls look shorter.

## Simplify workflows as well as code

Orchestration adds decisions about who acts, which state is authoritative, how
results combine and what happens on partial failure. For a fixed dependency
chain, ordinary application control flow may express the job more clearly than
a planner, task broker and worker fleet. For genuinely variable subtasks, a
dynamic coordinator may remove brittle branching rather than add ceremony.

Separate parallel work only where the contributions can be integrated without
losing a relationship the decision needs. Splitting one tightly coupled judgment
among workers can create more reconciliation than useful independence. An
evaluation loop earns its place when feedback can materially improve a result
and the loop has a usable stopping condition, rather than because the framework
offers one.

Simplification can also remove duplicate human work: repeated approvals of the
same settled choice, manual copying between owners, or a review queue that
exists only to reconcile redundant state. Preserve real decision rights and
effect boundaries while removing the machinery that accidentally repeats them.

## Make the survivor concrete

Describe one proposed path using the actual primitive, the residual custom work
and the disposition of what it replaces. A responsibility that is "handled
upstream" needs a named behavior at that owner; one that remains needs a reason.
Carry forward the product capability, including useful failure recovery, rather
than treating reduced scope as architectural economy.

When the remaining uncertainty is small and testable, a contained integration
can settle it. When it concerns a contractual limit or unavailable capability,
a demonstration of the happy path cannot resolve it. An unsatisfied requirement
can justify keeping the current architecture or choosing a different primitive.

[Primitive fit and contrasting designs](references/primitive-fit-and-workflows.md)
contains worked responsibility transfers and workflow choices. Cross-layer
change design owns carrying an accepted replacement through source, generators
and consumers; provider support design and agent tool design own their
distinct variation and exposure problems. This skill chooses the architecture to carry.
