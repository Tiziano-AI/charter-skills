# Charter · Instruction System Design

An agent works under a composed set of instructions: a base or system prompt,
harness additions, workplace guides such as AGENTS.md and CLAUDE.md, rules
files, skills, task briefs, and the messages the runtime injects on its own
for modes, permissions, tools and transitions. The design problem is to supply
the distinctions whose absence would change the work, each at the one place
that should carry it, without leaving two applicable instructions that
disagree.

## Start from the difference in the work

Compare the requested result with what the agent actually produced and the
consequence for its receiver. Then inspect the instructions, resources and
tools that occurrence received. A different result in another harness, model
or session supplies a useful contrast, but also changes other conditions;
it does not isolate the effect of a sentence. Trace only far enough to choose
an intervention the evidence supports, leaving the cause unresolved when the
available observations cannot distinguish it.

Often the cause is one line holding a stale fact: a renamed script, a moved
path, a check command that no longer matches anything and so verifies nothing.
Then the answer is short: the corrected line, and a fresh check of whatever
the stale line let through. The layers are fine, and redesigning them answers
a question nobody asked. Otherwise, place the defect:

- **Meaning or scope.** The distinction is missing, wrong or applied where it
  does not hold. "Verify before claiming
  success" can make an agent add checks after direct observation has already
  settled the result; what is missing is a model of when evidence suffices,
  not stronger emphasis on verification. Rewrite or enrich at the owner.
- **Delivery.** A correct rule never reached the model: it was not rendered,
  not installed, not loaded for that session, cut from a listing or never
  opened. Rewording it works on the wrong layer. [Instruction
  delivery](references/instruction-delivery.md) traces the path from source to
  what the model read; open it when a rule that exists in source seems absent
  from the behavior.
- **Interaction.** The rule arrived and dominates where it should
  not, alone or combined with others. "Explain your plan before acting" turns
  every one-line fix into a proposal; a confirmation rule written for one
  destructive command also stops every harmless one beside it. Narrow the rule
  to the case it was meant for; delete it only when that case no longer needs
  it.
- **Application.** Useful knowledge arrived but did not govern the relevant
  choice. Reading, quoting and explaining it establish different things from
  applying it. Look for the choice it should have changed before deciding that
  stronger wording would help.
- **Means or capability.** The work may need an editable source, a native
  component, a different production route or expertise the model cannot yet
  exercise reliably. Being able to describe a good result does not establish
  the ability to make or recognize one. More instruction is not the default
  remedy for missing means or insufficient capability.

When the evidence identifies a faulty instruction, replace or remove it at its
owner. A delivery repair, a practical resource, a different production route,
or no instruction change can instead be the justified result.
Adding a counter-rule beside it ("skip the plan for small fixes") leaves two
applicable instructions that the model must reconcile, and it may follow
either; capitals, IMPORTANT and repetition make the conflict louder without
resolving it. Give the replacement text for every line you change, name the
lines to delete, and say where each surviving rule lives.

When a hook, CI check, permission or missing credential can prevent the harm,
that control is more reliable than any wording, and the instruction can shrink
to naming it. Branch protection keeps an agent off the main branch better than
a louder rule does.

## Put each rule where it reaches the work that needs it

Always-loaded text is present even when irrelevant. Conditional text saves
that cost but can arrive too late, go unselected or go unread; some models
rarely open a reference linked from an entrypoint, so whatever changes the
first substantive move belongs in the text they read first. Choose the carrier
by the scope of the knowledge:

- judgment that holds in every kind of work: the shared prompt;
- facts about one runtime and the contracts that follow from them: that
  harness's layer;
- a specialist method for a recurring job: a skill;
- a bounded contribution to one task: its brief or role;
- what is true of one place: the workplace guide nearest the work. A rule that
  applies to every change in a repository, such as a changelog entry per
  change, goes in the always-loaded file rather than a skill that may not be
  selected.

This is not a split between permanent and temporary text. A task brief can
carry the most important obligation of the work, and a standing file can hold
plain data. Identify what each passage asks the agent to do and why its source
may require it. Removing a repeated rule reduces interference; removing the one
exception that separates permitted from prohibited action destroys meaning.

One rule has one editable owner. When two layers state it, keep the owner and
delete the copy; a generated carrier such as a rendered prompt or a projected
skill can be binding without being the file to edit. Precedence tells you which
of two conflicting rules should survive. Then remove the other from what the
model receives, because a declared hierarchy does not make a model resolve a
live conflict reliably. Messages the runtime injects stay part of the
environment even under a replacement base: design around them rather than
copying them, since a copy drifts and local priority wording cannot take
control of what another owner supplies. [Authority and
composition](references/authority-and-composition.md) tells specialization,
condition, conflict, duplication and interaction apart, and separates
instructions from data that merely contains imperatives; open it when
instructions seem to compete.

## Teach knowledge where judgment varies; keep steps where order protects something

For judgment under changing conditions, a causal account lets the model choose
an intervention instead of imitating a sequence, and a contrasting example
marks the nearby case where the same intervention is wrong. Exact procedures
stay where order itself protects a transaction, protocol or fragile operation;
replacing them with open reflection removes engineering rather than improving
the teaching.

Judge a proposed line by what it adds and by what it does when obeyed
literally. More questions help an ambiguous decision and burden a clear one;
more checks reveal defects or displace the requested work. A redesign can
change every heading and word as long as the useful obligations survive,
whether consolidated, moved or freed of duplicates. [Admission and
feedback](references/rule-admission-removal-and-feedback.md) covers when to
retain, rewrite, move, merge or retire guidance and how to read a field miss;
open it when deciding what happens to existing guidance.

## After a model or harness upgrade

Start from the exact release that runs: the app or binary and the model that
executed the work, and that release's base template, not upstream main or a
cached catalog. When a behavior seen after the upgrade is the trigger, first
establish what that thread loaded; a thread that ran on built-in instructions
says nothing about yours. Whenever the job is reviewing instructions after a
model or harness upgrade, open [Model or harness
adoption](references/model-or-harness-adoption.md) before comparing any text.

Writing or choosing the text of one prompt for one model call or role is
`charter-prompt-design`; designing one skill package, its card and body, is
`charter-skill-package-design`; measuring over a set of cases whether an
instruction change improves behavior is `charter-ai-evaluation`.

## The result

The result is the intervention the evidence supports, or a recommendation to
leave the instructions unchanged. For an instruction repair, give the
replacement text, what it replaces and the reason for its placement. For a
delivery repair, resource or production change, name the changed owner and
what it enables. A fresh session's loaded input can show that repaired
delivery reaches the model; whether the knowledge improves the work is a
separate observation.

A reviewer that follows the instructions under review can inspect their
source, but cannot supply independent behavioral acceptance of them. A new
session or different model does not establish independence: inspect what the
reviewer actually loaded. For a consequential recurring failure, use a
reviewer outside the target guidance when available and when its judgment
could change the repair. Otherwise retain the limitation and judge against
the observed work and real product constraints, not agreement with the text.
