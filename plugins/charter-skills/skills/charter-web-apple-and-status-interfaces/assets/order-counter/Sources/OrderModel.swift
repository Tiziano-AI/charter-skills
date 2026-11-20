// Adapted from Apple's Food Truck sample. See ../LICENSE.txt and README.md.
import Observation
import SwiftUI

/// The boxes the shop folds. Staff pick the box before anything else, so the
/// ticket groups its lines by box.
enum BoxSize: Int, Sendable {
    case single = 1, halfDozen = 6, dozen = 12

    var name: String {
        switch self {
        case .single: "Single"
        case .halfDozen: "Half-dozen"
        case .dozen: "Dozen"
        }
    }

    /// Slots seen from above: rows × columns.
    var grid: (rows: Int, columns: Int) {
        switch self {
        case .single: (1, 1)
        case .halfDozen: (2, 3)
        case .dozen: (3, 4)
        }
    }
}

struct TicketLine: Identifiable, Sendable {
    var id: String { flavor }
    let count: Int
    let flavor: String
}

struct Box: Identifiable, Sendable {
    let id: Int
    let size: BoxSize
    let lines: [TicketLine]
}

struct Order: Identifiable, Sendable {
    /// The number printed on the ticket and called aloud at the counter.
    let id: Int
    /// The cross-check when someone steps forward.
    let name: String
    let boxes: [Box]
    let note: String?
    /// Paid online before the order reached the counter.
    let paidCents: Int
    var isReady = false

    var count: Int { boxes.flatMap(\.lines).reduce(0) { $0 + $1.count } }
    var status: String { isReady ? "Ready" : "Preparing" }
    /// One verb for the button, the menu item and the Undo title.
    var statusCommand: String { isReady ? "Mark as Preparing" : "Mark as Ready" }
}

@MainActor @Observable
final class OrderStore {
    var orders: [Order] = SampleOrders.morningRush

    var preparing: [Order] { orders.filter { !$0.isReady } }
    var ready: [Order] { orders.filter(\.isReady) }

    func order(_ id: Int?) -> Order? { orders.first { $0.id == id } }

    /// Sets readiness and registers the reverse change. Undo and Redo keep
    /// the name of the command that made the change, as in Undo Mark as Ready.
    func setReady(_ ready: Bool, for id: Int, undoManager: UndoManager?, actionName: String? = nil) {
        guard let index = orders.firstIndex(where: { $0.id == id }), orders[index].isReady != ready else { return }
        let name = actionName ?? (ready ? "Mark as Ready" : "Mark as Preparing")
        orders[index].isReady = ready
        undoManager?.registerUndo(withTarget: self) { store in
            store.setReady(!ready, for: id, undoManager: undoManager, actionName: name)
        }
        undoManager?.setActionName(name)
    }
}

/// Selection and the compact path belong to one window, not to the store.
@MainActor @Observable
final class CounterNavigation {
    var selection: Int?
    var path: [Int] = []

    func select(_ id: Int?, compact: Bool) {
        selection = id
        if compact { path = id.map { [$0] } ?? [] }
    }

    func adapt(toCompact compact: Bool) {
        if compact, let selection { path = [selection] }
        if !compact { path = [] }
    }
}

/// The shop takes euros; the amount is written the way this Mac writes money.
func paid(_ cents: Int) -> String {
    (Double(cents) / 100).formatted(.currency(code: "EUR"))
}

/// Fictional orders. Nothing here is a real customer or a live order.
enum SampleOrders {
    static let morningRush: [Order] = [
        Order(id: 211, name: "Priya Raman", boxes: [
            Box(id: 1, size: .dozen, lines: [
                TicketLine(count: 4, flavor: "Glazed"),
                TicketLine(count: 4, flavor: "Chocolate Glazed"),
                TicketLine(count: 4, flavor: "Cinnamon Sugar")
            ])
        ], note: nil, paidCents: 1800, isReady: true),
        Order(id: 212, name: "Tom Okafor", boxes: [
            Box(id: 1, size: .single, lines: [TicketLine(count: 1, flavor: "Cruller")])
        ], note: nil, paidCents: 280, isReady: true),
        Order(id: 213, name: "Morgan Bell", boxes: [
            Box(id: 1, size: .halfDozen, lines: [
                TicketLine(count: 2, flavor: "Brown Butter"),
                TicketLine(count: 2, flavor: "Raspberry Glaze"),
                TicketLine(count: 2, flavor: "Cinnamon Sugar")
            ]),
            Box(id: 2, size: .single, lines: [TicketLine(count: 1, flavor: "Raspberry Glaze")])
        ], note: "Raspberry one in its own box, it's a gift", paidCents: 1380),
        Order(id: 214, name: "Alexandra Kowalczyk-Brennan", boxes: [
            Box(id: 1, size: .dozen, lines: [
                TicketLine(count: 6, flavor: "Glazed"),
                TicketLine(count: 6, flavor: "Rainbow Sprinkle")
            ]),
            Box(id: 2, size: .halfDozen, lines: [
                TicketLine(count: 3, flavor: "Old-Fashioned"),
                TicketLine(count: 3, flavor: "Maple Bar")
            ])
        ], note: "Keep the sprinkles away from the old-fashioneds", paidCents: 2760),
        Order(id: 215, name: "Sam Rivera", boxes: [
            Box(id: 1, size: .halfDozen, lines: [TicketLine(count: 6, flavor: "Glazed")])
        ], note: nil, paidCents: 960),
        Order(id: 216, name: "Zoë Lefèvre", boxes: [
            Box(id: 1, size: .single, lines: [TicketLine(count: 1, flavor: "Vegan Chocolate")])
        ], note: "Vegan, use the clean tongs", paidCents: 320),
        Order(id: 217, name: "Jun-seo Park", boxes: [
            Box(id: 1, size: .dozen, lines: [
                TicketLine(count: 3, flavor: "Brown Butter"),
                TicketLine(count: 3, flavor: "Raspberry Glaze"),
                TicketLine(count: 3, flavor: "Vanilla Bean"),
                TicketLine(count: 3, flavor: "Chocolate Glazed")
            ])
        ], note: nil, paidCents: 1920),
        Order(id: 218, name: "Ana Lucía Ortega", boxes: [
            Box(id: 1, size: .halfDozen, lines: [
                TicketLine(count: 2, flavor: "Maple Bar"),
                TicketLine(count: 2, flavor: "Cruller"),
                TicketLine(count: 2, flavor: "Glazed")
            ])
        ], note: nil, paidCents: 1020)
    ]
}
