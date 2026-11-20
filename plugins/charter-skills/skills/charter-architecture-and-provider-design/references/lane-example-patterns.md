# Provider-Support Lane Patterns

Use these patterns to translate a provider difference into product behavior.

## Default lane

The product selects a lane when the request names none.

```text
capability: image generation
selection: default from effective configuration
lane: local GPU / model A
state: native when the local service and model are available
unavailable behavior: offer visible remote fallback
fallback consequence: remote processing, different price and style variance
diagnostics: requested=default, effective=local/model-A, reason=configured-default
```

Exercise selection through the default path itself; forcing model A directly does not test the
router or configuration that users rely on.

## Explicit override

The user names a provider or model.

```text
capability: transcription
selection: explicit request override
lane: provider X / realtime-v3
state: unknown for this account tier
behavior: inspect account capability or run an admitted bounded probe
upload boundary: do not send private data outside the authorized destination
fallback: only after the user accepts provider Y and its residency difference
diagnostics: preserve requested lane, observation and unresolved support limit
```

Do not silently use the default. The choice itself may encode cost, privacy, output style, or
compatibility intent.

Unknown support is an evidence gap, not itself a prohibition. A low-consequence
authorized probe can settle it. Deny when the capability is known absent or
the attempted path would cross a real constraint, not merely because it has
never been tried.

## Adapted lane

An adapter can preserve the user job despite API differences.

```text
capability: structured text generation
lane: provider Z / model B
state: adapted
transformation: product validates and retries invalid schema output once
limit: streaming structured output is unavailable
product promise: structured result for non-streaming requests
failure: exhausted validation returns an explicit failure, never unvalidated success
```

Validation makes a successful result conform to the checked schema; it does
not guarantee that a retry succeeds or that the contents are factually correct.
Describe the product behavior rather than claiming provider-native support.

## Degraded lane

The lane offers a useful subset.

```text
capability: document analysis
lane: local CPU model
state: degraded
supported: plain text and common tables
missing: handwriting and diagrams
choice: continue locally or switch to remote full analysis
```

Narrow the promise at selection time; do not discover the limitation only after a low-quality
result.

## Temporary unavailability

Support exists, but the current attempt cannot run because of quota, outage, capacity, or local
service state.

```text
requested: remote/provider-Q
effective: remote/provider-Q
state: unavailable
reason: account quota exhausted
recovery: wait for reset, raise quota, or explicitly select local fallback
status: show retry eligibility and the quota reset time when known
```

Keep `unavailable` distinct from `unsupported`; the recovery and public meaning differ.

## Patterns to reject

- A catalog row proves the feature works.
- The default succeeded, so every override is supported.
- Silent fallback counts as success on the requested lane.
- A green provider status page proves this account, model, region, and capability work.
- One provider request proves the product router, diagnostics, and recovery behave correctly.
