# Identity in a native app

Open this when the look of a new app or screen is open, when an app feels
interchangeable with others in its category, or when deciding how far a custom
view may depart from system components. Type, color, density and copy figures
are in [native craft](native-craft.md).

## Where identity lives

Start conventional navigation and actions (bars, menus, sheets, alerts, Back,
search, settings and standard controls) from system components, which carry
learned behavior across apps. Custom appearance is useful when it helps this
work and preserves recognizable meaning, sizing and placement. Inspect the
composition with its actual content and settings; using a system component
does not establish that the whole screen adapts correctly.

| Place | What carries identity | When it changes |
| --- | --- | --- |
| The app's own objects | Drawn in the form the field already uses: a tide curve, a seat map, a score, a stroke-order square | When the objects are plain records, a well-set list is the form, and identity moves to words, icon and one interaction |
| Its data, drawn well | A chart in the units, scales and reference marks the field reads, built with Swift Charts so it adapts and speaks to VoiceOver | A single figure the person acts on wants one large number, not a chart |
| Accent and state | An accent from the subject for actions, selection or attention; distinct semantic treatment for warning, destruction and completion. Brand color may also belong in content, where glass controls pick it up as content scrolls beneath them | On the Mac the person's accent replaces it unless they chose Multicolor; over photos or maps, monochrome bars read better |
| Type design and width | Design and width chosen for the role and script; tabular digits for comparable figures, a readable text face such as New York for prose, SF Mono for codes, condensed for dense columns, rounded for a soft subject, a distinctive face where its voice helps | Content may need a reading or script-specific face; small interface labels often benefit from the system font |
| Icon and symbols | The app icon identifies the product; symbols take a rendering mode and weight matched to the type; custom symbols keep the platform's metaphor, so Share still looks like Share | Use standard iconography when it already expresses the meaning |
| Words | A voice that stays and a tone that follows the moment, in the field's own vocabulary | An error or a destructive choice gets plainer than the voice |
| Feedback | A haptic, sound or symbol effect at the commit point the field cares about | Frequent feedback stays brief and non-disruptive; selection feedback can help a precise adjustment |
| One custom moment | The view or interaction that carries the identity at full strength | A creative tool may need several; a working tool may spend it on precision |

A launch screen bridges startup rather than explaining the product. A welcome
screen can introduce useful content or choices. Put a logo or custom treatment
where it supplies context, which a logo in the navigation bar or solid color
bars that letterbox the content rarely do; otherwise give that space to the
person's content and actions. Apple's
[Branding](https://developer.apple.com/design/human-interface-guidelines/branding)
guidance describes these distinctions.

## Finding the subject's world

Ask what the subject already has, before choosing anything:

- What do its people read or hold? Tables, tickets, charts, forms, diagrams,
  labels, instruments: their notation, grouping and sequence show what people
  already recognize; retain the parts that help this interaction rather than
  copying the physical format wholesale.
- What do they call things, in which units and which language or script?
- Where are they, and what are their hands and eyes doing: on a deck in
  spray, at a desk for eight hours, on a sofa three meters from a screen,
  between two other tasks?
- What does the real content look like at its worst: the longest name, the
  missing value, the exception, four hundred rows, right-to-left text?
- What is the one act they repeat, and what would make it feel exact?

The answers name the custom moment and most of the type, color and density
decisions.

## Worked translations

Each of these subjects pulls the same platform toward a different result.
None is a template; together they show that the source of the choices is the
subject.

**A tide planner for small-boat sailors, iPhone and Apple Watch.** Sailors
read tide tables (times and heights of high and low water) and tidal-stream
arrows with rates in knots. The custom moment is the day's tide curve with
high and low water labeled and now marked; dragging along it scrubs time, and
the stream arrow for that hour turns with it. Heights and times use monospaced
digits; the next high water is a title-sized figure readable in spray. The
accent can come from the magenta that nautical charts print their lights and
routes in. The watch shows
the next turn of the tide and nothing else. Ports, search and settings stay
system. It replaces the weather-app reflex: rounded cards on an ocean-blue
gradient with a wave symbol.

**A kanji handwriting trainer, iPad with Apple Pencil, in Japanese.** For a
lesson using cross-guided practice squares and numbered strokes, make that
square the writing surface. Show corrections to stroke order and endings (a
stop, a flick or a sweep) on the learner's actual strokes, drawn in a
teacher's red. Characters in the square use a textbook-style face, since that
is the form stroke order is taught from; the rest of the interface uses the
system font. The sidebar groups characters by school grade. On supported
Pencil and iPad hardware, hover can preview the next stroke; the lesson
remains usable without hover. It replaces flashcards in rounded cards with
confetti on a right answer.

**A DJ's track library, Mac.** DJs read track lists with tempo, musical key
and length, and waveforms with a beat grid. There is no ornamental moment: the
identity is precision. A `Table` with sortable, resizable columns shows tempo
in monospaced digits, key in the notation the DJ mixes by, and a compact
waveform column. Give titles room through column resizing and access to the
full title; a condensed face can help if it stays legible in the actual
scripts. Arrow keys keep their table behavior, a focused preview action can
use Space when it does not conflict with text entry, commands remain
discoverable in menus, independent crates can open side by side when
comparison requires it, and tracks drag into playlists. It replaces an
album-art grid of large cards with a gradient player bar.

**An Arabic poetry reader, iPhone and iPad, right to left.** For a collection
whose verses use paired half-lines, preserve that relationship across a shared
gap, with the verse number as an anchor and the meter named as the tradition
names it. Choose an Arabic reading face with clear vowel marks and adjust
leading to the actual text so marks do not collide. System navigation uses SF
Arabic and follows the locale, so Back points to the right; use reading-order
layout for the poem's interface and inspect mixed-direction text and custom
drawing. It replaces an English-first layout with a calligraphy hero image and
left-aligned text.

**A party quiz on Apple TV, with iPhones as buzzers.** Players read a
game-show board from the sofa. Play is the subject, so the board can be loud:
a display face, saturated team colors, a countdown with sound, a reveal with
real motion. Text starts at tvOS sizes (body 29 points) and focus moves
predictably for the host's remote. On the phones the buzzer is one enormous
target with a strong haptic. The focus behavior, the remote's Back and the
settings stay system. It replaces a quiet gray list of questions.

**The counter-case: a two-factor code app.** The system list, search and
sheets are the right form, and decoration would make it feel less
trustworthy. Character goes into the icon, the words and one exact
interaction: the code set in monospaced digits grouped for reading aloud, and
copying it confirmed by a symbol that changes to a checkmark and a light
haptic.

## Defaults and the move each displaces

These are likely unsteered moves, inferred from web habits carried into
SwiftUI rather than measured; they shift with the model and the tools. Each
can be a considered choice in the right work.

| Default | What it displaces | Where it is right |
| --- | --- | --- |
| A web page in a window: `ScrollView` of padded cards with shadows | `List`, `Form`, `Table`, split view: selection, swipe actions, edit mode, keyboard navigation, density | A feed of unlike, rich objects; an editorial layout |
| A home screen of stat tiles: big number, small label, symbol in a circle | The queue, document or canvas the person came to act on | Glanceable monitoring, such as a status board or a widget |
| Fixed point sizes and `.rounded` everywhere | Text styles with Dynamic Type; a design chosen per role | A figure whose size is its meaning; a soft or playful subject; watch complications, which use SF Compact Rounded |
| Hard-coded colors in one appearance | Semantic colors; an accent with dark and High Contrast variants | Color inside the content itself, such as a drawing, artwork, a game scene or a color-critical representation |
| Touch-sized rows, capsule buttons, one window and Settings as a tab on the Mac | Compact rows, regular controls, a full menu bar, a Settings window, several windows | A kiosk or other touch-operated work can justify larger controls; one bounded operation can suit one window. Use the platform's Settings convention independently of those choices |
| An all-caps label over every title and middle-dot meta lines | The navigation title, a subtitle, a real column or row structure | A label the field itself prints in capitals, such as a departure board's column heads; a short overline that distinguishes content kind; concise related metadata that does not need column-by-column comparison |
| Self-drawn chrome: a floating pill tab bar, a custom Back button, a "Good morning" hero header | The system tab bar, toolbar and navigation title | A game, a camera, an instrument, where the control is the subject; elsewhere, a useful subject-specific interaction or presentation that preserves familiar action and navigation behavior |
| Glass or a gradient wash over content; glass on glass | Quiet content with glass on the elevated controls above it | Floating controls that need separation, such as over photos, video or maps; a gradient encoding a continuous value or atmosphere integral to the content |
| A tint picked from the system list, or a purple gradient | An accent from the subject | Wherever color only means action, as in a utility whose subject has no color; the system accent then reads as plain "action" |
| Everything as a `Form` of rows and toggles | A representation of the content: a waveform, a map, a canvas | Preferences and bounded configuration |
| A symbol beside every heading; sparkles for anything automated | Text, and symbols only where recognition speeds use | Standard actions people already recognize |
| A spring on every change; staggered entrances on appear | Motion that answers an action | A rare milestone worth celebrating |
| Four perfect fixtures: short names, two states, every action succeeds | Real content: long names, empty, error and permission states | A bounded teaching sample that states which states it omits; a product still needs its own real content and failure cases |

## Committing to a direction and testing it

Write the direction as decisions someone could disagree with. For the tide
planner: the custom moment is the day's tide curve, scrubbed by drag, with the
stream arrow following; the accent is chart magenta, used for now, the
selected hour and the primary action; times and heights use `.title2` and
`.body` with `monospacedDigit()`, and the next high water gets `.largeTitle`;
the watch shows only the next turn; the verbs are Plan, Save Passage and
Share. A direction such as "clean, nautical, modern" decides nothing.

Test it from both sides, on the plan and again on the first running build:

- **Does the subject matter?** Substitute a sibling brief and see which
  content, hierarchy or interaction decisions should change. A tide planner
  beside a fishing log or a weather app may share system navigation but need
  different records and time relationships. Keep a shared form when those
  relationships really are the same.
- **Does it belong on the platform?** Try the relevant native interactions:
  commands and standard shortcuts on the Mac, such as Settings on
  Command-comma, Back and dismissal on iPhone, keyboard and pointer alongside
  touch on iPad. Compare density and window behavior, such as whether the
  window remembers its size, with the actual task. Add swipe actions,
  resizable sheets or independent windows when they help that task, not as
  evidence that the app is native.

Inspect the running result, not the code, in the conditions that can expose
this direction's mistakes, such as the light and dark renders, the largest
text size and the inactive Mac window. An established app keeps its
direction; a repair inspects the content and interaction it changes without
restarting this exercise.

## Building the custom moment so it stays native

A custom drawing and a custom control need different support. Preserve
behavior already supplied by a standard control; add what the custom
interaction requires, using APIs available in the selected SDK.

- **Placement.** Put subject-specific drawing in content, under system bars
  and toolbars. Keep navigation and action scope recognizable when a custom
  interaction reaches into a toolbar or control.
- **Keyboard and focus.** If the view is interactive, make its operations
  reachable by keyboard. Keep a standard table's or control's existing
  navigation. Use `focusable()` and `onKeyPress` for an interaction that needs
  its own focus and key handling, such as arrow keys stepping through the tide
  hours, without capturing keys belonging to surrounding controls or text
  editing.
- **VoiceOver.** Prefer a styled standard control when its semantics fit. For
  a custom interaction, expose its name, value and actions; an adjustable
  scrubber can use `accessibilityAdjustableAction`. Use
  `accessibilityRepresentation` when replacing the view's accessibility
  elements is appropriate, not as an automatic wrapper. Swift Charts supplies
  chart accessibility; inspect its labels and summary. A custom-rendered chart
  can provide an accurate `accessibilityChartDescriptor` for VoiceOver and
  audio graphs.
- **Text size.** Scale dimensions tied to text with `@ScaledMetric` where
  Dynamic Type is available. Let layout reflow at accessibility sizes
  (`dynamicTypeSize.isAccessibilitySize`); keep plot geometry and gesture
  range tied to their own meaning and available space. On the Mac, account for
  any text scale the app offers.
- **Appearance.** Check custom drawing with the actual backgrounds, supported
  appearances and contrast settings, including dark mode and Increase
  Contrast.
- **Motion.** Make direct manipulation track the input and preserve its
  meaning under Reduce Motion. A static view needs no motion merely because
  it is custom.
- **Direction.** Use leading and trailing for reading-order layout. Decide
  custom drawing and directional symbols by meaning, then inspect the
  supported RTL languages; preserve artwork and real-world direction where
  mirroring would change their meaning.

When a custom view needs more of this than its identity is worth, a system
component with a well-chosen type treatment is the better answer.
