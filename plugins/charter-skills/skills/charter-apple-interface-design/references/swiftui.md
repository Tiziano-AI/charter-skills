# SwiftUI

Use this file when the task includes SwiftUI implementation, API mapping, or code review.

## Source Anchors

- <https://developer.apple.com/videos/play/wwdc2026/269/>
- <https://developer.apple.com/videos/play/wwdc2026/292/>
- <https://developer.apple.com/videos/play/wwdc2025/323/>
- <https://developer.apple.com/documentation/swiftui/menubarextra>
- <https://developer.apple.com/documentation/swiftui/navigationsplitview>
- <https://developer.apple.com/documentation/SwiftUI/Adding-a-search-interface-to-your-app>
- <https://developer.apple.com/documentation/SwiftUI/bringing-multiple-windows-to-your-swiftui-app>
- <https://developer.apple.com/documentation/swiftui/openwindowaction/callasfunction(value:)>
- <https://developer.apple.com/documentation/swiftui/settingslink>
- <https://developer.apple.com/documentation/swiftui/scene/commands%28content%3A%29>
- <https://developer.apple.com/documentation/swiftui/commandmenu>
- <https://developer.apple.com/documentation/swiftui/commandgroup>
- <https://developer.apple.com/documentation/swiftui/glasseffectcontainer>
- <https://developer.apple.com/documentation/swiftui/glass>
- <https://developer.apple.com/documentation/swiftui/glassbuttonstyle>
- <https://developer.apple.com/documentation/swiftui/view/glasseffectid(_:in:)>
- <https://developer.apple.com/documentation/swiftui/view/glasseffect(_:in:)>
- <https://developer.apple.com/documentation/swiftui/glasseffecttransition>
- <https://developer.apple.com/documentation/swiftui/view/glasseffecttransition(_:)>
- <https://developer.apple.com/documentation/swiftui/view/glasseffectunion(id:namespace:)>
- <https://developer.apple.com/documentation/swiftui/view/backgroundextensioneffect()>
- <https://developer.apple.com/documentation/swiftui/view/searchtoolbarbehavior(_:)>
- <https://developer.apple.com/documentation/swiftui/view/safeareabar(edge:alignment:spacing:content:)>
- <https://developer.apple.com/documentation/swiftui/view/tabbarminimizebehavior(_:)>
- <https://developer.apple.com/documentation/swiftui/view/tabviewbottomaccessory(content:)>
- <https://developer.apple.com/documentation/swiftui/labeledcontent>
- <https://developer.apple.com/documentation/swiftui/accessibilitychildbehavior/combine>
- <https://developer.apple.com/documentation/swiftui/view/accessibilityidentifier(_:)>
- <https://developer.apple.com/documentation/swiftui/view/textselection(_:)>

## Names, availability and adoption

This file maps design decisions to SwiftUI structures; it is not the API
catalog. For names, signatures, availability and adoption, use the relevant
Apple-authored framework guidance when it is available. Reordering, image
caching, toolbar overflow, state initialization and document protocols each
depend on the API the project actually builds against. Confirm the declaration
in the selected SDK; many shape
and view types are declared in `SwiftUICore` rather than `SwiftUI`.
[Official sources](official-sources.md) shows where to search and how to
typecheck a snippet.

Adopt a newer API when it replaces a local substitute that intersects the
work: a hand-built reorder, image cache or eagerly initialized observable
state. For a document-based app, choose the document protocol and creation flow
from the actual access, diffing and file-size requirements. Re-test resizable
windows, toolbar overflow or minimization, inactive-window appearance or mixed
UIKit and SwiftUI geometry when the affected layout depends on them.

Prefer `NavigationStack`, `NavigationSplitView`, `TabView`, toolbars, sheets
and search where they own the structure; remove conflicting backgrounds and add
custom glass only where the standard structure still fails the intended
hierarchy.

## Strong Defaults

- Use `NavigationSplitView` when hierarchy and parallel panes matter.
- Use `WindowGroup` and `openWindow` when separate objects benefit from simultaneous windows instead of deeper navigation.
- Use `MenuBarExtra` for quick status and quick entry, not for deep workspace flows.
- Use `backgroundExtensionEffect()` when content imagery should visually extend behind the sidebar without duplicating interactive content.
- Use `SettingsLink` for standard settings entry instead of inventing custom settings affordances.
- Use `tabBarMinimizeBehavior(.onScrollDown)` when content-first behavior is valuable on iPhone.
- Use `tabViewBottomAccessory` only for persistent cross-section accessories, not screen-specific actions.
- Group toolbar items by meaning with `ToolbarItemGroup` and `ToolbarSpacer`, not by implementation order or arbitrary whitespace.
- Put app-wide actions in the menu bar with `commands`, `CommandMenu` and `CommandGroup`, and route them to the active window's object through `focusedSceneValue` and `@FocusedValue` rather than a global current item.
- Design search scope, suggestions, result destination, cancellation, and focus behavior before
  treating `.searchable` as a visual modifier choice.
- When people need to reorder content in lists, grids or sections, use the current
  reorderable-container support rather than preserving a list-only interaction by accident.
- For read-only property rows, consider `LabeledContent` before manually replacing
  accessibility elements. Keep the property's name distinct from its value, and
  preserve any required text selection and copying in the actual composition.
  Combining static fragments can improve spoken reading; combining controls can
  move their actions onto the group. Keep separately navigable controls when that
  navigation matters, and preserve access to each needed action when grouping.
  An accessibility identifier targets an element for automation; it is not its
  spoken label.

## Custom Liquid Glass

Use only for custom elevated controls.

```swift
BadgeView()
    .padding(.horizontal, 14)
    .padding(.vertical, 10)
    .glassEffect(.regular, in: .rect(corners: .concentric))
```

`.rect(corners: .concentric)` is shorthand for `ConcentricRectangle()`: the
corners follow the enclosing container's shape instead of a fixed radius, and
`.concentric(minimum:)` sets a minimum radius. System containers supply that
shape; inside a custom container, declare it with `.containerShape(_:)`.
UIKit and AppKit spell the same idea `containerConcentric` on `UICornerRadius`
and `NSViewCornerRadius`; that spelling does not exist on SwiftUI shapes.

- Default to `.regular`.
- Use `.clear` only over media-rich backgrounds after real legibility testing.
- Prefer `.buttonStyle(.glass)` and `.buttonStyle(.glassProminent)` before building custom treatments.
- Keep custom glass attached to control affordances, not to content slabs.

## Advanced Custom Control Notes

- Use `glassEffectTransition(_:)` for explicit transition behavior when a custom glass control appears or changes state.
- Use `glassEffectUnion(id:namespace:)` only when related glass elements need to read as one group despite greater spacing.
- Use `searchToolbarBehavior(.minimize)` on iOS and visionOS when toolbar search is useful but should stay visually subordinate until needed.
- Prefer stable `GlassEffectContainer` groupings over one-off isolated glass controls scattered around the screen.

## Grouping And Morphing

```swift
@Namespace private var glassNamespace

GlassEffectContainer(spacing: 28) {
    Button("Edit") { }
        .buttonStyle(.glass)
        .glassEffectID("edit", in: glassNamespace)

    Button("Done") { }
        .buttonStyle(.glassProminent)
        .glassEffectID("done", in: glassNamespace)
}
```

- Use `GlassEffectContainer` when nearby glass elements should share a sampling region.
- Use `glassEffectID` with a shared namespace when elements morph between related states.
- Keep grouping logical; do not merge unrelated actions just because the effect looks impressive.

## Presentations And Continuity

```swift
@Namespace private var transition
@State private var showSheet = false

Button("Info", systemImage: "info.circle") {
    showSheet = true
}
.matchedTransitionSource(id: "info", in: transition)

.sheet(isPresented: $showSheet) {
    InfoView()
        .navigationTransition(.zoom(sourceID: "info", in: transition))
}
```

- Prefer source-anchored transitions for sheets or detail presentations that originate from a specific control. The zoom navigation transition is unavailable on macOS.
- Remove old `presentationBackground` overrides unless they are still truly necessary.
- Use `safeAreaBar` or `safeAreaInset` to preserve readable margins around floating controls instead of manually padding around guessed bar heights.

## Review Questions

- Does the app still rely on custom backgrounds for sheets, bars, or lists that the system now handles better?
- Are toolbar items grouped by semantics rather than implementation order?
- Are primary actions using tint or prominence intentionally and sparingly?
- Are custom glass elements attached to controls, not to content slabs?
- In macOS workspaces, are quick actions, windows, and menu commands distinct enough to stay discoverable?

Additional source:
- <https://developer.apple.com/documentation/swiftui/landmarks-building-an-app-with-liquid-glass>
