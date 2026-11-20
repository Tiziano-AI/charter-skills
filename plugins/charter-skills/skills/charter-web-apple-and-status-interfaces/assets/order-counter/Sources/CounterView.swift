// Adapted from Apple's Food Truck sample. See ../LICENSE.txt and README.md.
import SwiftUI

struct StatusCommand {
    let title: String
    let perform: () -> Void
}

struct StatusCommandKey: FocusedValueKey { typealias Value = StatusCommand }
struct LargerTextKey: FocusedValueKey { typealias Value = Binding<Bool> }

extension FocusedValues {
    var statusCommand: StatusCommand? {
        get { self[StatusCommandKey.self] }
        set { self[StatusCommandKey.self] = newValue }
    }
    var largerText: Binding<Bool>? {
        get { self[LargerTextKey.self] }
        set { self[LargerTextKey.self] = newValue }
    }
}

/// Wide windows show the queue and the ticket together; under this width the
/// same content becomes a stack. The threshold suits this queue, not a device.
let compactWidth: CGFloat = 720

struct CounterView: View {
    @Bindable var store: OrderStore
    @Bindable var navigation: CounterNavigation
    @Environment(\.undoManager) private var undoManager

    var body: some View {
        GeometryReader { geometry in
            let compact = geometry.size.width < compactWidth
            Group {
                if compact {
                    NavigationStack(path: $navigation.path) {
                        QueueList(store: store, navigation: navigation, compact: true)
                            .navigationDestination(for: Int.self) { id in detail(id) }
                    }
                } else {
                    NavigationSplitView {
                        QueueList(store: store, navigation: navigation, compact: false)
                            .navigationSplitViewColumnWidth(min: 250, ideal: 290, max: 380)
                    } detail: {
                        detail(navigation.selection)
                    }
                }
            }
            .onChange(of: compact) { _, value in navigation.adapt(toCompact: value) }
            .focusedSceneValue(\.statusCommand, command)
        }
        .navigationTitle("Pickup Counter")
        .navigationSubtitle("Sample orders, not live")
    }

    private var command: StatusCommand? {
        guard let order = store.order(navigation.selection) else { return nil }
        return StatusCommand(title: order.statusCommand) { toggle(order.id) }
    }

    private func toggle(_ id: Int) {
        guard let order = store.order(id) else { return }
        store.setReady(!order.isReady, for: id, undoManager: undoManager)
    }

    @ViewBuilder private func detail(_ id: Int?) -> some View {
        if let order = store.order(id) {
            OrderDetail(order: order) { toggle(order.id) }
        } else {
            ContentUnavailableView("No Order Selected", systemImage: "ticket",
                                   description: Text("Choose an order in the queue to see its ticket."))
        }
    }
}

struct QueueList: View {
    @Bindable var store: OrderStore
    @Bindable var navigation: CounterNavigation
    let compact: Bool
    // The queue takes the keyboard at launch, so the arrow keys move through it.
    @FocusState private var focused: Bool

    var body: some View {
        Group {
            if compact {
                // In the stack a row opens the ticket; arrow keys must not push it.
                List {
                    sections { order in NavigationLink(value: order.id) { QueueRow(order: order) } }
                }
            } else {
                List(selection: Binding(get: { navigation.selection },
                                        set: { navigation.select($0, compact: false) })) {
                    sections { order in QueueRow(order: order).tag(order.id) }
                }
                .focused($focused)
                .task { focused = true }
            }
        }
        .listStyle(.sidebar)
    }

    @ViewBuilder
    private func sections<Row: View>(@ViewBuilder row: @escaping (Order) -> Row) -> some View {
        if !store.preparing.isEmpty {
            Section("Preparing") { ForEach(store.preparing) { row($0) } }
        }
        if !store.ready.isEmpty {
            Section("Ready") { ForEach(store.ready) { row($0) } }
        }
    }
}

/// Number, name, count and state at Mac density. The section names the state;
/// the symbol's shape repeats it on every row.
struct QueueRow: View {
    let order: Order

    var body: some View {
        HStack(spacing: 8) {
            StatusSymbol(isReady: order.isReady)
            Text(order.id, format: .number.grouping(.never))
                .fontWeight(.semibold)
                .monospacedDigit()
            Text(order.name)
                .lineLimit(1)
                .truncationMode(.tail)
            Spacer(minLength: 6)
            Text(order.count, format: .number)
                .monospacedDigit()
                .foregroundStyle(.secondary)
        }
        .textStyle(.body)
        .help("\(order.name), \(order.count) doughnuts")
        .accessibilityElement(children: .ignore)
        .accessibilityLabel("Order \(order.id), \(order.name)")
        .accessibilityValue("\(order.count) doughnuts, \(order.status)")
    }
}

struct OrderDetail: View {
    let order: Order
    let changeStatus: () -> Void
    @Environment(\.contentTextScale) private var scale

    var body: some View {
        ScrollView {
            TicketOnRail(order: order)
                .padding(.horizontal, 24)
                .padding(.bottom, 28)
                .frame(maxWidth: .infinity)
        }
        // The action stays in view however long the ticket is, at the ticket's
        // trailing edge, where the eye ends after reading it.
        .safeAreaInset(edge: .bottom, spacing: 0) {
            VStack(spacing: 0) {
                Divider()
                HStack {
                    Spacer()
                    StatusButton(order: order, action: changeStatus)
                }
                .frame(maxWidth: 440 * scale)
                .padding(.horizontal, 42)
                .padding(.vertical, 14)
                .frame(maxWidth: .infinity)
            }
            .background(.bar)
        }
    }
}

/// Marking ready is the primary action; taking it back is a correction, so it
/// steps down to a plain button. Its label carries it where no tint is drawn.
struct StatusButton: View {
    let order: Order
    let action: () -> Void

    var body: some View {
        Group { buttons }
            .controlSize(.large)
            .textStyle(.body, weight: .semibold)
    }

    @ViewBuilder private var buttons: some View {
        if order.isReady {
            Button(action: action) {
                Label(order.statusCommand, systemImage: "arrow.uturn.backward")
            }
            .help("Return this order to Preparing")
        } else {
            Button(action: action) {
                Label(order.statusCommand, systemImage: "checkmark")
            }
            .buttonStyle(.borderedProminent)
            .help("Mark this order as Ready once it is boxed")
        }
    }
}
