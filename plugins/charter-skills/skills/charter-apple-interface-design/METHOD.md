# Charter · Apple Interface Design

Native quality comes from making the platform's structures serve the person's
work. Windows, navigation, commands, focus and material teach people where they
are and what an action will affect. Apple styling cannot rescue the wrong
container, and custom character need not mean abandoning native behavior.

This package develops that judgment across iOS, iPadOS, macOS, watchOS, tvOS and
windowed visionOS. When the framework is already chosen, start from that
framework's reference below. An Apple-inspired web page still has browser
semantics.

A question about one API or one control needs no container analysis: answer it
against the SDK, as described under API names below, and the framework
reference. The structural reasoning is for choosing or repairing where work
lives, how it adapts and how it looks.

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
Use the source when that relationship is the problem; its bakery identity and
two-state queue are not a template for every native product.

System bars and presentations coordinate geometry, material and accessibility.
Custom material is useful when it supplies a missing grouping or elevated
affordance. Its sampling background matters: moving media and adjacent glass
can change contrast without changing the foreground. Related controls can share
a material container; unrelated actions do not become related because they can
morph together.

When a surface feels detached, examine placement and grouping before adding
blur. When contrast fails, improve separation rather than continually increasing
tint. When motion disorients, simplify the transition rather than slowing an
unnecessary sequence. These corrections preserve room for expressive craft:
optically balanced forms, satisfying direct manipulation and a distinctive
content world without sacrificing operability. For a new app whose look is
still open, a few generated takes of a key screen in distinct directions,
shown to the person, can find that world before it is built;
`charter-visual-asset-production` says when they help and how to make them.
Take type, colour, imagery and material from them, not controls or layout,
which follow from the native structure.

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
- [Worked native flow](references/order-counter.md): source, navigation,
  shared state, command scope and text enlargement in a small order counter.
- [Visual references](references/visual-reference.md): the worked flow first;
  linked official conference and newsroom examples for material comparisons.
