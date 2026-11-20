---
name: charter-web-apple-and-status-interfaces
description: Design a website, web app or native Apple interface, or fix misleading
  progress, outcomes and controls in a GUI or CLI. Covers editorial pages, working
  screens, accessible input, responsive layout, Apple windows and commands, and terminal-only
  status. Reporting a stuck operation is not recovering it.
metadata:
  content_version: charter-web-apple-and-status-interfaces@2026.11.20.0
---
# Charter · Web, Apple & Status Interfaces

Choose the medium from where the person acts. A beautifully typeset reading
page still needs browser history. Two Mac windows on the same manuscript
share its text, not its insertion point. A command that watches a print job
needs neither a window nor a browser. If the person might wait, cancel or
retry because of what the interface says, settle what the evidence supports
before composing that part of the view.

**In a browser**, read [web interface design](web-interface-design.md) before
choosing the composition or changing navigation, input or async state.
Arrange what the visitor came for: on a printmaker's portfolio the first view
might put an impression beside its inked block; on an edition comparison tool
dimensions, impressions and prices should align *across* works. A grid of
handsome cards can serve the first and destroy the second. Use the real work,
names and figures. Carry a chosen look through the type, scale and rhythm of
the layout; subject matter is not an icon above a generic headline. When the
look is open, compare materially different first views rendered with the
actual content. A local repair in a settled design needs no new direction.
For concrete constructions, the [working compositions](references/authored-compositions.md)
show what changes when a spread or table no longer fits the available width.
Compare [composition studies](references/composition-contrasts.md) when
choosing what should dominate; use [visual character](references/visual-character.md)
for type, palette, imagery and motion, and the [visual system](references/visual-system.md)
when repeated controls drift apart.

A link gives an object an address people can copy, revisit and open
elsewhere; a button acts. Put shareable state in the URL, not private inputs.
Keep a pending edit with the object it belongs to: if saving work A finishes
after the visitor has opened B, B has not been saved. Keep focus and the
return path through the change. Inspect a narrow layout with its real labels
and zoom, and follow a keyboard route through it: a screenshot can establish
the crop, not that Back restores the work. For history, drafts, dialog focus
or conflicting responses, open [browser interaction](references/web-interface-design-workflow.md).

**On an Apple platform**, read [native interface design](apple-interface-design.md)
before choosing the scene, container, command target or framework seam.
[Native structure](references/design-principles.md) maps the object relationships;
[platform adaptation](references/platform-adaptation.md) follows the input.
Independent documents can deserve windows; selection and its properties can
share a split view and inspector; a bounded choice can occupy a sheet.
Putting the reference under a sheet is wrong when the person must compare
against it throughout. Keep focus, selection and navigation local to their
scene even when the underlying records are shared. A menu command acts on
the active object, not the last one a background task touched. The
[order counter](references/order-counter.md) shows how to keep the selected
object and its actions when a wide pair of panes becomes a compact stack.
Use the [Mac companion](references/macos-companion.md) for work split between
a glance and a persistent window; the [assistant workbench](references/assistant-workbench.md)
for a conversation, its artifacts and work that outlives a turn.

Keep familiar system controls where people rely on their behavior. Spend
identity on what this app lets them see or handle: the letterform traced
under a Pencil, the [crate library's](references/crate-library.md) aligned beats
and keys. When the look is open, [native identity](references/native-identity.md)
and the [visual references](references/visual-reference.md) show where an
app can be its own; [native craft](references/native-craft.md) sets the type,
density and words. Use [symbols](references/icons-and-symbols.md) for optical
weight and meaning, [glass composition](references/liquid-glass-composition.md)
for grouping over live content and [custom controls](references/custom-control-patterns.md)
when an instrument needs its own behavior.
Adapt to the actual input, space and text size; when larger text pushes an
action out of a toolbar, give it a reachable home. Exercise that interaction,
including focus and its nonvisual names, on the relevant platform. A
Mac-looking page that runs in Safari still uses browser semantics.

Use the scene's framework: [SwiftUI](references/swiftui.md) for state and
scene composition, [UIKit](references/uikit.md) or [AppKit](references/appkit.md)
for the lifecycle or responder that owns a capability, and [visionOS](references/visionos.md)
for spatial input and placement. Before wiring speech or realtime capture to
a view, read [callback and teardown contracts](references/callback-and-realtime-contracts.md).
Confirm unfamiliar declarations against the [target SDK](references/official-sources.md).

**For status, including terminal output alone**, use [status design](status-interface-design.md)
before deriving the label, progress or offered action. Identify the job or
attempt, who recorded the state, when it was observed and what decision
depends on it. If a print monitor disconnects after confirming ten sheets
of a run, “10 sheets confirmed; current progress unavailable” neither
erases those sheets nor implies the press stopped. Give percentages a known
denominator; while work is still being discovered, say what was counted.
Keep a request to cancel distinct from cancellation, and show completion if
it won the race. The executor must recheck the actual prerequisites. A retry
whose earlier effect may exist is not an ordinary enabled action.

A terminal watcher may redraw a line on a TTY. In a pipe emit complete
records without animation or colour; a status report goes to stdout when
it is the requested data, incidental progress to stderr. Say whether the exit
code describes the query's success or the job's result. Stopping the watcher
does not cancel the job: leave its identifier and how to watch it again.
On screen, convey consequential transitions without stealing focus or relying
on colour; a screen reader needs the result, not a spoken update at every
poll. Open [state reasoning](references/status-interface-design-workflow.md)
when freshness, partial results or racing transitions can change which
control is safe. A single wrong label with a known derivation needs a fix
there, not a new dashboard.

If the operation itself lost its receipt and the job is to recover it,
`charter-workflow-recovery` establishes the surviving effect; design the
control from that finding rather than rerunning it to improve the display.
If scripts consume the command, take the state distinctions to
`charter-agent-tool-design` for its machine schema and exit contract. If
the composition needs new imagery, give `charter-3d-and-visual-production`
the crop, safe area and receiving sizes; judge the returned variants in the
interface. The player decision a game's cue must support belongs to
`charter-game-design`; focus in its pause menu belongs to the interface.
