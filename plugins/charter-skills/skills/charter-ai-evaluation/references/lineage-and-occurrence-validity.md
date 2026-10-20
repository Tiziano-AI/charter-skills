# Lineage and occurrence validity

## Which configuration a result speaks for

"Did this serve the consumer?" and "what difference did this change cause?"
are different questions. A new model adopted with a rewritten prompt can be
the right choice while the prompt's own contribution stays unknown, and a
reproducible effect of one change can be real yet worthless to the consumer.
To attribute an effect, hold model, runtime, tools, task and assistance fixed
and change one thing; that still leaves ordinary model variability, which
repeated runs measure.

Bind a behavioral claim to the input and configuration capable of causing it.
Relevant lineage can include model, requested and effective reasoning effort, provider,
transport, runtime binary, base and developer instructions, skills, role,
task, workspace state and human assistance. Hold fixed what can confound the
contrast; do not log unrelated state.

For a change to an agent's instructions or skills, installing, exposing,
selecting, loading, executing and helping are separate events. An installed
package is not proof that a run loaded it, and a version marker does not
exclude another injected instruction. If the run's records do not show that
the candidate was loaded, the result can still judge the whole product path,
but it says nothing specific about the candidate. When a runtime never
recorded which roles or skills were visible, visibility cannot be
reconstructed from a later selection; the claim for that layer stays open
rather than justifying a new sensor.

Claim only the scope observed: behavior predicted from source, behavior under
an effective product configuration, the causal effect of a controlled change,
or usefulness for a particular receiver. Transfer to another model or runtime
is a separate claim.

## Keep occurrence identity intact

Use the product's own request, run, task or session identity and its native
terminal state. A retry, child or corrective attempt is a separate
occurrence, and the original stays in the sample. Keep the exact input,
complete output and effect evidence needed to interpret each one; summaries
can point to those objects, not replace them.

Classify each occurrence before judging quality:

- a completed result whose configuration supports the intended comparison;
- an owned terminal failure, which is reliability evidence even without an
  artifact to grade;
- an indeterminate transmission or terminal state, which is neither success
  nor failure;
- a comparison invalidated by a material uncontrolled change.

Complete failures belong to the evidence; dropping them because they produced
no polished artifact overstates the candidate. Contamination concerns
attribution, not whether an unfavorable result counts. An order effect, shared
memory, different assistance or one arm seeing the other's result can
invalidate a prompt-only contrast; ordinary model variability under the same
configuration does not. A product defect found during an invalid comparison
may still need repair, and excluding it from attribution must not hide its
consequence for users.

## Failed or ambiguous effects

Do not repeat a possibly transmitted effect to complete a pair. Follow the
product's lifecycle and recovery semantics. A later distinct attempt needs
known replay safety or a separate destination that cannot duplicate the
effect, keeps the earlier evidence, and must still have a decision to
resolve. Never rewrite the original occurrence's identity or preconditions
around a successful retry.
