# Native structure and hierarchy

## Choose a place for the work

Container choice determines navigation, focus, restoration and action scope.
Start from the relationship among the person's objects and tasks:

| Relationship | Candidate native structure | A reason to choose differently |
| --- | --- | --- |
| Peer destinations or modes | Tabs | The work is a hierarchy or simultaneous comparison |
| Hierarchical browse and detail | Navigation stack or split view | A shallow task gains nothing from permanent navigation chrome |
| Parallel objects or documents | Separate windows | The views are inseparable steps of one operation |
| Selected-object properties | Inspector | The content is primary work, not supporting properties |
| Brief contextual choice | Menu or popover | The operation needs sustained reading or a branching flow |
| Bounded dependent task | Sheet | The person needs concurrent access to the underlying work |
| Quick presence and entry | Menu bar extra or status item on Mac | Most use requires a workspace |
| Window-associated spatial controls | Ornament on visionOS | The task needs immersive or volumetric interaction |

These are alternatives to reason with, not a layout template. A focused utility
may have no sidebar. A document app may need several peer windows rather than
one “main” workspace.

## Keep state attached to the right object

Data, selection, focus, navigation and presentation have different lifetimes.
In multiwindow work, two windows can share a document while keeping different
selections and scroll positions. App-wide commands must act on the intended
scene or object rather than whichever model was most recently updated.

Restoration should rebuild a place in the work. Preserve identifiers and
necessary transient state without making a second database. Recreating a view
must not resubmit a purchase, send or background job.

Search is an architecture decision: corpus, scope, result destination,
suggestions, filters, cancellation and the route back. Choose field placement
after those meanings are clear. A combined search/command palette can be useful
if it makes the distinction between finding and acting legible.

## Hierarchy and material

It is often useful to distinguish content, navigation or controls, and
temporary presentations. These are visual relationships, not a requirement to
classify every view into three planes.

Use grouping and placement before adding emphasis. Controls near their
content make scope legible; toolbars group shared commands; persistent
navigation should not be confused with contextual actions. Overflow is useful
for secondary commands, but hiding a primary action is not a density solution.

Liquid Glass and other materials should express elevation and interaction.
Prefer native containers where they already provide the desired behavior.
Remove an override when it conflicts with the chosen system behavior, not
merely because it is custom or old. Use
[material composition](liquid-glass-composition.md) for sampling, grouping and
background decisions.

## Shape, typography and identity

Container-relative shape can make nested controls coherent. Fixed radii and
sizes can fail as windows, text and control families change. Preserve desktop
comparison density rather than converting every Mac control into a large
capsule.

Typography and alignment carry hierarchy even without color. Use dynamic
colors and materials where they fit the system; do not make a brand treatment
obscure state or legibility. Symbols are compact when their meaning is known;
text is better when the action would be guessed.

Motion should explain continuity or state. A source-anchored transition can
help orientation, but motion is not required to prove that two objects relate.
Preserve the interaction under reduced motion rather than merely slowing
an elaborate sequence.

## Adaptation and access

Design around available scene geometry and input. Text enlargement, keyboard
navigation, contrast and transparency preferences can change the viable
structure. Do not mistake a clipped view at one accessibility setting for a
cosmetic problem.

Inspect actual content under the conditions affected by the change. Glass
over a static neutral background tells little about moving media. A simulator
screenshot does not establish keyboard focus, VoiceOver traversal, spatial
comfort or command routing between windows.

## Authorities

- <https://developer.apple.com/design/human-interface-guidelines/>
- <https://developer.apple.com/design/human-interface-guidelines/toolbars>
- <https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos>
- <https://developer.apple.com/videos/play/wwdc2026/250/>
- <https://developer.apple.com/videos/play/wwdc2026/292/>
- <https://developer.apple.com/design/whats-new/>

Use the applicable guidance for the target platform and SDK. The design
choices above are an interpretation for product work, not additional Apple
API requirements.
