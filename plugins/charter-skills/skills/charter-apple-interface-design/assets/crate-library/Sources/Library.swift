import Foundation
import Observation

/// Where a track lives. Every track is in exactly one crate; All Tracks is a view.
enum CrateID: String, CaseIterable, Identifiable, Sendable {
    case all, warmUp, peakTime, lateNight, breaks, toSort

    var id: Self { self }
    static let crates: [CrateID] = [.warmUp, .peakTime, .lateNight, .breaks, .toSort]

    var title: String {
        switch self {
        case .all: "All Tracks"
        case .warmUp: "Warm-Up"
        case .peakTime: "Peak Time"
        case .lateNight: "Late Night"
        case .breaks: "Breaks & Bass"
        case .toSort: "To Sort"
        }
    }

    var symbol: String {
        switch self {
        case .all: "music.note.list"
        case .toSort: "tray"
        default: "archivebox"
        }
    }
}

/// A key in the Camelot notation DJs read: 1–12 round the wheel, A minor, B major.
struct CamelotKey: Hashable, Sendable, CustomStringConvertible {
    let number: Int
    let isMajor: Bool

    init(_ code: String) {
        number = Int(code.dropLast())!
        isMajor = code.hasSuffix("B")
    }

    var description: String { "\(number)\(isMajor ? "B" : "A")" }
    /// 1A, 1B, 2A … so a key sort walks the wheel.
    var sortKey: Int { number * 2 + (isMajor ? 1 : 0) }
}

/// How a track's key sits against the deck's on the Camelot wheel.
enum KeyMatch: Sendable {
    case onDeck, same, up, down, relative, far, unknown, noDeck

    init(deck: CamelotKey?, track: CamelotKey?, isDeckTrack: Bool) {
        if isDeckTrack { self = .onDeck; return }
        guard let deck else { self = .noDeck; return }
        guard let track else { self = .unknown; return }
        let step = (track.number - deck.number + 12) % 12
        switch (step, track.isMajor == deck.isMajor) {
        case (0, true): self = .same
        case (1, true): self = .up
        case (11, true): self = .down
        case (0, false): self = .relative
        default: self = .far
        }
    }

    /// Mixes cleanly first, clashes last, unknown after that.
    var rank: Int {
        switch self {
        case .onDeck: 0
        case .same: 1
        case .up, .down, .relative: 2
        case .far: 3
        case .unknown: 4
        case .noDeck: 5
        }
    }

    var isCompatible: Bool { rank <= 2 }
}

/// The pitch-fader move that brings a track to the deck's tempo, allowing for
/// half- and double-time (a 87 BPM track sits under a 174 BPM one).
struct PitchMatch: Sendable {
    let ratio: Double
    let percent: Double

    init(deckBPM: Double, trackBPM: Double) {
        let options = [1.0, 2.0, 0.5].map { ratio in (ratio, (deckBPM / (trackBPM * ratio) - 1) * 100) }
        let best = options.min { abs($0.1) < abs($1.1) }!
        ratio = best.0
        percent = (best.1 * 10).rounded() / 10
    }

    /// Within a few percent a mix sounds natural; past a pitch fader's usual
    /// range it does not mix at all.
    var isClose: Bool { abs(percent) <= 3 }
    var isReachable: Bool { abs(percent) <= 8 }
}

/// The overview's shape, generated from a seeded function rather than audio:
/// an intro, a drop, a breakdown and an outro, each a whole number of phrases.
struct Waveform: Sendable {
    let samples: [Double]
    let drop: Double
    let breakdown: Double
    let outro: Double

    static let resolution = 360

    init(seed: Int, bpm: Double, seconds: Int) {
        var random = SeededRandom(seed: UInt64(seed) &* 0x9E37_79B9_7F4A_7C15)
        let length = Double(seconds)
        let phrase = 32 * 4 * 60 / bpm / length
        let drop = phrase * Double(random.next(in: 1...2))
        let breakdown = min(0.82, drop + phrase * Double(random.next(in: 2...3)))
        let breakdownEnd = min(0.9, breakdown + phrase * (random.next(in: 0...1) == 0 ? 0.5 : 1))
        let outro = max(breakdownEnd + 0.02, 1 - phrase)
        let floor = 0.28 + Double(random.next(in: 0...10)) / 100
        (self.drop, self.breakdown, self.outro) = (drop, breakdown, outro)
        samples = (0..<Waveform.resolution).map { index in
            let x = Double(index) / Double(Waveform.resolution - 1)
            let level: Double
            switch x {
            case ..<drop: level = floor + 0.2 * x / max(drop, 0.01)
            case ..<breakdown: level = 0.86
            case ..<breakdownEnd: level = floor - 0.06
            case ..<outro: level = 0.94
            default: level = floor + 0.18 * (1 - (x - outro) / max(1 - outro, 0.01))
            }
            let beat = index % 4 == 0 ? 0.06 : 0
            return min(1, max(0.06, level + beat + Double(random.next(in: -10...10)) / 100))
        }
    }

    /// For VoiceOver: where the sections fall, in the track's own time.
    func summary(seconds: Int) -> String {
        "Intro until \(clock(drop, seconds)), breakdown at \(clock(breakdown, seconds)), outro from \(clock(outro, seconds))"
    }
}

func clock(_ fraction: Double, _ seconds: Int) -> String {
    clock(Int((fraction * Double(seconds)).rounded()))
}

func clock(_ seconds: Int) -> String {
    String(format: "%d:%02d", seconds / 60, seconds % 60)
}

struct SeededRandom {
    private var state: UInt64
    init(seed: UInt64) { state = seed }
    mutating func next(in range: ClosedRange<Int>) -> Int {
        state &+= 0x9E37_79B9_7F4A_7C15
        var z = state
        z = (z ^ (z >> 30)) &* 0xBF58_476D_1CE4_E5B9
        z = (z ^ (z >> 27)) &* 0x94D0_49BB_1331_11EB
        z ^= z >> 31
        return range.lowerBound + Int(z % UInt64(range.count))
    }
}

struct Track: Identifiable, Sendable {
    let id: Int
    let title: String
    let artist: String
    let bpm: Double
    let key: CamelotKey?
    let seconds: Int
    var crate: CrateID
    let waveform: Waveform

    init(_ id: Int, _ title: String, _ artist: String, _ bpm: Double, _ key: String?, _ length: String, _ crate: CrateID) {
        let parts = length.split(separator: ":").compactMap { Int($0) }
        self.id = id
        self.title = title
        self.artist = artist
        self.bpm = bpm
        self.key = key.map(CamelotKey.init)
        seconds = parts[0] * 60 + parts[1]
        self.crate = crate
        waveform = Waveform(seed: id, bpm: bpm, seconds: seconds)
    }
}

/// One table row: a track read against whatever is on the deck.
struct Row: Identifiable, Sendable {
    let track: Track
    let pitch: PitchMatch?
    let match: KeyMatch

    var id: Int { track.id }
    var pitchSortKey: Double { pitch.map { abs($0.percent) } ?? .infinity }
    var keySortKey: Int { track.key?.sortKey ?? 999 }
    var matchSortKey: Double { Double(match.rank) * 1000 + min(pitchSortKey, 999) }
}

/// A preview has no audio: a playhead runs from the drop in real time.
struct Preview: Sendable {
    let trackID: Int
    let started: Date

    func position(in track: Track, at date: Date) -> Double {
        min(1, track.waveform.drop + date.timeIntervalSince(started) / Double(track.seconds))
    }
}

/// The library is the app's shared data. The deck and the preview are shared
/// too: there is one deck in the room and one pair of headphones.
@MainActor @Observable final class Library {
    var tracks: [Track] = SampleTracks.all
    private(set) var deckID: Int?
    private(set) var preview: Preview?

    var deck: Track? { track(deckID) }

    func track(_ id: Int?) -> Track? {
        guard let id else { return nil }
        return tracks.first { $0.id == id }
    }

    func count(in crate: CrateID) -> Int {
        crate == .all ? tracks.count : tracks.filter { $0.crate == crate }.count
    }

    func rows(in crate: CrateID, matching query: String) -> [Row] {
        let deck = deck
        return tracks
            .filter { crate == .all || $0.crate == crate }
            .filter { query.isEmpty || $0.title.localizedStandardContains(query) || $0.artist.localizedStandardContains(query) }
            .map { track in
                Row(track: track,
                    pitch: deck.map { PitchMatch(deckBPM: $0.bpm, trackBPM: track.bpm) },
                    match: KeyMatch(deck: deck?.key, track: track.key, isDeckTrack: track.id == deck?.id))
            }
    }

    func load(_ id: Int) {
        deckID = id
    }

    func eject() {
        deckID = nil
    }

    func startPreview(_ id: Int) {
        preview = Preview(trackID: id, started: .now)
    }

    func stopPreview() {
        preview = nil
    }

    /// Moving tracks is the one edit; Undo puts each back where it was.
    func move(_ ids: Set<Int>, to crate: CrateID, undoManager: UndoManager?) {
        let changes = Dictionary(uniqueKeysWithValues: ids.map { ($0, crate) })
        apply(changes, undoManager: undoManager, actionName: "Move to \(crate.title)")
    }

    private func apply(_ changes: [Int: CrateID], undoManager: UndoManager?, actionName: String) {
        var previous: [Int: CrateID] = [:]
        for (id, crate) in changes {
            guard let index = tracks.firstIndex(where: { $0.id == id }), tracks[index].crate != crate else { continue }
            previous[id] = tracks[index].crate
            tracks[index].crate = crate
        }
        guard !previous.isEmpty else { return }
        undoManager?.registerUndo(withTarget: self) { library in
            library.apply(previous, undoManager: undoManager, actionName: actionName)
        }
        undoManager?.setActionName(actionName)
    }
}
