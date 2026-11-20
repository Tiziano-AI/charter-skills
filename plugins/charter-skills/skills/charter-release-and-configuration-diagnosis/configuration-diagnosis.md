# Configuration Diagnosis

A setting is an input to a computation, not a property of the file displaying
it. The same bytes can produce different behavior in two processes because
their reachable inputs, resolver or capture time differ. Start at the reader
performing the disputed behavior: which process or request, launched how,
consumes which setting? This makes the visible file a hypothesis rather than
the assumed repair target.

When the reader reports the winning source, the answer can be short: name
that source, the observation that showed it and, if a different result is
wanted, the input that would change it. Explaining why a setting wins does
not require changing it.

## Configuration is a computation over time

The effective value depends on more than precedence:

```text
reachable inputs -> merge/replace -> normalization -> selection -> captured value
```

Files, environment, flags, profiles, generated layers and request overrides
contribute only if this reader reaches them. A launch service can give a daemon
a different environment from a shell. A child can inherit a snapshot rather
than reread the file. Build-time substitution cannot be repaired by changing
a runtime environment variable.

Absent, empty, null, invalid and unreadable can have different semantics.
Deep merge, append, replacement and deletion markers are different operators.
Aliases, enum mappings and path resolution can legitimately transform the
selected value after precedence: a relative path resolves against the
consumer's working directory, which for a systemd system service defaults to
`/` rather than the directory the shell was in.

Distinguish the logical setting from its effective representation. A documented
mapping explains a difference; an arbitrary mismatch does not. The contrast
determines the search: if shell and service disagree, examine launch inputs;
if one process ignores a file edit, examine capture; if two diagnostic surfaces
disagree at the same time, examine their readers before changing values.

Presence is often the hidden branch. A fallback written as `value or default`
can erase an intentional false, zero or empty string. Conversely, treating an
invalid explicit path as absence can silently select a different account or
profile. Correct resolution preserves the product's meaning of presence,
validity and omission rather than imposing one convenient truthiness rule.

## Diagnose with the closest observation

Prefer the actual resolver's readback, with value, provenance and capture
time. Ask for the setting by name where possible: for Git,
`git config --show-origin --show-scope --get <key>`. When a tool provides a
broad diagnostic such as `pip config debug` or `npm config ls -l`, select
only the relevant non-secret fields before displaying output. A service
manager can show what it hands a job:
`systemctl show -p Environment,EnvironmentFiles <unit>` reports what systemd
has loaded (`EnvironmentFiles` names the files; systemd reads their contents at
each start, so `/proc/<pid>/environ` shows the values), while `systemctl cat <unit>` shows files on disk that it may not
have reloaded; on macOS, `launchctl print gui/$(id -u)/<label>` shows a job's
program and environment. On Linux, `/proc/<pid>/environ` holds the environment
a running process received at exec, not changes it made afterward. Filter
these to the keys in question, since environments carry credentials.

A status command that loads today's file proves neither an already-running
process's snapshot nor which executable the app launched. Observe as close to
consumption as the contrast requires: a normalized request can distinguish
parser and resolver defects from downstream interpretation; a startup
snapshot can distinguish a stale daemon from a wrong file. When the resolver
cannot be observed, its source can establish how it should work, though not
the value a running process holds.

[Reader and precedence analysis](references/configuration-diagnosis-workflow.md) has a table of
contrasts and the observation that separates each, and covers lossy
normalization when the logical and wire values differ.

## Repair the owner, not the display

The correction follows the broken dependency: remove an unintended shadowing
override, align divergent readers, propagate a lost value across a launch seam,
repair normalization, regenerate a projection or reload a stale consumer.
Restart changes captured state, not precedence. It can repair a daemon holding
old values but cannot repair a launcher that supplies the wrong environment;
the next start will reproduce that defect.

Preserve deliberately different profiles and sources owned by other products.
When several programs write one file, change each field through the program
that writes it; a hand edit to a generated field is reverted at its next run.

Feedback comes from the original contrast. Does the setting now reach the
consumer, and does an intentional neighboring override still win? Identical
profiles are not the goal; intelligible differences are. The answer names the
winning source and capture point with the effective value, the readback that
showed it, the change, and what that change also reaches: a restart the
consumer needs before it captures the value, or other consumers of the same
layer. If the repair changes the public schema, give
`charter-codebase-analysis-and-change` the affected readers, writers and
stored values. If the expected reader never ran, trace [the build the
launcher or route actually selects](release-engineering.md) before editing
another setting.
