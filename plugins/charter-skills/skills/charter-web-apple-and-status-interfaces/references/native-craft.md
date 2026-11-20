# Native craft: type, color, density, words and feedback

Open this when choosing or reviewing type, color, density or interface copy,
or to pick the cases worth checking. Figures come from Apple's Human
Interface Guidelines; open the linked page when a figure decides a layout, and
take API names and availability from the selected SDK. Where identity should
live, and the defaults these choices replace, are in
[native identity](native-identity.md).

## Type

### Text styles as the starting scale

System text styles provide a useful starting scale, platform metrics and
Dynamic Type where supported. Adjust each role's weight, design or width to
the content and viewing conditions; a custom scale still needs coherent
hierarchy and accessible sizing.

| Platform | Default body | Recommended minimum | Dynamic Type |
| --- | --- | --- | --- |
| iOS, iPadOS | 17 pt | 11 pt | Yes |
| macOS | 13 pt | 10 pt | No |
| tvOS | 29 pt | 23 pt | Yes |
| visionOS | 17 pt | 12 pt | Yes |
| watchOS | 16 pt | 12 pt | Yes |

At iPhone's default text size the styles run Large Title 34, Title 1 28,
Title 2 22, Title 3 20, Headline 17 semibold, Body 17, Callout 16,
Subheadline 15, Footnote 13, Caption 1 12 and Caption 2 11 points. The Mac's
run Large Title 26, Title 1 22, Title 2 17, Title 3 15, Headline 13 bold,
Body 13, Callout 12, Subheadline 11 and Footnote, Caption 1 and Caption 2 10.
A large title is therefore a different object on each platform: a Mac sidebar
or window rarely carries one, while an iPhone navigation stack often does.
visionOS adds `extraLargeTitle` and `extraLargeTitle2` for wide editorial
layouts. Light, thin and ultralight weights lose legibility at small sizes.

| Need | SwiftUI | UIKit | AppKit |
| --- | --- | --- | --- |
| A text style | `.font(.headline)` | `UIFont.preferredFont(forTextStyle:)` with `adjustsFontForContentSizeCategory` | `NSFont.preferredFont(forTextStyle:options:)` |
| A custom face that scales | `Font.custom(_:size:relativeTo:)` | `UIFontMetrics(forTextStyle:).scaledFont(for:)` | No Dynamic Type; match control text with `NSFont` system variants such as `controlContentFont(ofSize:)` |
| Spacing or image size that scales | `@ScaledMetric(relativeTo:)` | `UIFontMetrics.scaledValue(for:)` | Not applicable |
| Figures that change in place | `monospacedDigit()`, `contentTransition(.numericText())` | `UIFont.monospacedDigitSystemFont(ofSize:weight:)`, scaled through `UIFontMetrics` | `NSFont.monospacedDigitSystemFont(ofSize:weight:)` |

### Roles, not sizes

Decide what the person recognizes first and compares next, and give each a
role. At a coat check the ticket number is called across the room, so it is
the dominant figure; on a ward handover the patient's name and bed come first
and the numbers follow. Align quantities and amounts that are compared, let
names and instructions wrap, and keep a single reading column for prose.

- **Design.** Use a design that supports the role and script: `.default` (SF
  Pro) for interface text, a readable text face such as `.serif` (New York)
  for long passages, monospaced characters (`.monospaced`, SF Mono) for codes
  and identifiers that need them, or tabular digits for comparable figures.
  Rounded (`.rounded`) or serif forms can carry a chosen voice, as in a
  children's app or a watch complication, without becoming the default for
  every heading.
- **Width.** A condensed width (`fontWidth(.condensed)` or `.compressed`) can
  save horizontal space in a dense view or on a narrow watch face if the
  actual strings remain legible. Keep resizing, wrapping or access to full
  text where narrowing cannot fit the content. An expanded width (`.expanded`)
  can give a short display heading presence.
- **A brand or reading face** can serve headings, the custom moment or
  sustained content when it supports the actual scripts and remains legible at
  the required sizes, scaled through a text style. Preserve Bold Text and
  text-size behavior; pairing expressive headings with system body text is one
  useful arrangement.
- **Capitals.** A short uppercase label (`.textCase(.uppercase)`) can
  distinguish a content kind or follow a field convention, such as a departure
  board's column heads. If it only repeats the title, remove the repetition
  rather than treating uppercase itself as the defect.

### Larger text changes the arrangement

Apple recommends ideally supporting enlargement of at least 200 percent, or
140 percent on watchOS; inspect the text sizes the app actually supports.
At accessibility sizes, stack inline items under the text they follow, reduce
columns, keep the primary element at the top and let text wrap rather than
truncate; `dynamicTypeSize.isAccessibilitySize` and `ViewThatFits` let a
SwiftUI layout switch. The Mac has no Dynamic Type, so an app people read in
for long stretches can offer its own text size, as the
[order counter](order-counter.md) exercises with an explicit text scale; the
[crate library](crate-library.md) leaves it out and says so.

## Color

- **Semantic colors** carry ordinary text, backgrounds and separators:
  `.primary`, `.secondary` and `.tertiary` styles in SwiftUI; `label`,
  `secondaryLabel`, `systemBackground` and `systemGroupedBackground` in UIKit;
  `labelColor`, `secondaryLabelColor` and `windowBackgroundColor` in AppKit.
  Use each for its stated purpose: a separator color as text breaks when the
  system changes either.
- **One accent.** Define it as the `AccentColor` set in the asset catalog, with
  a dark appearance and the High Contrast variants. Supply light and dark
  values even for an app that ships in one appearance, because Liquid Glass
  adapts between them. Use it for actions, selection, badges and attention
  where these meanings remain clear; keep warning, destructive and completion
  states distinguishable. Brand color beyond that belongs in the content
  layer.
- **Text on the accent.** A selected row and a prominent button put text on
  the accent, so choose every variant to carry that text. The system's own
  colors grow brighter in dark High Contrast; an accent that follows them can
  end up a pale fill under white text. On macOS 27.2.1 a `Table` drew its
  selection in the dark High Contrast value exactly as given, which left white
  text at 1.8:1 on a bright amber until the
  [crate library](crate-library.md) took a deep one.
- **The Mac accent.** The person's accent setting replaces the app's on
  buttons, selection and sidebar icons unless they chose Multicolor. A
  fixed-color sidebar icon keeps its color because its color is its
  meaning. Text on those fills then sits on a color the app did not choose:
  hold the app's own values to the ratio, and let nothing depend on reading
  small text there. The crate library's renders on macOS 27.2.1 drew sidebar
  symbols monochrome at default contrast under either accent, so look at the
  running app before counting on tinted sidebar icons.
- **Colorful content** such as photos or maps reads better under monochrome
  toolbars and tab bars; a mostly monochrome app can carry its brand color as
  the accent.
- **Contrast.** Check text against its actual background in the supported
  appearances and contrast settings. Use 4.5:1 for ordinary text and a lower
  ratio only where the applicable standard permits it. For a WCAG conformance
  claim, 3:1 applies to large text: 18-point regular or 14-point bold, or the
  equivalent. Apple's Dark Mode guidance recommends aiming for 7:1 for small
  custom-colored text.
- **Color has a role.** Keep action, selection and state meanings clear in
  context. Static colored text should not look actionable, and each state
  also needs text or a distinguishable shape.

## Density per platform

| Platform | Default control size | Minimum |
| --- | --- | --- |
| iOS, iPadOS | 44 × 44 pt | 28 × 28 pt |
| macOS | 28 × 28 pt | 20 × 20 pt |
| tvOS | 66 × 66 pt | 56 × 56 pt |
| visionOS | 60 × 60 pt | 28 × 28 pt |
| watchOS | 44 × 44 pt | 28 × 28 pt |

- **Mac.** Large displays show more content in fewer nested levels. Use native
  row and control metrics, with enough space for the actual text and targets;
  `controlSize(.small)` suits inspectors and dense panels. A `Table` serves
  comparison: sortable columns, resizable columns, alternating rows when it is
  wide, an outline for hierarchy. Windows resize and go full screen. Make app
  commands discoverable in the appropriate menus. Preserve the standard menu
  order when those menus are present (the app menu, File, Edit, Format, View,
  app-specific menus, Window, Help), with a Window menu even for a one-window
  app, Settings… in the app menu opening a Settings window on Command-comma,
  and Undo and Redo at the top of Edit. On a Mac with a touch display,
  controls expand on touch while their size and density stay set for pointer
  and keyboard.
- **iPhone.** Account for one-handed reach and native 44-point touch targets.
  Grouped lists suit settings and forms. Row actions can use swipe or context
  menus with an accessible alternative; a resizable sheet suits progressive
  disclosure, while composition may need full height.
- **iPad.** Choose simultaneous panes when comparison or hierarchy benefits
  from them, and independent windows when the work has independent objects.
  Support pointer and keyboard alongside touch. Use the platform's menu
  conventions for the commands the app provides: a menu bar with the same
  menus and order as the Mac.
- **Watch, TV and visionOS** follow [platform adaptation](platform-adaptation.md)
  and [visionOS](visionos.md): glance, focus at a distance, and spacing for
  gaze.

## Words

These conventions are for English; other languages follow their own.

- **Capitalization.** Use title style for menu items, multiword menu titles,
  buttons, alert buttons and table column headings. Capitalize the first and
  last word; within the phrase, capitalize words other than articles,
  coordinating conjunctions and short prepositions. Use sentence style and
  appropriate punctuation for complete-sentence alert titles and informative
  text; use title style without ending punctuation for fragment titles.
  Elsewhere, choose a consistent style per element type.
- **Ellipsis.** A menu item or push button uses an ellipsis character when the
  person must supply more information or choose before the action completes,
  as in Export…. Merely opening another view or window is not enough; retain
  standard labels such as Settings….
- **One verb through a flow.** The button, the menu item, the Undo title, any
  confirmation and the result all use the same verb: Archive, Undo Archive,
  "Archived". A flow that spans screens picks Continue or Next and keeps it,
  and ends with Done.
- **Toggled items.** Add a verb when a label could read as a state: Turn HDR
  On rather than HDR On.
- **Alerts.** The title says what happened. Buttons take one or two words that
  name the result (Erase, Replace, View All); OK fits only a purely
  informational alert, and the button that cancels is always Cancel.
- **Undo.** On platforms that support Undo and Redo, register reversible
  edits with `UndoManager`, including the redo behavior and an action name.
  `registerUndo(withTarget:handler:)` and `setActionName(_:)` supply that
  registration and label. Keep the name short and informative, since the
  system adds "Undo " in front, as in Undo Typing or Undo Mark as Ready. On
  the Mac, put Undo and Redo in Edit with Command-Z and Shift-Command-Z.
  iPhone supports standard gestures and the shake alert, which uses the same
  title; dedicated toolbar buttons with the standard symbols help when
  reversal is central to the work. tvOS and watchOS need their own clear
  correction interaction.
- **Voice and tone.** The voice stays; the tone follows the moment: brisk for
  an operator's correction, warmer for a finished milestone. Prefer "Unable to
  load content" to "We're having trouble", and say what to do next ("Choose a
  password with at least 8 characters").
- **Empty states** say what to do and offer the button that does it. An empty
  search result helps change the search (`ContentUnavailableView.search`)
  rather than inviting creation.
- **The device's verbs.** Tap on touch devices, click with a pointer.
- **Useful notices.** Keep implementation notes and debug wording in
  documentation. Keep an on-screen sample or preview notice when a person
  could otherwise mistake fictional content or a simulated action for live
  work.

## Feedback, motion and haptics

- **Motion answers an action.** Use brief, precise motion to explain change;
  preserve immediate interaction and avoid extra animation that repeatedly
  competes with the task. A source-anchored transition helps when the origin
  explains the destination. Under Reduce Motion the meaning survives without
  the movement.
- **Symbol effects mark status.** Bounce once to say an action happened;
  pulse or breathe for something ongoing, such as a recording; replace when a
  state changes, as a copy symbol becoming a checkmark; variable color for a
  level or progress.
- **Haptics on iPhone** use the system patterns by their meaning:
  notification for an outcome, impact for a physical metaphor such as a snap
  into place, selection while a value changes. In SwiftUI,
  `sensoryFeedback(.success, trigger:)` ties one to a state change. Pair each
  with visible feedback, keep them short in apps, and let them be turned off.
- **Startup.** Keep the launch screen a bridge into the app. A useful welcome
  or onboarding view can carry identity while helping the person begin; an
  ornamental entrance should not hold the task behind it.

## Checking a native screen

Select the rows that can expose a failure in the work being changed. A new
screen needs broad coverage; a local repair need not repeat unrelated cases.
Inspect the rendered composition and use the affected interaction. A window
the app draws into a bitmap itself (`cacheDisplay`) shows sidebar and bar
materials as flat fallbacks and toolbar glass untinted; it serves layout, type
and color, and glass is judged on screen or in a screen capture.

| Condition | How to reach it | What to look for |
| --- | --- | --- |
| Light and dark | System appearance, or preview variants | The custom moment and accent look designed in both |
| Increase Contrast, Reduce Transparency | Accessibility settings; `colorSchemeContrast`, `accessibilityReduceTransparency` | Separation holds without glass; High Contrast colors apply and still carry the text set on them |
| Largest text | The largest accessibility size on iOS; the app's own scale on the Mac | The key figure and primary action survive; layout reflows instead of truncating |
| Inactive Mac window | Click into another window; `appearsActive` | The primary action still reads as primary by placement and label when its tint is dimmed |
| Compact and wide | Resize the window or scene; split view on iPad | The same object and selection survive the change |
| Long and right-to-left text | Run in a right-to-left language and one with long words, such as German | Nothing clips; reading order, mixed-script text and directional controls remain correct; artwork and real-world direction keep their meaning |
| Real content | The longest names, empty, error and permission-denied states, a large collection | The hierarchy still chooses what matters |
| VoiceOver and keyboard | VoiceOver, Full Keyboard Access, Accessibility Inspector | Every action is reachable and named |

## Sources

- <https://developer.apple.com/design/human-interface-guidelines/typography>
- <https://developer.apple.com/design/human-interface-guidelines/color>
- <https://developer.apple.com/design/human-interface-guidelines/branding>
- <https://developer.apple.com/design/human-interface-guidelines/accessibility>
- <https://developer.apple.com/design/human-interface-guidelines/writing>
- <https://developer.apple.com/design/human-interface-guidelines/menus>
- <https://developer.apple.com/design/human-interface-guidelines/the-menu-bar>
- <https://developer.apple.com/design/human-interface-guidelines/alerts>
- <https://developer.apple.com/design/human-interface-guidelines/undo-and-redo>
- <https://developer.apple.com/design/human-interface-guidelines/lists-and-tables>
- <https://developer.apple.com/design/human-interface-guidelines/motion>
- <https://developer.apple.com/design/human-interface-guidelines/playing-haptics>
- <https://developer.apple.com/design/human-interface-guidelines/designing-for-macos>
- <https://developer.apple.com/documentation/xcode/specifying-your-apps-color-scheme>

The guidance above interprets these for product work; check the page itself
when its current revision decides a choice.
