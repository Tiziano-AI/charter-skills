import AppKit
import SwiftUI

struct LibraryCommands: Commands {
    @FocusedValue(\.libraryActions) private var actions

    var body: some Commands {
        CommandMenu("Track") {
            Button("Load to Deck") { actions?.load() }
                .keyboardShortcut("l")
                .disabled(!(actions?.canLoad ?? false))
            Button("Eject Track") { actions?.eject() }
                .keyboardShortcut("e")
                .disabled(!(actions?.canEject ?? false))
            Divider()
            Menu("Move to Crate") {
                ForEach(Array(CrateID.crates.enumerated()), id: \.element) { index, crate in
                    Button(crate.title) { actions?.move(crate) }
                        .keyboardShortcut(KeyEquivalent(Character(String(index + 1))), modifiers: [.option, .command])
                        .disabled(!(actions?.canMove(crate) ?? false))
                }
            }
        }
        CommandMenu("Controls") {
            // Space plays and stops a preview in the table. It is not a menu key
            // equivalent, which risks catching Space typed in the search field.
            Button(actions?.isPreviewing == true ? "Stop Preview" : "Play Preview") { actions?.togglePreview() }
                .disabled(!(actions?.canPreview ?? false))
        }
        CommandGroup(after: .toolbar) {
            Menu("Sort By") {
                ForEach(Array(SortField.allCases.enumerated()), id: \.element) { index, field in
                    Toggle(field.title, isOn: Binding(get: { actions?.sortField == field },
                                                      set: { _ in actions?.sort(field) }))
                        .keyboardShortcut(KeyEquivalent(Character(String(index + 1))), modifiers: [.control, .option, .command])
                        .disabled(actions == nil || (field.needsDeck && !(actions?.deckLoaded ?? false)))
                }
            }
        }
    }
}

/// One window. Its crate, selection and sort come back with the window when
/// the system restores it; the library and the deck are shared.
struct LibraryScene: View {
    let library: Library
    @State private var state = WindowState()
    @SceneStorage("crate") private var savedCrate = CrateID.all.rawValue
    @SceneStorage("selection") private var savedSelection = ""
    @SceneStorage("sort") private var savedSort = SortField.title.rawValue

    var body: some View {
        LibraryWindow(library: library, state: state)
            .frame(minWidth: 760, minHeight: 420)
            .background(WindowReader { LiveExercise.register(window: $0, state: state) })
            .onAppear {
                state.crate = CrateID(rawValue: savedCrate) ?? .all
                state.sortOrder = [(SortField(rawValue: savedSort) ?? .title).comparator]
                state.selection = Set(savedSelection.split(separator: ",").compactMap { Int($0) })
            }
            .onChange(of: state.crate) { _, crate in savedCrate = crate.rawValue }
            .onChange(of: state.selection) { _, ids in savedSelection = ids.sorted().map(String.init).joined(separator: ",") }
            .onChange(of: SortField(state.sortOrder.first)) { _, field in
                // Pitch and Key Match need a deck, which is not restored, so a
                // restored window falls back to Title for those.
                savedSort = (field.flatMap { $0.needsDeck ? nil : $0 } ?? .title).rawValue
            }
    }
}

final class LibraryAppDelegate: NSObject, NSApplicationDelegate {
    func applicationDidFinishLaunching(_ notification: Notification) {
        MainActor.assumeIsolated { LiveExercise.startIfRequested() }
    }
}

struct CrateLibraryApp: App {
    @NSApplicationDelegateAdaptor(LibraryAppDelegate.self) private var delegate
    @State private var library = Library()

    var body: some Scene {
        WindowGroup("Crate Library", id: "library") {
            LibraryScene(library: library)
                .onAppear { LiveExercise.library = library }
        }
        .defaultSize(width: 1200, height: 760)
        .commands { LibraryCommands() }
    }
}

@main
enum Entry {
    @MainActor static func main() {
        if CommandLine.arguments.dropFirst().first == "--exercise" {
            StateChecks.run()
        } else {
            CrateLibraryApp.main()
        }
    }
}
