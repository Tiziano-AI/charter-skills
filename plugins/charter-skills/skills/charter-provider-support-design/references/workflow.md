# Capability Equivalence and Routing

One product promise can cross several implementations. Support design decides
which differences can be absorbed, which must remain visible, and which make a
path ineligible.

## The lane is the unit of support

Define the tuple precisely:

```text
capability + provider/backend + model/version + runtime/host/transport
+ region/tier/hardware + selection mode
```

Then answer:

- What product behavior is expected?
- Is this the default, an explicit override, or an automatic routing candidate?
- What limits or transformations are inherent to this lane?
- What will users experience if it is unavailable or degraded?

One well-understood lane often resolves the product decision.

## Support states predict different actions

Use states that imply behavior:

| State | Meaning | Product behavior |
| --- | --- | --- |
| `native` | capability is implemented directly on the lane | expose normally |
| `adapted` | an adapter preserves the promise with known transformations | expose and document material differences |
| `degraded` | only a narrower capability is available | narrow the promise or offer a choice |
| `unsupported` | the lane cannot perform the capability | deny before execution |
| `unavailable` | support exists but the lane cannot run now | show recovery or eligible fallback |
| `unknown` | current behavior is not established | investigate or run an admitted bounded probe; do not advertise unobserved support |

A provider may be native for one capability and unsupported for another. Keep capability identity in
every decision.

Fallback is not a support state. It is a path decision taken when the requested lane is
unavailable, unsupported or degraded, and it runs on another lane that has its own state; its
semantic and timing boundaries are below.

Classification depends on the promise. An adapter that validates a completed
JSON object can provide structured results without providing incremental
structured streaming. Calling both "JSON support" hides the distinction that
determines whether the UI can render fields before completion. Narrow the
capability description rather than forcing a single label to cover both jobs.

Transport and capability routing are independent dimensions until the actual
selector couples them. Enabling WebSocket need not change which compact,
inference or job backend runs. Configuration states intent; capture the chosen
route and any fallback before attributing a result to a transport.

## Selection carries intent

- **Default:** the product chooses the lane; it may fall back according to the product promise.
- **Explicit override:** the user chose the lane; silent substitution usually violates that intent.
- **Automatic router:** selection criteria and fallback order are product behavior and should be
  explainable after execution.
- **Effective runtime:** configuration, availability, and routing may produce a different lane than
  either docs or the request imply.

Default behavior does not establish override behavior. A disputed selector is
a configuration and routing question; changing support logic before resolving
it can "fix" a path that was never selected. Use `charter-configuration-diagnosis` for that
subproblem when its launch or precedence analysis is needed.

## Evidence reaches a particular path

Catalog listings, package installation, model residency, endpoint reachability, credentials, and
feature flags show that a lane may be attempted. A request through the exact selection path shows
what the capability actually does. Use each observation only for the decision it can support.

When a volatile provider fact can change the lane decision, check the applicable current vendor
source and retain the date, plan, region, or version needed to interpret it. Do not generalize an
observed default path to every override, account, or deployment.

## Substitution has both semantic and temporal boundaries

A fallback decision names:

- trigger;
- selected replacement lane;
- capability, quality, price, latency, residency, or attribution difference;
- whether the user may decline or choose another lane;
- user-visible consequences and any needed choice or recovery, with route details in diagnostics.

If the original attempt may have crossed an effect boundary, fallback is not
merely another selection. Reconcile that operation or preserve its unknown
outcome; a second provider can duplicate the same logical effect.

Deny early when no fallback preserves the product promise or explicit
selection forbids substitution. When support is unknown, connect any restraint
to the actual consequence: a synthetic local probe and an upload of confidential
documents have different exposure, even if they test the same unknown feature.

## Make the decision intelligible at use

Carry the lane decision through routing, configuration, errors, status, help, examples,
documentation, and public copy that expose it. Diagnostics should show requested lane, effective
lane, selection reason, support state, fallback taken, and recovery action where applicable.
Primary copy carries the capability, consequence and useful action; provider
identities belong there when they explain those differences or preserve the
user's selection, not merely because the router records them.

When several exposed lanes must stay coherent, keep one row per lane with the fields the product
actually uses:

- identity: provider or backend, model or version, and runtime, host, region or tier;
- selection: mode, requested and effective lane, and the reason;
- support: state, supported scope, limitations, and when the source or observation was taken;
- fallback: whether it is allowed, to which lane, on which trigger, the material differences, and
  whether the user must choose;
- user surface: status copy, denial or recovery action, and where diagnostics appear;
- consequences: quality, latency, cost, residency or privacy.

## Feedback that changes the support promise

Choose the smallest reachable set of default, exposed-override, unsupported, unavailable,
degraded, or fallback branches whose outcomes can change the lane decision or readiness claim.
Check the product consequences material to that decision—such as quality, latency, price,
residency, limits, attribution, or user control—not merely a successful provider response.

Return the chosen support behavior and the changes required in product routing and surfaces.

Compare a nearby path that should behave differently when it can expose the
decision error. A default may fall back while an explicit provider selection
must not; an adapted non-streaming response may work while its streaming form
is deliberately denied. Those contrasts test the product distinction, whereas
repeating successful direct calls mostly tests provider availability.
