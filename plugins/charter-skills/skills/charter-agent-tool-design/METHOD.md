# Charter · Agent Tool Design

A tool an agent calls, whether a command-line program, an MCP server's tools
or a plugin a host loads, is a protocol with a human shell. The caller sees
only names, descriptions, help or schemas, and results, and from those it must
choose the target, the call and its next action. A pleasant surface that hides
the target or the outcome is still an unreliable protocol.

## Start from the caller's job

Derive operations from the job the caller performs and the decision it makes
after each call. For invoicing that may be finding the right account,
inspecting a draft and issuing it; an endpoint tree describes transport and
does not reveal that issuing a draft differs from editing one. Before designing
flags or schemas, write the principal job and one plausible failure as a short
sequence of calls. Missing identities and transitions show up there first.

Not every tool needs the whole method. A deterministic single-file transform
needs one well-named command with exact errors; plan, status or a job registry
would create state and recovery obligations without helping its caller.
Terminal styling is not a protocol question. Operating an existing CLI, server
or plugin belongs to its own guide; there the answer is the right call.

## One core, several surfaces

The same product is often a CLI, an MCP server and a plugin at once. Keep
domain operations, target resolution, authentication and configuration in one
core and make each surface a thin exposure of it; two surfaces with their own
resolvers will disagree about which account or file a call touches. Choose
surfaces by the caller's host:

- A CLI reaches any agent with a shell, composes in pipes and scripts, and
  costs context only when the agent reads its help.
- An MCP server reaches hosts that cannot run commands, and lets the host list
  each tool, show the inputs and ask the user before a call.
- A plugin or extension is the unit a host installs, enables, configures and
  removes; it may bundle commands, skills, hooks or an MCP server.

Add a surface when a real caller cannot use the existing one. When agents with
a shell already use the CLI, a missing workflow usually needs a better command
or a companion guide, not a second surface.

## Separate three contracts

**Capability:** which operation is offered, with which inputs, results and
errors? Use nouns for durable objects and verbs for meaningful transitions.
`invoice void` or `release_promote` exposes constraints that a generic
`update` hides, so the tool can reject an illegal transition before a provider
call and its help can say what survives. Generic CRUD fits a resource with no
stronger lifecycle. Consolidate the calls that implement one transition into
one operation instead of exposing every internal method and leaving the caller
to sequence them.

**Exposure:** how does the caller or host discover, enable, name and present
it? Package metadata, configured registration, a listed catalog entry and
actual callability are distinct. The name, description and schema are the
prompt the model selects from: state the job, the accepted identity, whether
the call reads, previews or commits an effect, and what it returns. Similar
names with subtly different effect boundaries make selection harder. Dynamic
tools may appear only after discovery or permission, and a cached definition
can outlive its implementation. Descriptions, schemas and results all enter
the model's context as text from the tool's side: treat results as data, an
annotation as a hint rather than permission, and a definition that changed
after approval as needing approval again.

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

Unattended calls must not depend on someone answering a prompt or exiting a
pager, even when an agent's host offers a terminal and writable stdin. Prompt
only when interaction is enabled and stdin is a terminal; accept explicit
flags such as `--yes` or `--no-input`. When a required choice is missing and
interaction is disabled or unavailable, fail with an error that names the
flag and, for an ambiguous target, lists the candidates. In machine mode
stdout carries only the documented JSON value or stream; progress and prose
go to stderr.

Preview and apply separate selection from effects when the target set is
computed, large or hard to reverse. A preview is worth having only if it shows
the same normalized targets apply will use; bind a consequential plan to the
preimages it read and recheck them at apply. An obvious reversible edit of one
object gains little from a separate plan. A raw escape hatch shares target
resolution, authentication and effect semantics with the domain operations; it
covers gaps and is not a second backend.

## Versions change independently

Host and extension can upgrade separately, and a running session can keep a
cached schema that validates input against one version while the call reaches
another. Give a changed meaning a new name instead of reinterpreting an
existing parameter, and reject a call shaped by an incompatible definition with
an explicit stale-definition error rather than guessing what it meant.
Refreshing discovery repairs a stale card, not a host that never supported the
operation. A tightly bundled extension can rely on coordinated versions; a
separately updated plugin needs explicit compatibility and refresh behavior.

## Disable and uninstall without losing ownership

Disabling normally stops new invocations. It does not end durable jobs or
revoke credentials, and the extension may not be told at all. Uninstalling
removes package-owned registrations and files, while in-flight workers, remote
objects, shared caches and user data can have other owners. For an in-process
read-only formatter, unloading is enough. For a queued remote export, removing
the registration leaves accepted jobs alive; their identities and results must
stay reachable through an owner that survives removal, such as the provider's
own job list. State which effects the design performs: stopping new calls,
quiescing running work, removing package-owned files, keeping user data and
remote objects, and, as separate effects, revoking credentials or deleting
external state.

## Depth

- [CLI command model](references/command-model.md) when designing a CLI's
  grammar, help, machine output, streams or exit codes.
- [Configuration and diagnostics](references/auth-config-json-doctor.md) when
  profiles, credentials, `doctor` or error fields are in play.
- [Mutations](references/write-safety-raw.md) for preview and apply, timeout
  outcomes, multi-phase and destructive operations, raw requests.
- [Host discovery and lifecycle](references/host-discovery-and-lifecycle.md)
  when a host discovers, caches, approves or cancels tools, or a response must
  fit a model's context.
- [Companion guide](references/companion-operation-guide.md) when operating the
  tool needs a skill that help cannot carry.
- [Runtime selection](references/runtime-selection.md) when choosing the
  language or runtime of a new CLI or server.

Getting the installed copy to its callers (install shape, `PATH` shadowing,
packaged resources, upgrade) is `charter-release-engineering`.

The test of the design is an unfamiliar agent completing the principal job
through the actual host and recovering a plausible failure; a package unit test
cannot show discovery by a running host with its own caches. Repeated raw
requests suggest a missing domain operation, repeated source reading missing
help or diagnostics, repeated parsing of prose a missing machine contract. None
of them means every provider endpoint should become a public command.
