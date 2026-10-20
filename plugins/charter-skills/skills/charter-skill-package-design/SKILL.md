---
name: charter-skill-package-design
description: 'Skill package design when creating a SKILL.md skill or fixing one that
  misroutes, goes unused or underperforms: decide what belongs in it, write a truncation-proof
  card, put decisive rules in the body. Native creators scaffold.'
metadata:
  content_version: charter-skill-package-design@2026.10.12.0
---
# Charter · Skill Package Design

A skill packages expertise that changes how an agent handles a recurring job.
The agent meets it in three layers: a card (name and description) in a catalog
it scans before choosing, the SKILL.md body it reads once it has chosen, and
references, scripts or assets it opens when a subproblem calls for them. Each
layer fails differently, and an excellent body cannot rescue a card that is
never chosen.

A capable generalist already knows how to research, plan, act and check.
Specialist knowledge earns its place by explaining what that sequence does
not: why a transaction fails after an acknowledgement is lost, which visual
relationships make a composition legible, when a weighted decision model
misrepresents preferences.

## Decide what belongs in a skill

A skill loads only when the agent selects it, so some material belongs
elsewhere:

- Rules that apply to every task in a repository, such as commit message
  format or files never edited by hand, belong where every task reads them or
  a check enforces them, since a skill may go unselected;
  `charter-instruction-system-design` owns which layer carries a rule.
- Library or API documentation the agent can read on demand from
  version-matched sources, such as generated docs or the installed package, is
  not something to bundle. Keep only the project's own non-obvious usage.
- A catch-all "repo assistant" skill competes with every neighbor and routes on
  nothing. Split by job: each package owns one recurring job with its own
  trigger, such as preparing release notes.
- Responsibility for one task belongs in its brief or role, and operating one
  product may need that product's own manual rather than another portable
  skill.

Two packages that compete for the same decision and payoff usually need one
owner; two jobs that share vocabulary can deserve separate packages when each
needs its own method. Scaffolding (directory layout, frontmatter template,
validation) comes from the harness's native skill creator; the judgment about
boundary, card and content is the work here. The text of one prompt or agent
role is `charter-prompt-design`'s job, and where a rule lives across a
composed instruction system is `charter-instruction-system-design`'s. A small
defect, such as a broken link, a malformed field or a typo in a card, needs
only its fix.

## The card decides whether the body is read

Before the body loads, the agent has only the card. "State management" names a
topic; "recover an interrupted workflow without duplicating an uncertain
effect" names a consequential problem and a first action different from
ordinary implementation.

Catalogs can cut cards to fit a budget, keep only an opening prefix or show
some packages by name alone. Inspect the listing the selector actually sees;
the name itself should say the job when its description is absent.

- Put the domain noun and the discriminating condition in the first clause, in
  the words users have for the objects involved (file types, artifacts,
  tools), then the payoff, then any boundary against the nearest neighbor.
- Count the characters. When you know where a listing cuts, everything
  decisive has to fall before that point. A boundary clause past the cut does
  not exist for the selector, so shorten the payoff or leave the boundary to
  the body.
- Name the job rather than claiming a whole area. "Always use this for any
  database work" over-triggers and takes query work from a SQL skill; "write or
  review schema migrations" routes the right work.
- Keep the method out of the card; squeezing it in makes recognition worse.

[Routing metadata](references/routing-metadata.md) covers field constraints,
YAML quoting, listing limits and invocation controls; open it when writing
frontmatter or harness metadata, alongside the target loader's schema.

## The body carries the first move

Some models read SKILL.md and rarely open its references, even when allowed to.
Whatever changes the agent's first substantive move belongs in the body: the
decisive rule ("drop a column in two deploys: first stop the code using it,
then drop it"), the routing between input types, the default that avoids the
common mistake. A body that says only "see references/" hides the rule from
exactly those models.

A reference carries depth for a recognizable subproblem, linked with a cue that
says when to open it ("open when totals or VAT don't reconcile"). Code the
agent would otherwise retype goes into `scripts/` with explicit inputs, outputs
and failure behavior, and the body gives the command to run. A template helps
when the output has stable structure and hurts when its headings imply
findings that do not exist. History, team lists and explanations of what the
model already knows come out. A package never holds a secret; the body says
where the credential comes from.

For judgment-heavy work, the body gives a causal model from which the agent can
derive an approach, plus a nearby case where the same intervention is wrong:
an explanation of retry amplification separates overload from a merely slow
response, while "increase the timeout, then retry" does not. Exact procedures
stay where dependencies are real, such as a signing sequence or a reversible
data transition. [Resource design](references/resource-design.md) covers what
moves out of the body, redesigning a package that already has resources, and
scripts, templates and visual assets; open it before splitting or
restructuring a package.

## When a package misses

Start with the requested result and the observed miss, then distinguish what
was available, selected, read and applied. An unselected skill may have an
unclear card, a missing or truncated listing, or a selector that never
considered its expertise. Rewrite the card when recognition is the supported
defect, not merely because selection failed. Knowledge that arrived can still
be unused, misapplied or insufficient; apparent compliance does not isolate a
wrong causal model in the package.

Missing knowledge may call for a richer body; unreachable depth may call for
a clearer cue or moving the decisive part into the body. A task that needs
construction can instead need a reusable source, native component, practical
demonstration or different production tool. Inspecting a finished example can
teach recognition without teaching how to build it. Match the resource to the
missing ability, and retain the possibility that the model's capability, or
the available evidence, is the limit rather than the package's wording.

Check a package when the result would change what you do with it:

- After a selection repair, use natural requests without naming the skill.
  A named run helps when the difference would separate recognition from
  application; it cannot count as spontaneous selection.
- When deciding whether a package earns its place, or which of two cards to
  keep, compare runs with and without the skill on a few realistic tasks and
  near-miss requests.

Use the native creator or evaluator available in the target harness for the
checks it actually supports: with-skill and baseline runs, selection on
should-trigger and near-miss requests, or a fresh agent handling a realistic
task. A source validator cannot stand in for those observations. [Package
observations](references/discriminating-package-probes.md) explains how to read
a miss by layer and choose a check; open it when a package underperforms and
the failing layer is not obvious.
