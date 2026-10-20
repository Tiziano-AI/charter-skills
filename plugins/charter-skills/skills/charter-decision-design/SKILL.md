---
name: charter-decision-design
description: 'Decision design for consequential choices involving uncertainty, competing
  preferences or shared commitments: integrate existing contributions, compare feasible
  options and recommend an actionable choice. Market bets are product strategy.'
metadata:
  content_version: charter-decision-design@2026.10.16.0
---
# Charter · Decision Design

A decision model connects choices to consequences and consequences to what the
decision owner values. It is useful when that connection is obscure or
contested. When a constraint, a dominant option or an agreed commitment
already settles the choice, or an ordinary implementation merely has
alternatives, the answer is that choice and the fact that settles it, in a
sentence or two. A polished score table can be less informative than one
well-explained trade-off. Whom a product serves and which market bet comes
first are `charter-product-strategy`'s questions, and which machinery to build
on is `charter-architecture-simplification`'s.

## Begin with what the participants have already contributed

A shared decision rarely begins with an empty page. A partner's proposal, a
previously rejected option, the user's correction and an expert's estimate may
already settle much of it. Recover the meaning of those contributions before
asking their authors to supply them again. Attribute a claim to its source;
agreement about a problem does not imply agreement with its proposed remedy.

Integration is more than summarizing each participant in turn. Put comparable
claims against the same consequence and conditions. Two proposals may disagree
only because one assumes an existing capability and the other assumes it must
be built. Conversely, apparently compatible proposals may assign the same
responsibility to different people. Separate common ground, factual uncertainty,
preference differences and commitments that nobody has yet accepted.

Disagreement has a mechanism. Participants may observe different facts,
expect different causes, weigh the same consequences differently or disagree
about who must act, and each difference is settled by something else. A choice
can also commit several parties, each able to accept only its own consequence.
When either happens, the
[shared-decision reference](references/contributions-and-decision-rights.md)
maps the kinds of disagreement, separates the parties' permissions and finds
the smallest question that still needs an answer.

## Feasibility and value answer different questions

A constraint removes an option from consideration; a preference changes its
attractiveness. Treating an unacceptable exposure as a low score allows enough
cost savings elsewhere to compensate for it. Conversely, treating a preference
as a veto hides a trade-off the owner might willingly make.

Options need to be feasible and materially different. Status quo, delay and a
staged commitment are real alternatives only when their consequences are
credible. A fictional "do nothing" that ignores an expiring contract biases
the comparison as surely as a fictional perfect replacement.

Dominance is a strong simplifier when one option is no worse on every material
concern and better on at least one. Most consequential choices are not
dominated: they exchange cost, speed, reliability, flexibility or downside.
A model must show that exchange rather than conceal it inside labels.
[Framing and alternatives](references/decision-workflow.md) explains how the
decision boundary and horizon change what is actually being compared.

## A number is only as meaningful as its scale

"Quality," "accuracy" and "error reduction" may count the same benefit three
times. A weight on an undefined criterion means little; a swing weight values
a specified improvement over a specified range. Changing the range changes
the trade-off. Ordinal ranks express order, not equal gaps in value.

Weighted sums assume that gains on one criterion can compensate for losses on
another. Expected value assumes meaningful probabilities and comparable
payoffs. Risk aversion, survival constraints and tail losses can make utility
or robustness more relevant than the average. These are different models of
the decision, not increasingly sophisticated versions of one score.

The [quantitative reference](references/quantitative-methods.md) supplies
dominance, swing weights, expected value, break-even probability, regret and
value-of-information methods with their assumptions. Use the model whose
assumptions fit the trade-off; numbers cannot supply missing preferences or
make weak estimates objective.

## The switching boundary is often the real result

A recommendation becomes intelligible when the owner knows what would make
another option win. A cheaper system may win above a certain workload; a faster
launch may win only if delay destroys enough revenue. Solving that boundary
can be more useful than estimating every input precisely.

Compute the boundary rather than asserting it: recompute both options just
past the stated value and confirm that the ranking actually flips. A variable
that can only widen the favored option's lead has no switching point. Say that
the choice is robust to it, and look for the premise that can reverse it.

Scenarios describe coherent possible states. Their count is not a probability,
and coupled drivers cannot be varied independently without inventing impossible
worlds. A robust choice remains acceptable over credible states; a fragile
choice depends on a narrow premise. The latter can justify learning or staged
exposure, but not automatically more analysis.

Information is valuable through the better choice it enables, less cost,
delay and exposure. If all possible findings leave the same action preferred,
further research has no decision value for this choice. An experiment may
still have another purpose, but should not receive credit for a choice it
cannot change.

Reversibility changes both downside and learning. Canceling a contract may
leave migration work, expectations, team skills and integration residue.
A pilot preserves an option only if those commitments stay limited and its
observation addresses the uncertainty that matters. [Commitment and learning](references/reversibility-and-learning.md)
develops these temporal trade-offs.

The recommendation should expose the decisive rationale, the downside it
accepts, the strongest countercase and the switching condition, which makes it actionable now and
recomputable when premises change.

When contributions or sources the decision rests on contradict each other on
a point that changes the choice, first check whether they describe the same
object, scope and time: an earlier decision still binds within its scope until
its owner revisits it, while an earlier measurement merely ages. A corrected
premise also changes the conclusions built on it, not only the sentence that
stated it. An unstable external premise belongs to
`charter-current-fact-research`.
