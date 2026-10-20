import AppKit
import SwiftUI

// In-process events go only to this off-screen window; no global input is posted.
@MainActor enum NativeExercise {
    static func run(output: String) {
        let app = NSApplication.shared
        app.setActivationPolicy(.prohibited)
        app.finishLaunching()
        let directory = URL(fileURLWithPath: output, isDirectory: true)
        do { try FileManager.default.createDirectory(at: directory, withIntermediateDirectories: true) }
        catch { fatalError("Cannot create output directory: \(error)") }
        let store = OrderStore()
        let navigation = CounterNavigation()
        let controller = NSHostingController(rootView: CounterView(store: store, navigation: navigation))
        let host = controller.view
        let window = NSWindow(contentRect: NSRect(x: -4000, y: -4000, width: 1000, height: 720),
                              styleMask: [.titled, .closable, .resizable], backing: .buffered, defer: false)
        window.contentViewController = controller
        window.setContentSize(NSSize(width: 1000, height: 720))
        window.appearance = NSAppearance(named: .aqua)
        window.orderBack(nil)
        settle(host)
        capture(host, name: "01-wide-list", directory: directory)
        click(host, at: NSPoint(x: 130, y: 180))
        settle(host)
        precondition(navigation.selection == "104")
        capture(host, name: "02-wide-detail", directory: directory)
        click(host, at: NSPoint(x: 415, y: 428))
        settle(host)
        precondition(store.order("104")?.isReady == true)
        precondition(store.readyCount == 2 && store.order("105")?.isReady == false)
        precondition(navigation.selection == "104")
        capture(host, name: "03-wide-ready", directory: directory)
        window.setContentSize(NSSize(width: 390, height: 780))
        settle(host)
        precondition(navigation.selection == "104" && navigation.path == ["104"])
        capture(window.contentView!.superview!, name: "04-compact-detail", directory: directory)
        // The inactive host cannot activate its native title-bar back button.
        // Set up the list for the next rendered/control check; this is not a back-action test.
        navigation.path = []
        settle(host)
        precondition(navigation.path.isEmpty && navigation.selection == "104")
        capture(host, name: "05-compact-list", directory: directory)
        click(host, at: NSPoint(x: 130, y: 180))
        settle(host)
        click(host, at: NSPoint(x: 140, y: 444))
        settle(host)
        precondition(store.order("104")?.isReady == false)
        controller.rootView = CounterView(store: store, navigation: navigation, textScale: 1.5)
        settle(host)
        click(host, at: NSPoint(x: 160, y: 538))
        settle(host)
        precondition(store.order("104")?.isReady == true)
        capture(host, name: "06-enlarged-detail", directory: directory)
        window.close()
        print("PASS: native row → detail → status action; updated queue; selection through resize; compact row reopen and correction; enlarged-text action. Compact back was arranged through navigation state, not activated by this probe.")
    }

    static func settle(_ host: NSView) {
        for _ in 0..<12 {
            RunLoop.main.run(until: Date(timeIntervalSinceNow: 0.03))
            host.layoutSubtreeIfNeeded()
            host.displayIfNeeded()
        }
    }

    static func click(_ host: NSView, at topLeftPoint: NSPoint) {
        let window = host.window!
        let viewPoint = host.isFlipped ? topLeftPoint : NSPoint(x: topLeftPoint.x, y: host.bounds.height - topLeftPoint.y)
        let point = host.convert(viewPoint, to: nil)
        for type in [NSEvent.EventType.leftMouseDown, .leftMouseUp] {
            let event = NSEvent.mouseEvent(with: type, location: point, modifierFlags: [],
                                          timestamp: ProcessInfo.processInfo.systemUptime,
                                          windowNumber: window.windowNumber, context: nil,
                                          eventNumber: 0, clickCount: 1, pressure: 1)!
            window.sendEvent(event)
        }
    }

    static func capture(_ view: NSView, name: String, directory: URL) {
        let host = view.window!.contentView!.superview!
        guard let bitmap = host.bitmapImageRepForCachingDisplay(in: host.bounds) else { fatalError("No bitmap") }
        host.cacheDisplay(in: host.bounds, to: bitmap)
        // A retained example needs a standard color interpretation, not the capture display's profile.
        guard let standardBitmap = bitmap.converting(to: .sRGB, renderingIntent: .perceptual),
              let png = standardBitmap.representation(using: .png, properties: [:]) else { fatalError("No sRGB PNG") }
        try! png.write(to: directory.appendingPathComponent(name + ".png"))
    }
}
