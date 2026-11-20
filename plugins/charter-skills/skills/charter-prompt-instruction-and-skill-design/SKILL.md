---
name: charter-prompt-instruction-and-skill-design
description: Write, adapt or compare prompts for a model call or agent role; create
  a SKILL.md or fix a skill agents overlook; repair conflicting instructions or review
  guidance after a model or harness upgrade. Missing source facts need retrieval,
  not stronger wording.
metadata:
  content_version: charter-prompt-instruction-and-skill-design@2026.11.20.0
---
# Charter · Prompt, Instruction & Skill Design

What decision should the receiving model make differently, and what will it have in front of it then? A billing assistant that invents a due date might need a distinction in its extraction prompt: a payment term is not a stated date. But if the invoice's second page never reached the model, neither a better example nor a stricter rule will recover it. Take the missing page and the assembled input to `charter-context-engineering`. If the model returned a correct date and the application discarded it, fix the application.

## Write the prompt the call needs

For a new prompt, start with a real input, its intended use and the output the caller needs. State what counts as evidence, what to do when it is absent, and the exact structure where another program depends on it. For judgment rather than extraction, show the distinction that selects a different answer: asking the user about their preference is useful; asking them for a fact already visible in the supplied record is not. Give the ready-to-use prompt, not advice to its author. A clear local wording fix needs only the fix.

Read [Prompt design](prompt-design.md) before a substantive rewrite, model adaptation or candidate choice. Preserve the reason for an unusual exception. On a new model, an unchanged prompt on the same inputs makes a useful baseline. Read competing texts **in full**: a later exception can reverse an apparent advantage. Choose on the provision that matters in use; say what case would favor the runner-up.

When authorship or presentation could tip a close comparison, use the [blinded review procedure](references/review-contract.md) before sending candidates to reviewers. Its [packet builder](scripts/build_blind_packet.py) keeps the label mapping private. Give each fresh context one order, the complete finalists and the same question, without another verdict. A preference that flips is unresolved, not a tie. Blinding hides labels, not a familiar style or a judge's own instructions. If the choice matters, compare the actual outputs on the target model without labels. A judgment from reading prompts predicts behavior; it does not demonstrate it.

## Repair the instruction that reached the decision

Before moving a rule between a base prompt, runtime adapter, workplace guide, role or skill, read [Instruction system design](instruction-system-design.md). Inspect the task and the input the failing session actually received. If a correct source rule is missing there, trace [instruction delivery](references/instruction-delivery.md); don't edit the missing passage to make it louder. When two instructions seem to compete, read [Authority and composition](references/authority-and-composition.md) to distinguish a narrower condition from a contradiction. Replace conflicting text at its editable owner. Use [Rule admission, removal and feedback](references/rule-admission-removal-and-feedback.md) when a field miss prompts a proposed standing rule: would this addition help in another case without interfering where the old behavior was right? The agent may instead lack a tool or know-how. A permission enforced by the system is a better control than a prohibition in prose.

For a changed model or harness, read [Model or harness adoption](references/model-or-harness-adoption.md) **before comparing instructions**: work from the release and base text the host actually ran. For a consequential recurring miss, a reviewer can inspect the composed instructions as evidence; if governed by them, it cannot independently validate them. A fresh session or another provider is not a clean review unless its actual loaded input establishes that separation. Take observed outcomes, configuration and remaining causal uncertainty to `charter-ai-evaluation-and-session-learning` when they will decide adoption.

## Make specialist knowledge findable and usable

Read [Skill package design](skill-package-design.md) before defining a skill's scope or repairing a package agents miss. Use the target harness's native creator for its scaffolding and supported checks. A card has to be recognizable from a natural request **before** the model can read the body: consult [Routing metadata](references/routing-metadata.md) when writing the card, and put the job and its distinguishing condition where the actual listing won't cut them off. A rule every task must obey belongs somewhere every task receives it, not behind selection.

The body must change the first difficult choice itself. Use [Resource design](references/resource-design.md) before splitting out references, tools or examples: where construction is the missing ability, a working template may teach more than a description of a good result. When the package underperforms, use [Package observations](references/discriminating-package-probes.md) to distinguish a skill not listed, not selected, selected but unread, and read without changing the artifact. Try an unprompted request and a neighboring one that should *not* select the skill; explicitly naming it tests application, not discovery. Correct the layer that failed and keep one source for the surviving guidance.
