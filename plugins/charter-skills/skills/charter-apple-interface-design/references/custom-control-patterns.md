# Custom glass control patterns

Use this file when a custom elevated control needs Liquid Glass and standard
Apple containers do not provide the required grouping. These are material
patterns, not a repertoire of native product layouts. For a content-led flow
built from standard controls, use the [order counter](order-counter.md).

## Source Anchors

- <https://developer.apple.com/videos/play/wwdc2025/323/>
- <https://developer.apple.com/videos/play/wwdc2025/284/>
- <https://developer.apple.com/videos/play/wwdc2025/310/>
- <https://developer.apple.com/documentation/swiftui/glasseffectcontainer>
- <https://developer.apple.com/documentation/swiftui/view/glasseffectid(_:in:)>
- <https://developer.apple.com/documentation/swiftui/view/glasseffect(_:in:)>
- <https://developer.apple.com/documentation/swiftui/glasseffecttransition>
- <https://developer.apple.com/documentation/swiftui/view/glasseffecttransition(_:)>
- <https://developer.apple.com/documentation/swiftui/view/glasseffectunion(id:namespace:)>
- <https://developer.apple.com/documentation/swiftui/glassbuttonstyle>

## Pattern 1: Floating Action Cluster

Use when a small set of high-value actions must stay close to content and no standard bar or menu fits.

```swift
@Namespace private var glassNamespace
@State private var expanded = false
@Environment(\.accessibilityReduceMotion) private var reduceMotion

GlassEffectContainer(spacing: 28) {
    VStack(spacing: 12) {
        if expanded {
            Button("Edit", systemImage: "pencil") { }
                .buttonStyle(.glass)
                .glassEffectID("edit", in: glassNamespace)
                .glassEffectTransition(.materialize)

            Button("Share", systemImage: "square.and.arrow.up") { }
                .buttonStyle(.glass)
                .glassEffectID("share", in: glassNamespace)
                .glassEffectTransition(.materialize)
        }

        Button(
            expanded ? "Hide actions" : "Show actions",
            systemImage: expanded ? "xmark" : "plus"
        ) {
            withAnimation(reduceMotion ? nil : .bouncy) { expanded.toggle() }
        }
        .labelStyle(.iconOnly)
        .buttonStyle(.glassProminent)
        .buttonBorderShape(.circle)
        .glassEffectID("toggle", in: glassNamespace)
    }
}
```

The cluster works because proximity makes action scope apparent. As it grows,
it occludes content and makes the primary action harder to find; move secondary
choices into a menu or use a toolbar when the actions are global. The right
size follows the work and available space, not a fixed action count.

## Pattern 2: Media Overlay Controls

Use when controls must float over photos, video, or maps and content still needs to stay visible.

```swift
ZStack {
    mediaView

    controls
        .padding()
        .glassEffect(.clear, in: .capsule)
}
```

Guardrails:

- Use `.clear` only after readability testing on real media.
- Add support layers only when needed for legibility.
- Keep the overlay compact and control-focused.

## Pattern 3: Grouped But Distant Controls

Use `glassEffectUnion(id:namespace:)` only when related controls must remain visually grouped across greater spacing.

Guardrails:

- Use this for semantic grouping, not decoration.
- If the elements are not read as one action family, do not union them.

## Inspect the affected interaction

These snippets illustrate composition, not complete shipping controls. Check
API availability in the selected SDK. Inspect the dimensions that can break
the actual control:

1. Background stress:
   the control remains legible over light, dark, colorful, and media-heavy content.
2. State stress:
   focus, pressed, disabled, and selected states remain readable and distinct.
3. Density stress:
   nearby content remains scannable while the control is visible.
4. Fallback stress:
   reduced transparency, increased contrast, reduced motion, and larger text still produce an intentional result.
