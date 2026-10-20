# Charter · AI Evaluation

An evaluation of model outputs or agent behavior exists to make a decision:
adopt a model, prompt, skill or pipeline change, repair a failure it exposed,
keep the incumbent, change the model or its payload, or stop. The system may
be an extraction step, a summarizer, a classifier, a synthetic voice, a search
ranking, or an agent's instructions and tools. What counts is the result its
consumer receives end to end: the table a reader uses, the answer a customer
acts on, the work an agent hands back.

If source inspection or one observed failure already explains the defect,
repair it; a renderer that drops a rule needs a fix, not an evaluation. If the
person who uses the result has judged it on real work and the choice is
reversible, that judgment is the evaluation, and the answer names the decision
and the observation behind it in a sentence or two.

## Anchor on the decision and the end-to-end result

The characteristic failure of this work is proof theater: qualification
scripts, acceptance files, per-stage scores and hashes accumulate while nobody
has checked whether the product's final output got better. Optimizing a stage
that is easy to measure, such as retrieval nDCG, OCR character error rate or a
field match rate, can raise the number while the answer the user reads stays
wrong. Measure the end-to-end result first, and use stage metrics only to
locate the first upstream stage where a failing case goes wrong.

Before spending runs, write in a few lines which outcome leads to which
action: "if the new extractor loses any table the incumbent kept on the hard
cases, keep the incumbent; if it keeps them all and costs half, adopt it."
Left vague, either outcome can later be narrated as support for the same
choice. Keep cases, labels and criteria with their product owner; private inputs
can stay at their authorized source behind usable pointers rather than being
copied into a code repository. The evaluation leaves a decision. Retain reusable
cases or a regression suite when later changes need the same check, rather than
building an evaluation service for a one-off choice.

## Read outputs before choosing metrics

Start with error analysis. Take the current system's outputs on real inputs,
from use when they exist or from a fresh run, read them with the domain expert
when there is one, write in plain words what is wrong with each, and group the
notes into failure classes. Read enough variation that further examples no
longer change the criteria or the decision. The classes become the criteria,
and those that could change the decision become what you measure. Metrics
chosen before reading measure what
is easy to count, and graders' criteria shift as they see outputs, so this
first read is part of defining the criteria. When the decision already names
the failure class, as in the extractor example, a short read that confirms no
other class matters is enough.

## Hard cases chosen by an expert

A case is useful when it contains the mechanism the decision turns on. Choose
deliberately hard exemplars with the expert, such as the scanned bilingual
table with merged cells or the conversation in which the user reverses an
earlier request. Real failures from use are the best source. For an agent, a
judgment case needs the competing legitimate aims, not a prompt that says
which one wins. An easy
exemplar is a smoke test: it shows that the system runs, not that it handles
the difficulty, and cleaning a case up can remove the phenomenon.

A deliberately hard set tests known weaknesses, not their frequency in use.
Include ordinary cases when a repair could harm them, and use a representative
sample when the decision turns on production rates or total operating cost.
Report that sample separately from an oversampled challenge set; pooling them
does not create an estimate of the traffic mix.

Report strata separately, per language, document type or task class; an
unexplained weighted average can hide the class that regressed. Compare
against a named floor, such as the incumbent, a simpler baseline or another
system that already does the job. The question is often whether the candidate
is no worse on the classes that matter while costing less, not whether it wins
on average.

## Grade with the cheapest reliable judge

Use code where the property is exact: valid schema, a field equal to ground
truth, a forbidden effect that did or did not happen. Use the expert where
judgment is the point. An LLM judge can extend the expert only after it agrees
with the expert's labels on a sample containing both passes and failures,
measured on each class; agreement on passes says nothing about catching
failures.

LLM judges have known biases: position (the preference changes with candidates'
placement), verbosity (the longer answer wins) and self-preference (a model
favors text it recognizes as its own).
Judge pairwise comparisons in both orders using fresh contexts that have seen
neither the other order nor its verdict, and count a preference only when it
survives the swap. Keep lengths comparable or report the difference, and never
let the model that produced a candidate be its only judge. Read the
transcripts of failed cases: a grader that rejects a valid answer is a grader
defect, not a model defect.

## Cost is an outcome

Tokens, latency and money per useful result belong beside quality. A
candidate that matches the incumbent at a fraction of the cost is a different
decision from one that is slightly better and much dearer. The model and its
payload (context, examples, retrieved material) interact, so when both are
open, compare them together rather than tuning one against a fixed other.

## What a sample can support

One unauthorized or destructive effect can disqualify a candidate for a
sensitive use whatever its average quality, so count severe failures apart
from quality. Clean results bound the failure rate less than they seem to:
zero failures in twenty independent trials still leaves an upper failure-rate
bound of about one in seven at 95% confidence (the rule of three approximates
this bound as 3/n). This binomial bound assumes a fixed probability under the
tested conditions. Correlated retries, a hand-picked challenge set or a changed
configuration do not establish a production failure-rate bound.

When one evaluation covers many items, such as the skills of a catalog or the
document types of an extractor, and each item will be acted on separately,
each rests on its own few cases: the aggregate can be steady while per-item
rankings are noise. An item-level decision needs cases that cover the relevant
variation for that item. Add cases where that coverage is missing, or limit
the decision to the scope the evidence supports. A second model on the same
cases can test dependence on model choice; it does not cover omitted cases
or repair sparse item-level evidence.

Another run is worth its cost only when its plausible outcomes would lead to
different actions.

## Depth and neighbors

- [Cases, judges and comparisons](references/cases-judges-and-comparisons.md):
  open it to build a case set, validate a judge, compare candidates over
  repeated runs (paired comparison, pass@k against pass^k, ordinal scores), or
  read variation that may be structure rather than noise.
- [Lineage and occurrence validity](references/lineage-and-occurrence-validity.md):
  open it to attribute an effect to one change rather than to a bundle, when
  the change is to an agent's instructions, skills or runtime, or when runs
  failed, were retried or ended indeterminate.

Writing or choosing one prompt from its text, with at most a small trial, is
`charter-prompt-design`; deterministic tests with exact oracles are
`charter-test-design`; building one document for its destination is
`charter-document-fidelity`; defining what a model-backed function must
achieve is `charter-functional-design`. Observed quality over a set of cases,
including an extractor measured over a corpus, belongs here.

The result is a recommendation in a few lines: the action, the failure classes
and hard cases that decided it, the cost difference, and the observation that
would reverse it, with failed and indeterminate runs reported alongside. Use a
table only when several candidates are compared across several classes.
