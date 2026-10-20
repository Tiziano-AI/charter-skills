# Investigating a product journey

## The unit of observation

Choose an actual user occasion, not an undifferentiated persona or a catalog of
screens. An occasional administrator recovering access and a daily operator
processing a queue may use the same page but need different priorities.

Locate the first meaningful payoff and the real end of the job. “Exported” can
still fail if the receiver cannot open the file. “Account created” may be a
prerequisite rather than value. Include those boundaries when they determine
whether the product fulfilled its promise.

Trace enough of entry, expectation, setup, action, feedback, result and return
to find the limiting transition. Include an interruption or failure when it
changes trust, preserved work or the ability to continue. This is not a demand
to test every state for every change.

## Separate the evidence

- Marketing and onboarding show the expectation being set.
- Source and service contracts show possible behavior and implementation
  causes, not what the user encountered.
- Rendered inspection shows layout, affordance and the observed path.
- A usability session shows a participant's behavior under its test conditions.
- Support and telemetry expose patterns but can miss silent abandonment or
  people who never reached the instrumented step.
- Interviews reveal reasons and language; stated intent is not future use.

Ask participants to pursue a plausible result rather than recite the intended
sequence. Leading instructions can teach the very interaction being tested.
Watch hesitation, recovery and unexpected strategies as well as completion.
A person who finishes only after moderator help has supplied different
evidence from unaided completion.

Identify the denominator when using metrics: people exposed, people who
attempted, successful attempts or retained users. Faster completion can mean
an improved path, premature abandonment, or exclusion of slower users.
Aggregate improvement can conceal harm to keyboard users, novices or those
with large real datasets.

## Locate the mechanism

Connect the observed difficulty to what the interface makes the person do:

| Observation | Plausible mechanism | Discriminating observation |
| --- | --- | --- |
| People open several sections before acting | Labels do not predict contents, or the job spans sections | Ask what each label implies; trace where needed information lives |
| A short form is frequently abandoned | Requested effort, sensitivity or uncertainty exceeds expected value | Locate the abandonment step and ask about the specific request |
| A successful operation is repeated | Feedback does not establish completion, or the result is not available where needed | Follow the result into its actual destination |
| Errors trigger support requests | Work is lost, recovery is ambiguous, or the person lacks required control | Attempt the available recovery with the same permissions |
| First use succeeds but return is weak | Low recurring need, inadequate ongoing value, or repeated setup | Observe the next real occasion, not only a first-run survey |

These are hypotheses, not diagnoses from a metric alone. A low click rate may
be desirable if the task no longer needs that click.

## Select and test the intervention

Prioritize consequences, recurrence and reach across the journey. A coherent
change may touch several screens or surfaces; “smallest” does not mean one
CSS patch. Preserve successful expert paths while improving first use.

For the chosen change, state the expected mechanism and the side effect worth
watching: a default may hide scope, inline validation may interrupt typing,
automatic navigation may lose comparison context, and proactive assistance
may interrupt concentration. Compare the resulting journey at that seam.

Return findings in decision order, not discovery order. Show the decisive
moment, the change and why it should help. Keep source-only conclusions
source-only; do not turn a walkthrough into a claim about measured demand,
accessibility conformance or population-wide usability.
