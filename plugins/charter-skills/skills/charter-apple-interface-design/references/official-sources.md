# Official Apple Sources

Use Apple's current documentation, SDK declarations and release guidance for
platform authority. Examples, visual inspiration and product recommendations do
not acquire API authority merely by appearing beside an official link.

## API names, availability and the SDK

Use the Apple-authored guidance available for the selected framework and
toolchain. Its scope may cover API usage, document protocols, scene migration
or device interaction; inspect that scope rather than inferring coverage from
its presence. A framework skill does not by itself supply the product's
interaction design.

When Xcode exposes `agent skills export`,
`xcrun agent skills export --output-dir <scratch directory>` writes readable
copies. Discover the installed command and available skills rather than
assuming a release's catalog remains unchanged. Exported text is a source to
inspect, not evidence that the current agent can invoke that skill.

Check a symbol against the selected SDK before depending on it:

- `xcrun --show-sdk-version` and `xcrun --show-sdk-path` name the macOS SDK;
  add `--sdk iphoneos`, `appletvos`, `watchos` or `xros` for another platform.
- Swift declarations are in the SDK's
  `System/Library/Frameworks/<Framework>.framework/**/*.swiftinterface` files.
  Many SwiftUI shapes and view types, `ConcentricRectangle` among them, are
  declared in `SwiftUICore.framework`. Objective-C declarations and their
  `API_AVAILABLE` macros are in the framework's `Headers/`.
- The `@available` line gives the first OS for a symbol and the platforms where
  it is unavailable. Compare it with the deployment target, and guard with
  `if #available` when the target is older.
- `xcrun swiftc -typecheck -sdk <selected-sdk-path> -target <project-target-triple> Snippet.swift`
  typechecks a snippet without building an app. Substitute the SDK path and
  target triple from the project; the triple carries its architecture,
  platform and deployment target. A snippet checked against a different
  target does not establish that the app can use it.

## Design and framework sources

- Apple Design, What's New:
  <https://developer.apple.com/design/whats-new/>
  Resolve current design kits, tools and guidance here. Tool listings do not
  establish deployment availability or stable API guarantees.
- Principles of great design:
  <https://developer.apple.com/videos/play/wwdc2026/250/>
- Design intuitive search experiences:
  <https://developer.apple.com/videos/play/wwdc2026/292/>
- Modernize your AppKit app:
  <https://developer.apple.com/videos/play/wwdc2026/289/>
- Modernize your UIKit app:
  <https://developer.apple.com/videos/play/wwdc2026/278/>
- What's new in SwiftUI:
  <https://developer.apple.com/videos/play/wwdc2026/269/>

Conference sessions explain a particular design or implementation context.
Use the one relevant to the decision, and resolve API availability against the
project's SDK rather than treating its conference year as authority.

## Canonical Design Principles

- Liquid Glass overview:
  <https://developer.apple.com/documentation/technologyoverviews/liquid-glass>
- Adopting Liquid Glass:
  <https://developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass>
- Human Interface Guidelines root:
  <https://developer.apple.com/design/human-interface-guidelines/>
- HIG Materials:
  <https://developer.apple.com/design/human-interface-guidelines/materials>
- HIG Toolbars:
  <https://developer.apple.com/design/human-interface-guidelines/toolbars>
- HIG Designing for macOS:
  <https://developer.apple.com/design/human-interface-guidelines/designing-for-macos>
- HIG The menu bar:
  <https://developer.apple.com/design/human-interface-guidelines/the-menu-bar>
- HIG Menus:
  <https://developer.apple.com/design/human-interface-guidelines/menus>
- HIG Alerts:
  <https://developer.apple.com/design/human-interface-guidelines/alerts>
- HIG Managing notifications:
  <https://developer.apple.com/design/human-interface-guidelines/managing-notifications>
- HIG Accessibility:
  <https://developer.apple.com/design/human-interface-guidelines/accessibility>
- HIG App Icons:
  <https://developer.apple.com/design/human-interface-guidelines/app-icons>
- HIG SF Symbols:
  <https://developer.apple.com/design/human-interface-guidelines/sf-symbols>
- HIG Designing for visionOS:
  <https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos>
- HIG Designing for watchOS:
  <https://developer.apple.com/design/human-interface-guidelines/designing-for-watchos>
- HIG Designing for tvOS:
  <https://developer.apple.com/design/human-interface-guidelines/designing-for-tvos>

## Material, icon and interface sessions

- Get to know the new design system:
  <https://developer.apple.com/videos/play/wwdc2025/356/>
- Meet Liquid Glass:
  <https://developer.apple.com/videos/play/wwdc2025/219/>
- Build a SwiftUI app with the new design:
  <https://developer.apple.com/videos/play/wwdc2025/323/>
- Build a UIKit app with the new design:
  <https://developer.apple.com/videos/play/wwdc2025/284/>
- Build an AppKit app with the new design:
  <https://developer.apple.com/videos/play/wwdc2025/310/>
- Design foundations from idea to interface:
  <https://developer.apple.com/videos/play/wwdc2025/359/>
- Say hello to the new look of app icons:
  <https://developer.apple.com/videos/play/wwdc2025/220/>
- Create icons with Icon Composer:
  <https://developer.apple.com/videos/play/wwdc2025/361/>
- What's new in SF Symbols 7:
  <https://developer.apple.com/videos/play/wwdc2025/337/>

## Framework And API References

### SwiftUI

- `MenuBarExtra`:
  <https://developer.apple.com/documentation/swiftui/menubarextra>
- `NavigationSplitView`:
  <https://developer.apple.com/documentation/swiftui/navigationsplitview>
- Adding a search interface to your app:
  <https://developer.apple.com/documentation/SwiftUI/Adding-a-search-interface-to-your-app>
- Bringing multiple windows to your SwiftUI app:
  <https://developer.apple.com/documentation/SwiftUI/bringing-multiple-windows-to-your-swiftui-app>
- `openWindowAction.callAsFunction(value:)`:
  <https://developer.apple.com/documentation/swiftui/openwindowaction/callasfunction(value:)>
- `SettingsLink`:
  <https://developer.apple.com/documentation/swiftui/settingslink>
- `Scene.commands(content:)`:
  <https://developer.apple.com/documentation/swiftui/scene/commands%28content%3A%29>
- `CommandMenu`:
  <https://developer.apple.com/documentation/swiftui/commandmenu>
- `CommandGroup`:
  <https://developer.apple.com/documentation/swiftui/commandgroup>
- `GlassEffectContainer`:
  <https://developer.apple.com/documentation/swiftui/glasseffectcontainer>
- `glassEffectID(_:in:)`:
  <https://developer.apple.com/documentation/swiftui/view/glasseffectid(_:in:)>
- `backgroundExtensionEffect()`:
  <https://developer.apple.com/documentation/swiftui/view/backgroundextensioneffect()>
- `safeAreaBar(edge:alignment:spacing:content:)`:
  <https://developer.apple.com/documentation/swiftui/view/safeareabar(edge:alignment:spacing:content:)>
- `tabBarMinimizeBehavior(_:)`:
  <https://developer.apple.com/documentation/swiftui/view/tabbarminimizebehavior(_:)>
- `tabViewBottomAccessory(content:)`:
  <https://developer.apple.com/documentation/swiftui/view/tabviewbottomaccessory(content:)>
- `ToolbarSpacer`:
  <https://developer.apple.com/documentation/swiftui/toolbarspacer>

### UIKit

- `UIGlassEffect`:
  <https://developer.apple.com/documentation/uikit/uiglasseffect>
- `UIGlassContainerEffect`:
  <https://developer.apple.com/documentation/uikit/uiglasscontainereffect>
- `UIBackgroundExtensionView`:
  <https://developer.apple.com/documentation/uikit/uibackgroundextensionview>
- `UITab`:
  <https://developer.apple.com/documentation/uikit/uitab>
- `UITabGroup`:
  <https://developer.apple.com/documentation/uikit/uitabgroup>
- `UITabAccessory`:
  <https://developer.apple.com/documentation/uikit/uitabaccessory>
- Technote TN3106, navigation bar appearance:
  <https://developer.apple.com/documentation/technotes/tn3106-customizing-uinavigationbar-appearance>

### AppKit

- `NSStatusBar`:
  <https://developer.apple.com/documentation/appkit/nsstatusbar>
- `NSGlassEffectView`:
  <https://developer.apple.com/documentation/appkit/nsglasseffectview>
- `NSGlassEffectContainerView`:
  <https://developer.apple.com/documentation/appkit/nsglasseffectcontainerview>
- `NSBackgroundExtensionView`:
  <https://developer.apple.com/documentation/appkit/nsbackgroundextensionview>

### Speech And Realtime Callback Contracts

- Recognizing speech in live audio:
  <https://developer.apple.com/documentation/speech/recognizing-speech-in-live-audio>
- `SFSpeechRecognizer.recognitionTask(with:resultHandler:)`:
  <https://developer.apple.com/documentation/speech/sfspeechrecognizer/recognitiontask(with:resulthandler:)>
- `SFSpeechRecognizer.queue`:
  <https://developer.apple.com/documentation/speech/sfspeechrecognizer/queue>
- `AVAudioNode`:
  <https://developer.apple.com/documentation/avfaudio/avaudionode>

### visionOS / Spatial UI

- `ornament(visibility:attachmentAnchor:contentAlignment:ornament:)`:
  <https://developer.apple.com/documentation/swiftui/view/ornament(visibility:attachmentanchor:contentalignment:ornament:)>
- `glassBackgroundEffect(in:displayMode:)`:
  <https://developer.apple.com/documentation/swiftui/view/glassbackgroundeffect(in:displaymode:)>
- `glassBackgroundEffect(displayMode:)`:
  <https://developer.apple.com/documentation/swiftui/view/glassbackgroundeffect(displaymode:)>

## Official Visual Benchmarks

- Apple newsroom design launch:
  <https://www.apple.com/newsroom/2025/06/apple-introduces-a-delightful-and-elegant-new-software-design/>
- Apple new design gallery:
  <https://developer.apple.com/design/new-design-gallery/>
- Apple Design Awards:
  <https://developer.apple.com/design/awards/>
- Landmarks sample app with Liquid Glass:
  <https://developer.apple.com/documentation/swiftui/landmarks-building-an-app-with-liquid-glass>
- tvOS What's New:
  <https://developer.apple.com/tvos/whats-new/>

## Match the source to the claim

HIG explains interaction guidance; framework documentation and the selected SDK
own APIs, availability and callback contracts; release notes can qualify changed
behavior. A conference session explains a release's design and migration
direction. An image shows only the pixels it contains.

The package's design recommendations are interpretations, not additional Apple
requirements. In particular, assistant workbenches, menu-bar companion
architecture and notification placement have legitimate alternatives depending
on the product. Do not cite a general HIG page as proof that one layout is
mandatory.

## When sources disagree

Resolve disagreement against the target OS and SDK. Newer guidance may apply to
a different release; older documentation may still own the deployed API.

The bundled [source verifier](../scripts/verify_official_sources.py) checks that
Apple URLs resolve, WWDC links carry their declared titles and referenced
`assets/` files exist. Run it with Python using its absolute path in the
installed package, not a path relative to the project's working directory.
With no arguments it locates this package from the script's own location;
optional file arguments name caller-selected text files, relative to the
caller's working directory or absolute. The [title declarations](../scripts/apple_source_scan.py)
and [network reader](../scripts/apple_source_network.py) share its script
directory. These checks establish neither the advice, API availability nor
runtime behavior.
