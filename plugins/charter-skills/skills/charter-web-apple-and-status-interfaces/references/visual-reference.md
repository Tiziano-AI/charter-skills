# Visual Reference

Use this file when the user wants visual direction, moodboards, or concrete
examples to inspect. Choose by the relationship you need to study.

## Working native apps

Two small macOS apps come with editable SwiftUI source, a build script and
renders drawn by the running app, in light, dark and Increase Contrast, in an
active window beside an inactive one, and on a Mac set up with its owner's
accent. Each walkthrough says which particulars of the work became which
decision and what was observed in the running app. The renders show those
implementations; the source makes the relationships reproducible.

- The [order counter](order-counter.md), a doughnut shop's pickup counter,
  spends its identity on one object: a paper ticket on its rail, read at arm's
  length. Its renders show an order before and after Mark as Ready, the
  compact stack, and the app's own Larger Text scale in both layouts. It is a
  Charter adaptation of Apple's MIT-licensed Food Truck sample, not Apple
  artwork or a current Apple product recommendation.
- The [crate library](crate-library.md), a DJ choosing the next track by
  tempo and key, spends its identity on density and on reading every row
  against the deck: a sortable table, compatibility shown by shape and word, a
  keyboard path and menu commands. Its renders show a tempo sort with a
  preview running, a key-compatibility sort, and long and non-Latin titles in
  a narrowed column. Its tracks and artists are invented.

Study where each spends its identity and what it leaves to the system, and
why the two differ, not the particular look.

## Identity within native behavior

Apple's [Communicate your brand identity on iOS](https://developer.apple.com/videos/play/wwdc2026/251/)
shows apps that keep navigation, toolbars and context menus native while
their content carries the brand: a moon-phase calendar drawn as a custom
component inside a standard sheet, full-bleed product video that changes each
week, playful illustration beside detailed fitness charts, a custom icon set
that keeps the platform's Share metaphor, and brand color moved out of solid
bars into the scrolling content. Study where each app spends its identity and
what it leaves to the system, not the particular look. The
[Apple Design Awards](https://developer.apple.com/design/awards/) calibrate the
same balance across categories and platforms.
[Native identity](native-identity.md) turns that division into choices for a
particular subject.

## Material-specific examples from Apple

The official sources below provide visual examples to inspect in their original
context. They can calibrate a material choice but do not supply a whole product's
workflow or its visual identity. Material and composition do not establish API
availability, adaptive behavior or a complete workflow; use
[official sources](official-sources.md) and the selected SDK for implementation
decisions.

### Conference sessions

- [Meet Liquid Glass](https://developer.apple.com/videos/play/wwdc2025/219/):
  foundational material language, lensing and hierarchy.
- [Build a UIKit app with the new design](https://developer.apple.com/videos/play/wwdc2025/284/):
  UIKit bar structure, controls and floating navigation.
- [Build an AppKit app with the new design](https://developer.apple.com/videos/play/wwdc2025/310/):
  the session title artwork shows a grouped glass control over landscape
  imagery, not a complete window or sidebar. Study its material grouping,
  not interaction or restoration behavior.

### Newsroom examples

Apple's [introduction to the new software design](https://www.apple.com/newsroom/2025/06/apple-introduces-a-delightful-and-elegant-new-software-design/)
contains these contrasting examples:

- **Clear macOS desktop, Dock and widgets:** study clear desktop composition,
  Dock presence and widget material. No application window is open in this
  example.
- **Dark and tinted macOS desktop:** study tint restraint, widget legibility
  and material contrast.
- **Icon Composer:** study the visible icon-layer preview, sidebar/inspector
  structure and control grouping, not current tool behavior.

Open the relevant source when the visual ask needs it. Use these examples to
calibrate hierarchy, control density, tint restraint and shape language, not as
a license to mimic Apple layouts without the same interaction needs.
