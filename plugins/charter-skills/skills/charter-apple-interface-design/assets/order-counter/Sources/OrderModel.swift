// Adapted from Apple's Food Truck sample. See ../LICENSE.txt and README.md.
import Observation
import SwiftUI

struct OrderItem: Identifiable {
    let id: String
    let quantity: Int
    let unitPrice: Int
}

struct Order: Identifiable {
    let id: String
    let customer: String
    let items: [OrderItem]
    let note: String
    var isReady = false

    var total: Int { items.reduce(0) { $0 + $1.quantity * $1.unitPrice } }
    var itemCount: Int { items.reduce(0) { $0 + $1.quantity } }
    var status: String { isReady ? "Ready for pickup" : "Preparing" }
    var action: String { isReady ? "Return to preparing" : "Mark ready for pickup" }
}

@MainActor @Observable
final class OrderStore {
    var orders: [Order] = [
        Order(id: "104", customer: "Morgan Bell", items: [
            OrderItem(id: "Brown butter", quantity: 2, unitPrice: 450),
            OrderItem(id: "Raspberry glaze", quantity: 1, unitPrice: 475)
        ], note: "Pack the raspberry donut in a separate gift box."),
        Order(id: "105", customer: "Alex Chen", items: [
            OrderItem(id: "Vanilla bean", quantity: 4, unitPrice: 425)
        ], note: "One box, please."),
        Order(id: "106", customer: "Sam Rivera", items: [
            OrderItem(id: "Cinnamon sugar", quantity: 2, unitPrice: 400),
            OrderItem(id: "Brown butter", quantity: 2, unitPrice: 450)
        ], note: "", isReady: true),
        Order(id: "107", customer: "Taylor Brooks", items: [
            OrderItem(id: "Raspberry glaze", quantity: 3, unitPrice: 475)
        ], note: "Include napkins.")
    ]

    var readyCount: Int { orders.filter(\.isReady).count }

    func order(_ id: String?) -> Order? { orders.first { $0.id == id } }

    func toggleReady(_ id: String) {
        guard let index = orders.firstIndex(where: { $0.id == id }) else { return }
        orders[index].isReady.toggle()
    }
}

// Selection and the compact back path belong to this window, not the store.
@MainActor @Observable
final class CounterNavigation {
    var selection: String?
    var path: [String] = []

    func select(_ id: String, compact: Bool) {
        selection = id
        if compact { path = [id] }
    }

    func adapt(toCompact compact: Bool) {
        if compact, let selection { path = [selection] }
        if !compact { path = [] }
    }
}

func price(_ cents: Int) -> String {
    (Double(cents) / 100).formatted(.currency(code: "EUR").locale(Locale(identifier: "en_IE")))
}
