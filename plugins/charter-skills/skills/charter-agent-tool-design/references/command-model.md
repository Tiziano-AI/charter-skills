# CLI Command Model

Design the CLI from the product's objects, state transitions, and repeated operator jobs. Do not
start by mapping every API endpoint or internal function to a subcommand.

## Derive the grammar

Start with the shortest first success. Add a recovery or neighboring job when it reveals a
different object or transition. Identify the nouns that persist and the verbs that change or
inspect them; a fixed quota of examples does not determine the grammar.

Two common shapes are:

```text
tool <noun> <verb> [identity] [options]
tool <verb> <noun> [identity] [options]
```

Choose one based on how operators think and keep it predictable. Nested nouns are useful when the
relationship is real (`project deployment logs`); deep nesting that mirrors an implementation tree
makes discovery harder.

Use domain verbs where generic CRUD obscures meaning. `release promote`, `invoice void`, and
`job retry` express stronger lifecycle constraints than `update` or `execute`. Avoid vague verbs
such as `sync`, `fix`, `process`, and `run` when they hide several effects.

## Discovery and identity

An agent must be able to obtain the identity a later command requires. Provide a path from the
user's reference—name, URL, slug, current directory, account, or parent object—to a stable product
identifier.

Useful patterns include:

- finite lists with filters and explicit pagination;
- `get` or `show` by stable ID;
- `resolve` when names, URLs, or aliases need disambiguation;
- parent-scoped listing when identities are only unique within a container;
- current-context output when a repository, profile, or working directory supplies scope.

Do not require callers to scrape display tables for IDs. When a name is ambiguous, return candidates
and the discriminators needed to choose rather than silently selecting one.

## Command families that earn their place

Add a family only when the product owns the state behind it:

- `list`, `search`, `get`, or `show` for observation;
- `create`, domain transitions, or explicit destructive verbs for mutation;
- `plan` or `preview` when the mutation's target set or consequence is not obvious from arguments;
- `status` for a concise lifecycle view;
- `doctor` for setup and dependency diagnosis;
- `logs`, `events`, or `history` when ordered context is a real product object;
- `retry`, `resume`, `cancel`, `rollback`, or `repair` when the runtime owns those transitions;
- `raw` or `request` for coverage gaps and diagnosis, not as the primary user experience.

A local transform tool may need one well-designed command and excellent errors; a provider operator
may need discovery, mutation, and polling across several resources.

## Help as the first interface

Top-level help should state the product job, show the principal nouns or workflows, and include one
realistic first command. Subcommand help should explain:

- target identity and scope;
- required versus defaulted input;
- whether the command observes, plans, or changes state;
- output modes;
- important lifecycle or recovery consequences;
- one representative example.

Keep advanced transport and provider flags out of the first screen unless most invocations need
them. Shell completion should follow the same noun, verb, and option vocabulary as help.

## Non-interactive use

An unattended caller must be able to finish without answering a prompt,
picking from a menu or quitting a pager. Some agent hosts provide a PTY and
writable stdin; that capability does not make interactive input dependable in
every invocation. Decide interactivity from the streams and explicit controls,
not from a separate "agent mode" the caller has to know about:

- prompt, show pickers, or open a pager only when interaction is enabled and stdin (and, for a pager, stdout) is a terminal;
- accept `--no-input` to forbid interaction outright, and `--yes` or an explicit flag for each
  confirmation a script must be able to give;
- when a required value or confirmation is missing and interaction is not possible, exit with a
  usage error that names the flag to pass and, for an ambiguous target, lists the candidates with
  their IDs;
- drop color and animation when output is not a terminal or `NO_COLOR` is set to a non-empty value.

## Machine-readable output

Under a machine mode such as `--json`:

- reserve stdout for one documented JSON value or a declared stream format;
- send interactive progress to stderr or suppress it;
- keep field names and types stable within a versioned contract;
- return stable object IDs, lifecycle states, and cursors rather than formatted labels only;
- represent absence, emptiness, partial results, and failure distinctly;
- expose request, attempt, or operation IDs needed for later status and recovery;
- never mix ANSI decoration or explanatory prose into the JSON channel.

Use a single object for bounded results, an array only when pagination is irrelevant and size is
bounded, and JSON Lines for a deliberate record or event stream.

Human and JSON output can differ in presentation but must describe the same effect state: prose
can explain a conflict while JSON carries its stable code and the current revision.

## Pagination and streams

Finite collection output should identify the applied limit, returned count, and continuation token
or next offset when more data exists. Apply a default limit to collections that can grow; do not
silently fetch an unbounded provider collection or silently discard later pages. When an agent
reads the output into its context, a field selection or a summary form lets it ask for less.

For streams, define event identity, ordering scope, reconnect cursor, heartbeat, terminal events,
and what stdout contains after interruption. A `--follow` command should not make a caller guess
whether EOF means completion, disconnect, timeout, or cancellation.

## Exit behavior

Map outcomes to a small stable exit taxonomy. The common convention is 0 for success, 1 for a
general failure, and 2 for invalid usage (Python's `argparse` exits with 2 on a parse error). A
process killed by signal N reports 128+N in the shell, so Ctrl-C shows as 130; on Ctrl-C, stop
promptly and bound any cleanup. Add further categories only when callers act differently on
them—for example not found, conflict, authentication, unavailable dependency, timeout, or partial
completion—and document them as part of the contract.

An empty successful search is usually data, not a process error. A remote request that was accepted
but not completed should return its operation identity and state rather than pretend the final job
succeeded; a condition that clears by waiting, such as an index still building, should name the
command that waits for it.

## Evolution

Command paths, flags, JSON fields, exit categories, and defaults become external contracts once
scripts or operators depend on them. Prefer additive evolution while that boundary is current. In a
greenfield replacement, remove the losing grammar completely instead of teaching two active ways to
perform the same job.
