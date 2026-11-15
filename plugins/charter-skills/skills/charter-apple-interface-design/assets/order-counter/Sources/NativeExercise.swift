import AppKit
import SwiftUI

// Off-screen state checks. The actual CounterView is hosted in a window placed
// off-screen in a process that never activates; the checks drive the same
// store, navigation and undo manager the controls use. It posts no events and
// writes nothing. The live exercise (LiveExercise.swift) covers the menus and
// the rendered window.
@MainActor enum NativeExercise {
    static func run() {
        let app = NSApplication.shared
        app.setActivationPolicy(.prohibited)
        app.finishLaunching()
        let store = OrderStore()
        let navigation = CounterNavigation()
        let controller = NSHostingController(rootView: CounterView(store: store, navigation: navigation))
        let window = NSWindow(contentRect: NSRect(x: -4000, y: -4000, width: 1000, height: 700),
                              styleMask: [.titled, .closable, .resizable], backing: .buffered, defer: false)
        window.contentViewController = controller
        window.setContentSize(NSSize(width: 1000, height: 700))
        window.orderBack(nil)
        settle(window)
        var failures = 0
        func check(_ condition: Bool, _ message: String) {
            print((condition ? "PASS: " : "FAIL: ") + message)
            if !condition { failures += 1 }
        }

        check(store.preparing.map(\.id) == [213, 214, 215, 216, 217, 218], "six orders are Preparing, in number order")
        check(store.ready.map(\.id) == [211, 212], "two orders are Ready")
        navigation.select(213, compact: false)
        settle(window)
        check(navigation.selection == 213 && navigation.path.isEmpty, "a wide selection does not push a path")

        let undo = window.undoManager
        check(undo != nil, "the window supplies an undo manager")
        store.setReady(true, for: 213, undoManager: undo)
        settle(window)
        check(store.order(213)?.isReady == true && store.order(214)?.isReady == false, "Mark as Ready changes only 213")
        check(store.ready.map(\.id) == [211, 212, 213], "213 moves to the Ready section")
        check(undo?.undoMenuItemTitle == "Undo Mark as Ready", "undo title is Undo Mark as Ready")
        undo?.undo()
        check(store.order(213)?.isReady == false, "Undo returns 213 to Preparing")
        check(undo?.redoMenuItemTitle == "Redo Mark as Ready", "redo title keeps the command's name")
        undo?.redo()
        check(store.order(213)?.isReady == true, "Redo marks 213 Ready again")
        store.setReady(false, for: 213, undoManager: undo)
        check(undo?.undoMenuItemTitle == "Undo Mark as Preparing", "the correction has its own name")
        store.setReady(false, for: 213, undoManager: undo)
        check(undo?.undoMenuItemTitle == "Undo Mark as Preparing", "a no-op change registers nothing")

        window.setContentSize(NSSize(width: 390, height: 760))
        settle(window)
        check(navigation.path == [213], "narrowing stacks the selected ticket")
        navigation.path = []
        settle(window)
        check(navigation.selection == 213, "leaving the ticket keeps the selection")
        navigation.select(215, compact: true)
        check(navigation.path == [215], "a compact row opens its ticket")
        window.setContentSize(NSSize(width: 1000, height: 700))
        settle(window)
        check(navigation.path.isEmpty && navigation.selection == 215, "widening keeps 215 selected and clears the stack")

        let other = CounterNavigation()
        other.select(217, compact: false)
        check(navigation.selection == 215, "a second window's selection is its own")

        window.close()
        print(failures == 0 ? "PASS: all off-screen checks" : "FAIL: \(failures) off-screen checks")
        exit(failures == 0 ? 0 : 1)
    }

    static func settle(_ window: NSWindow) {
        for _ in 0..<10 {
            RunLoop.main.run(until: Date(timeIntervalSinceNow: 0.03))
            window.contentView?.layoutSubtreeIfNeeded()
            window.displayIfNeeded()
        }
    }
}
