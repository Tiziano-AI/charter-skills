# Hosted Release Observation and Diagnostics

Use this reference to observe a deployment, cutover, regression, or recovery at the hosted target.

## Observation layers

Each layer answers a different question:

| Layer | Useful observations | What it does not establish |
| --- | --- | --- |
| control plane | deployment ID, revision, status, traffic allocation, config version | application behavior |
| artifact/runtime | image digest, process version, startup log, instance health | routed consumer behavior |
| service | target-linked logs, traces, metrics, queue or worker state | end-to-end product outcome |
| route | DNS, TLS, HTTP response, synthetic transaction, client version | broad user success |
| product | public workflow, conversion, latency, errors, support events | causes without diagnosis |

Attach provider account, project, service, environment, deployment or revision, route, and time
window to observations so similarly named targets do not mix.

## Bounded diagnostic reads

Prefer queries with explicit resource and time boundaries:

- deployment history for one service and environment;
- logs for one revision, request, trace, instance, or finite time window;
- metrics for one resource with stated aggregation and comparison window;
- traffic allocation and route mapping at the time of cutover;
- configuration or migration state for the affected release;
- synthetic transactions through the consumer route.

Watch modes are useful during an attended cutover but poor post-hoc records unless the time window
and release identity are captured.

## Diagnose by release mechanism

Common patterns:

- **build failure:** artifact never produced; inspect compiler, dependency, platform, and build
  inputs.
- **startup failure:** artifact deployed but process cannot initialize; inspect entrypoint,
  runtime, configuration, dependencies, migrations, and resources.
- **route failure:** healthy revision is not reachable; inspect traffic, DNS, TLS, proxy, port,
  region, and policy.
- **mixed-version failure:** clients, workers, or replicas disagree; inspect rollout allocation,
  schema compatibility, queues, and caches.
- **capacity regression:** release works but breaches latency or error budgets; inspect saturation,
  concurrency, memory, retries, and dependency load.
- **product regression:** infrastructure is healthy but the user journey fails; trace one real
  request through the changed path.

Avoid cause claims from one log line or metric spike when several mechanisms predict the same
observation.

## Cutover signals

For a staged cutover, choose the signals whose result changes exposure:

- leading safety signals: startup failures, error rate, saturation, queue depth, migration errors;
- capability signals: one or more synthetic or real public journeys;
- business or user signals: success rate, completion, revenue, or support indicators relevant to
  the change;
- rollback thresholds and observation duration.

Read these per version, the new cohort against a control cohort still on the old version over the
same window: a before-and-after comparison confuses the release with whatever else changed in that
time. Generic health is useful but insufficient when the released capability has a distinct public
path.

## Report useful state

State target identity, deployed and routed revision, traffic exposure, relevant observations,
consumer outcome, current regression or recovery state, and material uncertainty. If an operation
was accepted but its target-linked result cannot be read, report the state as unknown rather than
assuming either success or failure.
