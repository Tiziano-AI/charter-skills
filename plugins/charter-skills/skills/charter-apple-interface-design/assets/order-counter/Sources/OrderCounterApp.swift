import SwiftUI

struct CounterCommands: Commands {
    @FocusedValue(\.readyCommand) private var command
    @FocusedValue(\.largerText) private var largerText

    var body: some Commands {
        CommandMenu("Order") {
            Button(command?.title ?? "Mark ready for pickup") { command?.perform() }
                .keyboardShortcut("r", modifiers: [.command, .shift])
                .disabled(command == nil)
        }
        CommandGroup(after: .toolbar) {
            Toggle("Larger Text", isOn: largerText ?? .constant(false))
                .disabled(largerText == nil)
        }
    }
}

struct CounterScene: View {
    @State private var navigation = CounterNavigation()
    @State private var largerText = CommandLine.arguments.contains("--large-text")
    let store: OrderStore

    var body: some View {
        CounterView(store: store, navigation: navigation, textScale: largerText ? 1.5 : 1)
            .focusedSceneValue(\.largerText, $largerText)
            .frame(minWidth: 360, minHeight: 520)
    }
}

struct OrderCounterApp: App {
    @State private var store = OrderStore()
    private let compactStart = CommandLine.arguments.contains("--compact")

    var body: some Scene {
        WindowGroup("Pickup counter", id: compactStart ? "compact-counter" : "counter") {
            CounterScene(store: store)
        }
            .defaultSize(width: compactStart ? 390 : 1000, height: 720)
            .commands { CounterCommands() }
    }
}

@main
enum Entry {
    @MainActor static func main() {
        if CommandLine.arguments.count == 3, CommandLine.arguments[1] == "--exercise" {
            NativeExercise.run(output: CommandLine.arguments[2])
        } else {
            OrderCounterApp.main()
        }
    }
}
