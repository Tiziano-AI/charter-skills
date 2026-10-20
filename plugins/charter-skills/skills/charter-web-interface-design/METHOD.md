# Charter · Web Interface Design

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
code; `charter-visual-asset-production` says when they help and how to make
them. Take type, colour, imagery and composition from them, not layout
measurements or copy, and build the chosen one from real components and
content.

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
that inform without narrating every token or poll.

## Visual direction: make the subject and the work legible

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

Type gives the composition a voice and a readable structure. One family, or two
with distinct jobs, and a small scale of roles such as display, heading, body,
label and data carry the hierarchy the composition set. Roles differ through
size, weight and spacing together; five sizes a pixel apart read as noise rather
than hierarchy. A display face's contour, line endings and surrounding space
can set a page's identity, while the reading measure and data alignment need
their own quieter rules. Enlarging the title without changing those
relationships usually enlarges the same generic composition.

Colour, imagery and typography can generate the composition, not merely
decorate it. A photograph's crop can establish the focal point; an expressive
headline can set the rhythm. A neutral ground and a restrained accent are useful
when the work needs that restraint, not a universal aesthetic. Semantic colours
must retain their meaning. Studying the page in greys can expose weak grouping
or emphasis, but it is one diagnostic, not a required first design. Colour
cannot rescue unrelated regions competing at equal weight; removing colour
does not by itself produce hierarchy either. Motion can explain a transition
or direct attention; persistent movement also competes with the work.

Judge a direction by rendering it and looking at it, with real content at the
widths and states that matter. Look at what reads first, whether the density
suits the experience and how type, image and space express this particular
subject. A primary action should stand out when taking that action is the
purpose; a reading experience need not turn every passage into a conversion.
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
choices through a creative entrance, a dense comparison, a subject-led page and
a shared control family. Open the rendered pairs when the corresponding
relationship is at issue; each includes a changed condition under which the
other arrangement is preferable. They are examples to discriminate between,
not a house style or exercises to reproduce on every task.

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

## Judge the design and follow the interaction

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

Open [browser design and implementation](references/workflow.md) when the work
turns on history and push versus replace, form semantics, dialogs and focus
order, draft merging, uncertain writes and compensation, disabled versus hidden
controls, narrow-screen tables, or which rendered checks can expose the defect.

For browser games, `charter-game-design` supplies the specialist decisions
about mechanics and control feel. Browser semantics, focus, accessible input
and the surrounding interface remain here; a menu defect alone does not need
a gameplay redesign.
