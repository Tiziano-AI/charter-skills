# Charter · Apple Interface Design

Native quality comes from making the platform's structures serve the person's
work. Windows, navigation, commands, focus and material teach people where they
are and what an action will affect, and people expect them to behave the same
in every app. System components carry that learned behavior, so an app's
character comes first from its content and from the interactions particular
to its work; a familiar control is customized where the work gains something
and its meaning, placement and behavior stay recognizable. Apple styling cannot
rescue the wrong container, and a distinctive app need not abandon native
behavior.

This package develops that judgment across iOS, iPadOS, macOS, watchOS, tvOS and
windowed visionOS. When the framework is already chosen, start from that
framework's reference below. An Apple-inspired web page still has browser
semantics.

A question about one API or one control needs no container analysis: answer it
against the SDK, as described under API names below, and the framework
reference. A repair keeps the established type, color and voice unless the
defect concerns those choices; inspect the affected interaction without
reopening the rest of the design. The structural reasoning is for choosing or
repairing where work lives and how it adapts; the identity reasoning is for a
new app or screen whose look is still open.

## Choose a place that preserves the relationship

Look at how the person's objects relate. Peer destinations suggest tabs;
hierarchical browse and detail suggest a stack or split view; independent
documents may benefit from simultaneous windows. An inspector follows a selected
object's properties. A sheet concentrates a bounded dependent task, but is a poor
home for work requiring continuing access to what it covers.

The structure has a cost as well as a benefit. A permanent sidebar spends space
and attention when the task has no meaningful hierarchy. A menu-bar popover is
excellent for a glance or quick capture, but sustained editing needs a place
that stays open. Choose the native container from the relationship, not from
the product category or a familiar screenshot.

Shared data and scene-local selection, drafts, navigation and focus have
different lifetimes. Two windows can show the same document without sharing a
cursor. Menu commands must act on the intended active object. Restoration
reconstructs a useful place in the work; appearing again must not repeat the
operation that brought the person there. Closing a window, quitting an app and
stopping background work are separate choices whenever the implementation
makes them separate.

## Adapt the interaction, not a silhouette

Touch, pointer, keyboard, Pencil, crown, remote and spatial input change reach,
precision, focus and available attention. A device label or orientation is only
a proxy for the actual scene geometry. Desktop comparison can need dense
simultaneous panes; a watch interaction can need glanceable completion; TV
navigation is organized around focus rather than touch.

Accessibility changes the viable structure, not just final styling. Text
enlargement may turn a toolbar into overflow; keyboard traversal needs a stable
order and destination; nonvisual names and values must carry the distinction
the pixels communicate. An automation snapshot does not establish the assistive
interaction. Workarounds that change accessibility semantics also change what
assistive technologies receive, so preserve the person's ability to navigate,
act and copy where the task needs it. Reduced motion should preserve continuity
without requiring the animation. A clipped action under larger text is lost
capability, not cosmetic variance.

Search is also structural: corpus, scope, suggestions, result destination and
return path determine where the field belongs. Combining search and commands
can be efficient when finding an object remains distinguishable from acting
on it.

## Make hierarchy tangible

Content, controls and temporary presentations need recognizable relationships.
Placement, typography, spacing and grouping establish them before tint, glass
or motion. A compact symbol works when its meaning is familiar; text is better
when a mode, scope or consequence would otherwise be guessed.

For a concrete browse–act–return construction, the
[order counter](references/order-counter.md) contains an offline SwiftUI app,
native renders and an exercised status change. Its wide split view and compact
stack keep the same order identity while changing what is visible together.
Use it to follow state ownership, routing and command scope. The
[crate library](references/crate-library.md) is its dense counterpart: a
sortable table read against a reference track and worked from the keyboard.
Both are small fixtures exercised through their own menus; they demonstrate
those relationships, not every production density, appearance or assistive
interaction.

System bars and presentations coordinate geometry, material and accessibility.
Custom material is useful when it supplies a missing grouping or elevated
affordance. Its sampling background matters: moving media and adjacent glass
can change contrast without changing the foreground. Related controls can share
a material container; unrelated actions do not become related because they can
morph together.

When a surface feels detached, examine placement and grouping before adding
blur. When contrast fails, improve separation rather than continually increasing
tint. When motion disorients, simplify the transition rather than slowing an
unnecessary sequence.

## Spend identity in the content

People recognize a native app by how fully it behaves like its platform, and
remember it by how it draws its own subject. Start bars, menus, sheets,
settings, Back, search and ordinary controls from the system's components:
people already know them, and the components carry most of the adaptation to
text size, input, appearance and new OS releases, though the composition
around them still has to be inspected. Spend identity where only this app can:
its own objects drawn the way its field already draws them, its data drawn
well, an accent color, the design and width of the type that carries its key
figures, the icon and the symbols it chooses, the words it uses, and one
custom moment. That moment is the view or interaction that carries the
identity at full strength while the rest stays quiet and exact. A working tool
may spend it on precision rather than ornament; a creative tool may need
several related moments.

Take these choices from the subject's world rather than its category. Look at
what its people already read and handle (a tide table, a boarding pass, a
score, a dosage chart, a stroke-order diagram), the words and units they use,
how they work (at arm's length, one hand on a rail, a keyboard all day, a
glance between tasks), and the real content, with its long names, gaps,
exceptions and scripts. A tide planner's moment can be the tide curve with now
marked on it and heights in tabular figures. A kanji trainer's is the stroke
drawn under the Pencil in its proper order. A DJ's Mac library spends almost
nothing on ornament and everything on a dense, sortable table where tempo and
key line up. A party quiz on Apple TV can be loud in type, color and sound,
because play is the subject.

How much an app draws for itself depends on what its controls do for the
subject. A camera, instrument, game or drawing tool can own its controls,
because manipulating them is the work. For conventional navigation and actions
a system component gives people familiar behavior at less cost, and a custom
one has to improve how this subject is handled or understood while keeping
that behavior, not reproduce a standard control in another shape. A utility,
document app or business tool usually spends its character in content, icon
and words. A brand that already owns a typeface or color brings it through the
places that help this work, not through a redesign of every component.

Where nobody steers it, native work is likely to reach for the same few moves
whatever the subject. The list is an inference from web habits carried into
SwiftUI, not a measurement, and it shifts with the model and the year. Each is
right somewhere, and where the brief leaves the choice open it is a default
rather than a choice:

- A web page ported into a window: a scrolling column of padded, shadowed
  cards where `List`, `Form`, `Table` or a split view would carry selection,
  keyboard navigation, swipe actions and density. Cards suit a feed of unlike,
  rich objects.
- A card dashboard of big numbers and small labels as the first screen, when
  the person came to work on a queue, a document or a canvas. It suits
  glanceable monitoring.
- Fixed point sizes, `.rounded` on every heading and hard-coded colors, in
  place of text styles and semantic colors that follow Dynamic Type, dark
  mode and increased contrast. A fixed size suits a figure whose size is its
  meaning; a fixed color suits a drawing, artwork or a color-critical
  representation; rounded suits a subject that is soft or playful.
- Touch-sized rows, large capsule buttons and a single window on the Mac,
  where pointer-sized controls leave more attributes visible and menus and
  shortcuts carry the commands. A kiosk or touch-operated task keeps larger
  targets, and one bounded job suits one window.
- An all-caps label over every title and meta lines joined by middle dots,
  carried over from web templates, where the label repeats what the title
  says and the dotted line hides values people compare. Capitals suit a label
  the field itself prints in capitals, such as a departure board's column
  heads, or one that tells content kinds apart; a short dotted line suits
  related details nobody compares down a column.
- A custom control or self-drawn bar that only reproduces a system one: a
  floating pill tab bar, a hand-made Back button, a home-grown segmented
  control. A custom control suits the place where it improves how the subject
  is handled, and keeps the familiar action recognizable.
- Glass or a gradient wash laid over content as decoration, and a tint taken
  from the system list rather than from the subject. Glass suits floating
  controls that need separating from content; a gradient suits a continuous
  value or an atmosphere that belongs to the content; a system tint is right
  when color only means action.

[Native identity](references/native-identity.md) gives each default with its
alternative, worked translations for unlike subjects, and how to build the
custom moment so it stays native; open it when the look of a new app or
screen is open, or when an app feels interchangeable with its neighbors.

When the look is open, settle a direction before building, in decisions
concrete enough to be wrong: which view or interaction is the custom moment
and how it draws the subject; the accent and the few places it is spent; the
text style, design and width for each role, and which figure, if any, gets a
size of its own; the density on each platform; the verbs the interface uses.
Then ask two questions: would this have come out the same for any similar app,
and would anything in it feel foreign to someone who lives on this platform?
Where a sibling brief would leave everything unchanged, look for the
difference in the subject that was missed, and keep the similarities that make
the work easier: a two-factor code utility can rightly look like its
neighbors. Where something feels foreign, keep it only if it helps this work.
Ask both again of the first running build, which shows what the plan hid. A
new app warrants this; a new screen takes its app's direction; a repair checks
what it changes and takes no new direction.

An open look is settled with the person before anything expensive is built on
it, as `charter-visual-asset-production` describes; a few generated takes of
the custom moment or a key screen in distinct directions are usually the
cheapest way to put those directions before them. Take type, color, imagery,
material and the way content is drawn from the chosen take. Navigation and
controls come from the object relationships above, which a generated screen
does not know. Where the person has left the choice to you, or nobody can be
asked, commit to one direction and say which and why in a line or two
alongside the work.

## Craft that carries the identity

**Type.** Use the system text styles, `.largeTitle` through `.caption2`, as
the starting scale, and choose per role the weight, the design (`.serif`,
`.rounded`, `.monospaced`) and the width (`.condensed`, `.compressed`,
`.expanded`) for what people read and compare there: a serif for long
reading, a condensed width where long strings must fit a dense view, rounded
where softness belongs to the subject. `monospacedDigit()` gives figures equal
widths, so columns align and a changing number does not jitter; a condensed
width saves space but aligns nothing. A reading or brand face can carry
headings or sustained text when it covers the actual scripts and stays legible
at the sizes used; set it through `Font.custom(_:size:relativeTo:)` so it
scales with a text style. iOS, iPadOS, watchOS, tvOS and visionOS scale the
styles with Dynamic Type; macOS has no Dynamic Type, and its body style is 13
points where iPhone's is 17.

**Color.** Semantic system colors carry interface text, backgrounds and
separators. One accent, the `AccentColor` set in the asset catalog with dark
and High Contrast variants, marks actions and selection; warning, destructive
and completion states keep their own distinguishable treatment, and text or a
symbol's shape carries each state alongside its color. Where the accent is a
fill behind text, as in a selected row or a prominent button, every variant,
High Contrast included, is chosen to carry that text. On the Mac the person's
chosen accent replaces the app's unless they picked Multicolor, so identity
there cannot rest on the accent alone.

**Density.** Follow the input. Apple's default control size is 44 by 44 points
on iPhone and iPad and 28 by 28 on the Mac, and a Mac with a touch display
still starts from Mac density. People comparing many objects across
attributes on the Mac are served by a compact `Table` with sortable, resizable
columns; a glanceable or touch-operated task needs larger targets. Keep
commands discoverable in the appropriate menus, preserve the standard
shortcuts and add shortcuts for the app's frequent actions.

**Words.** Follow the language's conventions. In English, menu items, buttons
and alert buttons take title-style capitalization; an alert title that is a
complete sentence and its explanatory text take sentence style, and a title
that is a fragment takes title style. A command ends in an ellipsis when it
needs more information or a choice before it acts (Export…), not merely
because a window opens. One verb runs through a flow: the button, the menu
item, the confirmation and the Undo title (Undo Mark as Ready). Alert buttons
name the result (Delete, Replace); OK suits only a purely informational alert.
On platforms that support Undo, a reversible edit registers it with a named
action, which on the Mac is the expected route back; tvOS and watchOS need
their own clear way to correct a mistake.

**Checking.** Look at what the change can affect. For a new screen that is the
custom moment and the primary action in light and dark, with Increase Contrast
and Reduce Transparency, at the largest text size the platform offers, at
compact and wide sizes, and on the Mac with the window inactive as well as
active; a repair looks at the cases its change touches. An action that reads
as primary only through its tint stops reading that way wherever the tint is
not drawn; a key figure that truncates at large text has lost its job. Judge
glass and materials on screen or in a screen capture: a window the app draws
into a bitmap itself shows them as flat fallbacks.

[Native craft](references/native-craft.md) has the platform tables, the
matching API in each framework, copy conventions, feedback and haptics, and
the table of checks; open it when choosing type, color, density or copy, or
to pick the cases worth checking.

## Let lifecycle choose the framework seam

SwiftUI, UIKit and AppKit offer different object, scene and responder models.
Use the one that owns the needed capability, and bridge a specific gap without
creating two owners for the same state. A hosting view does not erase the
host's lifecycle responsibilities.

A UI object's callback is not necessarily delivered in UI isolation. Delivery
queue, actor isolation, cancellation and resource lifetime can decide whether
the design works; for speech, audio capture or another realtime callback, read
[callbacks and audio](references/callback-and-realtime-contracts.md) before
wiring results into the interface.

## Take API names and availability from Apple and the SDK

This package owns interaction judgment, not the current API surface. When
Apple's agent skills are available for the framework and task, use their
applicable API guidance. Check a symbol you recalled rather than read against
the selected SDK before depending on it:
`xcrun --sdk <iphoneos|macosx|xros> --show-sdk-path` locates the SDK, and its
frameworks' `.swiftinterface` files or headers give each declaration with its
availability; when the project builds, a build or typecheck is that check.
Related frameworks can expose the same idea through different declarations;
a plausible spelling borrowed from one is not an API in another. HIG informs
interaction; SDK declarations and applicable release notes govern
implementation.
[Official sources](references/official-sources.md) shows where to search and
how to typecheck a snippet.

## Depth for the decision in front of you

- [Native structure](references/design-principles.md) and
  [platform adaptation](references/platform-adaptation.md): containers,
  hierarchy and input relationships.
- [Native identity](references/native-identity.md) and
  [native craft](references/native-craft.md): where identity lives, the
  defaults it displaces, type, color, density, interface copy, feedback and
  the appearance check.
- [SwiftUI](references/swiftui.md), [UIKit](references/uikit.md),
  [AppKit](references/appkit.md), [visionOS](references/visionos.md):
  implementation mappings and platform boundaries.
- [Mac companions](references/macos-companion.md) and
  [assistant workbenches](references/assistant-workbench.md): presence,
  sustained work, commands, artifacts and background interaction.
- [Liquid Glass](references/liquid-glass-composition.md),
  [custom controls](references/custom-control-patterns.md),
  [icons and symbols](references/icons-and-symbols.md): material,
  interaction and optical identity.
- [Callbacks and audio](references/callback-and-realtime-contracts.md):
  delivery, concurrency, teardown and UI publication.
- [Official sources](references/official-sources.md): which Apple source
  settles which claim, and how to check an API in the SDK.
- Worked native apps, each with source and renders: the
  [order counter](references/order-counter.md) for navigation, shared state,
  command scope and text enlargement around one object; the
  [crate library](references/crate-library.md) for a dense table read against
  a reference, a keyboard path and meaning carried by shape and word.
- [Visual references](references/visual-reference.md): the worked apps first;
  linked official examples of identity, material and composition.
