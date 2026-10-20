# Host Discovery and Lifecycle

Use this when a host stands between the tool and the model: an MCP client, a plugin loader, an
extension host, or an agent runtime with tool search. The host discovers, caches, approves,
presents, cancels, and removes tools, and each of those steps can separate a correct package from a
usable capability.

## Definitions and results are read by a model

A tool's name, description, and schema reach the model as text and decide selection. Name tools in
the vocabulary of the task, and when a host loads many tools, namespace related ones by service or
resource (`asana_search`, `jira_search`). Tool search and progressive discovery reduce schema
noise, but only if the operation can be found in the task's words; a caller cannot assume that a
hidden tool is callable from a remembered schema. Keep accepted arguments and errors aligned with
the implementation: a clearer description cannot repair a backend that returns the wrong account's
results.

Results enter the same context. A count answers a count query; a recovery call needs an exact
operation ID and an outcome-unknown state. These are semantic needs, not a mandatory envelope for
every tool. Keep units, timestamps, account or query scope, and source distinctions next to the
values they qualify, and do not let a concise success label merge queued, submitted, delivered, and
received into one event. Some hosts cap the size of a tool response, so give large reads sensible
default limits, filters, or a choice between a concise and a detailed form, and make truncation say
how to get the rest.

Structured output helps when the caller relies on stable fields; an MCP tool can declare an
`outputSchema` so clients validate its `structuredContent`. Prose helps when relationships need
interpretation. Structure does not make an uncertain fact true.

## Trust at the host boundary

Definitions and results come from the tool's side of the boundary. The MCP specification requires
clients to treat tool annotations as untrusted unless they come from a trusted server: an
annotation that calls a tool read-only describes intent and enforces nothing, so the host or
operation owner enforces the actual destination and scope. Tool output is data for the model, not
instructions to it. A host that approved a definition should treat a changed description, schema,
or permission as a new approval; Chrome, for example, disables an extension whose update asks for
more privileges until the user accepts them.

## Versions change independently

Host and extension share a protocol, not a release cadence or process lifetime. Hosts cache names,
schemas, permissions, and catalogs, and an extension can upgrade while a session keeps old
metadata. Decide which version owns validation, when discovery refreshes, whether a running
invocation keeps its implementation, and how an incompatible call fails. A running host also works
from the configuration it captured at start, which can differ from the configuration file now. An
MCP server that declares the `listChanged` capability should send
`notifications/tools/list_changed` when its tools change, so clients list them again; a client that
ignores it keeps a stale catalog.

With deferred discovery, a missing catalog row may mean "not loaded here yet," and a stale row may
name an operation that is no longer callable. Use the host's own discovery and diagnostics rather
than a second, shadow registry.

A useful capability path is:

```text
package -> host discovery/configuration -> exposed callable -> invocation
        -> execution/effect -> delivered result
```

These are not universally ordered states: a permission change can remove exposure, a process can
survive package removal, and a session can keep a card after disablement.

## Cancellation is not undo

Define what connection, execution, and shutdown timeouts mean. Propagate cancellation to the worker
that performs the effect, and say whether it stops acceptance, stops work, or only stops waiting.
Keep four observations distinct: acknowledgement of the cancellation request, the operation's
reported lifecycle state, termination of the worker, and the disposition of external effects.
A successful cancellation response can confirm a state transition without proving the worker has
stopped; even a stopped worker cannot undo a provider request already accepted.

Use the cancellation mechanism the exposed protocol supports. A fire-and-forget notification,
such as MCP's `notifications/cancelled`, supplies no acknowledgement by itself.
For [MCP task-augmented requests](https://modelcontextprotocol.io/specification/2025-11-25/basic/utilities/tasks#task-cancellation),
cancellation uses `tasks/cancel`, not `notifications/cancelled`; check the peer's
advertised `tasks.cancel` capability. A successful response reports `cancelled`,
but does not establish that execution stopped or external effects were undone.
Retrieve needed recovery information before cancelling: a receiver may delete
the cancelled task immediately, even while an external effect survives.
A caller that must recover
after cancellation needs an operation identity, readback and documented terminal semantics,
whether those come from protocol tasks or the product's own lifecycle surface.

A late result can belong to a canceled waiter while the provider operation completed. If an effect
may exist, return its identity and a way to read it; a missing terminal response is not permission
to replay. Idempotency binds the same logical operation, not repeated transport bytes, and a
wrapper over a provider without readback or deduplication preserves the unknown outcome rather than
simulating certainty.

## Diagnostics by boundary

Diagnostics use the same resolver and identities as invocation: package and host version, discovery
state, exposed operations, configuration source, permission decision, and operation identity. Point
each failure at its boundary: absent package, discovery, disablement, configuration, permission,
provider, malformed result, or effect state. Local setup checks stay useful without launching work
or requiring a successful login.
