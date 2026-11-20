# Pickup Counter

A small, offline macOS SwiftUI app for a doughnut shop's pickup counter,
adapted from Apple's Food Truck sample.

It is used behind the counter in the morning rush, read at arm's length with both hands busy.
Orders arrive paid; staff box one, call its number aloud, and check the name when someone steps forward.

Choose an order in the queue, read its ticket, box it, then **Order → Mark as
Ready**. The order moves to the Ready section and stays selected, and the
ticket shows its new state. **Edit → Undo Mark as Ready** takes it back. Wide
windows show the queue and the ticket together; under 720 points the same
content becomes a stack with a native Back control.

## Build and open

Requires a Mac with Xcode (for `swift` and `actool`) and the macOS SDK. From
this directory:

```sh
./build-app.sh /tmp/charter-order-counter
open /tmp/charter-order-counter/OrderCounter.app
```

The script builds the Swift package, assembles an unsigned `.app` in the
directory you give it, and compiles `Assets.xcassets` with `actool` into
`Contents/Resources/Assets.car`. `Info.plist` names the catalog's color through
`NSAccentColorName`, which is how AppKit finds the app's accent. The script
neither installs nor launches the app. The package has no dependencies,
network calls, accounts or storage; the eight fictional orders reset on quit.

`--compact` starts a separate, 390-point-wide window; `--large-text` starts
with the larger text on.

## What the counter decides

- **The ticket is the custom moment.** The order hangs as a paper ticket from
  a rail: a square top, a torn edge, dashed perforations between its parts.
  The called number is the one figure with a fixed size, 92-point bold
  condensed with tabular figures, because it is read and called from arm's
  length. The name sits under it as the cross-check.
- **The contents read like the ticket.** Each box is headed by its size
  (Single, Half-dozen, Dozen) beside a small glyph of its slots, and the
  quantities share one aligned column across every box.
- **The note is the note someone wrote.** It is set in Noteworthy, which ships
  with macOS, at a size matched to the Title 3 text beside it, with no card
  around it.
- **Money is secondary.** Orders are paid online, so the total only settles a
  question at the counter. It sits at the foot of the ticket in a smaller,
  secondary style, written in the Mac's own currency format.
- **Everything else is the system's.** The queue is a sidebar list at Mac
  density: state, number, name and doughnut count, sectioned Preparing and
  Ready. Text uses system text styles with a weight chosen for each role,
  and colors are semantic.
- **State is shape and word.** Ready is a filled check in green, the system's
  completion color, beside the word Ready; Preparing is an open dotted ring
  beside the word Preparing in a secondary style. Neither is the accent.
- **One accent, from the shop.** The pink of the doughnut box marks the
  primary action and selection. Pink means no system state, so it never reads
  as Ready. `AccentColor` has light, dark and High Contrast values for each.
  On the Mac the person's accent setting replaces it unless they chose
  Multicolor.
- **One verb everywhere.** The button, the Order menu item and the Undo title
  all say Mark as Ready, or Mark as Preparing for the correction, which steps
  down to a plain button. The action stays at the ticket's trailing edge in a
  bar under it, however long the ticket is.
- **A quiet sample notice.** The window subtitle reads "Sample orders, not
  live".

Commands: **Order → Mark as Ready / Mark as Preparing** (Command-R) for the
selected order in the focused window, **Edit → Undo** and **Redo** with the
command's name, **View → Larger Text** for a 150 percent content scale, and
**File → New Pickup Counter Window**. Larger Text is this app's own scale; the
Mac has no Dynamic Type.

## Follow the construction

- `Sources/OrderModel.swift`: the shared `OrderStore`, the orders and box
  sizes, the undoable status change, and one window's `CounterNavigation`.
- `Sources/CounterView.swift`: the split view and the compact stack, the queue,
  the detail with its action bar, and the focused status command.
- `Sources/TicketView.swift`: the ticket, its number, contents, note and rail.
- `Sources/TextScale.swift`: the Larger Text scale applied to text styles.
- `Sources/OrderCounterApp.swift`: commands, per-window restoration of the
  selected order and text scale, and the entry point.
- `Sources/NativeExercise.swift` and `Sources/LiveExercise.swift`: the two
  exercises below.

The model has only Preparing and Ready. Placing, collecting and paying for
orders, persistence, notifications and any service contract are outside it.

## Exercises

```sh
/tmp/charter-order-counter/OrderCounter.app/Contents/MacOS/OrderCounter --exercise
```

`--exercise` hosts `CounterView` in an off-screen window that never activates
and checks state through the same store, navigation and undo manager the
controls use: section membership, a change that leaves its neighbour alone,
Undo and Redo titles, a no-op change that registers nothing, selection through
narrowing and widening, and a second window's separate selection. It prints
PASS or FAIL lines and posts no events.

```sh
open -n -W /tmp/charter-order-counter/OrderCounter.app --args \
  -ApplePersistenceIgnoreState YES -AppleAccentColor 7 \
  --live-exercise /tmp/charter-order-counter/renders --appearance light
```

`--live-exercise` runs inside a normal launch. It invokes the app's own menu
items (Order, Edit, File and View), draws each window into a bitmap from inside
the process, writes PNGs and a log, and quits; a watchdog quits it after 45
seconds. `--steps` chooses from `wide`, `undo`, `inactive`, `large`, `compact`
and `single`, and `--prefix` names the files. It sends no keystrokes or clicks
and raises no permission prompt. The log records, for every capture, whether
the app was active and the window key, and at launch the appearance, Increase
Contrast, the effective control accent and the `AccentColor` value, which is
how the build is confirmed to use its catalog.

## Renders

All renders are 2x PNGs in sRGB, drawn by the running app from its own window
during `--live-exercise`, one launch per row. The log records the app active
and the window key at every capture; the right half of the active-and-inactive
pair is the inactive window. Only `as-configured-wide.png` shows the Mac as it
is set up. Every other render ran with per-process overrides,
`--appearance light` (`dark` for `dark-wide.png`) and `-AppleAccentColor 7`,
plus `-increaseContrast 1` for `increase-contrast-wide.png`, so it shows the
app in a chosen state rather than this Mac's window as configured.

| File | What it shows | How it was made |
| --- | --- | --- |
| `wide-preparing.png`, `wide-ready.png` | Order 213 before and after Order → Mark as Ready, in the same window | Light appearance and the app's accent, by the per-process arguments below |
| `wide-active-and-inactive.png` | The same ticket in a second window (active, left) and the first window (inactive, right) | File → New Pickup Counter Window, then 213 selected in the new window |
| `wide-larger-text.png`, `compact-larger-text.png` | View → Larger Text, the app's own 150 percent scale, not Dynamic Type | Menu item invoked in each layout |
| `compact-list.png`, `compact-ticket.png` | The stack at 390 points: the queue, then 213's ticket | Window resized in-process; the queue is reached by clearing the stack path, the state Back produces, without pressing Back |
| `dark-wide.png` | Dark appearance | `--appearance dark` |
| `increase-contrast-wide.png` | Increase Contrast, light | `-increaseContrast 1` |
| `as-configured-wide.png` | The Mac as it was set up: dark, with the person's Orange accent replacing the app's | No appearance, accent or contrast override |

The overrides apply to the app's process only and leave the Mac's settings
alone: `--appearance light|dark` sets the app's appearance;
`-AppleAccentColor 7` made the system accent follow the app's `AccentColor`,
as Multicolor does; `-increaseContrast 1` turned on Increase Contrast for the
app, which then drew its High Contrast colors; `-ApplePersistenceIgnoreState
YES` skips restoring earlier windows. Drawing a window into a bitmap renders
sidebar and bar materials as their flat fallbacks.

The [worked-flow reference](../../references/order-counter.md) walks through
these renders and what was observed.

## Upstream and rights

The source relationship is Apple's [Food Truck sample at
3954a769e99f3cc53297d94f2b960ceb2665b3d6](https://github.com/apple/sample-food-truck/tree/3954a769e99f3cc53297d94f2b960ceb2665b3d6),
especially `App/Navigation/ContentView.swift`, `App/Orders/OrdersView.swift`,
`App/Orders/OrderDetailView.swift` and the `FoodTruckKit` order model. The
adaptation keeps the relationship between stable selection, one owner of order
state and the detail's action; it replaces the original order lifecycle with
two states and uses Observation rather than ObservableObject.

It is not an unchanged Apple sample or an Apple design recommendation. The
shop, its orders and the presentation are Charter's; no Apple artwork is
copied. SF Symbols and the Noteworthy face are drawn from macOS at run time and
are not bundled. Apple's MIT notice and the terms for these adaptations are in
`LICENSE.txt`.
