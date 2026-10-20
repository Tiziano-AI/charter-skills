# Cases, judges and comparisons

## The case set

A discriminating case links an observable result to an action. Better
explanation may favor a candidate for a teaching task, while one unauthorized
effect disqualifies it for a sensitive workflow regardless of explanation
quality. Pick cases whose plausible results would choose different actions,
and name for each what a pass and a failure look like before the run.

Natural cases from real use reveal interactions and usefulness that an
isolated case omits. A synthetic case can isolate a mechanism, such as one
ambiguous acknowledgement or one malformed table, but only if it keeps the
difficulty. Neither kind transfers automatically to another model or runtime.

When a prompt or pipeline is iterated against the same cases, those cases
become part of the design: every change was chosen because it fixed them.
Keep some hard cases unseen until the decision, and read a result on the cases
used for tuning as an optimistic one.

## Validating an LLM judge

The judge's job is mostly to catch failures, so the expert's labelled sample
needs real failures in it, not only the passes a healthy system mostly
produces. Compare the judge with the expert on each class separately: how
often it passes what the expert passes, and how often it fails what the expert
fails. One overall agreement rate on a sample that is mostly passes can look
high while the judge misses most failures.

A judge asked a narrow binary question per failure class ("does the answer
cite a clause that is not in the contract?") is easier to validate and to
debug than one asked for a score from 1 to 10. Where the expert and the judge
disagree, read the case against the source and intended criterion. The judge
may be wrong, the criterion may be unstated or ambiguous, or the expert's
label may be mistaken or inconsistent with their other labels. Resolve the
disagreement at that owner rather than tuning the judge to reproduce an
unexamined label. Check agreement again after changing the labels, criterion,
judge's prompt or model.

Bias controls in practice:

- Position: run each pairwise judgment in both orders in separate fresh
  contexts. When the verdicts disagree, record an unresolved preference rather
  than choosing either verdict. Repeated disagreement shows unstable judgment,
  not necessarily close candidates: position sensitivity, ambiguous criteria,
  sampling variation or unequal strengths can also explain it. Inspect the
  reasons against the expert's criteria before deciding whether a direct trial,
  expert judgment or a judge repair would settle the choice.
- Verbosity: compare candidates of similar length, or state the length
  difference beside the verdict so a reader can discount it.
- Self-preference: a judge from a different model family than the author
  of either candidate reduces this bias when the person has configured or
  named such a collaborator. A fresh context on the same model does not remove
  model self-preference. Hiding labels does not hide authorship that the text's
  style reveals; state the remaining limitation when no different judge is available.
- Shared instructions: a judge running under the same instructions or doctrine
  as a candidate inherits its assumptions. Several personas in one context are
  one judgment, not several.

## Comparing candidates

Run both candidates on the same cases and compare case by case. Per-case
differences are usually less noisy than two separate averages, because each
case's difficulty affects both arms and cancels in the difference. Repetition on the same case reveals how
much a single run varies. Neither pairing nor repetition gives independence
if one arm sees the other's output, shares changed state or receives
different help; equivalent isolated destinations avoid duplicate live
effects.

pass@k is the chance that at least one of k attempts succeeds; it describes
what a person who can retry or choose among attempts gets. pass^k is the
chance that all k attempts succeed; it describes reliability when every run
reaches a user. A candidate can look strong on single attempts while its
pass^k falls quickly, so choose the measure that matches how the consumer
meets the output.

Ordinal judgments do not acquire equal intervals through arithmetic: the
average of "poor, good, excellent" coded 1 to 3 is not a quality level. Human
preference, operational reliability, cost and source coherence measure
different outcomes, and combining them needs an actual value model, such as
"no regression on tables, then the cheaper one", rather than an unexplained
weighted score.

## Variation contains structure

Another occurrence can reveal a one-off, a recurring mechanism, a boundary
condition or a transfer failure. A candidate that helps short tasks and harms
long ones is not merely noisy: task length is a moderator, and the decision
may be to adopt it for one class only. Ranking the best replica, or averaging
everything together, conceals that. A prompt that helps novices and constrains
experts shows the same pattern.

## The next action, including stopping

Adoption is attractive when the benefit matters for the intended scope and
the strongest counterevidence does not overturn it. A specific defect may
support a repair candidate; keeping the incumbent and retiring the candidate
are ordinary conclusions, not failed evaluations. Several good results may
justify a reversible trial while saying little about a rare severe effect;
if that effect would change the acceptable exposure, the next case should
target it. When no plausible further observation would change the action,
stop, and leave the cases and criteria with the product for the next decision.
