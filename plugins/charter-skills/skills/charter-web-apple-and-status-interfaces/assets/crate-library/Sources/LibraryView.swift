import AppKit
import SwiftUI

/// One window's place in the library: its crate, selection, sort and search.
/// Shared data lives in `Library`; this belongs to the window.
@MainActor @Observable final class WindowState {
    var crate: CrateID = .all
    var selection: Set<Int> = []
    var sortOrder: [KeyPathComparator<Row>] = [SortField.title.comparator]
    var query = ""
}

enum SortField: String, CaseIterable, Identifiable {
    case title, artist, bpm, pitch, key, match, time

    var id: Self { self }

    var title: String {
        switch self {
        case .title: "Title"
        case .artist: "Artist"
        case .bpm: "BPM"
        case .pitch: "Pitch"
        case .key: "Key"
        case .match: "Key Match"
        case .time: "Time"
        }
    }

    var comparator: KeyPathComparator<Row> {
        switch self {
        case .title: KeyPathComparator(\Row.track.title, comparator: .localizedStandard)
        case .artist: KeyPathComparator(\Row.track.artist, comparator: .localizedStandard)
        case .bpm: KeyPathComparator(\Row.track.bpm)
        case .pitch: KeyPathComparator(\Row.pitchSortKey)
        case .key: KeyPathComparator(\Row.keySortKey)
        case .match: KeyPathComparator(\Row.matchSortKey)
        case .time: KeyPathComparator(\Row.track.seconds)
        }
    }

    /// Pitch and Key Match mean nothing until a track is on the deck.
    var needsDeck: Bool { self == .pitch || self == .match }

    init?(_ comparator: KeyPathComparator<Row>?) {
        guard let comparator,
              let field = SortField.allCases.first(where: {
                  ($0.comparator.keyPath as AnyKeyPath) == (comparator.keyPath as AnyKeyPath)
              }) else { return nil }
        self = field
    }
}

/// What the menu bar can do in the focused window.
struct LibraryActions {
    let canLoad: Bool
    let load: () -> Void
    let canEject: Bool
    let eject: () -> Void
    let isPreviewing: Bool
    let canPreview: Bool
    let togglePreview: () -> Void
    let canMove: (CrateID) -> Bool
    let move: (CrateID) -> Void
    let sortField: SortField?
    let deckLoaded: Bool
    let sort: (SortField) -> Void
}

struct LibraryActionsKey: FocusedValueKey { typealias Value = LibraryActions }

extension FocusedValues {
    var libraryActions: LibraryActions? {
        get { self[LibraryActionsKey.self] }
        set { self[LibraryActionsKey.self] = newValue }
    }
}

struct LibraryWindow: View {
    @Bindable var library: Library
    @Bindable var state: WindowState
    @FocusState private var tableFocused: Bool
    @Environment(\.undoManager) private var undoManager

    var body: some View {
        let rows = library.rows(in: state.crate, matching: state.query).sorted(using: state.sortOrder)
        NavigationSplitView {
            CrateSidebar(library: library, crate: $state.crate)
                .navigationSplitViewColumnWidth(min: 170, ideal: 196, max: 260)
        } detail: {
            VStack(spacing: 0) {
                DeckStrip(deck: library.deck)
                Divider()
                TrackTable(rows: rows, state: state, preview: library.preview,
                           load: library.load, togglePreview: togglePreview, move: move,
                           focused: $tableFocused)
            }
        }
        .searchable(text: $state.query, placement: .toolbar, prompt: Text("Search \(state.crate.title)"))
        .navigationTitle(state.crate.title)
        .navigationSubtitle("Invented tracks, no audio")
        .focusedSceneValue(\.libraryActions, actions)
        .task { tableFocused = true }
        // Search belongs to the crate it was typed in.
        .onChange(of: state.crate) { _, _ in
            state.query = ""
            state.selection = []
        }
        // Once a preview is running, moving through the table previews each
        // track in turn, so the arrow keys audition a crate.
        .onChange(of: state.selection) { _, ids in
            guard library.preview != nil else { return }
            if ids.count == 1, let id = ids.first { library.startPreview(id) } else { library.stopPreview() }
        }
    }

    private var single: Int? { state.selection.count == 1 ? state.selection.first : nil }

    private var actions: LibraryActions {
        let single = single
        let selectedCrates = Set(state.selection.compactMap { library.track($0)?.crate })
        return LibraryActions(
            canLoad: single != nil && single != library.deck?.id,
            load: { if let single { library.load(single) } },
            canEject: library.deck != nil,
            eject: { library.eject() },
            isPreviewing: library.preview != nil,
            canPreview: library.preview != nil || single != nil,
            togglePreview: togglePreview,
            canMove: { crate in !selectedCrates.isEmpty && selectedCrates != [crate] },
            move: move,
            sortField: SortField(state.sortOrder.first),
            deckLoaded: library.deck != nil,
            sort: { field in state.sortOrder = [field.comparator] })
    }

    private func togglePreview() {
        if library.preview != nil {
            library.stopPreview()
        } else if let single {
            library.startPreview(single)
        }
    }

    private func move(_ crate: CrateID) {
        library.move(state.selection, to: crate, undoManager: undoManager)
        // A track that left this crate is no longer in the table to select.
        if state.crate != .all, crate != state.crate { state.selection = [] }
    }
}

struct CrateSidebar: View {
    let library: Library
    @Binding var crate: CrateID

    var body: some View {
        List(selection: Binding(get: { crate }, set: { if let value = $0 { crate = value } })) {
            Section("Library") { row(.all) }
            Section("Crates") { ForEach(CrateID.crates) { row($0) } }
        }
        .listStyle(.sidebar)
    }

    private func row(_ crate: CrateID) -> some View {
        Label(crate.title, systemImage: crate.symbol)
            .badge(library.count(in: crate))
            .tag(crate)
    }
}

// MARK: Table

struct TrackTable: View {
    let rows: [Row]
    @Bindable var state: WindowState
    let preview: Preview?
    let load: (Int) -> Void
    let togglePreview: () -> Void
    let move: (CrateID) -> Void
    var focused: FocusState<Bool>.Binding

    var body: some View {
        Table(rows, selection: $state.selection, sortOrder: $state.sortOrder) {
            TableColumn("Title", value: \.track.title) { TitleCell(track: $0.track) }
                .width(min: 90, ideal: 250)
            TableColumn("Artist", value: \.track.artist) { row in
                Text(row.track.artist).lineLimit(1).help(row.track.artist)
            }
            .width(min: 70, ideal: 150)
            TableColumn("BPM", value: \.track.bpm) { row in
                Text(row.track.bpm, format: .number.precision(.fractionLength(1))).monospacedDigit()
            }
            .width(min: 44, ideal: 52, max: 72)
            .alignment(.trailing)
            TableColumn("Pitch", value: \.pitchSortKey) { PitchCell(pitch: $0.pitch, onDeck: $0.match == .onDeck) }
                .width(min: 58, ideal: 72, max: 110)
                .alignment(.trailing)
            TableColumn("Key", value: \.keySortKey) { KeyCell(key: $0.track.key) }
                .width(min: 34, ideal: 40, max: 60)
                .alignment(.trailing)
            TableColumn("Key Match", value: \.matchSortKey) { MatchCell(match: $0.match) }
                .width(min: 70, ideal: 96, max: 140)
            TableColumn("Time", value: \.track.seconds) { row in
                Text(clock(row.track.seconds)).monospacedDigit()
            }
            .width(min: 40, ideal: 46, max: 64)
            .alignment(.trailing)
            TableColumn("Overview") { row in OverviewCell(track: row.track, preview: preview) }
                .width(min: 60, ideal: 120)
        }
        .tableStyle(.inset(alternatesRowBackgrounds: true))
        .contextMenu(forSelectionType: Int.self) { ids in
            if ids.count == 1, let id = ids.first {
                Button("Load to Deck") { load(id) }
            }
            Menu("Move to Crate") {
                ForEach(CrateID.crates) { crate in Button(crate.title) { move(crate) } }
            }
        } primaryAction: { ids in
            if ids.count == 1, let id = ids.first { load(id) }
        }
        .focused(focused)
        // Return and Space act on the table only while it has focus, so typing
        // in the search field never loads or previews anything.
        .onKeyPress(.return) {
            guard state.selection.count == 1, let id = state.selection.first else { return .ignored }
            load(id)
            return .handled
        }
        .onKeyPress(.space) {
            togglePreview()
            return .handled
        }
    }
}

/// Titles are long and the mix name comes last, so they lose their middle,
/// keeping both the name and "(Extended Mix)" in view. The full title is in
/// the tooltip, in the deck once loaded, and read in full by VoiceOver.
struct TitleCell: View {
    let track: Track

    var body: some View {
        Text(track.title)
            .lineLimit(1)
            .truncationMode(.middle)
            .help(track.title)
    }
}

struct PitchCell: View {
    let pitch: PitchMatch?
    let onDeck: Bool

    var body: some View {
        if let pitch, !onDeck {
            HStack(spacing: 4) {
                if pitch.ratio != 1 {
                    Text(pitch.ratio == 2 ? "2×" : "½×").foregroundStyle(.secondary)
                }
                Text(signed(pitch.percent))
                    .monospacedDigit()
                    .foregroundStyle(pitch.isClose ? .primary : pitch.isReachable ? .secondary : .tertiary)
            }
            .accessibilityElement(children: .ignore)
            .accessibilityLabel("Pitch")
            .accessibilityValue(spoken(pitch))
        }
    }

    /// Signed, one decimal, in the Mac's own number format.
    private func signed(_ percent: Double) -> String {
        (percent / 100).formatted(.percent.precision(.fractionLength(1)).sign(strategy: .always(includingZero: false)))
    }

    private func spoken(_ pitch: PitchMatch) -> String {
        let time = pitch.ratio == 2 ? ", at double time" : pitch.ratio == 0.5 ? ", at half time" : ""
        if pitch.percent == 0 { return "Same tempo" + time }
        let amount = (abs(pitch.percent) / 100).formatted(.percent.precision(.fractionLength(1)))
        return (pitch.percent > 0 ? "Speed up " : "Slow down ") + amount + time
    }
}

struct KeyCell: View {
    let key: CamelotKey?

    var body: some View {
        if let key {
            Text(key.description).monospacedDigit()
        } else {
            Text("—").foregroundStyle(.tertiary).accessibilityLabel("Not analysed")
        }
    }
}

/// Filled marks mix; hollow ones do not. The word says which, so the column
/// reads the same without color and inside a selected row.
struct MatchCell: View {
    let match: KeyMatch

    var body: some View {
        if let mark {
            HStack(spacing: 5) {
                Image(systemName: mark.symbol)
                Text(mark.word)
            }
            .foregroundStyle(match.isCompatible ? .primary : .tertiary)
            .accessibilityElement(children: .ignore)
            .accessibilityLabel("Key match")
            .accessibilityValue(mark.spoken)
        }
    }

    /// +1 and -1 in the same number format as the pitch beside them.
    private func step(_ value: Int) -> String {
        value.formatted(.number.sign(strategy: .always()))
    }

    private var mark: (symbol: String, word: String, spoken: String)? {
        switch match {
        case .onDeck: ("smallcircle.filled.circle", "On Deck", "This track is on the deck")
        case .same: ("circle.fill", "Same", "Same key as the deck")
        case .up: ("arrow.up.circle.fill", step(1), "One step up the wheel")
        case .down: ("arrow.down.circle.fill", step(-1), "One step down the wheel")
        case .relative: ("circle.lefthalf.filled", "Relative", "Relative major or minor")
        case .far: ("circle", "Far", "Clashes with the deck's key")
        case .unknown: ("circle.dashed", "No Key", "Key not analysed")
        case .noDeck: nil
        }
    }
}

struct OverviewCell: View {
    let track: Track
    let preview: Preview?

    var body: some View {
        if let preview, preview.trackID == track.id {
            TimelineView(.animation(minimumInterval: 1 / 30)) { context in
                WaveformView(track: track, playhead: preview.position(in: track, at: context.date))
            }
            .frame(height: 16)
        } else {
            WaveformView(track: track, playhead: nil)
                .frame(height: 16)
        }
    }
}

/// The seeded overview. Unplayed sound is secondary; during a preview the part
/// heard since the drop turns primary and a playhead marks the position.
struct WaveformView: View {
    let track: Track
    let playhead: Double?
    var showsCue = false

    var body: some View {
        Canvas { context, size in
            let samples = track.waveform.samples
            let mid = size.height / 2
            func shape(from start: Double, to end: Double) -> Path {
                let first = Int(start * Double(samples.count - 1))
                let last = max(first, Int(end * Double(samples.count - 1)))
                return Path { path in
                    let points = (first...last).map { index in
                        CGPoint(x: size.width * Double(index) / Double(samples.count - 1),
                                y: samples[index] * mid)
                    }
                    path.move(to: CGPoint(x: points[0].x, y: mid))
                    for point in points { path.addLine(to: CGPoint(x: point.x, y: mid - point.y)) }
                    for point in points.reversed() { path.addLine(to: CGPoint(x: point.x, y: mid + point.y)) }
                    path.closeSubpath()
                }
            }
            context.fill(shape(from: 0, to: 1), with: .style(showsCue ? AnyShapeStyle(.tertiary) : AnyShapeStyle(.secondary)))
            if let playhead {
                let drop = track.waveform.drop
                context.fill(shape(from: drop, to: max(drop, playhead)), with: .style(.primary))
                let x = size.width * playhead
                context.fill(Path(CGRect(x: x - 0.75, y: 0, width: 1.5, height: size.height)), with: .style(.primary))
            }
            if showsCue {
                // The cue point at the drop, in the cue button's color.
                let x = size.width * track.waveform.drop
                let marker = Path { path in
                    path.move(to: CGPoint(x: x - 5, y: size.height))
                    path.addLine(to: CGPoint(x: x + 5, y: size.height))
                    path.addLine(to: CGPoint(x: x, y: size.height - 7))
                    path.closeSubpath()
                }
                context.fill(Path(CGRect(x: x - 0.75, y: 0, width: 1.5, height: size.height)), with: .color(.accentColor))
                context.fill(marker, with: .color(.accentColor))
            }
        }
        .accessibilityElement()
        .accessibilityLabel("Waveform")
        .accessibilityValue(spoken)
    }

    private var spoken: String {
        let summary = track.waveform.summary(seconds: track.seconds)
        guard let playhead else { return summary }
        return "Previewing at \(clock(playhead, track.seconds)). " + summary
    }
}

// MARK: Deck

/// The track that is playing, which every row is read against. Its readouts
/// are the deck's display: tempo, key and length in large tabular figures.
struct DeckStrip: View {
    let deck: Track?

    var body: some View {
        Group {
            if let deck { loaded(deck) } else { empty }
        }
        .padding(.horizontal, 20)
        .padding(.top, 12)
        .padding(.bottom, 14)
        .frame(maxWidth: .infinity, minHeight: 104, alignment: .leading)
        .background(Color(nsColor: .windowBackgroundColor))
        .accessibilityElement(children: .contain)
        .accessibilityLabel("Deck")
    }

    private func loaded(_ track: Track) -> some View {
        VStack(alignment: .leading, spacing: 10) {
            HStack(alignment: .firstTextBaseline, spacing: 22) {
                VStack(alignment: .leading, spacing: 2) {
                    Text(track.title)
                        .font(.title3.weight(.semibold))
                        .fixedSize(horizontal: false, vertical: true)
                        .textSelection(.enabled)
                    Text(track.artist)
                        .foregroundStyle(.secondary)
                }
                Spacer(minLength: 12)
                Readout(value: Text(track.bpm, format: .number.precision(.fractionLength(1))), unit: "BPM")
                Readout(value: Text(track.key?.description ?? "—"), unit: "Key")
                Readout(value: Text(clock(track.seconds)), unit: "Time")
            }
            WaveformView(track: track, playhead: nil, showsCue: true)
                .frame(height: 36)
        }
    }

    private var empty: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text("No Track on the Deck")
                .font(.title3.weight(.semibold))
                .foregroundStyle(.secondary)
            Text("Select the track that is playing and press Return to load it. Every row then shows how it would mix with it.")
                .foregroundStyle(.secondary)
                .fixedSize(horizontal: false, vertical: true)
        }
    }
}

struct Readout: View {
    let value: Text
    let unit: String

    var body: some View {
        VStack(alignment: .trailing, spacing: 0) {
            value
                .font(.title2.weight(.medium))
                .monospacedDigit()
            Text(unit)
                .font(.caption)
                .foregroundStyle(.secondary)
        }
        .fixedSize()
        .accessibilityElement(children: .combine)
    }
}
