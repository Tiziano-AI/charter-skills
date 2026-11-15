import AppKit
import SwiftUI

// The custom moment: the order drawn as the paper ticket on the shop's rail.
// The number is the one figure with a size of its own, because it is read and
// called from arm's length. Everything around the ticket is system.

struct TicketOnRail: View {
    let order: Order
    @Environment(\.contentTextScale) private var scale

    var body: some View {
        // The rail the ticket hangs from: a plain bar a little wider than the
        // ticket, not a picture of steel.
        TicketView(order: order)
            .frame(maxWidth: 440 * scale, alignment: .leading)
            .padding(.horizontal, 18)
            .overlay(alignment: .top) {
                Capsule()
                    .fill(Color(nsColor: .tertiaryLabelColor))
                    .frame(height: 5)
                    .offset(y: -2)
                    .accessibilityHidden(true)
            }
            .padding(.top, 22)
    }
}

struct TicketView: View {
    let order: Order
    @Environment(\.contentTextScale) private var scale

    var body: some View {
        VStack(alignment: .leading, spacing: 14) {
            header
            Perforation()
            contents
            if let note = order.note {
                Perforation()
                ScribbledNote(text: note)
            }
            Perforation()
            HStack(alignment: .firstTextBaseline) {
                Text("Paid online")
                Spacer(minLength: 12)
                Text(paid(order.paidCents)).monospacedDigit()
            }
            .textStyle(.callout)
            .foregroundStyle(.secondary)
            .accessibilityElement(children: .combine)
        }
        .padding(.horizontal, 22)
        .padding(.top, 14)
        .padding(.bottom, 26)
        .background(TicketShape().fill(Color.ticketPaper))
        .overlay(TicketShape().stroke(Color(nsColor: .separatorColor), lineWidth: 1))
        .textSelection(.enabled)
    }

    private var header: some View {
        VStack(alignment: .leading, spacing: 2) {
            // Number and state share a line when they fit; in a narrow window or
            // at the larger text size the state drops under the number rather
            // than either of them wrapping.
            ViewThatFits(in: .horizontal) {
                HStack(alignment: .firstTextBaseline) {
                    number
                    Spacer(minLength: 16)
                    status
                }
                VStack(alignment: .leading, spacing: 4) {
                    number
                    status.padding(.bottom, 8)
                }
            }
            Text(order.name)
                .textStyle(.title, weight: .semibold)
                .fixedSize(horizontal: false, vertical: true)
        }
    }

    /// The called number: a fixed size by intent, tabular so it never jitters.
    private var number: some View {
        Text(order.id, format: .number.grouping(.never))
            .font(.system(size: 92, weight: .bold).width(.condensed))
            .monospacedDigit()
            .lineLimit(1)
            .fixedSize()
            .accessibilityLabel("Order \(order.id)")
    }

    private var status: some View {
        StatusLabel(isReady: order.isReady)
            .textStyle(.title3, weight: .semibold)
            .lineLimit(1)
            .fixedSize()
    }

    // Quantities share one column across every box, as a printed ticket aligns them.
    private var contents: some View {
        Grid(alignment: .leadingFirstTextBaseline, horizontalSpacing: 14, verticalSpacing: 5) {
            ForEach(order.boxes) { box in
                GridRow {
                    BoxGlyph(size: box.size)
                        .gridColumnAlignment(.trailing)
                    Text(box.size.name)
                        .textStyle(.headline)
                        .foregroundStyle(.secondary)
                        .accessibilityLabel("\(box.size.name) box")
                }
                .padding(.top, box.id == order.boxes.first?.id ? 0 : 10)
                ForEach(box.lines) { line in
                    GridRow {
                        Text(line.count, format: .number)
                            .monospacedDigit()
                            .fontWeight(.semibold)
                        Text(line.flavor)
                            .fixedSize(horizontal: false, vertical: true)
                    }
                    .textStyle(.title3)
                    .accessibilityElement(children: .combine)
                }
            }
        }
    }
}

/// The note someone wrote on the ticket, set in a hand the way it was written.
struct ScribbledNote: View {
    let text: String
    @Environment(\.contentTextScale) private var scale

    var body: some View {
        // Noteworthy ships with macOS. Its small x-height needs a larger size
        // than the Title 3 it sits beside to read at the same distance.
        Text(text)
            .font(.custom("Noteworthy-Bold", size: Font.TextStyle.title3.macPointSize * 1.3 * scale,
                          relativeTo: .title3))
            .fixedSize(horizontal: false, vertical: true)
            .accessibilityLabel("Note: \(text)")
    }
}

/// A box seen from above, one ring per slot: the shape staff reach for first.
struct BoxGlyph: View {
    let size: BoxSize
    @Environment(\.contentTextScale) private var scale

    var body: some View {
        let ring = 5 * scale
        let gap = 1.5 * scale
        VStack(spacing: gap) {
            ForEach(0..<size.grid.rows, id: \.self) { _ in
                HStack(spacing: gap) {
                    ForEach(0..<size.grid.columns, id: \.self) { _ in
                        Circle().strokeBorder(lineWidth: 1.1 * scale).frame(width: ring, height: ring)
                    }
                }
            }
        }
        .padding(2 * scale)
        .overlay(RoundedRectangle(cornerRadius: 1.5 * scale).stroke(lineWidth: 1))
        .foregroundStyle(.secondary)
        .accessibilityHidden(true)
    }
}

struct StatusLabel: View {
    let isReady: Bool

    var body: some View {
        Label {
            Text(isReady ? "Ready" : "Preparing")
                .foregroundStyle(isReady ? .primary : .secondary)
        } icon: {
            StatusSymbol(isReady: isReady)
        }
    }
}

/// Ready is a filled check; Preparing is an open dotted ring. Green is completion,
/// never the accent, so the action color and the state never read as one thing.
struct StatusSymbol: View {
    let isReady: Bool

    var body: some View {
        if isReady {
            Image(systemName: "checkmark.circle.fill")
                .symbolRenderingMode(.palette)
                .foregroundStyle(.white, Color(nsColor: .systemGreen))
                .accessibilityLabel("Ready")
        } else {
            Image(systemName: "circle.dotted")
                .foregroundStyle(.secondary)
                .accessibilityLabel("Preparing")
        }
    }
}

struct Perforation: View {
    var body: some View {
        HorizontalLine()
            .stroke(Color(nsColor: .separatorColor), style: StrokeStyle(lineWidth: 1, dash: [3, 3]))
            .frame(height: 1)
            .accessibilityHidden(true)
    }
}

struct HorizontalLine: Shape {
    func path(in rect: CGRect) -> Path {
        Path { path in
            path.move(to: CGPoint(x: rect.minX, y: rect.midY))
            path.addLine(to: CGPoint(x: rect.maxX, y: rect.midY))
        }
    }
}

/// Square top where it hangs from the rail, torn edge at the bottom.
struct TicketShape: Shape {
    func path(in rect: CGRect) -> Path {
        let tooth: CGFloat = 8
        let depth: CGFloat = 4
        return Path { path in
            path.move(to: CGPoint(x: rect.minX, y: rect.minY))
            path.addLine(to: CGPoint(x: rect.maxX, y: rect.minY))
            path.addLine(to: CGPoint(x: rect.maxX, y: rect.maxY - depth))
            var x = rect.maxX
            var down = true
            while x > rect.minX {
                x = max(rect.minX, x - tooth / 2)
                path.addLine(to: CGPoint(x: x, y: down ? rect.maxY : rect.maxY - depth))
                down.toggle()
            }
            path.addLine(to: CGPoint(x: rect.minX, y: rect.minY))
            path.closeSubpath()
        }
    }
}

extension Color {
    /// The ticket's paper: the text background in light, one step above the
    /// window in dark, so it stays a sheet on the ground in both.
    static let ticketPaper = Color(nsColor: NSColor(name: "TicketPaper") { appearance in
        appearance.bestMatch(from: [.aqua, .darkAqua]) == .darkAqua
            ? NSColor.white.withAlphaComponent(0.08)
            : NSColor.textBackgroundColor
    })
}
