---
name: charter-prompt-design
description: 'Prompt design for a system prompt, task prompt or agent role: write
  or improve it, adapt it to another model or provider, or choose between complete
  candidates, controlling judge bias and naming the cheapest trial that would settle
  a close call.'
metadata:
  content_version: charter-prompt-design@2026.10.16.0
---
# Charter · Prompt Design

A prompt is a proposed influence on behavior: the system prompt of a product
feature, an extraction or classification prompt, a compaction prompt, the
brief of an agent role. The work is to write one, improve or adapt one, or
choose between complete candidates. In each case the question is which
complete text makes the receiving model do the intended work in its real
situation, not which reads as the most elegant, strict or thorough.

A small wording fix with an evident effect needs no method: make it. When the
person asks for a prompt, the answer is the prompt itself, ready to paste,
followed by a line or two on the choices that matter.

## Reconstruct the intent before writing

From the request, the current prompt and its known failures, establish who
receives the text, what situation it will meet, what a good output looks like
and what has already gone wrong. In a rewrite, the existing clauses are
evidence: an odd exception or a repeated warning usually records a past
failure, so find out what it guards against before deleting it, and keep the
protection that still matters in a better form. "Optimize this prompt
for the new model" usually asks for the same intent carried more effectively,
not for a new policy.

## Write for the receiver's situation

An instruction links a recognizable situation to a judgment or action.
Explain the purpose where the model must generalize to cases the text cannot
list, and be exact where the output is fragile: the schema, the identifiers,
the format a parser expects. Examples teach strongly and get copied, so vary
their incidental features and keep constant only what should be copied.
Resolve contradictions instead of ranking them with emphasis: capitals and
repetition added to compensate for one model's inattention can make a more
literal model over-apply the rule.

A variant changes behavior when it changes recognition, supplies a missing
distinction, changes priority or alters what seems permissible. Consider "ask
when uncertain" against a text that separates uncertainty about the user's
preference from uncertainty an inspection can resolve. The first may produce
more questions without better decisions; the second preserves the user's
control while avoiding needless interruption. If the task has no inspection
access and hinges on a personal preference, asking directly is exactly right.
The contrast, not a general preference for autonomy, supports the choice.

Read the draft as a literal reader would and follow each sentence fully. If
full compliance with a passage harms the intended result, the passage
optimizes the wrong proxy.

## Models and providers

Wording and format can affect how a model responds even when a human reads
the same meaning. A prompt tuned by reading, or by trials on one model, is a
hypothesis for another; the successful form is not itself evidence of transfer.

The provider's current prompting guidance for the target model, whether it
comes as a native skill or as documentation, owns that model's tendencies,
parameters and syntax; read it when adapting to that model. This package
carries the provider-independent method. When a product must run on several
models or routes, try the prompt on each admitted route and prefer text that
states intent and constraints plainly over devices that work on one model.
To move a working prompt to a new model, carry the same intent over and apply
the provider's guidance for that model. When you can run the new model, run
the old prompt unchanged on a few real inputs first and change only what it
gets wrong, one change at a time where you need to know which change did it;
when you cannot, deliver the adapted prompt and name the inputs to try first.

## Choosing between candidates

Read every candidate complete: exceptions and competing clauses can reverse
the reading of a fragment, and a diff locates changes only after the operative
texts are understood. Brevity can remove irrelevant competition or the
decisive distinction; strictness can protect a boundary or freeze judgment
where degree matters; explanation can transfer knowledge or elaborate a wrong
premise. None is a quality metric on its own. The strongest alternative often
reveals the real trade-off: one candidate may be better for exact operations
and worse for open diagnosis, and the recommendation should say which feature
of the intended use decides it.

A synthesis is justified when candidates supply complementary knowledge under
one coherent contract. Concatenating attractive passages can keep both sides
of the original conflict; often the best synthesis is one candidate's model
with another's exact constraint.

## Judge bias and the cheapest trial

A judgment from the text is a prediction, and a model judging candidates,
including you, has known biases: position (the preference changes with the
candidates' placement), verbosity (the longer text looks better) and
self-preference (a model favors text it recognizes as
its own). The usual case is the most exposed one: the agent drafted one
candidate and then compares it. When one candidate is plainly better for the
stated use, say so from the text and name the trial that would reverse it.
When the call is close, compare both orders in separate fresh contexts that
have seen neither the other order nor its verdict, and keep a preference only
if it survives the swap. Compare at similar length or state the difference,
and use a judge from a different model family than the author when the person
has configured or named such a collaborator. A fresh context on the same model
does not remove model self-preference. Rereading in reverse order in the same
context is another look, not an isolated order check. Without those controls, make the
text-based assessment and state the limit, including when you also wrote the
candidate. A flip leaves the preference unresolved; it does not establish that
the candidates are equally good. If a wrong choice is costly or hard to undo,
run the cheapest trial that can settle it: both prompts on a handful of real
inputs, including a hard one, read side by side without labels. A prompt that
will run on a different model from the one judging it makes a text-only call
weaker, so reach for the trial sooner.
[Blinded review](references/review-contract.md) explains when and how to hand
candidates to separate reviewers and how to read two orders;
[build_blind_packet.py](scripts/build_blind_packet.py) builds the packets in
both orders with a private label mapping.

## Neighbors and result

A system of several instruction surfaces and their authority, such as a
kernel, adapters, skills and workplace guides, is
`charter-instruction-system-design`. Quality observed over a set of cases,
with graders and a stated decision, is `charter-ai-evaluation`.

For writing or rewriting, return the complete text and the few choices that
matter with their reasons. For a choice, return one recommendation or
coherent synthesis, its decisive operative difference, the strongest
countercase, and the trial that would reverse it.
