# Authentication, Configuration, Doctor, And Errors

Configuration and diagnosis should let an operator explain the effective invocation without reading
implementation code or exposing credential material unnecessarily.

## Configuration model

Define one precedence order across sources such as:

1. explicit command arguments;
2. selected profile;
3. environment variables;
4. user configuration;
5. project configuration;
6. product defaults.

The exact order is product-specific; what matters is that the command and diagnostics use the same
resolver. Profiles should name coherent target contexts, not become bags of unrelated overrides.
Relative paths need an explicit base. Working-directory discovery should stop at a documented
boundary and expose which file won.

Provide a command or diagnostic view that shows effective non-secret values, source category, and
shadowed definitions when precedence is a frequent source of failure. Distinguish “unset,” “set to
empty,” “invalid,” “unreadable,” and “defaulted.”

## Authentication shape

Prefer the provider's standard credential mechanism when it is mature: environment reference,
well-known config, platform key store, workload identity, or provider CLI session. Design for
multiple accounts or targets when the domain requires them.

The CLI normally needs to report credential **source and status**, not credential bytes. Avoid
reading secrets merely to display them. A one-off secret flag is often visible in shell history and
process listings; prefer stdin, a file descriptor, key store, or provider-native login for ongoing
use.

Separate these states:

- no credential source selected;
- credential material unavailable;
- credential parsed but rejected;
- credential valid for one target but insufficient for the requested scope;
- provider unreachable, so validity is unknown;
- authenticated identity established.

## `doctor`

`doctor` explains why the public command path can or cannot operate. It should avoid changing state
and should remain useful when credentials, network, config, or optional dependencies are missing.

Choose checks from the product:

- executable and product version;
- selected profile, target, endpoint, region, account, or workspace;
- config locations found and the source of each effective setting;
- credential source category and authenticated identity when a bounded check is possible;
- required executable, library, service, socket, app, or filesystem dependency;
- local database, queue, cache, bridge, or support-root health when the CLI owns it;
- network or provider reachability separated from authentication and authorization;
- pending, failed, stuck, or recoverable local operations;
- the narrow setup or repair action corresponding to each failed check.

Run independent checks independently so one missing prerequisite does not erase later diagnostics.
Use stable check IDs and states such as `ok`, `warning`, `blocked`, `unavailable`, and `not_applicable`
when machine callers need them.

Do not make `doctor` a full inventory or operation transcript. Link or name the deeper diagnostic
command for logs, events, queue rows, or provider responses.

## Version and lineage readback

Source execution, a built artifact, an installed launcher, and the executable selected from `PATH`
can all be different versions, so the command should say which one is answering. `--version`,
`version --json`, or `doctor --json` can report:

- product version and executable path;
- build revision or package version when relevant;
- runtime or interpreter version when behavior depends on it;
- config home and selected profile;
- plugin or bridge versions that change the command contract.

Keep one canonical version source so help, package metadata, and diagnostics do not drift.

## Error model

Error detail follows the caller's next action. An invalid value in a pure
transform may need only a stable code, the rejected input and its accepted
form. A failure across services or after a possible effect needs more context.
Include the distinctions that change diagnosis or recovery:

- what operation failed;
- which target or object was involved;
- whether any effect may already have occurred;
- whether retry is safe and under what identity;
- which input or dependency the operator can change;
- which request, attempt, or operation ID supports deeper diagnosis, when one exists.

A machine error benefits from a stable code, message and relevant structured
fields; nested causes belong where they explain the failure. These are semantic
needs, not a mandatory envelope for every error. Preserve provider status and
response detail in an appropriate diagnostic field rather than flattening every
failure into `unknown error`.

Keep usage errors, local setup failures, network failures, authentication, authorization, not-found,
conflict, rate limit, timeout, provider rejection, and partial completion distinct when recovery
differs.

## Common design failures

- The command reports the configured value while the runtime uses a different resolver.
- `doctor` crashes at the first missing dependency or requires successful login.
- Credential absence is reported as provider outage.
- A default target changes with working directory but is not shown.
- JSON errors are prose strings while success is structured.
- Retry guidance ignores whether the first attempt may have produced an effect.
- Debug mode dumps unrelated internal state rather than the causal operation context.
