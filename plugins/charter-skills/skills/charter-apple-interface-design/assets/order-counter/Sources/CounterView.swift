// Adapted from Apple's Food Truck sample. See ../LICENSE.txt and README.md.
import SwiftUI

struct ReadyCommand {
    let title: String
    let perform: () -> Void
}

struct ReadyCommandKey: FocusedValueKey { typealias Value = ReadyCommand }
struct LargerTextKey: FocusedValueKey { typealias Value = Binding<Bool> }

extension FocusedValues {
    var readyCommand: ReadyCommand? {
        get { self[ReadyCommandKey.self] }
        set { self[ReadyCommandKey.self] = newValue }
    }
    var largerText: Binding<Bool>? {
        get { self[LargerTextKey.self] }
        set { self[LargerTextKey.self] = newValue }
    }
}

struct CounterView: View {
    @Bindable var store: OrderStore
    @Bindable var navigation: CounterNavigation
    var textScale = 1.0

    var body: some View {
        GeometryReader { geometry in
            let compact = geometry.size.width < 720
            Group {
                if compact {
                    NavigationStack(path: $navigation.path) {
                        orders(compact: true)
                            .navigationDestination(for: String.self) { id in detail(id) }
                    }
                } else {
                    NavigationSplitView {
                        orders(compact: false)
                            .navigationSplitViewColumnWidth(min: 260, ideal: 300, max: 360)
                    } detail: {
                        detail(navigation.selection)
                    }
                    .navigationSplitViewStyle(.balanced)
                }
            }
            .onChange(of: compact) { _, value in navigation.adapt(toCompact: value) }
            .focusedSceneValue(\.readyCommand, selectedCommand)
        }
        .font(.system(size: 14 * textScale))
        .tint(.orange)
        .background(Color(nsColor: .windowBackgroundColor))
    }

    private var selectedCommand: ReadyCommand? {
        guard let order = store.order(navigation.selection) else { return nil }
        return ReadyCommand(title: order.action) { store.toggleReady(order.id) }
    }

    private func orders(compact: Bool) -> some View {
        VStack(alignment: .leading, spacing: 0) {
            VStack(alignment: .leading, spacing: 7) {
                Label("SUNRISE DONUTS", systemImage: "sun.max.fill")
                    .font(.system(size: 11 * textScale, weight: .bold))
                    .foregroundStyle(.secondary)
                Text("Pickup counter")
                    .font(.system(size: 26 * textScale, weight: .bold, design: .rounded))
                Text("\(store.orders.count - store.readyCount) preparing · \(store.readyCount) ready")
                    .foregroundStyle(.secondary)
                    .accessibilityIdentifier("queue-summary")
            }
            .padding(20)

            List(selection: $navigation.selection) {
                ForEach(store.orders) { order in
                    Button {
                        navigation.select(order.id, compact: compact)
                    } label: {
                        OrderRow(order: order, textScale: textScale)
                            .frame(maxWidth: .infinity, alignment: .leading)
                            .contentShape(Rectangle())
                    }
                    .buttonStyle(.plain)
                    .accessibilityIdentifier("order-\(order.id)")
                    .tag(order.id)
                }
            }
            .listStyle(.sidebar)
            .navigationTitle("Orders")
            Text("Local sample · Changes reset when you quit")
                .font(.system(size: 11 * textScale))
                .foregroundStyle(.secondary)
                .padding(20)
        }
    }

    @ViewBuilder private func detail(_ id: String?) -> some View {
        if let order = store.order(id) {
            OrderDetail(order: order, textScale: textScale) { store.toggleReady(order.id) }
        } else {
            ContentUnavailableView("Choose an order", systemImage: "takeoutbag.and.cup.and.straw",
                                   description: Text("Review the items, then mark the order ready for pickup."))
        }
    }
}

struct OrderRow: View {
    let order: Order
    let textScale: Double

    var body: some View {
        VStack(alignment: .leading, spacing: 6) {
            HStack(alignment: .firstTextBaseline) {
                Text("#\(order.id)").fontWeight(.bold).monospacedDigit()
                Spacer(minLength: 8)
                Text(price(order.total)).foregroundStyle(.secondary)
            }
            Text(order.customer).fontWeight(.medium)
            Text("\(order.itemCount) donuts")
                .foregroundStyle(.secondary)
            StatusLabel(isReady: order.isReady, textScale: textScale)
        }
        .padding(.vertical, 10)
        .accessibilityElement(children: .combine)
    }
}

struct StatusLabel: View {
    let isReady: Bool
    let textScale: Double

    var body: some View {
        Label {
            Text(isReady ? "Ready for pickup" : "Preparing")
                .foregroundStyle(isReady ? Color.primary : Color.secondary)
        } icon: {
            Image(systemName: isReady ? "checkmark.circle.fill" : "circle.dotted")
                .foregroundStyle(isReady ? Color.green : Color.secondary)
        }
        .font(.system(size: 12 * textScale, weight: .semibold))
    }
}

struct OrderDetail: View {
    let order: Order
    let textScale: Double
    let changeStatus: () -> Void

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 28) {
                VStack(alignment: .leading, spacing: 10) {
                    Text("ORDER #\(order.id)")
                        .font(.system(size: 12 * textScale, weight: .bold))
                        .foregroundStyle(.secondary)
                    Text(order.customer)
                        .font(.system(size: 32 * textScale, weight: .bold, design: .rounded))
                        .fixedSize(horizontal: false, vertical: true)
                    StatusLabel(isReady: order.isReady, textScale: textScale)
                        .accessibilityIdentifier("detail-status")
                }
                VStack(alignment: .leading, spacing: 16) {
                    Text("In the box").font(.system(size: 18 * textScale, weight: .semibold))
                    ForEach(order.items) { item in
                        HStack(alignment: .firstTextBaseline, spacing: 12) {
                            Text("\(item.quantity)×").foregroundStyle(.secondary).monospacedDigit()
                            Text(item.id).fixedSize(horizontal: false, vertical: true)
                            Spacer(minLength: 4)
                            Text(price(item.quantity * item.unitPrice)).monospacedDigit()
                                .fixedSize()
                        }
                    }
                    Divider()
                    HStack {
                        Text("Total").fontWeight(.semibold)
                        Spacer()
                        Text(price(order.total)).fontWeight(.semibold).monospacedDigit()
                    }
                }
                if !order.note.isEmpty {
                    VStack(alignment: .leading, spacing: 8) {
                        Label("Packing note", systemImage: "shippingbox")
                            .fontWeight(.semibold)
                        Text(order.note).fixedSize(horizontal: false, vertical: true)
                    }
                    .padding(16)
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .background(.quaternary.opacity(0.5), in: .rect(cornerRadius: 12))
                }
                VStack(alignment: .leading, spacing: 12) {
                    Button(action: changeStatus) {
                        Label(order.action, systemImage: order.isReady ? "arrow.uturn.backward" : "checkmark")
                            .fixedSize(horizontal: false, vertical: true)
                            .padding(.vertical, 4)
                    }
                    .buttonStyle(.borderedProminent)
                    .controlSize(.large)
                    .accessibilityIdentifier("change-status")
                    Text(order.isReady ? "The order stays in the queue so the counter can find it."
                         : "Mark ready after every item is packed. You can change it back.")
                        .font(.system(size: 12 * textScale))
                        .foregroundStyle(.secondary)
                        .fixedSize(horizontal: false, vertical: true)
                }
            }
            .padding(28)
            .frame(maxWidth: 640, alignment: .leading)
            .frame(maxWidth: .infinity, alignment: .leading)
        }
        .navigationTitle("Order #\(order.id)")
        .textSelection(.enabled)
    }
}
