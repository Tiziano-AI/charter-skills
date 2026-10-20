# Interaction mechanisms

Use mechanisms to explain a design choice, not named “laws” to certify it.
Familiar cognitive effects do not establish a universal menu size, response
threshold, conversion gain or emotional outcome. Likewise, a design-system
example records one vendor's convention, not a universal requirement.

## Predictability and orientation

Labels, placement and conventions let people predict what an action will do.
A familiar pattern reduces learning only when it carries the familiar meaning.
A checkbox that immediately purchases something is not made understandable by
looking standard.

Keep the current object, scope and state visible when they change the meaning
of an action. A destination summary can show where work will go while its
account chooser stays closed; the summary must track the actual target when
selection changes. Recognition reduces memory burden when it brings relevant
alternatives together, but showing unrelated choices alongside them makes the
comparison harder. Do not derive a fixed number of controls from working-memory
studies.

Information density is not the same as cognitive load. An expert comparing
many records may benefit from a dense table; a sparse sequence of cards can
force repeated navigation and memory. Remove irrelevant complexity, not useful
information.

## Attention and feedback

Hierarchy should reflect what matters now: a primary action, a changed value,
a warning or the content itself. Multiple emphatic elements compete. A quiet
surface can still fail if its next action is invisible.

Distinguish acknowledgement, ongoing progress and result. Feedback timing and
form depend on the action, expected latency and interruption cost. A local
button can show pending state without a page-wide spinner; a long background
job may need a persistent destination and later notification. Fabricated
percentages and endless activity animation damage trust.

Progress is informative when it tells people what remains or whether they can
leave. A checklist that reveals optional work as unfinished can instead create
an obligation the product never needed. Avoid making completion pressure the
source of engagement.

## Input and recovery

Prevent predictable slips through constraints, sensible grouping, separation
of destructive actions and clear consequences. Allow editing and undo when
the system can genuinely restore the prior state. Use confirmation for
consequential choices that cannot be safely recovered, not as compensation
for ambiguous controls.

Preserve correct input when another field fails. Validate at a point that
helps correction rather than scolding incomplete typing. Accept harmless
format variation when meaning is unambiguous; reject ambiguity where locale,
identity, money or destructive scope could be misread. Canonical output does
not require guessing ambiguous input.

Retry, cancel, undo and compensate have different meanings. Stopping a wait
may not stop remote work; retrying a create may duplicate it; refunding a
purchase does not erase the original transaction. Recovery design needs the
actual operation contract, not merely a set of reassuring buttons.

## Effort, defaults and disclosure

A default helps when the product can make a dependable choice for the common
occasion and people can adjust it when their needs differ. Requiring the same
stable preference on every operation gives that work back to them. A choice
about this operation's commitment is different: a saved destination or spending
limit may supply a starting value, but cannot supply consent or authority that
the operation still needs. Hidden scope or consent is not a useful reduction
in friction.

The same control can deserve different prominence in different products. A
model selector can be secondary in a creation tool, where the person wants an
artifact and rarely changes the model; in a model laboratory, selecting and
comparing models is the work. There, a dense view of settings and results can
reduce memory and navigation work. Calling a control advanced does not make
it optional, and its technical availability does not make it central.

Postpone setup that is optional or irrelevant to first value. Do not postpone
a consequential constraint until the user has invested effort they cannot
recover. If an import needs a connected account, the import action should lead
to that connection step rather than leave people to discover it in settings.
Disclosure can keep optional tuning from competing with the main path; it must
not conceal the required next step. Examples and sample data can teach the
interaction, but must remain distinguishable from real results.

## Embodied and inclusive interaction

Target size, spacing, reach, pointer travel and keyboard access affect action
cost. Large targets do not solve poor naming; tiny destructive adjacency can
create slips even when labels are correct. Design for the actual posture,
input method and consequence.

Contrast, text enlargement, focus, reading order and nonvisual names carry
meaning. Test the relevant complete interaction, not just isolated controls.
Localization changes string length, direction, sorting, date interpretation
and error comprehension; those are design inputs rather than final polish.

Visual craft can help people parse hierarchy and recognize care, but can also
make a misleading result seem more credible. Judge aesthetic quality and task
success separately, then make them reinforce each other.
