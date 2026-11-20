# UIKit

Use this file when the task includes UIKit implementation, migration, or review.

## Source Anchors

- <https://developer.apple.com/videos/play/wwdc2026/278/>
- <https://developer.apple.com/documentation/uikit/transitioning-to-the-uikit-scene-based-life-cycle>
- <https://developer.apple.com/videos/play/wwdc2025/284/>
- <https://developer.apple.com/documentation/technotes/tn3106-customizing-uinavigationbar-appearance>
- <https://developer.apple.com/documentation/uikit/uiglasseffect>
- <https://developer.apple.com/documentation/uikit/uiglasscontainereffect>
- <https://developer.apple.com/documentation/uikit/uibackgroundextensionview>
- <https://developer.apple.com/documentation/uikit/uitab>
- <https://developer.apple.com/documentation/uikit/uitabgroup>
- <https://developer.apple.com/documentation/uikit/uitabaccessory>

## Choose the affected seam

Check the deployed OS, build SDK and current UIKit contract when they change
this implementation. For an adaptive-layout or SDK adoption task, inspect the
scene lifecycle, scene geometry and the affected containers. Choose
`UITabBarController` with `UITab` and `UITabGroup`, `UISplitViewController` or
`UINavigationController` from the object relationship in
[native structure](design-principles.md). Remove appearance overrides that
conflict with the chosen system behavior; add custom glass only where a
standard component does not fit.

For API names, availability and the replacement of shared-state APIs such as
`UIScreen.main`, interface orientation and the app-level lifecycle, use Apple's
`uikit-app-modernization` skill when it is in your skill list, and confirm a
recalled or recent declaration in the selected iOS SDK either way; [official sources](official-sources.md)
shows where to search.

## Strong Defaults

- Derive available geometry from the active scene and window, and derive layout from size classes;
  do not use `UIScreen.main`, interface idiom, or orientation as layout proxies.
- Let the tab bar float above content and minimize on scroll when the content benefits from extra focus.
- Use a tab accessory only for truly persistent cross-section controls such as playback.
- When a sidebar or bar overlays meaningful imagery, let that content remain
  perceptible where legibility permits; do not add decorative imagery simply
  to showcase translucency.
- Use `UIBackgroundExtensionView` when hero content should continue beneath
  those bars, rather than a hand-built blur stack. Text-heavy working surfaces
  may need quieter, more opaque content backgrounds.
- Respect automatic grouping and scroll-edge behavior in navigation bars and toolbars.

## Migration Pressure Points

- Remove fixed full-screen, main-screen, interface-idiom and orientation
  assumptions where resizable layouts require adaptive behavior.
- Treat scene-lifecycle adoption as launch-critical when building with the
  iOS 27 SDK: UIKit requires it for launch. Check the actual build SDK and
  target platform rather than extending that requirement to every existing
  app. Scene lifecycle does not itself require multiwindow support.
- Re-audit `UINavigationBarAppearance` and `UITabBarAppearance` customizations before carrying them forward.
- Remove custom backgrounds, shadows, and opaque bar materials when they defeat the chosen
  system behavior; retain deliberate custom appearance that still serves the product.
- Prefer system tabs, tab groups, and accessories to custom segmented or floating navigation clones.
- When resizable adaptation is affected, exercise it in current Xcode previews or Device Hub,
  then verify the relevant shipping paths, such as iPhone Mirroring or iPad. A fixed simulator
  size cannot establish behavior under resizing; an unsupported platform adds no useful check.

## Custom Liquid Glass

Use `UIVisualEffectView` plus `UIGlassEffect` for custom elevated controls.

```swift
let glass = UIGlassEffect()
glass.isInteractive = true

let glassView = UIVisualEffectView(effect: glass)
glassView.contentView.addSubview(buttonLabel)
```

- Prefer setting the effect to `nil` to dematerialize rather than fading alpha.
- Use dynamic colors for tint and foreground content.
- Set `cornerConfiguration` with `UICornerRadius.containerConcentric(minimum:)` when the view should adapt to its container geometry.
- Animate content and tint alongside the glass effect when the state changes.

## Multiple Glass Elements

Use `UIGlassContainerEffect` when nearby custom glass elements should interact.

- Keep close glass elements in the same container.
- Use the container `spacing` value to control merge behavior.
- Do not let one glass element sample another glass element from a separate container.

## Review Questions

- Are legacy `UINavigationBarAppearance` or toolbar customizations suppressing the new system behavior?
- Does the structure still use the right controller type before custom containers were introduced?
- Are accessory views truly persistent or are they leaking contextual actions into a global surface?
- Are custom glass views limited to high-value controls instead of replacing whole content regions?
