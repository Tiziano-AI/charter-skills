# Provider Fallback UX and Operation Boundaries

Use this reference when a lane decision must become user-visible fallback, denial, diagnostics,
or recovery behavior.

## Put consequence and action first

The primary surface explains what changes in the user's work and what they can
do about it:

1. which capability is unavailable or narrower, and why that matters;
2. which material consequences a substitution changes;
3. the choice or recovery action needed, if any.

Name consequences that matter in the product: output quality, supported modalities, price,
latency, residency, data handling, attribution, limits, and reproducibility.

For an equivalent substitution within accepted product-managed routing, no
interruption or backend selector may be needed. Keep requested and effective
lanes available in diagnostics or history. When the user chose a provider or
model, or its identity explains a material difference, name that path and the
replacement in the relevant copy. Offer restoration or reselection when it
serves a real preference or recovery need, not merely because a route changed.

For example, a transcription product that promises the same processing and
output guarantees across managed backends can retain route details in run
history without asking the user to choose one. A user who selected local
transcription instead needs the consequential choice before upload: “Local
transcription is unavailable. Use cloud processing and upload this audio, or
keep it local and retry when the local engine is available?”

## Copy patterns

Use the pattern needed by the branch, with user-recognizable capabilities and
options. Name providers where their identity matters to the choice; omit
irrelevant slots rather than turning routing diagnostics into a form.

### Denial

```text
{capability} cannot be performed because {specific_reason}.
{recovery_action}, or choose {supported_option}.
```

### Visible fallback before execution

```text
{capability} can continue with {material_difference}. Continue?
You can also {recovery_or_alternative}.
```

### Visible fallback after automatic routing

```text
{result_status}. This run used {changed_capability_or_processing}.
{material_difference}. {useful_recovery_action}.
```

### Degraded mode

```text
{supported_scope} is available, but {missing_scope} is not.
Continue with the narrower result or choose {full_capability_option}.
```

### Temporary unavailability

```text
{capability} is unavailable because {condition}.
Retry {eligibility_condition}, restore it with {action}, or select {alternative}.
```

## Operation boundaries

Provider-support decides product lane behavior; the owning integration performs setup and runtime
operations:

- configuration owner changes defaults and routing selectors;
- account owner changes quota, plan, region, or access;
- integration owner repairs request/response adaptation;
- runtime owner starts local models, services, or hardware dependencies;
- product surface exposes fallback, denial, diagnostics, and recovery;
- release owner deploys the changed integration.

## Diagnostics

Useful fields are:

- requested and effective lane;
- selection mode and reason;
- current support state;
- fallback lane and whether it ran;
- material capability difference;
- provider or local failure category;
- retry eligibility and recovery action.

Avoid raw credentials, opaque provider payloads, generic `error`, and a status label that implies a
capability was exercised when only setup was checked.

## Consequence checks

Before automatic fallback, ask whether the replacement changes privacy or residency, price,
quality, latency, format, features, attribution, or the user's explicit provider intent. A material
difference can already be included in the product's accepted automatic-routing policy. Require a
new choice when the substitution exceeds that policy or contradicts the user's actual selection
or constraints; do not interrupt an already-authorized fallback merely to choose it again. After
fallback, retain the effective lane in diagnostics or history so future diagnosis remains possible;
surface it in the result when it explains a consequential difference or the user's selection.
