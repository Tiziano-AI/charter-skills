# Quantitative Decision Methods

Use numbers to clarify a consequential trade-off, not to make judgment look
objective. Preserve the distinction between measured inputs, estimates,
probabilities and preferences.

## Dominance and feasibility

A constraint removes an option. Dominance removes it only when another is at
least as good on every material criterion and strictly better on one under
the same conditions. Uncertainty can defeat a supposed dominance claim.

## Multi-criteria value

Define each criterion's scale and meaningful best/worst anchors before weights.
A swing weight expresses the value of moving across that range, not the
importance of a vague label. Changing the range changes the trade-off.

A weighted sum assumes compensability and a suitable value model. Do not use
it to allow low cost to compensate for a non-negotiable safety or legal limit.
Do not count the same consequence under several proxy criteria; correlation
alone does not establish duplicate value. An additive model also assumes that
the relevant trade-offs do not depend materially on levels of other criteria.
If they do, combine the interacting concern or use a model that represents
the interaction. Ordinal ranks do not provide equal utility gaps.

Test plausible preference ranges. If the result depends on one arbitrary
weight, report the preference that actually decides it rather than a false
objective winner.

## Expected value and utility

For mutually exclusive, exhaustive states conditional on an action:

```text
EV(action) = sum(P(state | action) * value(action, state))
```

Actions can change probabilities as well as payoffs. Include material
downside, opportunity cost and timing. Use expected utility when risk
tolerance or nonlinear value matters; an attractive average does not override
a survival constraint.

For an option paying G on success and losing L on failure, versus an outside
value B, the risk-neutral break-even probability is:

```text
p* = (B + L) / (G + L)    when G + L > 0
```

The formula helps identify which probability matters; it does not supply that
probability or make the values comparable.

## Scenarios, regret and robustness

Build coherent states from causal drivers. Do not independently vary inputs
that are coupled in reality. Report where the preferred action switches.
Scenario counts are not probabilities.

Regret is the gap from the best action in the state that occurs. Minimax regret
can be useful when avoiding an avoidable worst miss matters and probabilities
are weak, but its result depends on the credible state set. Robustness asks
whether a choice remains acceptable across plausible conditions; define
"acceptable" rather than counting arbitrary grid points.

## Sensitivity and information value

Vary inputs that can change the choice. One-way break-even analysis can expose
a decisive assumption; two-way analysis helps when drivers interact. Show the
boundary, not a table of immaterial variation.

Gross expected value of information is the expected value of choosing after
the information minus the best choice without it. Perfect information gives
an upper bound for a fallible study. Net value subtracts study cost, delay,
exposure and opportunity loss.

If every possible study result leaves the same action preferred, the study
has no decision value for that choice. It may serve another real purpose,
but do not credit it with a decision it cannot change.
