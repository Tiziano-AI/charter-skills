# AppKit

Use this file when the task includes AppKit implementation, migration, or review.

## Source Anchors

- <https://developer.apple.com/videos/play/wwdc2026/289/>
- <https://developer.apple.com/videos/play/wwdc2025/310/>
- <https://developer.apple.com/documentation/appkit/nsstatusbar>
- <https://developer.apple.com/documentation/appkit/nsglasseffectview>
- <https://developer.apple.com/documentation/appkit/nsglasseffectcontainerview>
- <https://developer.apple.com/documentation/appkit/nsbackgroundextensionview>

## Decision-bearing modernization branches

Each branch applies when the change touches it. Take names and availability
from the selected macOS SDK's AppKit headers, as
[official sources](official-sources.md) describes.

- Inventory only the native and custom window, menu, toolbar, sidebar, inspector, text,
  collection, or bridging surfaces that intersect the chosen seam.
- Replace `mouseDown` overrides and tracking loops when selection, menus, drag-and-drop, control
  events, or gesture recognizers better own the affected interaction.
- Exercise keyboard navigation, custom status-item focus, graceful termination, or UI restoration
  when the change touches those behaviors or claims whole-surface readiness.
- Inspect `NSToolbar`, `NSSplitViewController`, sidebars, inspectors, scroll-edge behavior,
  concentric corners, or menus when custom structure or effects depend on them.
- Remove materials that block intended system glass; add `NSGlassEffectView` only for genuinely
  elevated controls that still need it.

## Strong Defaults

- Let `NSToolbar` handle automatic grouping.
- Use `NSToolbarItemGroup` or spacers to tune grouping when the automatic result is not semantically correct.
- Set `isBordered = false` on non-interactive toolbar items that should not read as buttons.
- Use prominent toolbar item styling only for true emphasis.
- Use split-item sidebar or inspector behaviors rather than hand-built floating panes.
- Use `NSStatusBar` when a persistent status item needs capabilities beyond SwiftUI `MenuBarExtra`.
- Use an `NSItemBadge` on a toolbar item's `badge` for a count or attention state, and let the item
  lead to the object the badge counts.
- Preserve keyboard and menu discoverability before adding visual treatments.
- Keep the window key-view loop current as views change.
- Where the deployment target supports `NSStatusItemExpandedInterfaceDelegate`,
  use it for a status item's custom window rather than toggling the window from
  the button's action, so the item joins keyboard navigation and menu tracking.
  When your own UI closes it, after a click elsewhere or a completed action,
  call `statusItem.expandedInterfaceSession?.cancel()`. Otherwise preserve those
  input relationships in the supported presentation route.

## Modern Input And Continuity

- Prefer collection or table selection APIs, view menus, and pasteboard delegates over decoding
  every interaction inside `mouseDown`.
- Use `NSTextSelectionManager` when a custom view needs native text-selection behavior, and use
  control events or `NSGestureRecognizer` for other custom interactions.
- Use `NSWindowRestoration` to reconstruct windows and UI state across launches. Persist the
  identifiers needed to rebuild the interface, not document or database contents that already
  have their own owner.
- Do not let a nonessential sheet or modal block graceful termination, and always complete a
  window-restoration request even when reconstruction fails.

## Sidebars And Edge-To-Edge Content

- When adopting the system's floating glass sidebar, remove an
  `NSVisualEffectView` override that prevents that chosen behavior. A deliberate
  opaque content surface is a different design, not inherently a defect.
- Use `automaticallyAdjustsSafeAreaInsets = true` on content that should extend under the sidebar.
- Use `NSBackgroundExtensionView` for hero imagery or artwork that should visually continue behind a sidebar.
- Keep actual text and controls outside the distorted extension area.
- Re-evaluate automatic scroll-edge effects, sidebar selection emphasis, and
  bordered toolbar items against the selected SDK before preserving an
  override of system behavior.
- When a control or view near a window corner should follow its container rather than hard-code a
  radius, override `cornerConfiguration` in the view subclass to return
  `.corners(radius: .containerConcentric)`. Unlike UIKit's, AppKit's property is get-only. Call
  `invalidateCornerConfiguration()` when the choice changes. A view that draws its own shape applies
  `effectiveCornerRadii` in `viewDidChangeEffectiveCornerRadii()`.

## Custom Liquid Glass

```swift
let statsGlass = NSGlassEffectView()
statsGlass.contentView = statsView

let container = NSGlassEffectContainerView()
container.spacing = 28
container.contentView = stackView
```

- Put content inside `contentView`; do not place a glass view behind content as a sibling.
- Use `NSGlassEffectContainerView` for nearby or morphing glass elements.
- Keep desktop density and command discoverability intact; not every AppKit control should become a large capsule.
- Favor calm, stable emphasis over animated intensity in multi-window workflows.

## Review Questions

- Did the migration keep keyboard, menu, and pointer affordances first-class?
- Are any custom materials still hiding the new toolbar or sidebar behavior?
- Are prominent toolbar treatments used only for emphasis or state?
- Does the design stay readable and calm in dense, multi-window workflows?
