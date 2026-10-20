# Visual systems in implementation

A visual system makes recurring decisions once, where the implementation can
preserve them. It is useful when a change to a shared relationship improves all
its legitimate instances without a tour of screen-specific corrections. Tokens
and component names are inputs to that system, not evidence that it exists.

## Separate a control's geometry from its placement

The control owns its internal relationships: text metrics, padding, border,
icon box, label gap, relevant states and supported size or emphasis variants.
Its containing screen owns grouping, placement, available space and the
relationship to surrounding content. A toolbar can align and space its actions
without independently setting each button's internal padding.

The distinction follows the repeated decision, not a particular framework.
A shared CSS class may be a sufficient owner; a component can own structure and
behavior where those recur too. A token for every measurement is not required.
Conversely, a component named Button supplies little consistency if each caller
passes a different line height, padding and minimum height for the same role.

A local adjustment is reasonable when its context is genuinely different.
If several screens need the same exception, the family may be missing a
meaningful variant. Name that variant for the recurring use, such as a compact
table action, rather than the screen that first needed it. Do not make every
one-off arrangement reusable or build an exhaustive library before its uses
exist.

## Geometry is a combination

For an ordinary single-line control in normal flow, the line box, vertical
padding and borders contribute to its height; a minimum height can enlarge it.
An icon or other child can become the tallest item. Explicit heights, box
sizing and flex or grid stretching can change that result. Equal font sizes
therefore do not establish equal control geometry.

When a rendered relationship is wrong, trace the role and variant to the
computed result. A label's line height may have changed while its nominal font
size stayed fixed. An SVG's view box may include empty space that makes its
visible mark look smaller than another icon in the same box. A parent with
stretch alignment and a separate minimum height may silently resize the child.
Correct the first owner that introduces the unexplained difference; another
screen-local correction leaves both rules in competition.

Optical alignment and box alignment are related, not identical. The visible
mark of an icon can need a small internal adjustment while its consistent box
keeps spacing stable. A compact badge may align with the text of a taller
button; its passive role does not require the same hit target. Actionable
controls still need sufficient targets and separation for their input method.

## Variants preserve a family while serving different jobs

Size, emphasis, content arrangement and state answer different questions.
A primary and a secondary action can share geometry while differing in
emphasis. A compact table action and a prominent starting action may differ in
size while preserving their label/icon relationship and focus behavior.
Combining variants should keep those purposes intelligible rather than create
an arbitrary set of per-screen appearances.

The same control can carry a short label, a longer translated label, an icon,
a pending indicator or a disabled state. Decide what needs to remain stable
through the actual transitions. Replacing text with a spinner can shrink a
button and move adjacent actions; keeping the label or a deliberately reserved
local width can preserve the relationship. Conversely, a wide reservation for
a rare status can leave a conspicuous empty strip in every ordinary state.
Reserve space for a reason visible in the transition, not as a blanket ban on
movement. Wrapping a long label may be better than truncating its meaning.

Changing a count should not move an action unnecessarily; tabular figures can
stabilize its digits, while grouping keeps the count associated with its
object. They do not solve a label that outgrows the whole row. At that boundary,
the composition may need to wrap or change arrangement while the controls keep
their internal contract.

## Compare relationships in their actual contexts

A component specimen makes variants and states easy to compare. The same
component in a real toolbar, dense row and empty state reveals what the
specimen omits: inherited type, wrapper stretching, constrained width and
competing emphasis. Inspect the instances relevant to the problem together,
including the content or state that exposes the difference. There is no need
to enumerate every theoretical combination.

The [control-family study](composition-contrasts.md#shared-control-family)
shows shared names with local geometry beside a family whose internal
relationships survive changes of screen and state. Look at the actual image,
then at the source owner when the question is why the difference occurs.
Making all items the same height would erase a useful distinction between
status and action without necessarily repairing the row.

## Further depth

[Carbon's button specifications](https://www.carbondesignsystem.com/building-blocks/core/components/button/specifications)
separate anatomy, measurements and states;
[its usage guidance](https://www.carbondesignsystem.com/building-blocks/core/components/button/guidelines)
relates variants to their contexts. The transferable knowledge is ownership of
relationships, not Carbon's measurements or visual style.
[Spectrum's attention hierarchy](https://spectrum.adobe.com/foundations/attention-hierarchy)
explains how emphasis works across controls and content: a family can be
internally consistent while competing with the wrong thing on the page.
