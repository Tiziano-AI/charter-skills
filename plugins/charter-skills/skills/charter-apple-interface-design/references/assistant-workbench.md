# Assistant workbenches

Use this reference when a native Mac product organizes work with an assistant.
The platform-independent design comes first and belongs to
`charter-product-experience`: the center of gravity chosen from the promised
job, expectations and scope, the visible state of delegated work, stop scope,
correction and handing control back. This file covers how a Mac carries those
decisions.

## Map the center of gravity onto Mac structure

Distinguish navigation among tasks from inspection of a selected task: a
sidebar or split view lists the work, the content area holds the selected
conversation or artifact, and an inspector shows its details and settings.
Artifacts need a real editing and comparison surface in the content area or
their own window, not only a transcript attachment. Restore windows, selection
and scroll position so the person returns to the work where they left it.

Several windows let a person watch one task while starting another. A
long-running operation keeps its identity when its window closes, and reopening
the task shows its current state rather than the state at close.

## Commands, focus and status in Mac chrome

Use toolbars for meaningful commands and local status for the state of the
selected work. A small toolbar warning can work when its meaning and
destination are clear. History, automations, accounts, permissions, memory and
diagnostics need discoverable homes, such as a Settings scene, a dedicated
window or a menu command, reached when they answer the current question rather
than crossed before routine use.

Menus and keyboard shortcuts expose every frequent command, including stop and
retry for the selected task. Preserve focus and command routing as tasks or
artifacts change: a persistent composer must not steal keyboard input from an
editor, and a menu command acts on the focused window's work.

## Voice

Voice adds interruption and transient-input problems. Show the transcript or
another persistent representation when exact wording matters, and distinguish
stopping speech from stopping work. The framework callback contract, not the
workbench layout, owns audio and actor isolation; see
[callback and realtime contracts](callback-and-realtime-contracts.md).

## Sources

The product choices here interpret native capabilities; they are not Apple
requirements for all assistant apps. Relevant starting points:

- <https://developer.apple.com/design/human-interface-guidelines/designing-for-macos>
- <https://developer.apple.com/design/human-interface-guidelines/toolbars>
- <https://developer.apple.com/design/human-interface-guidelines/accessibility>
- <https://developer.apple.com/documentation/SwiftUI/bringing-multiple-windows-to-your-swiftui-app>
- <https://developer.apple.com/documentation/swiftui/scene/commands%28content%3A%29>
