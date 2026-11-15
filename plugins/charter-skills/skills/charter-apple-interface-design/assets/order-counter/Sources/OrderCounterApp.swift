import AppKit
import SwiftUI

struct CounterCommands: Commands {
    @FocusedValue(\.statusCommand) private var command
    @FocusedValue(\.largerText) private var largerText

    var body: some Commands {
        CommandMenu("Order") {
            Button(command?.title ?? "Mark as Ready") { command?.perform() }
                .keyboardShortcut("r")
                .disabled(command == nil)
        }
        CommandGroup(after: .toolbar) {
            Toggle("Larger Text", isOn: largerText ?? .constant(false))
                .disabled(largerText == nil)
        }
    }
}

struct CounterScene: View {
    let store: OrderStore
    @State private var navigation = CounterNavigation()
    // Restoration brings back this window's ticket and text size, not a shared one.
    @SceneStorage("selectedOrder") private var savedSelection: Int?
    @SceneStorage("largerText") private var largerText = false

    var body: some View {
        CounterView(store: store, navigation: navigation)
            .environment(\.contentTextScale, largerText ? 1.5 : 1)
            .focusedSceneValue(\.largerText, $largerText)
            .frame(minWidth: 360, minHeight: 480)
            .background(WindowReader { LiveExercise.register(window: $0, navigation: navigation) })
            .onAppear {
                if CommandLine.arguments.contains("--large-text") { largerText = true }
                // Start on the restored ticket, or on the next order to box.
                navigation.selection = store.order(savedSelection)?.id ?? store.preparing.first?.id
            }
            .onChange(of: navigation.selection) { _, id in savedSelection = id }
    }
}

final class CounterAppDelegate: NSObject, NSApplicationDelegate {
    func applicationDidFinishLaunching(_ notification: Notification) {
        MainActor.assumeIsolated { LiveExercise.startIfRequested() }
    }
}

struct OrderCounterApp: App {
    @NSApplicationDelegateAdaptor(CounterAppDelegate.self) private var delegate
    @State private var store = OrderStore()
    private let compactStart = CommandLine.arguments.contains("--compact")

    var body: some Scene {
        WindowGroup("Pickup Counter", id: compactStart ? "compact-counter" : "counter") {
            CounterScene(store: store)
                .onAppear { LiveExercise.store = store }
        }
        .defaultSize(width: compactStart ? 390 : 1000, height: 700)
        .commands { CounterCommands() }
    }
}

@main
enum Entry {
    @MainActor static func main() {
        if CommandLine.arguments.dropFirst().first == "--exercise" {
            NativeExercise.run()
        } else {
            OrderCounterApp.main()
        }
    }
}
