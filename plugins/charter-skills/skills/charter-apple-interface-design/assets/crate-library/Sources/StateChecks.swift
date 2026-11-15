import AppKit
import SwiftUI

// Off-screen state checks: the compatibility rules, the sample content and the
// undoable move, run against the same types the window uses. No window is
// shown, no event is posted and nothing is written.
@MainActor enum StateChecks {
    static func run() {
        var failures = 0
        func check(_ condition: Bool, _ message: String) {
            print((condition ? "PASS: " : "FAIL: ") + message)
            if !condition { failures += 1 }
        }
        let deck = CamelotKey("8A")
        func match(_ code: String?) -> KeyMatch { KeyMatch(deck: deck, track: code.map(CamelotKey.init), isDeckTrack: false) }
        check(match("8A") == .same, "8A beside 8A is the same key")
        check(match("9A") == .up && match("7A") == .down, "9A is one step up, 7A one step down")
        check(match("8B") == .relative, "8B is the relative key")
        check(KeyMatch(deck: CamelotKey("12A"), track: CamelotKey("1A"), isDeckTrack: false) == .up, "the wheel wraps from 12 to 1")
        check(match("3A") == .far && match("9B") == .far, "3A and 9B are far")
        check(match(nil) == .unknown, "a track with no key is unknown, not far")

        check(PitchMatch(deckBPM: 126, trackBPM: 124).percent == 1.6, "a 124 BPM track needs +1.6% under 126")
        let double = PitchMatch(deckBPM: 174, trackBPM: 87)
        check(double.ratio == 2 && double.percent == 0, "87 BPM sits under 174 at double time")
        let half = PitchMatch(deckBPM: 87, trackBPM: 172)
        check(half.ratio == 0.5 && half.percent == 1.2, "172 BPM sits under 87 at half time, +1.2%")

        let tracks = SampleTracks.all
        check(tracks.count == 60 && Set(tracks.map(\.id)).count == 60, "sixty tracks with distinct identifiers")
        check(tracks.map(\.bpm).min() == 86 && tracks.map(\.bpm).max() == 174, "tempos run from 86 to 174")
        check(tracks.filter { $0.key == nil }.count == 4, "four tracks have no key yet")
        func has(_ range: ClosedRange<UInt32>) -> Bool {
            tracks.contains { $0.title.unicodeScalars.contains { range.contains($0.value) } }
        }
        check(has(0x3040...0x30FF) && has(0x0600...0x06FF) && has(0x0400...0x04FF), "Japanese, Arabic and Cyrillic titles are present")
        check(Waveform(seed: 7, bpm: 120, seconds: 418).samples == tracks[6].waveform.samples, "a waveform is the same every time")

        let library = Library()
        let undo = UndoManager()
        undo.groupsByEvent = false
        undo.beginUndoGrouping()
        library.move([27, 28], to: .lateNight, undoManager: undo)
        undo.endUndoGrouping()
        check(library.track(27)?.crate == .lateNight && library.track(28)?.crate == .lateNight, "two tracks move together")
        check(undo.undoMenuItemTitle == "Undo Move to Late Night", "undo title is Undo Move to Late Night")
        undo.undo()
        check(library.track(27)?.crate == .peakTime && library.track(28)?.crate == .peakTime, "Undo puts both back")
        check(undo.redoMenuItemTitle == "Redo Move to Late Night", "redo keeps the command's name")
        undo.redo()
        check(library.track(28)?.crate == .lateNight, "Redo moves them again")
        let before = undo.undoMenuItemTitle
        // No group is opened here: a move that changes nothing must not register.
        library.move([28], to: .lateNight, undoManager: undo)
        check(undo.undoMenuItemTitle == before && library.track(28)?.crate == .lateNight, "a move to the same crate registers nothing")

        library.load(17)
        let rows = library.rows(in: .peakTime, matching: "").sorted(using: [SortField.match.comparator])
        check(rows.first?.id == 17 && rows.dropFirst().first?.match == .same, "sorted by Key Match, the deck's track leads, then the same key")
        check(library.rows(in: .lateNight, matching: "трамвай").map(\.id) == [31], "search finds a Cyrillic title")
        check(library.rows(in: .warmUp, matching: "трамвай").isEmpty, "search stays inside the crate")

        print(failures == 0 ? "PASS: all state checks" : "FAIL: \(failures) state checks")
        exit(failures == 0 ? 0 : 1)
    }
}
