# Routing metadata

Use this when writing `SKILL.md` frontmatter or a harness's metadata file for a
skill.

## Frontmatter in the Agent Skills specification

- `name` is required: 1-64 characters, lowercase ASCII letters, digits and
  hyphens only, no leading or trailing hyphen, no consecutive hyphens, and
  exactly the name of the parent directory.
- `description` is required: 1-1024 characters. It says what the skill does
  and when to use it, and the specification asks it to include specific
  keywords that help an agent identify relevant tasks. Those are the words
  users have for the objects and artifacts involved (file types, formats,
  tools), not a list of trigger phrases.
- Optional fields: `license`; `compatibility` (1-500 characters, only for real
  environment requirements such as required system packages or network
  access); `metadata` (a map from string keys to string values); and the
  experimental `allowed-tools`, one space-separated string whose support varies
  by agent.
- Keep file references one level deep from `SKILL.md`.
- Add a field only when a loader in use needs and accepts it. A loader can
  reject unknown keys rather than ignore them, so a skill meant to travel
  keeps harness extensions out of its portable source unless each consumer
  accepts them. Check the specification and the actual target loader's schema.
- Put trigger conditions in the description, not only in the body: the body
  loads after selection.

## Quoting

YAML reads an unquoted value by its own rules, and a description is a
sentence.

- Double-quote `description`. A sentence routinely contains `: `, which YAML
  rejects as a nested mapping, or ` #`, which starts a comment and silently
  drops the rest. An unquoted value that begins with a backtick, `@`, `[`,
  `{`, `*`, `!`, `|`, `>` or `%`, or with a quoted phrase followed by more
  text, fails to parse, and one that begins with `&` loses its first word to
  an anchor.
- Double-quote any other string that contains that punctuation, or that a YAML
  loader could read as another type: `yes`, `no`, `on`, `off`, `true`, `null`,
  numbers, and dates such as `2026-09-26`.
- Plain identifiers such as a skill's `name` can stay unquoted when the loader
  reads them as strings.
- Inside double quotes, escape `"` and `\`.

A frontmatter parse failure usually makes the loader skip the whole skill
before its body loads, so parse the frontmatter after editing it.

## Writing the description

The card has to work when the user describes the job and never names the
skill. Its positive sentence exposes the concrete task and the decision,
artifact, action or improvement the skill helps produce. A payoff that appears only after
a long noun list arrives too late for a crowded catalog. Prefer plain work
verbs such as decide, choose, trace, classify, recover or design; internal
taxonomy and schema terms stay in the body unless they are the user's actual
object. A short card that loses the trigger or the output has failed, however
compact it is. Keep the card well inside the 1024-character limit and preserve
the distinctions that decide selection before brevity; display budgets are the
harness's, and thinning the body or references does not fix a card.

## Harness extensions

Harnesses may add frontmatter keys, sidecar metadata or configuration controls.
Use only fields the target loader accepts, and inspect the rendered listing
when recognition depends on its selection or truncation behavior. Per-card
limits and whole-catalog budgets can hide different parts of a description;
changing the body cannot restore a discriminator cut from the card.

Keep the controls separate:

- **Model discovery:** whether the model can find and select the skill without
  the user naming it.
- **User invocation:** whether the person can start it through a menu or
  explicit invocation.
- **Presentation:** the display name, description and invocation affordance
  shown to a person or selector.
- **Dependencies and tool access:** what capability the skill needs and what
  the host allows an invocation to call.

These can live in different fields and need not imply one another. Hiding a
skill from a user menu need not hide it from the model, and listing a tool
dependency need not install or authorize it. Read the exposed contract before
assigning those effects to a metadata value. Quote string values and keep
booleans typed according to the schema.

Discovering expertise is not authorizing its effects. A skill about deployment
or correspondence may be useful for preparation and diagnosis before any
deployment or message is permitted. Do not make it explicit-only merely
because some of its operations have side effects; effect authority belongs to
the requested action and its governing controls. Explicit-only invocation can
still be appropriate when deliberate invocation is itself the intended
product interaction or an actual boundary requires it. When recognition is
the defect, fix the card rather than hiding knowledge from the tasks it should
serve.

Human-facing display names and short descriptions are scan copy, not a second
trigger list; a suggested invocation prompt is a start affordance for deliberate
use, not the selection mechanism. Add icons and brand colors
only when an interface uses them, with real package-relative paths and files of
the right type and size for where they appear.

## Metadata parity

The description, display name, short description, default prompt, invocation
policy, references and any inventory or manifest entry describe the same
skill boundary. When one changes, check the others. When a card or name is
replaced, check the new one by routing; a test that the old wording never
appears protects nothing a model depends on.
