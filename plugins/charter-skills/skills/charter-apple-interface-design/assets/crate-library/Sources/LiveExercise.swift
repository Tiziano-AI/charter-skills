import AppKit
import SwiftUI

// The live exercise runs inside the normally launched app. It changes state
// through the app's own menu items, and where a step stands in for a click or
// an arrow key (choosing a crate, selecting a row, narrowing a column) it sets
// the same state that input would and says so in the log. It draws its own
// windows into bitmaps and quits. It posts no events to the system and reads
// nothing outside the process.

@MainActor enum LiveExercise {
    private struct Registered {
        weak var window: NSWindow?
        let state: WindowState
    }

    private static var registered: [Registered] = []
    static weak var library: Library?
    private static var log: [String] = []

    static func register(window: NSWindow, state: WindowState) {
        registered.removeAll { $0.window == nil || $0.window === window }
        registered.append(Registered(window: window, state: state))
    }

    static func startIfRequested() {
        let arguments = CommandLine.arguments
        guard let flag = arguments.firstIndex(of: "--live-exercise"), flag + 1 < arguments.count else { return }
        let output = URL(fileURLWithPath: arguments[flag + 1], isDirectory: true)
        let steps = value(after: "--steps")?.split(separator: ",").map(String.init)
            ?? ["tempo", "match", "move", "inactive", "narrow"]
        let prefix = value(after: "--prefix") ?? ""
        NSWindow.allowsAutomaticWindowTabbing = false
        switch value(after: "--appearance") {
        case "light": NSApp.appearance = NSAppearance(named: .aqua)
        case "dark": NSApp.appearance = NSAppearance(named: .darkAqua)
        default: break
        }
        Task {
            try? await Task.sleep(for: .seconds(60))
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
        guard let first = await firstWindow(), let library else { note("FAIL: no window appeared"); return }
        let window = first.window!
        let state = first.state
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
        let symbols = ["music.note.list", "tray", "archivebox", "smallcircle.filled.circle", "circle.fill",
                       "arrow.up.circle.fill", "arrow.down.circle.fill", "circle.lefthalf.filled", "circle", "circle.dashed"]
        let missing = symbols.filter { NSImage(systemSymbolName: $0, accessibilityDescription: nil) == nil }
        expect(missing.isEmpty, "every SF Symbol the app names exists" + (missing.isEmpty ? "" : ": missing \(missing)"))
        window.setContentSize(NSSize(width: 1200, height: 760))
        await settle()

        for step in steps {
            switch step {
            case "tempo":
                note("Stand-in: choose Peak Time in the sidebar and select track 17, as a click would")
                state.crate = .peakTime
                await settle()
                state.selection = [17]
                await settle()
                save(capture(window), "\(prefix)library-empty-deck", output, window)
                expect(invoke("Track", "Load to Deck"), "Track › Load to Deck invoked")
                await settle()
                expect(library.deck?.id == 17, "track 17 is on the deck")
                expect(invoke("View", "Sort By", "BPM"), "View › Sort By › BPM invoked")
                await settle()
                let bpms = visibleRows(state, library).map(\.track.bpm)
                expect(bpms == bpms.sorted(), "rows are in tempo order")
                note("Stand-in: select track 14, as the Down Arrow would")
                state.selection = [14]
                await settle()
                expect(invoke("Controls", "Play Preview"), "Controls › Play Preview invoked")
                await settle(0.2)
                let start = library.preview.flatMap { p in library.track(p.trackID).map { p.position(in: $0, at: .now) } }
                await settle(2.0)
                let later = library.preview.flatMap { p in library.track(p.trackID).map { p.position(in: $0, at: .now) } }
                expect(library.preview?.trackID == 14, "the preview is of track 14")
                expect((later ?? 0) > (start ?? 1), "the playhead moved from \(start ?? -1) to \(later ?? -1)")
                expect(menuTitle("Controls", matching: { _ in true }) == "Stop Preview", "Controls now offers Stop Preview")
                save(capture(window), "\(prefix)library-tempo", output, window)
                expect(invoke("Controls", "Stop Preview"), "Controls › Stop Preview invoked")
                await settle()
                expect(library.preview == nil, "the preview stopped")
            case "match":
                expect(invoke("View", "Sort By", "Key Match"), "View › Sort By › Key Match invoked")
                await settle()
                let order = visibleRows(state, library)
                expect(order.first?.id == 17, "the deck's own track leads")
                expect(order.map(\.match.rank) == order.map(\.match.rank).sorted(), "rows run from mixable to clashing")
                save(capture(window), "\(prefix)library-key-match", output, window)
            case "move":
                note("Stand-in: select track 27, as a click would")
                state.selection = [27]
                await settle()
                expect(invoke("Track", "Move to Crate", "Late Night"), "Track › Move to Crate › Late Night invoked")
                await settle()
                expect(library.track(27)?.crate == .lateNight, "track 27 is in Late Night")
                expect(menuTitle("Edit", matching: { $0.action == Selector(("undo:")) }) == "Undo Move to Late Night",
                       "Edit shows Undo Move to Late Night")
                expect(invoke("Edit", where: { $0.action == Selector(("undo:")) }), "Edit › Undo invoked")
                await settle()
                expect(library.track(27)?.crate == .peakTime, "Undo returned track 27 to Peak Time")
                expect(menuTitle("Edit", matching: { $0.action == Selector(("redo:")) }) == "Redo Move to Late Night",
                       "Edit shows Redo Move to Late Night")
                expect(invoke("Edit", where: { $0.action == Selector(("redo:")) }), "Edit › Redo invoked")
                await settle()
                expect(library.track(27)?.crate == .lateNight, "Redo moved track 27 again")
                expect(invoke("Edit", where: { $0.action == Selector(("undo:")) }), "Edit › Undo invoked again")
                await settle()
                expect(library.track(27)?.crate == .peakTime, "track 27 is back for the next captures")
            case "inactive":
                let before = Set(NSApp.windows.map(ObjectIdentifier.init))
                expect(invoke("File", where: { $0.title.hasPrefix("New") && $0.title.contains("Window") }),
                       "File › New Window invoked")
                await settle(0.8)
                guard let second = registered.first(where: {
                    $0.window.map { !before.contains(ObjectIdentifier($0)) } ?? false
                }), let other = second.window else { note("FAIL: no second window"); break }
                other.setContentSize(NSSize(width: 1200, height: 760))
                note("Stand-in: choose Peak Time and select track 14 in the second window")
                second.state.crate = .peakTime
                await settle()
                second.state.selection = [14]
                second.state.sortOrder = state.sortOrder
                for _ in 0..<20 where !other.isKeyWindow { await settle(0.1) }
                await settle()
                state.selection = [14]
                await settle()
                let active = capture(other)
                let inactive = capture(window)
                note("Second window key \(other.isKeyWindow); first window key \(window.isKeyWindow); app active \(NSApp.isActive)")
                saveSideBySide(active, inactive, "\(prefix)library-active-and-inactive", output)
                other.close()
                await settle(0.6)
            case "narrow":
                note("Stand-in: choose Late Night and select track 32, as a click would")
                state.crate = .lateNight
                await settle()
                state.selection = [32]
                await settle()
                expect(invoke("Track", "Load to Deck"), "Track › Load to Deck invoked for track 32")
                await settle()
                expect(invoke("View", "Sort By", "Key Match"), "View › Sort By › Key Match invoked")
                await settle()
                if let table = trackTable(in: window), let title = table.tableColumns.first {
                    note("Stand-in: narrow the Title column to 150 pt, as dragging its edge would (was \(Int(title.width)) pt)")
                    let before = title.width
                    title.width = 150
                    await settle()
                    let after = table.tableColumns.first?.width ?? before
                    expect(after < before, "the Title column narrowed to \(Int(after)) pt after the table's own autoresizing")
                } else {
                    note("FAIL: no track table found")
                }
                save(capture(window), "\(prefix)library-narrow-title", output, window)
            case "prepare":
                // Each step can run in its own short launch: this sets up the
                // deck and sort that "tempo" leaves behind.
                state.crate = .peakTime
                await settle()
                state.selection = [17]
                await settle()
                expect(invoke("Track", "Load to Deck"), "Track › Load to Deck invoked")
                await settle()
                expect(invoke("View", "Sort By", "BPM"), "View › Sort By › BPM invoked")
                state.selection = [14]
                await settle()
            case "single":
                state.crate = .peakTime
                await settle()
                state.selection = [17]
                await settle()
                expect(invoke("Track", "Load to Deck"), "Track › Load to Deck invoked")
                await settle()
                expect(invoke("View", "Sort By", "BPM"), "View › Sort By › BPM invoked")
                state.selection = [14]
                await settle()
                save(capture(window), "\(prefix)library", output, window)
            default:
                note("Unknown step \(step)")
            }
        }
    }

    private static func visibleRows(_ state: WindowState, _ library: Library) -> [Row] {
        library.rows(in: state.crate, matching: state.query).sorted(using: state.sortOrder)
    }

    /// The track table is the NSTableView with more than two columns; the
    /// sidebar is an outline view with one.
    private static func trackTable(in window: NSWindow) -> NSTableView? {
        func search(_ view: NSView) -> NSTableView? {
            if let table = view as? NSTableView, table.tableColumns.count > 2 { return table }
            for child in view.subviews { if let found = search(child) { return found } }
            return nil
        }
        return window.contentView.flatMap(search)
    }

    // MARK: Menus

    private static func menu(_ title: String) -> NSMenu? {
        guard let menu = NSApp.mainMenu?.items.first(where: { $0.title == title })?.submenu else { return nil }
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

    /// A submenu item: the menu, the submenu's title and the item's title.
    private static func invoke(_ title: String, _ submenu: String, _ item: String) -> Bool {
        guard let parent = menu(title)?.items.first(where: { $0.title == submenu })?.submenu else { return false }
        parent.delegate?.menuNeedsUpdate?(parent)
        parent.update()
        guard let index = parent.items.firstIndex(where: { $0.title == item }), parent.items[index].isEnabled else {
            return false
        }
        note("Invoked \(title) › \(submenu) › \(item)")
        parent.performActionForItem(at: index)
        return true
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
