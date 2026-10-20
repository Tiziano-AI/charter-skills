# Reader, Precedence and Capture Analysis

Configuration is a function of inputs, resolution rules and time. The observed
contrast tells which dependency to inspect: different launchers suggest
different inputs, different effective values from the same inputs suggest
different readers, and unchanged behavior after an edit suggests capture or
an unreachable input. These are hypotheses, not diagnoses from symptoms alone.

## Locate the actual read

Identify the process or session performing the behavior, selected executable,
working directory/configuration root, resolver, and moment of capture.
Useful observation points are the normalized request, process startup
configuration or an existing resolver diagnostic.

The same command name can refer to a shell launcher and an app-bundled binary.
Probing one executable establishes that executable's result, not the state of
another process already running. A correct file can be irrelevant to both.

## Follow only reachable inputs

Work backward from the read site through defaults, files, environment,
profiles, generated layers, launch-service injection and explicit overrides.
The order is product-specific. Establish whether a layer replaces, merges,
appends, inherits or deletes; do not draw a generic chain and assume last wins.

Follow post-resolution transformations: relative-path base, variable expansion,
case or alias normalization, enum mapping, provider selection and feature
activation. Distinguish:
- configured logical value;
- selected or normalized value;
- wire/runtime value after documented mapping;
- observed behavior.

For example, Python's `logging` accepts the level `WARN` and reads it back as
`WARNING`. That is a documented alias, not drift; accepting any mismatch as a
mapping would conceal a defect.

Normalization can also be lossy. If two public settings map to the same wire
value intentionally, a wire readback cannot reconstruct which was requested:
the logger above reports `WARNING` whichever spelling was configured.
Diagnostics may need both logical and normalized values to explain selection.
Do not repair that many-to-one mapping by inventing a reverse lookup and
presenting it as the original request.

## Diagnose the contrast

Common contrasts and discriminating observations:

| Contrast | Useful observation |
| --- | --- |
| shell works, service does not | service environment, executable and config root |
| file changed, behavior unchanged | capture time and consuming process snapshot |
| status says A, request uses B | compare the status resolver with the request builder |
| explicit override ignored | parsing, precedence and value propagation across the launch seam |
| one profile works | reachable inputs and normalization for each profile |
| generated file reverts after an edit | the generator that writes it and when it reruns |

A source read can establish the algorithm without proving the running value.

## Check the repair on the selected path

Remove a shadowing override only if it is not intentional. After the repair,
exercise the path that failed, and test an override, alternate launch or
stale-process case when it distinguishes the fixed rule. Intentionally
different profiles need not converge.
