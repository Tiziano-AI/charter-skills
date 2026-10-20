# Primitive fit and contrasting designs

## Replace an imitation, retain the domain boundary

Consider a client with a custom HTTP transport, retry loop, streaming parser,
event queue, transcript store and account selector. An official SDK supports
transport, streaming and ordinary retries. The question is not whether the SDK
can send a request, but which responsibilities it can actually take over.

| Responsibility | Candidate simplification | Fit question that changes the choice |
| --- | --- | --- |
| HTTP transport and stream decoding | Use the SDK implementation | Does it expose the events and partial output the product consumes? |
| Retry handling | Choose one retry owner | Which failures does it retry, and can an external effect have already happened? |
| Event queue | Remove it for direct consumption, or retain bounded buffering | Does a slow consumer need backpressure or recovery beyond the SDK stream? |
| Transcript store | Use native history when sufficient | Is the required content retrievable with the needed identity, retention and privacy? |
| Account selection | Retain the product's real selection rule | Does the SDK credential model preserve the independently selected accounts? |

If both wrapper and SDK retry, a single apparent attempt can multiply requests.
If a wrapper flattens all terminal events to success or failure, replacing it
may actually recover distinctions the native API already provides. Neither
conclusion follows just from the presence of two layers; inspect their behavior.

A product-specific operation record may remain necessary when the provider
cannot settle whether a mutation occurred. Its job is then narrow: preserve
the original operation identity and unresolved outcome for reconciliation. It
does not need to become a replacement transport or an alternative SDK.

The smallest useful custom part may therefore be account selection, domain
result mapping and exact operation custody, with execution delegated directly
to the SDK. If the SDK cannot meet the product's stream or cancellation contract,
retaining the existing implementation can be the simpler viable design.

## One state owner versus one deployment

Co-locating components can remove network seams but introduce a release seam.
A local client and a hosted service may need independent upgrades, credentials
and failure recovery. Combining them into one distribution makes the diagram
smaller while coupling consumers that need independence.

Conversely, extracting a service solely to hold a table can create schema
negotiation, transport failures and two deployment owners without supplying a
useful independent capability. An ordinary module and a transaction in the
existing database may be the better boundary.

Choose where a state transition is authoritative. If one owner commits a job
and another publishes an event, the interval between those effects matters.
A transactional outbox or an upstream primitive that already supplies the
required atomicity can reduce coordination. Replacing both with sequential
calls does not preserve that property. If the event is only a disposable cache
hint and the consumer can rederive state, insisting on transactional delivery
may instead be unnecessary machinery.

## Workflow shape follows dependencies

For a fixed "extract, classify, summarize" transformation, separate stages
are useful when each has a materially different input, method or failure
boundary. A single model call may suffice when the relationships fit together
and decomposition supplies no benefit. A workflow engine is justified by
needed durability, resumption or coordination, not by the existence of three
verbs in the specification.

A research task that discovers new questions from each source may need dynamic
planning. Forcing it into a fixed chain can merely move hidden orchestration
into prompts. The simpler architecture may be a capable loop with clear tool
contracts rather than a large branch table. The question is where the real
variability is handled intelligibly.

Parallel execution works well for independent checks whose results combine
under a defined rule. If each worker must repeatedly obtain the others'
interpretation, the split is cutting through a coupled function. Bringing the
shared judgment together can remove synchronization and contradictory local
state. Conversely, independently checking the same result can have value when
the methods can fail differently; identical workers do not automatically
provide independent evidence.

## Inspect the contract at the version that will run

An architectural proposal can cite a current upstream feature without showing
that the adopted release or enabled configuration exposes it. Conversely, an
old limitation may have disappeared. Resolve the exact capability needed from
the installed package, authoritative documentation or an appropriately scoped
integration. A feature name in release notes is a lead, not an implementation
plan.

When transfer depends on semantics, demonstrate the seam itself: a canceled
stream, a preserved identifier, a failed commit, or an account selected by the
real caller. Avoid building demonstration infrastructure that becomes a reason
to replace an otherwise capable path. The evidence should answer the design's
live uncertainty; it need not reproduce the whole upstream test suite.

## Source perspective and its limit

Anthropic's [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
distinguishes predefined workflows from model-directed agents and relates
chaining, routing and dynamic orchestration to different task structures. Its
builder experience favors composable designs while allowing added structure
when it helps. This supports comparing orchestration to actual dependencies;
it does not establish that direct API calls, fewer stages or any vendor's SDK
always win. A conceptual account of workflow design does not establish the
capabilities exposed by an installed tool.
