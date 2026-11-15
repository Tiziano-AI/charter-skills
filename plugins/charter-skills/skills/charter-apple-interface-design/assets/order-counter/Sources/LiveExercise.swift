import AppKit
import SwiftUI

// The live exercise runs inside the normally launched app. It changes state
// only through the app's own menu items and the actions its controls call,
// draws its own windows into bitmaps, and quits. It posts no events to the
// system and reads nothing outside the process. Each capture is logged with
// whether the app was active and the window key when it was drawn.

@MainActor enum LiveExercise {
    private struct Registered {
        weak var window: NSWindow?
        let navigation: CounterNavigation
    }

    private static var registered: [Registered] = []
    static weak var store: OrderStore?
    private static var log: [String] = []

    static func register(window: NSWindow, navigation: CounterNavigation) {
        registered.removeAll { $0.window == nil || $0.window === window }
        registered.append(Registered(window: window, navigation: navigation))
    }

    static func startIfRequested() {
        let arguments = CommandLine.arguments
        guard let flag = arguments.firstIndex(of: "--live-exercise"), flag + 1 < arguments.count else { return }
        let output = URL(fileURLWithPath: arguments[flag + 1], isDirectory: true)
        let steps = value(after: "--steps")?.split(separator: ",").map(String.init) ?? ["wide", "undo", "inactive", "large", "compact"]
        let prefix = value(after: "--prefix") ?? ""
        // New Window must open a second window, not a tab, whatever the
        // person's tab preference; this applies to the exercise process only.
        NSWindow.allowsAutomaticWindowTabbing = false
        switch value(after: "--appearance") {
        case "light": NSApp.appearance = NSAppearance(named: .aqua)
        case "dark": NSApp.appearance = NSAppearance(named: .darkAqua)
        default: break
        }
        Task {
            try? await Task.sleep(for: .seconds(45))
            note("Watchdog quit the app before the exercise finished.")
            write(to: output, prefix: prefix)
            NSApp.terminate(nil)
        }
        Task {
            await run(steps: steps, prefix: prefix, output: output)
            write(to: output, prefix: prefix)
            NSApp.terminate(nil)
        }
    }

    private static func value(after flag: String) -> String? {
        let arguments = CommandLine.arguments
        guard let index = arguments.firstIndex(of: flag), index + 1 < arguments.count else { return nil }
        return arguments[index + 1]
    }

    private static func run(steps: [String], prefix: String, output: URL) async {
        try? FileManager.default.createDirectory(at: output, withIntermediateDirectories: true)
        guard let first = await firstWindow(), let store else { note("FAIL: no window appeared"); return }
        let window = first.window!
        let navigation = first.navigation
        // Let the system make the newly launched app active; never force it.
        for _ in 0..<30 where !(NSApp.isActive && window.isKeyWindow) { await settle(0.1) }
        var accents = ""
        window.effectiveAppearance.performAsCurrentDrawingAppearance {
            accents = "control accent \(hex(NSColor.controlAccentColor)), "
                + "AccentColor asset \(hex(NSColor(named: "AccentColor")))"
        }
        note("Launch: app active \(NSApp.isActive), window key \(window.isKeyWindow), "
             + "appearance \(window.effectiveAppearance.name.rawValue), "
             + "increase contrast \(NSWorkspace.shared.accessibilityDisplayShouldIncreaseContrast), "
             + accents + ", NSAccentColorName "
             + "\(Bundle.main.object(forInfoDictionaryKey: "NSAccentColorName") ?? "missing")")
        window.setContentSize(NSSize(width: 1000, height: 700))
        navigation.select(213, compact: false)
        await settle()

        for step in steps {
            switch step {
            case "wide":
                save(capture(window), "\(prefix)wide-preparing", output, window)
                expect(invoke("Order", "Mark as Ready"), "Order › Mark as Ready was enabled and invoked")
                await settle()
                expect(store.order(213)?.isReady == true, "213 is Ready after the menu command")
                expect(store.order(214)?.isReady == false, "214 is unaffected")
                expect(navigation.selection == 213, "selection stayed on 213")
                expect(menuTitle("Order", matching: { $0.keyEquivalent == "r" }) == "Mark as Preparing",
                       "the Order menu item now reads Mark as Preparing")
                save(capture(window), "\(prefix)wide-ready", output, window)
            case "undo":
                expect(menuTitle("Edit", matching: { $0.action == Selector(("undo:")) }) == "Undo Mark as Ready",
                       "Edit shows Undo Mark as Ready")
                expect(invoke("Edit", where: { $0.action == Selector(("undo:")) }), "Edit › Undo invoked")
                await settle()
                expect(store.order(213)?.isReady == false, "Undo returned 213 to Preparing")
                expect(menuTitle("Edit", matching: { $0.action == Selector(("redo:")) }) == "Redo Mark as Ready",
                       "Edit shows Redo Mark as Ready")
                expect(invoke("Edit", where: { $0.action == Selector(("redo:")) }), "Edit › Redo invoked")
                await settle()
                expect(store.order(213)?.isReady == true, "Redo made 213 Ready again")
                expect(invoke("Edit", where: { $0.action == Selector(("undo:")) }), "Edit › Undo invoked again")
                await settle()
                expect(store.order(213)?.isReady == false, "213 is Preparing for the next captures")
            case "inactive":
                let before = Set(NSApp.windows.map(ObjectIdentifier.init))
                expect(invoke("File", where: { $0.title.hasPrefix("New") && $0.title.contains("Window") }),
                       "File › New Window invoked")
                await settle(0.8)
                guard let second = registered.first(where: {
                    $0.window.map { !before.contains(ObjectIdentifier($0)) } ?? false
                }), let other = second.window else { note("FAIL: no second window"); break }
                other.setContentSize(NSSize(width: 1000, height: 700))
                second.navigation.select(213, compact: false)
                for _ in 0..<20 where !other.isKeyWindow { await settle(0.1) }
                await settle()
                let active = capture(other)
                let inactive = capture(window)
                note("Second window key \(other.isKeyWindow); first window key \(window.isKeyWindow); app active \(NSApp.isActive)")
                saveSideBySide(active, inactive, "\(prefix)wide-active-and-inactive", output)
                other.close()
                await settle(0.6)
            case "large":
                expect(invoke("View", "Larger Text"), "View › Larger Text turned on")
                await settle()
                save(capture(window), "\(prefix)wide-larger-text", output, window)
                expect(invoke("View", "Larger Text"), "View › Larger Text turned off")
                await settle()
            case "compact":
                window.setContentSize(NSSize(width: 390, height: 760))
                await settle()
                expect(navigation.path == [213], "narrowing kept 213 and stacked its ticket")
                // The state the stack's Back button produces; the button itself is not pressed.
                navigation.path = []
                await settle(1.2)
                save(capture(window), "\(prefix)compact-list", output, window)
                navigation.select(213, compact: true)
                await settle(1.0)
                save(capture(window), "\(prefix)compact-ticket", output, window)
                expect(invoke("View", "Larger Text"), "View › Larger Text turned on (compact)")
                await settle()
                save(capture(window), "\(prefix)compact-larger-text", output, window)
                expect(invoke("View", "Larger Text"), "View › Larger Text turned off (compact)")
                window.setContentSize(NSSize(width: 1000, height: 700))
                await settle()
                expect(navigation.path.isEmpty && navigation.selection == 213, "widening kept 213 selected")
            case "single":
                save(capture(window), "\(prefix)wide", output, window)
            default:
                note("Unknown step \(step)")
            }
        }
    }

    // MARK: Menus

    private static func menu(_ title: String) -> NSMenu? {
        guard let menu = NSApp.mainMenu?.items.first(where: { $0.title == title })?.submenu else { return nil }
        // What opening the menu would do: let its owner rebuild it, then validate.
        menu.delegate?.menuNeedsUpdate?(menu)
        menu.update()
        return menu
    }

    private static func menuTitle(_ title: String, matching match: (NSMenuItem) -> Bool) -> String? {
        menu(title)?.items.first(where: match)?.title
    }

    private static func invoke(_ title: String, _ item: String) -> Bool {
        invoke(title, where: { $0.title == item })
    }

    private static func invoke(_ title: String, where match: (NSMenuItem) -> Bool) -> Bool {
        guard let menu = menu(title), let index = menu.items.firstIndex(where: match),
              menu.items[index].isEnabled else { return false }
        note("Invoked \(title) › \(menu.items[index].title)")
        menu.performActionForItem(at: index)
        return true
    }

    // MARK: Capture

    private static func firstWindow() async -> Registered? {
        for _ in 0..<50 {
            if let entry = registered.first(where: { $0.window?.isVisible == true }) { return entry }
            await settle(0.1)
        }
        return nil
    }

    private static func settle(_ seconds: Double = 0.35) async {
        try? await Task.sleep(for: .seconds(seconds))
        for window in NSApp.windows where window.isVisible {
            window.contentView?.layoutSubtreeIfNeeded()
            window.displayIfNeeded()
        }
    }

    private static func capture(_ window: NSWindow) -> NSBitmapImageRep {
        let frame = window.contentView!.superview!
        let bitmap = frame.bitmapImageRepForCachingDisplay(in: frame.bounds)!
        frame.cacheDisplay(in: frame.bounds, to: bitmap)
        // A retained example needs a standard color interpretation, not the display's profile.
        return bitmap.converting(to: .sRGB, renderingIntent: .perceptual)!
    }

    private static func save(_ bitmap: NSBitmapImageRep, _ name: String, _ output: URL, _ window: NSWindow) {
        try? bitmap.representation(using: .png, properties: [:])?.write(to: output.appendingPathComponent(name + ".png"))
        note("Captured \(name).png: \(bitmap.pixelsWide)×\(bitmap.pixelsHigh) px at \(window.backingScaleFactor)x, "
             + "app active \(NSApp.isActive), window key \(window.isKeyWindow), "
             + "appearance \(window.effectiveAppearance.name.rawValue)")
    }

    private static func saveSideBySide(_ left: NSBitmapImageRep, _ right: NSBitmapImageRep, _ name: String, _ output: URL) {
        let gap = 48
        let width = left.pixelsWide + gap + right.pixelsWide
        let height = max(left.pixelsHigh, right.pixelsHigh)
        guard let canvas = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: width, pixelsHigh: height,
                                            bitsPerSample: 8, samplesPerPixel: 4, hasAlpha: true, isPlanar: false,
                                            colorSpaceName: .deviceRGB, bytesPerRow: 0, bitsPerPixel: 0) else { return }
        NSGraphicsContext.saveGraphicsState()
        NSGraphicsContext.current = NSGraphicsContext(bitmapImageRep: canvas)
        NSColor.clear.setFill()
        NSRect(x: 0, y: 0, width: width, height: height).fill()
        left.draw(in: NSRect(x: 0, y: height - left.pixelsHigh, width: left.pixelsWide, height: left.pixelsHigh))
        right.draw(in: NSRect(x: left.pixelsWide + gap, y: height - right.pixelsHigh,
                              width: right.pixelsWide, height: right.pixelsHigh))
        NSGraphicsContext.restoreGraphicsState()
        let srgb = canvas.converting(to: .sRGB, renderingIntent: .perceptual) ?? canvas
        try? srgb.representation(using: .png, properties: [:])?.write(to: output.appendingPathComponent(name + ".png"))
        note("Captured \(name).png: active window on the left, inactive on the right")
    }

    // MARK: Log

    private static func expect(_ condition: Bool, _ message: String) {
        note((condition ? "PASS: " : "FAIL: ") + message)
    }

    private static func note(_ line: String) {
        log.append(line)
        print(line)
    }

    private static func write(to output: URL, prefix: String) {
        let text = log.joined(separator: "\n") + "\n"
        try? text.write(to: output.appendingPathComponent("\(prefix)exercise-log.txt"), atomically: true, encoding: .utf8)
    }

    static func hex(_ color: NSColor?) -> String {
        guard let color = color?.usingColorSpace(.sRGB) else { return "none" }
        return String(format: "#%02X%02X%02X", Int((color.redComponent * 255).rounded()),
                      Int((color.greenComponent * 255).rounded()), Int((color.blueComponent * 255).rounded()))
    }
}

/// Reports the window that hosts a view, so the exercise can find each scene's window.
struct WindowReader: NSViewRepresentable {
    let found: (NSWindow) -> Void

    func makeNSView(context: Context) -> NSView { Probe(found: found) }
    func updateNSView(_ view: NSView, context: Context) {}

    private final class Probe: NSView {
        let found: (NSWindow) -> Void
        init(found: @escaping (NSWindow) -> Void) {
            self.found = found
            super.init(frame: .zero)
        }
        required init?(coder: NSCoder) { nil }
        override func viewDidMoveToWindow() {
            super.viewDidMoveToWindow()
            if let window { found(window) }
        }
    }
}
