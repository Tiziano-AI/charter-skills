# Web Interface Design

A website gives its subject a form and its visitor a way through it. Start
from what the visitor should encounter, understand, feel or accomplish. A
landing page, portfolio or editorial page may earn its value through a clear
argument, distinctive work or a compelling reading experience. An application
may earn it through comparison, creation or changing an object. Many sites
combine these purposes; their presentation and working views need not share
one composition.

Let that purpose shape the content, visual direction and interaction together.
Browser navigation and semantics still matter on a presentational page; an
application also has to keep changing data, drafts and actions coherent. An
orderly page can fail to express its subject, just as a striking interface can
fail if Back loses the draft, a response saves the wrong object or a control
has no keyboard behavior.

Size the work to the request. A defect in one transition, such as a stale
search result or a draft lost on Back, is repaired at that seam, and the fix is
the answer. A new screen inside an established design system starts from its
components and observed visual relationships; shared token names alone do not
establish a coherent system. A new product, or an interface whose look fails
its subject, needs a deliberate visual direction. While that direction is
still open, a few generated first takes of the key screen in distinct
directions, shown to the person, can find it faster than building one in
code. When using `charter-3d-and-visual-production` for these takes, give it
the subject, real content, viewport and what the visitor comes to do.
Take type, colour, imagery and composition from them, not layout
measurements or copy, and build the chosen one from real components and
content.

Interface words do work. Labels name objects and actions in the visitor's
vocabulary: “Notifications” fits a person choosing which messages arrive,
“Webhook endpoint” a developer supplying a delivery URL. An action keeps one
name through its whole flow, so the button that says Publish is answered by
“Published”, not “Success”. Help, errors and empty states say what happened and
what the person can do next. Copy that advertises the interface's own
cleverness can displace that information. Expressive writing can still be the
subject of an editorial or presentational page; judge it by that page's
purpose, not by a universal ban on slogans.

A presentational page needs something particular to show or say: a piece of the
work, a detail of the product, a claim it can support. Lead with it: the work
itself, the object at full size, a live piece of the product, or a sentence
only this subject could say; a headline with a supporting line and two buttons
is one of those forms, right when the claim is the strongest thing the page
has. When the brief supplies none, the familiar run of benefit headings, round
numbers and praise fills the space, and the scaffolding ends up deciding the
message. Write from what is actually known about the subject and let the
sections follow from it. A page that invents testimonials, client names,
statistics or awards publishes them under the person's name: leave such places
out, or mark them unmistakably as placeholders for the person to replace.

## Give the work a place

Organize around what people need to find, compare, decide and change. The
backend resource tree is a useful input, not necessarily the navigation.

A URL makes a promise about location. Put durable places and useful shareable
query state there; keep sensitive input and transient disclosure out of history
and referrers. Drafts need a deliberate lifetime of their own. Reload, a new tab,
Back and return after interruption should restore the meaning of the place,
not merely remount a component.

HTML supplies working affordances. A link supports navigation, copying and
opening elsewhere; a button performs an action; a form carries named input and
submission; headings, lists and tables expose relationships. Native semantics
help sighted, keyboard, assistive-technology and automated users together.
A custom widget may be necessary, but its role attribute supplies none of its
focus or keyboard behavior.

## Keep each kind of state with its owner

Server truth, cached snapshots, drafts, selection and pending mutations are
different state. A draft is allowed to diverge from the server; refetching must
not silently erase it. A selection that spans hidden pages needs visible scope
before a bulk action. A background job needs somewhere to return to after the
starting page disappears.

Responses belong to a query, object and operation, not to whichever view happens
to be mounted. If an older search arrives last, it must not replace the newer
result. If object A saves after navigation to B, B must not acquire a false
"saved" label. Tag each request with the query, object and version it asked
for, and drop a response that no longer matches the current one. Aborting
obsolete fetches saves work; only that check keeps an old result off the screen.

Optimism trades earlier feedback for reconciliation responsibility. It suits
recoverable changes with likely success, such as a local preference. A payment
or publication often needs server confirmation before it is represented as
settled. Rollback must not overwrite unrelated later edits, and client abort
does not establish that a remote effect stopped.

Empty, filtered out, not loaded, denied, stale and failed invite different
actions. Preserve useful content while refreshing and correct input when a
submission fails. Place feedback near its action, with nonvisual announcements
that inform without narrating every token or poll. If the words on the page
will make someone wait, intervene or retry, use [status design](status-interface-design.md)
to trace the claim to its source before deciding its label and controls.

## Composition follows the work

Composition gives the page its priorities. What the person must see first,
what they compare side by side and how much must be on screen at once come from
the content and the task, and they set hierarchy, rhythm and density. A
comparison tool wants aligned columns, tabular figures and a tight rhythm; a
long read wants a comfortable measure and generous pacing; a media or canvas
tool puts the object at the centre and pushes chrome to the edges.

An orderly interface can still emphasize the wrong thing. Look at what occupies
the first view, receives the strongest emphasis and asks for attention. Does
that correspond to what the person came to do, or to the machinery that
implements it? A creative tool can lead with the idea and summarize its chosen
settings; a model-comparison laboratory needs the models, settings and results
together. A quieter surface is not inherently the better one.

## Take the direction from the subject

A visual direction is a decision about this subject, and its material lies in
the subject's own world: the things its people handle and look at (tools,
documents, packaging, signs, instruments, the place itself), the lettering and
colour already found there, the pace of the occasion, and above all the real
content. A tide table, a boxing poster, the sodium light over a night market
and the ticket rail of a restaurant kitchen each have proportions, lettering,
colour or pace of their own. Name several such particulars before choosing
anything; two or three of them, translated into scale, type, colour, image and
movement, can carry a whole page. Translate their structure and manner (the
ruled density of a railway timetable, the bluntness of a hand-painted market
price, a scoreboard that changes one figure at a time), not the subject's
emblem: a law practice gains nothing from a gavel. Drawing the subject's
best-known object beside the headline is the weakest translation; letting it
set the grid, the type or the colour is the strong one. A working tool has such
a world too (a rota, a mixing desk's channel strip, a lab's sample sheet), and
its character usually lives in how its own data is drawn, not in decoration.

When a brief names a product and a category but no world, settle that first:
who uses it, where, at what moment, and which words they use for what they do.
Say what you assumed. Where the person, a brand or an existing design system
has already set the look, that is the direction: keep it, including when it is
one of the familiar looks below, and spend the judgment on composition and
craft inside it.

Every designer and every model has a first answer that arrives whatever the
subject. It is usually competent, which is why it is hard to see. An element
is a default when it would have come out the same for an unrelated subject of
the same kind: picture that other page for a moment, and what the two share
that neither brief asked for was not chosen. Keep such an element where it is
also the best answer here, for a reason found in this subject; otherwise the
decision is still open. The commonest first answers at present are below, so
that they can be recognized; they shift with the model and the year, and
steering away from all of them only arrives at the next one.

- Whole looks: a warm cream ground with a high-contrast serif display and a
  terracotta, burgundy or forest-green accent; a near-black ground with one
  acid or neon accent and monospace labels; white or dark with a blue-to-violet
  gradient, glowing blurs and translucent cards; a broadsheet of hairline rules
  and small capitals; heavy condensed capitals set tight on a flat, saturated
  ground, the usual answer when a page is asked to be bold.
- The presentational page: a headline of two or three clipped sentences with
  the last one in italic or a second colour, a small label above it and two
  buttons below, filling one half of the first view while the other half holds
  a flat drawing of the subject's best-known object or a floating product
  card; then identical icon cards, a band of big numbers, a row of logos,
  quote cards and a closing call to action.
- The application screen: a rail of icons, four number tiles, and everything
  else in cards of one radius and one soft shadow, with status pills.
- Small habits: a tracked capital label above every heading; 01, 02, 03 on
  things that are not a sequence; strings joined by middle dots or slashes; a
  monospace face on small labels to look technical; an arrow after every link
  and button; emoji or stock icons standing in for images; every section
  fading and rising into view.

Each has its case: the page run suits a product whose visitors really need a
claim, its proof and a price; four tiles suit a console whose four numbers are
what people check first; one accent on near-black suits a tool used in a dark
room. Outside its case, a familiar answer arrived and was not chosen.

Structure is information, which is how to tell a habit from a use. Each device
makes a claim about its content: a card, that it is a self-contained object; a
number, that order, rank or identity matters; a small label above a heading,
that the heading needs a category; a rule, that a boundary falls here; an
arrow, that something lies that way, a destination or a section about to open;
a monospace face, that the string is read character by character. Use each
where its claim is true of the content, and the page's structure starts to
describe the subject instead of dressing it.

When the direction is open, state it before building, as decisions concrete
enough to be wrong: the ground and the few colours as values, each with its
job; the typefaces and their roles; the layout idea in one sentence; and the
one thing a visitor would describe afterwards. “Clean, modern and friendly” is
not yet a direction, because it fits every page. Put each decision to the
question above and replace the ones that fail. An open look is settled with the
person before anything expensive is built on it: show the different
compositions as generated takes or rendered first views.
Where they have left the choice to you, or nobody can be asked, commit to one
direction and say which and why in a line or two alongside the work.

Spend the identity where it counts. One element usually carries it at full
strength (a title set as an image, a drawing, a field of colour, the way the
data itself is drawn) and the rest supports it; strong gestures that compete by
accident cancel each other, and a page of ornament reads as none. This is a
relationship, not a quota. A long editorial page may need related moments at
the turns of its argument, and a subject that is loud by nature, a carnival or
a fanzine, can be loud throughout, provided one thing still leads. In a working
tool the strong element is the working object, and character there is
precision: aligned figures, exact states and the density the task needs. Needed
density is not a fault to relieve with white space.

## Type, colour, image and motion

Type gives the composition a voice and a readable structure. Choose the faces
for this subject, not the neutral grotesque or the fashionable display serif
that would have arrived anyway. A typeface carries a period, a tool and a use
(signage, timetables, schoolbooks, engraving, terminals), and the right one
often comes from the particulars already named. Try it in the page's real
strings, including its figures, its longest label and its accented or
non-Latin text, before committing. One family, or two with distinct jobs, and
a small scale of roles such as display, heading, body, label and data carry
the hierarchy the composition set. Roles differ through size, weight and
spacing together; five sizes a pixel apart read as noise rather than
hierarchy.

A display face's contour, line endings and surrounding space can set a page's
identity, while the reading measure (roughly 45 to 75 characters in Latin text,
with more leading as lines lengthen) and tabular, aligned figures for data need
their own quieter rules. Display type is composed, not poured: choose its line
breaks, tighten its tracking and leading as it grows, and give a word emphasis
only when that word carries the meaning. A familiar system face with excellent
figures can be the right choice for a working tool whose identity lives
elsewhere. Confirm in the render that the chosen fonts loaded, since a silent
fallback changes the whole page. Enlarging the title without changing these
relationships usually enlarges the same generic composition.

Colour, imagery and typography can generate the composition, not merely
decorate it. Take the palette from the subject's materials and give each
colour a job: the ground, the text, the colour that carries the identity, and
the working colours for action, selection and status, which keep their meaning
wherever they appear. A dark, saturated or loud ground is as legitimate as
paper when the subject is; a neutral ground and a restrained accent are useful
when the work needs that restraint, not a universal aesthetic. Studying the
page in greys can expose weak grouping or emphasis, but it is one diagnostic,
not a required first design. Colour cannot rescue unrelated regions competing
at equal weight; removing colour does not by itself produce hierarchy either.

Choose imagery by what it lets the visitor see: one revealing crop for a
story, consistent viewpoints for objects to be compared, an annotated detail
for an explanation, the real product view for a tool. A photograph's crop can
establish the focal point; an expressive headline can set the rhythm. When
there is no imagery, draw from the subject (a diagram, a section, a map, a
specimen), let type be the image, or leave a plainly marked place for the
person's own. For a commissioned asset give `charter-3d-and-visual-production`
the subject's role, responsive crops and the space overlaid controls or text
must retain; inspect the delivered variants in those views.
An emoji, a stock icon or an abstract gradient standing in for
the subject tells the visitor nothing about it.

Motion that answers an action (opening, moving, confirming) earns its place
when it shows what changed, and it has to be quick. Motion nobody asked for
competes with the work: give it a composed moment tied to the subject where the
page's purpose allows, not an entrance on every section, and let a frequently
repeated operation respond at once without replaying it. The page is complete
without motion; under a reduced-motion setting, movement gives way to an
instant change or a short fade.

Open [visual character in detail](references/visual-character.md) when setting
a new direction, repairing a look that reads as generic, or settling a type,
colour, imagery or motion question the work turns on, a local repair included.
It works several unlike subjects through from their particulars to type, colour
and layout, and carries the detail of choosing and setting type, building a
palette, sourcing imagery and timing motion.

## Judge the rendered result

Judge a direction by rendering it and looking at it, with real content at the
widths and states that matter. Look at what reads first, whether the density
suits the experience and how type, image and space express this particular
subject. A primary action should stand out when taking that action is the
purpose; a reading experience need not turn every passage into a conversion.

Where the direction was open, ask of the render what was asked of the plan: put
another subject's name and headline on it, and see whether the page would still
fit. What survives that swap without a reason in the task, or in a convention
visitors rely on, is still a default, and decoration nobody would miss can go.
The element meant to carry the identity should be what a newcomer describes
first, without displacing what the visitor came to understand or do. A screen
inside an established design is judged instead by how well it belongs to that
design.

When choosing a new composition, or addressing a complaint that its look or
arrangement fails, compare materially different rendered arrangements. Judge
their character as well as their functional hierarchy: two equally generic
arrangements do not settle a complaint about identity. A first-view study can
settle the choice without two complete implementations; changing only colours
does not test a different composition. Generated takes can narrow the
direction; rendered arrangements with real content then test it. A local
repair inside an established direction needs no such exercise.

Use a material visual weakness to choose the next construction change. If app
chrome dominates a page whose subject should lead, alter the composition
rather than just its theme. If type and imagery give unrelated signals,
rework their relationship rather than explaining why each was chosen. The
rendered result, not that explanation, has to carry the intended character.

Real content reveals the actual layout: a long name, a missing value, an
unusual image proportion, a large collection or a translated label. A tiny
placeholder dataset rewards the wrong design.

The [worked visual contrasts](references/composition-contrasts.md) teach these
choices through a creative entrance, a dense comparison, a subject-led page, a
shared control family and a familiar look set beside a direction taken from
the subject. Open the rendered pairs when the corresponding relationship is at
issue; each includes a changed condition under which the other arrangement is
preferable. They are examples to discriminate between, not a house style or
exercises to reproduce on every task.

For the construction itself, [two implemented compositions](references/authored-compositions.md)
pair inspectable HTML/CSS/JavaScript with visible results: an editorial page
whose type, drawing and reading rhythm form one direction, and a dense
comparison whose identity survives filtering, selection and narrow widths.
They show what can be adapted and what needs recomposition, with bundled
fonts and source rights. Use the relevant construction when it supplies
missing means; neither its palette nor its page structure is a default for
another product.

## Give repeated visual decisions an implementation owner

Tokens supply values; components combine them into geometry, emphasis and
behavior. A component family owns the relationships that make its controls
recognizable, including type metrics, padding, icon alignment, relevant states
and meaningful variants. Shared names alone do not preserve those relationships.

Screens arrange the components. When screens independently redefine the same
internal relationships, repair the common owner of an unexplained difference
rather than matching each screen with another local patch. Coherence is not
identical pixels: a compact status badge and an actionable button can align
through baseline, spacing and emphasis without having the same height.

Open [visual systems in implementation](references/visual-system.md) when
building a recurring control family, choosing its variants, or repairing drift
across screens, content and states. It explains how geometry combines, where
composition belongs and how legitimate differences become reusable decisions.

## Adapt where the job stops fitting

Adapt at the point where the job no longer fits, not just at familiar device
widths. A narrow table may need horizontal comparison, priority columns or a
detail view; choose according to the relationship users must inspect. Zoom,
text enlargement, sticky regions and software keyboards can change available
space as much as the viewport. Preserve content and focus rather than hiding
the difficult columns.

## Review the design and its interaction

When the request concerns how an interface looks or feels, composition and
visual character are substantive parts of the result, not optional polish.
A review brief carries the person's intended experience and complaint, rather
than treating the implementer's arrangement as settled. Inspect what the
artifact communicates before accepting the explanation of why it was arranged
that way.

Judge the design choice before using tests to preserve it. A test requiring a
selector to remain visible proves that the implementation retains the selector;
it does not establish that permanent visibility serves the product. Visual
inspection, interaction inspection and technical tests answer different
questions about the same result, not successive approvals that can substitute
for one another.

A screenshot reveals hierarchy, crop and visual balance. It does not reveal
focus loss, broken history, stale responses or dead-end controls. Inspect those
through the affected route with the content and input conditions that can
expose the defect. Custom dialogs, drag interactions and asynchronous updates
deserve attention to focus, names, values and announcements.

When interaction feels slow, locate the delay: network, computation,
main-thread work, hydration, rendering or media. Another spinner cannot repair
blocked input. Virtualization can solve collection scale while impairing
find-in-page and traversal; debouncing can reduce search churn while making an
action's delivery ambiguous. Optimize the actual cost and preserve the job.

Open [browser design and implementation](references/web-interface-design-workflow.md) when the work
turns on history and push versus replace, form semantics, dialogs and focus
order, draft merging, uncertain writes and compensation, disabled versus hidden
controls, narrow-screen tables, or which rendered checks can expose the defect.

For browser games, `charter-game-design` supplies the specialist decisions
about mechanics and control feel. Browser semantics, focus, accessible input
and the surrounding interface remain here; a menu defect alone does not need
a gameplay redesign.
