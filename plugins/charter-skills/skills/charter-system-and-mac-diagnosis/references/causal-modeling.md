# Models for Recurrence

Choose the representation that distinguishes the failure mechanism. Each model
below exposes a different relationship; one boundary drawn well usually
explains the contrast better than a diagram of the whole system.

## Event and state models

A happens-before graph joins sends, receives, durable writes, callbacks and
acknowledgements. Wall-clock timestamps can disagree across machines; use
causal links and monotonic local order where available. Absence from a log
does not establish absence of an effect the log does not own.

A state machine exposes legal transitions and the owner of each decision.
Ask whether a stale observation can authorize a transition after ownership
changed. Separate resource identity, logical operation, delivery and attempt.

For example:
- duplicate queue deliveries can repeat one logical operation;
- one delivery with a lost acknowledgement can generate multiple attempts;
- a new legitimate request can resemble an old one without being a duplicate.

The effect boundary needs the identity that distinguishes these cases.

## Necessary conditions and sufficient causes

A fault tree represents combinations that can produce a top failure.
A necessary enabling condition is not the whole cause. Removing one trigger
may leave another route to the same outcome.

Correlation can reflect a common cause or selection effect. For instance,
long-running jobs may both time out more and overload a service; the timeout
setting alone may not explain the load. Look for the causal edge the repair
would actually change.

## Feedback and control

Model observed state, desired state, controller, actuator and delay.
Two controllers can fight over one resource. Delayed observations can make
each corrective action overshoot. The same parts describe a human workflow:
the metric a team is judged by is its observation, and the team is the
controller that acts on it.

Interventions act on different parts of the loop: reduce feedback gain, bound
retries, add backpressure, improve observation, account for delay, or choose
one controller.

## State the hypothesis as a prediction

A useful hypothesis predicts an observation:
"If acknowledgements are lost after the effect, the same operation key will
have a durable effect before the retry begins." A hypothesis that predicts
nothing observable cannot be told apart from its rivals.
