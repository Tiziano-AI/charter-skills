---
name: charter-agent-tool-design
description: 'Design CLIs, MCP servers and plugins or extensions that agents call:
  operations, identities, results, errors, host discovery, versions and what survives
  disable or uninstall, so callers act without reading source. Operating an existing
  tool follows its guide.'
metadata:
  content_version: charter-agent-tool-design@2026.11.25.0
---
# Charter · Agent Tool Design

Start with a caller's job and the decision after each call. For an invoice,
find the account, inspect the draft and issue it. What will the caller hold if
issuing succeeds but the response is lost? The answer shapes the operations,
identities, help and results before flags or endpoint names are chosen.
A deterministic single-file transform may need only one command with exact
errors; adding a registry creates recovery obligations. Terminal styling is
not a protocol problem. For operating an existing tool, use its own guide.

## One core, several surfaces

A CLI suits shell callers, an MCP server can expose tools to hosts without a
shell, and a plugin is a unit of installation and removal. Add a surface only
for a caller the existing one cannot serve. Share domain operations, target
resolution, authentication and configuration; native names need not be
identical but should lead to the same recognizable product. Before choosing
spellings or exposing endpoints, read [the command model](references/command-model.md).

## Separate three contracts

**Capability:** expose the actual lifecycle transition. `invoice void` can
reject a change that a generic `update` hides; CRUD is right when the
resource has no stronger lifecycle. Give callers one operation per meaningful
transition, not an endpoint tree they must sequence. For choosing its nouns,
verbs and cross-object spellings, use [command grammar](references/command-model.md).

**Exposure:** registration, listing, discovery after permission and actual
callability are different. A tool's name, description and schema must tell
the caller the job, accepted identity, effect boundary and result. A changed
definition can invalidate approval; an annotation or tool result cannot
grant it. [Host discovery](references/host-discovery-and-lifecycle.md) covers
these boundaries when a model selects the tool from a changing catalog.

**Execution:** what can the invocation affect, and who owns its lifecycle?
Schema validation, authorization, transport acceptance, effect completion and
result delivery are separate boundaries, and the host or operation owner
enforces the actual destination and scope.

These contracts fail differently. If the caller cannot find a tool, changing
its handler cannot fix discovery. If the tool is callable but its schema cannot
express the job, refreshing the catalog cannot fix capability. If the provider
completed work but the host lost the response, reinstalling cannot undo the
effect. Start from the step where the caller's job fails.

## Identities and results carry the next action

Every identifier a later call needs has a discovery path from what the caller
holds: a name, URL, current directory or parent object. Return stable IDs with
human discriminators; an ambiguous name returns the candidates and what tells
them apart, never an arbitrary pick. Names serve discovery, while a
consequential effect targets a stable ID. Keep three identities apart: a
resource ID says what changes, an attempt ID names one invocation, an
idempotency key names the logical effect. Confusing them makes recovery unsafe
even when the happy path looks clean.

A result holds what the caller needs to continue: data for a bounded read, with
its scope and whether it is complete; an operation identity and state for
accepted asynchronous work; the surviving effect and the next step still allowed after
a partial failure. A command that uploads and then attaches a file returns the
upload's identity if attaching fails, so recovery attaches instead of uploading
twice. Give large reads a default limit and a continuation cursor, so a capped
result never reads as a complete search. An empty search is successful data;
accepted work is not completed work.

Errors follow the caller's different next actions. Invalid input, missing
setup, denial, conflict, timeout, partial completion and unknown outcome do not
collapse into one retryable failure, and each error names what the caller can
change: the accepted values, the missing flag, the command that waits until the
resource is ready. An MCP server reports execution failures inside the tool
result with `isError: true`, where the model can read them and correct its
call; protocol errors are for unknown tools and malformed requests. After a
timeout that may have produced an effect, return the operation identity and a
status path rather than inviting a blind retry; reconciling the unknown outcome
is `charter-workflow-recovery`'s job.

## Non-interactive calls and safe effects

A machine-mode call must finish without prompting or invoking a pager.
Return a structured choice error if a needed flag or target is missing;
stdout carries only the promised value or stream, diagnostics go to stderr.
Use [the command model](references/command-model.md#non-interactive-use)
for the interaction and output contract.

Preview and apply separate selection from effects when the target set is
computed, large or hard to reverse. A preview is worth having only if it shows
the same normalized targets apply will use; bind a consequential plan to the
preimages it read and recheck them at apply. An obvious reversible edit of one
object gains little from a separate plan. A raw escape hatch shares target
resolution, authentication and effect semantics with the domain operations; it
covers gaps and is not a second backend.

## Versions change independently

A cached definition can outlive its implementation. Reject a call made to an
incompatible schema rather than silently changing its meaning. Before designing
upgrade behavior, follow the [host's discovery and caching path](references/host-discovery-and-lifecycle.md).

## Disable and uninstall without losing ownership

Disabling new calls does not cancel accepted work or revoke credentials.
An in-process formatter can simply unload; a remote export needs a way to
recover its ID and result after removal. Choose the surviving owner before
designing uninstall; [host lifecycle](references/host-discovery-and-lifecycle.md)
separates package-owned files, accepted jobs, user data and external state.

## Depth

- [CLI command model](references/command-model.md) for help, exit codes or streams.
- [Configuration and diagnostics](references/auth-config-json-doctor.md) for
  profiles, credentials, `doctor` and actionable errors.
- [Mutations](references/write-safety-raw.md) for preview, timeouts,
  multi-phase operations, destructive commands and raw requests.
- [Host discovery and lifecycle](references/host-discovery-and-lifecycle.md)
  for tool caching, approval, cancellation or context limits.
- [Companion guide](references/companion-operation-guide.md) when operating the
  tool needs a skill that help cannot carry.
- [Runtime selection](references/runtime-selection.md) when choosing the
  language or runtime of a new CLI or server.

If callers meet a different copy or schema than the one designed, take the
expected artifact and host to `charter-release-and-configuration-diagnosis`:
trace install shape, `PATH` shadowing, packaged resources and upgrades to
the version actually selected.

The test of the design is an unfamiliar agent completing the principal job
through the actual host and recovering a plausible failure; a package unit test
cannot show discovery by a running host with its own caches. Repeated raw
requests suggest a missing domain operation, repeated source reading missing
help or diagnostics, repeated parsing of prose a missing machine contract. None
of them means every provider endpoint should become a public command.
