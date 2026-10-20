# Mac companion structure

A companion can remain available around other work without trying to own the
desktop. Choose its surfaces according to attention and task duration, not a
fixed requirement to build a menu bar, palette, sidebar and dashboard.

## Presence, entry and sustained work

A menu-bar item or `MenuBarExtra` is useful for a glance, capture or quick
command. A small utility may live there entirely. Sustained reading, complex
editing, comparison or a branching workflow usually benefits from a window
that remains open and resizable.

A quick-entry panel accelerates a known action. It should not become a second
inconsistent workspace. A main window can be a document, a split view, an
activity feed, a canvas or an assistant workbench according to the product.

Notifications and Dock or menu-bar state represent background work. They are
not substitutes for a place to inspect its result. Keep background-service
lifetime separate from whether a presentation is currently visible.

## Windows and commands

Use simultaneous windows when independent objects benefit from comparison or
parallel work. A single focused window may be better for one shared operation.
Make reopening restore a useful place rather than a blank shell, and make
window close, app quit and cancellation mean different things when they are
different in the implementation.

Separate scene-local selection and focus from shared data. Menu and keyboard
commands need the intended active document or selection. Multiple windows
must not route an action through a stale global “current item.”

Use conventional menu organization and meaningful command labels. A status
item provides quick entry; application menus support discovery and shortcuts.
A command palette can supplement them without hiding the only route to an
important action.

Search finds or filters content; commands act. A combined interface can support
both when it identifies which result navigates and which causes an effect.
Do not make people infer that distinction from an icon alone.

## Native framework seams

SwiftUI can own scenes, navigation, commands and settings. `WindowGroup`,
`openWindow`, `MenuBarExtra`, `SettingsLink` and command APIs are useful
when their lifecycles fit. AppKit can own a narrower status-item, panel, menu,
responder or window behavior when that control is needed.

Bridge the specific seam and keep one owner for the affected state. A hosting
view does not erase AppKit lifecycle or responder responsibilities. Conversely,
a native-looking wrapper does not make embedded web content a native
interaction; use web content where it is the actual job.

Use an inspector for selected-object detail and a dedicated settings scene for
app preferences when appropriate. Local object settings can remain in the
object's context. Do not force unrelated configuration into a generic health
screen.

## Attention and background work

Choose inline feedback, a persistent activity destination or a notification
according to whether the person is present and whether action is needed.
Completion can deserve a notification when the user left to do other work;
the same event may need only inline feedback while they are watching.

Request notification permission where its value is understandable. Match
urgency and interruption level to the event, not the implementation's desire
for attention. Preserve a quiet, inspectable history for nonurgent activity.
A badge should lead to the specific object or problem it represents.

When an action needs permission, an account or provider setup, open that
specific correction path and retain the original context. Generic “Retry”
buttons are poor substitutes for a known missing prerequisite.

For an assistant-centered product, see [assistant workbenches](assistant-workbench.md).
For capture and transcription, see [callback contracts](callback-and-realtime-contracts.md);
presentation code does not determine a framework callback's execution context.

## Relevant authorities

- <https://developer.apple.com/design/human-interface-guidelines/designing-for-macos>
- <https://developer.apple.com/design/human-interface-guidelines/the-menu-bar>
- <https://developer.apple.com/design/human-interface-guidelines/menus>
- <https://developer.apple.com/design/human-interface-guidelines/managing-notifications>
- <https://developer.apple.com/design/human-interface-guidelines/alerts>
- <https://developer.apple.com/design/human-interface-guidelines/accessibility>
- <https://developer.apple.com/documentation/swiftui/menubarextra>
- <https://developer.apple.com/documentation/appkit/nsstatusbar>
- <https://developer.apple.com/documentation/SwiftUI/bringing-multiple-windows-to-your-swiftui-app>
- <https://developer.apple.com/documentation/swiftui/scene/commands%28content%3A%29>

These sources establish native affordances and guidance, not one mandatory
product architecture.
