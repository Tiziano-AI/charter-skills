# Reviewing instructions after a model or harness upgrade

Use this when a new model, a new app or CLI release, or a changed base prompt
has been adopted and the question is which of your own instructions to keep,
change, move or drop. Adoption is a composition problem: a vendor base, your
replacement or additions, and independent runtime messages can supply,
duplicate or contradict different parts of the model's guidance. The decision
is what local contribution stays useful in the composed system the adopted
release actually delivers, not how much vendor text to copy.

## Know when a review is due

Runtimes upgrade on their own schedule, often automatically, so a review needs
a trigger rather than a habit. Record, with each runtime's facts, the release
they were last reviewed on and the places that encode them: the runtime layer
of the instructions, and the data and code that depend on the runtime's names
and formats, such as tool deny lists, agent definition fields, transcript
readers, settings checks and skill locations. When a session or the installed
runtime reports a newer release than the recorded one, review those places
against it, assign each change to its owner and record the new release.
Between reviews, a runtime fact written as its consequence rather than as a
current name or number degrades instead of misleading.

## Source identity precedes comparison

Establish the release that runs and read what it ships:

- the app or binary that executed the work, and its version;
- the model, and its record in that release's model catalog;
- that release's base template for the model, and the configuration that
  selects your replacement or additions.

A moving upstream head, the version of whatever binary is first on the PATH or
a cached catalog does not identify it. A desktop app can run a build of its own
beside the CLI on the PATH, several releases apart, and can update apart from
the runtime it embeds, so a template read from upstream main may match neither.
Where the runtime keeps a session record, the release that record carries
settles which one ran, with the base instructions the thread captured where the
record keeps them; where sessions record no release, the runtime's own version
report is the nearest evidence. Keep accepted source, the candidate in your
worktree and the observed runtime distinct.

When the trigger is a behavior seen after the upgrade, establish what that
thread loaded before touching any wording. A thread that ran on built-in
instructions, or one resumed with instructions it captured before your change,
says nothing about your current text; only a fresh thread on the adopted
release shows what the setup now delivers. If the behavior persists once your
instructions are confirmed loaded, examine it as a separate question against
the template and binary that actually ran.

## Map the composition before interpreting prose

A replacement base coexists with separately injected messages: modes,
permissions, tool descriptions, skill discovery, workplace guides, model-switch
and other transition messages. Their selectors and capture times decide what
reaches an occurrence, and declared configuration can differ from what the
process or request that consumed it used. Fresh, resumed and model-switched
sessions can differ,
and CLI, IDE, desktop, local and cloud surfaces need not select the same
inputs. Compare them when the difference can change the decision, reading the
selecting implementation where that is what settles it.

Where your file replaces the vendor base, editorial changes in the vendor
template never reach the model. The review only has to catch new
behavior-bearing content: a changed tool contract, or a rule the old base
supplied that nothing else now supplies. Where the harness keeps the vendor
base and appends your files, an upgrade changes the text beneath yours; read
what the new base says and drop local copies of what it now supplies.

Tool names, effort mappings, transport and context limits belong to the current
schemas and configuration, not to prose. A catalog's request mapping does not
establish a child's settings, and a provider maximum does not choose an
operating threshold. Native mode hints are not a channel for imposing local
delegation preferences.

## Find the contribution, not an editorial delta

For each behavior that matters, ask what supplies it and what would change if
your instructions did not:

- The runtime or the new base already supplies it: rely on it, because a local
  copy is a competing carrier.
- The adopted base dropped something useful and nothing else supplies it: add
  it at its proper owner.
- The knowledge is specialist or about one place: make it conditional at that
  owner.
- Only maintainers need the fact: keep it out of standing model input.
- The instruction is redundant, conflicting or unhelpful: remove it, or reject
  it explicitly.

For example, if native mode guidance already supplies a behavior independently
of the replacement base, copying it locally adds a competing carrier rather
than repairing an omission. If the replacement removed a useful behavior that
no other message supplies, rejecting it for textual similarity would miss a
real contribution. The composition decides which case applies.

Literal compliance is a useful counterfactual: would obeying this sentence
improve the intended work, or could it replace the work with procedure? Greater
model capability makes old scaffolding worth reconsidering; it does not make an
authority or fidelity constraint obsolete. A vendor's announced tendency, such
as more literal reading or more eager tool use, is a hypothesis until it shows
up in real work under your unchanged instructions. Change wording for a
tendency you have seen, one change at a time, so each change stays
attributable.

A paragraph may carry several meanings with different owners, and several
changed sentences may express one unchanged behavior. Compare at that level,
not by headings, line count or diff volume.

## Decide at the owner that can change the behavior

Recommend change or no change with the decisive source evidence and the owner
of each item, including what you keep and what you reject, not merely a list of
files inspected. Shared prompt, harness layer, skill, role and workplace guide
have different jobs, and an accepted meaning needs one carrier. When a release
brings only typo and editorial template edits with unchanged tools, your layer
stays as it is and the review says so briefly. Do not pin vendor wording,
headings or length in tests: such a test fires on every editorial change and
protects nothing the model depends on. Recording the reviewed release, or
checking the exposed tool list at adoption, is enough.

After a change, a fresh session on the adopted binary and model can show
whether your file loaded. Its next choices and result, not loading alone,
show whether the revised knowledge guided the work.

When many decisions interact, a compact record keeps them reviewable after the
comparison is over. It is a current decision, not a release diary:

| Behavior or surface | What the adopted runtime supplies | What would be missing without yours | Decision and reason | Evidence and what remains open |
| --- | --- | --- | --- | --- |
| Meaning that changes work | Native supply | Local contribution | Keep, change, move or reject | Source basis and consequential unknown |

Name the exact operands read (release, template, catalog record,
configuration) and the composition operator that changed: "the prompt
changed" is too vague when only one selector did. Keep a direct observation
distinct from an inferred correspondence. Combine editorial variants that
have one consequence, split a paragraph whose
meanings belong to different owners, and skip rows for release-note sentences
that change nothing. Record the accepted source changes and the carriers
derived from them, and name which result you observed (source changed,
projected, loaded) rather than calling everything adopted. A narrow adoption
choice needs no table.

Release research stays with maintainers unless the model needs its conclusion
to act.
