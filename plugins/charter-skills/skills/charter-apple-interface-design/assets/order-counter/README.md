# Order counter

A small, offline macOS SwiftUI app adapted from Apple's Food Truck sample.
Choose an order, read its items and packing note, mark it ready, then find the
changed order in the same queue. The status can be corrected without removing
the order. Wide windows show list and detail together; narrow windows use a
stack and a native Back control.

## Build and open

Requires a Mac and the Swift toolchain declared in `Package.swift`, with the
macOS SDK. From this directory:

```sh
./build-app.sh /tmp/charter-order-counter
open /tmp/charter-order-counter/OrderCounter.app
```

The script compiles into the supplied directory and creates an unsigned local
`.app` there. It neither installs nor launches it. Quit the sample before
rebuilding that output. The package has no external dependencies, network
calls, accounts or persistent order storage. Its four fictional fixtures reset
on quit; the window geometry may be restored by macOS.

For an initially narrow window, quit the app and run:

```sh
open /tmp/charter-order-counter/OrderCounter.app --args --compact
```

`--compact` gives this launch a separate window identity and an initial width
of 390 points; a previously resized window may restore its saved geometry.
Resize either window to see the composition switch at 720 points. This
threshold belongs to this content, not to Apple platforms generally.

Select an order and use **Order → Mark ready for pickup**, or **Command-Shift-R**.
The same command becomes **Return to preparing** after the change. **View →
Larger Text** enlarges content text to 150%; `--large-text` starts that way.
This deliberate content-scale exercise is not an implementation or test of
iOS Dynamic Type or a replacement for assistive-technology testing.

## Follow the construction

- `Sources/OrderModel.swift`: app-shared observable orders, one reversible
  readiness mutation, stable IDs, and separate window-local navigation.
- `Sources/CounterView.swift`: queue, detail and status presentation; split
  versus stack composition; ID-based detail lookup; the focused scene command.
- `Sources/OrderCounterApp.swift`: per-window selection/text scale, shared
  store, native menu commands and app entry point.
- `Sources/NativeExercise.swift`: a bounded native rendering and control probe.

The model is intentionally only Preparing ↔ Ready for pickup. It excludes
order placement, collection, payment, service synchronization, persistence,
widgets, Live Activities and notifications. A production service would need
its own transition and failure contract rather than inheriting this local
toggle.

## Native exercise and renders

```sh
/tmp/charter-order-counter/OrderCounter.app/Contents/MacOS/OrderCounter \
  --exercise /tmp/charter-order-counter/renders
```

The exercise hosts the actual `CounterView` in an off-screen native window,
clicks rows and status buttons with in-process events, checks store and
navigation effects, and writes six PNGs. It does not post global input or
connect to a service. Output files with the same names are replaced.

Its coordinates are for the included fixtures and fixed geometry. It checks
wide selection and mutation, the unaffected neighboring order, selection
through narrowing, compact reopening/correction, and an enlarged-text action.
It arranges the compact list by clearing the navigation path: it **does not
activate the title-bar Back button or exercise menu shortcuts**. Those require
the running app.

The retained PNGs in `renders/` are sRGB native window captures in light appearance,
including inactive system chrome, not HTML or painted UI mockups. They show
the same selected order before and after the change, its updated compact row,
and compact detail with larger text. The adjacent
[worked-flow reference](../../references/order-counter.md) connects those
views to the design decisions.

The package's deployment minimum is a build declaration, not evidence of
execution on every supported system. To inspect the native interaction rather
than the off-screen probe, follow compact row → detail → status change →
native Back → updated row → reopen; use the status shortcut in wide and
compact layouts and the Larger Text menu control. Those paths exercise this
example, not every platform, input method or downstream product.

## Upstream and rights

The source relationship is Apple's [Food Truck sample at
3954a769e99f3cc53297d94f2b960ceb2665b3d6](https://github.com/apple/sample-food-truck/tree/3954a769e99f3cc53297d94f2b960ceb2665b3d6),
especially `App/Navigation/ContentView.swift`, `App/Orders/OrdersView.swift`,
`App/Orders/OrderDetailView.swift` and the `FoodTruckKit` order model. The
adaptation retains the relationship between stable selection, canonical order
state and detail actions; it replaces the original state lifecycle with the
two-state counter and uses Observation rather than ObservableObject.

It is not an unchanged Apple sample or an official Apple design recommendation.
The fictional identity, fixtures and presentation are Charter's adaptations;
no Apple artwork was copied. System symbols are supplied by macOS. Apple's
complete MIT notice and the terms for these adaptations are in `LICENSE.txt`.
