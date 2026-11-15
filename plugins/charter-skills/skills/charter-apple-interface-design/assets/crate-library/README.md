# Crate Library

A small, offline macOS SwiftUI app for a DJ preparing a set at home: choosing
the next record by tempo and key against the one that is playing.

It is used at home at a desk, at the keyboard, for hours before a set. The
next track mixes cleanly when its tempo is within a few percent of the deck's
and its key is the same, its relative or one step round the Camelot wheel.

Load the playing track to the deck with Return. Every row then shows the pitch
change it would need and how its key sits against the deck's. Sort by Key Match
and the tracks that mix come first. Every artist, title and remix credit is
invented, and there is no audio: a preview is a playhead moving over a
generated waveform.

## Build and open

Requires a Mac with Xcode (for `swift` and `actool`) and the macOS SDK. From
this directory:

```sh
./build-app.sh /tmp/charter-crate-library
open /tmp/charter-crate-library/CrateLibrary.app
```

The script builds the Swift package, assembles an unsigned `.app` in the
directory you give it, and compiles `Assets.xcassets` with `actool` into
`Contents/Resources/Assets.car`; `Info.plist` names the accent through
`NSAccentColorName`. It neither installs nor launches the app. The package has
no dependencies, network calls or storage; moves between crates last until the
app quits.

## What the library decides

- **Density is the identity.** One sortable, resizable `Table` with Mac-sized
  rows and alternating backgrounds to carry the eye across eight columns:
  Title, Artist, BPM, Pitch, Key, Key Match, Time and a waveform overview. No
  cards, artwork or dashboard.
- **The custom moment is compatibility with the deck.** A strip across the top
  holds the loaded track: its full title, its waveform with the cue point at
  the drop, and its tempo, key and length as readouts. Against it, Pitch gives
  the signed change a pitch fader would need, allowing half- and double-time,
  and Key Match says On Deck, Same, +1, -1, Relative, Far or No Key. Marks
  that mix are filled (half-filled for Relative) and in the primary style;
  Far is a hollow ring and No Key a dashed one, both tertiary. Shape and word
  carry the meaning, so the column reads the same without color and inside a
  selected row. Pitch dims as the change grows: primary up to 3 percent,
  secondary up to 8, tertiary beyond.
- **Type taken from the work.** Everything in the table is body size: tempo to
  one decimal and pitch in tabular figures, aligned on the right so they
  compare down the column; keys in Camelot notation with tabular digits; titles
  that lose their middle, because the mix name at the end ("Extended Mix",
  the remixer) is what tells two versions apart. Only the deck's readouts are
  large, in title size with a small legend under each, as a deck labels its
  display. Numbers follow the Mac's region.
- **One accent, from the deck.** The amber of a Cue button marks the
  selection and draws the cue point on the waveforms. Compatibility never uses
  it; neither does any other state. `AccentColor` has light, dark and High
  Contrast values, all deep enough to carry white text as a selection fill.
- **Figure and ground.** The table runs edge to edge with no single object to
  frame, and the deck is a band across its top that every row is read against.
- **Light first.** Preparation happens at a desk at home, often by daylight
  and for hours of reading, not in a dark booth, so the main renders are
  light. Dark is fully supported.
- **A quiet notice.** The window subtitle reads "Invented tracks, no audio".

## Keyboard path and commands

- Arrow keys move through the table as a table does.
- **Return**, a double-click or **Track → Load to Deck** (Command-L) loads the
  selected track.
- **Space** starts and stops a preview of the selection while the table has
  focus, also **Controls → Play Preview / Stop Preview**. Space is not a menu
  key equivalent, so a space typed in the search field stays a space. While a
  preview runs, moving the selection previews each track in turn from its
  drop.
- **Track → Eject Track** (Command-E) empties the deck.
- **Track → Move to Crate** (Option-Command-1 to 5) moves the selected tracks;
  **Edit → Undo Move to Late Night** puts them back.
- **View → Sort By** (Control-Option-Command-1 to 7) sorts as the column
  headers do; Pitch and Key Match need a loaded track.
- Crates are in the sidebar with their counts; search covers the current
  crate only and clears when the crate changes.

Each window keeps its own crate, selection and sort in scene storage for macOS
to restore with the window; a Pitch or Key Match sort is kept as Title,
because the deck is not restored. The library, the deck and the preview are
shared: there is one deck in the room and one pair of headphones.

## Follow the construction

- `Sources/Library.swift`: the shared `Library`, Camelot keys and key matching,
  pitch matching, the seeded waveform, the undoable move, and the table's
  `Row`, a track read against the deck.
- `Sources/SampleTracks.swift`: sixty invented tracks, among them Japanese,
  Arabic and Cyrillic titles, long remix credits and four tracks with no key
  yet, from 86 to 174 BPM.
- `Sources/LibraryView.swift`: the window state, sidebar, table, cells, deck
  strip and waveform.
- `Sources/CrateLibraryApp.swift`: the menu commands, per-window restoration
  and the entry point.
- `Sources/StateChecks.swift` and `Sources/LiveExercise.swift`: the exercises
  below.

## Exercises

```sh
/tmp/charter-crate-library/CrateLibrary.app/Contents/MacOS/CrateLibrary --exercise
```

`--exercise` checks the rules without a window: key matches round the wheel,
pitch with half- and double-time, the sample content, a two-track move with
its Undo and Redo titles, a no-op move that registers nothing, the Key Match
order, and search that finds a Cyrillic title and stays inside its crate.

```sh
open -n -W /tmp/charter-crate-library/CrateLibrary.app --args \
  -ApplePersistenceIgnoreState YES -AppleAccentColor 7 \
  --live-exercise /tmp/charter-crate-library/renders --appearance light
```

`--live-exercise` runs inside a normal launch, invokes the app's own menu items
(Track, Controls, View, Edit and File), draws each window into a bitmap from
inside the process, writes PNGs and a log, and quits; a watchdog quits it after
60 seconds. `--steps` chooses from `tempo`, `prepare`, `match`, `move`,
`inactive`, `narrow` and `single`, and `--prefix` names the files. Where a
step needs a click, a row selection or a column drag, it sets the state that
input produces and says so in the log. It sends no keystrokes or clicks and
raises no permission prompt. The log records whether the app was active and
the window key for each capture, and at launch the appearance, Increase
Contrast, the control accent and the `AccentColor` value the app resolved.

## Renders

All renders are 2x PNGs in sRGB, drawn by the running app from its own window
during `--live-exercise`, each step in its own short launch. The log records
the app active and the window key at every capture; the right half of the
active-and-inactive pair is the inactive window. Only
`library-as-configured.png` shows the Mac as it is set up. Every other render
ran with per-process overrides, `--appearance light` (`dark` for the dark
renders) and `-AppleAccentColor 7`, plus `-increaseContrast 1` for the
Increase Contrast pair, so it shows the app in a chosen state rather than this
Mac's window as configured.

| File | What it shows | How it was made |
| --- | --- | --- |
| `library-empty-deck.png` | Peak Time before anything is loaded | Peak Time chosen and track 17 selected in-process |
| `library-tempo.png` | Track 17 on the deck, sorted by BPM, track 14 previewing | Track → Load to Deck, View → Sort By → BPM, track 14 selected in-process as the Down Arrow would, Controls → Play Preview; captured two seconds into the preview |
| `library-key-match.png` | The same, sorted by Key Match | View → Sort By → Key Match |
| `library-narrow-title.png` | Late Night with its longest title on the deck and the Title column narrowed | Track 32 loaded by the menu; the Title column set to 150 points in-process, as dragging its edge would |
| `library-dark.png` | Dark appearance: track 17 on the deck, sorted by BPM, track 14 selected | `--appearance dark`; deck and sort set through the menus, the selection in-process |
| `library-increase-contrast.png`, `library-increase-contrast-dark.png` | Increase Contrast, light and dark, in the same state | `-increaseContrast 1` with each appearance |
| `library-active-and-inactive.png` | A second window (active, left) beside the first (inactive, right), both on track 14 | File → New Crate Library Window; crate and selection set in-process in the new window |
| `library-as-configured.png` | The Mac as it was set up: dark, with the person's Orange accent replacing the app's | No appearance, accent or contrast override |

The overrides apply to the app's process only: `--appearance light|dark` sets
the app's appearance; `-AppleAccentColor 7` made the system accent follow the
app's `AccentColor`, as Multicolor does; `-increaseContrast 1` turned on
Increase Contrast for the app; `-ApplePersistenceIgnoreState YES` skips
restoring earlier windows. Drawing a window into a bitmap renders sidebar and
bar materials as their flat fallbacks. The renders were made on a Mac whose
region writes a decimal comma.

The [walkthrough](../../references/crate-library.md) explains the decisions
and lists what the example does not show.

## Rights

Original to Charter and offered under the MIT terms in `LICENSE.txt`. Every
artist, title and remix credit is invented; the waveforms are generated from a
seed, not from audio. SF Symbols and the system fonts are drawn from macOS at
run time and are not bundled.
