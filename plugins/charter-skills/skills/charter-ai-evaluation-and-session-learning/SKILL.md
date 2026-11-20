---
name: charter-ai-evaluation-and-session-learning
description: 'Learn from agent sessions: why a correction kept recurring or a result
  worked. Evaluate models, prompts and agents from actual outputs to decide what to
  adopt or repair. Not a transcript recap, live status check or prompt rewrite.'
metadata:
  content_version: charter-ai-evaluation-and-session-learning@2026.11.20.0
---
# Charter · AI Evaluation & Agent Session Learning

“Why did I have to correct the handoff twice?” calls for the two decisions, not a benchmark. “Should every handoff use the new model?” calls for evidence about other handoffs, not just those two. An occurrence can establish that something happened, reveal a mechanism, or rule out a candidate for a use where even one such effect is unacceptable. It cannot say how often the problem occurs. Choose the evidence for the claim, not for the amount of material available.

## Learn from the session the person lived through

Read [Agent session learning](agent-session-learning.md) before assigning cause or proposing a lasting change from a record. Reconstruct the requirement **in force at the decision** from the person's own words. Place the instruction, brief or source the agent received beside the action it took and the result the person received. A later correction clarifies the gap; it wasn't evidence available earlier. An agent saying “understood” followed by a brief that still requests the old result locates a break in the handoff. If the revised brief was correct, inspect execution and the artifact instead. Neither the agent's explanation nor silence from the person establishes success.

Trace each finding to the original message or event. Distinguish a human correction from a reviewer's recommendation, a replayed delivery from a second turn, a planned action from an observed effect. A named transcript means the whole transcript unless narrowed; use [large-record analysis](references/large-record-analysis.md) before dividing it, and identify unread portions, omitted children or unavailable evidence that limit the conclusion. Check earlier advice and what happened when it was applied. A comparable success can disprove a proposed explanation and reveal a practice worth retaining.

Check the current brief, guidance or artifact before calling a historical defect live. Return what to change or keep, the ready text or concrete repair, its owner, and the next occurrence that could show whether it helped. Keep the source's claim apart from yours. Learning from a transcript does not resume its work, write memory or change instructions. If the evidence implicates guidance, bring the failing decision and missing distinction to `charter-prompt-instruction-and-skill-design`; if the question is what needs attention *now*, use `charter-session-status-coordination-and-wind-down`.

## Decide whether a change improves the result

Read [AI evaluation](ai-evaluation.md) before choosing cases, criteria or graders. State what finding would favor the candidate, keep the incumbent, or reject both. Read actual outputs for errors in what the consumer uses: a table can parse perfectly while assigning a total to the wrong supplier. A deterministic renderer dropping a correct value needs a fix, not more model runs. One receiver's judgment of real work can settle a reversible choice for that receiver.

For a broader choice, compare the same cases against a named baseline. Use expert-chosen hard cases to expose the failure mechanism; include ordinary cases to catch harm from the fix. Estimate rates or operating cost from representative traffic, reported separately. A pooled average can conceal a regression in the very class that decides adoption. Compare cost and latency **per useful result**, not per successful-looking response.

Use exact checks for exact properties. For judgments, start with the expert's labels; only extend them with a model judge that detects both passes and failures in the classes that matter. Before scoring, read [Cases, judges and comparisons](references/cases-judges-and-comparisons.md) for held-out cases, paired trials and judge checks. Hide candidate identity; judge each pair in opposite orders in separate fresh contexts. A flip is inconclusive. Account for length and model self-preference; another family can still share the instructions under review.

Before attributing a gain to a particular change, or counting incomplete or retried runs, read [Lineage and occurrence validity](references/lineage-and-occurrence-validity.md). A better result from a new prompt **and** a new model supports the combination, not a claim about the prompt alone. Keep terminal failures, successes, indeterminate outcomes and invalid comparisons distinct; never substitute a successful retry for the original. Report the decision, decisive classes, severe failures, cost and what observation would reverse it. If context was missing from the assembled request, give that case to `charter-context-engineering`; if recurrence involves several services, give their event sequence to `charter-system-and-mac-diagnosis` rather than grading more answers.
