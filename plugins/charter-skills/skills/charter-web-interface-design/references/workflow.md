# Browser design and implementation

## Navigation and history

Keep scope, location and selected object apparent when they change an action's
meaning. Separate navigation, view switching, filtering, selection and mutation
even when the controls look similar.

Component memory suits temporary disclosure or hover; the URL suits durable
locations and query state worth sharing or reloading. Decide explicitly which
state should survive back/forward, a new tab and a return after interruption.

Prefer a real link for navigation so open-in-new-tab, copy-link and ordinary
browser behavior work. A client router should preserve those semantics.
Choose push versus replacement history according to whether the user expects
to revisit the previous state, not merely what avoids an extra entry.

## Semantics and custom interaction

Use elements for their meaning: persistent labels for fields, descriptions for
help, associated errors for correction, headings for structure, tables for
row-column relationships and lists for collections. Placeholder text is not a
persistent field label.

Prefer native elements when they fit, and implement the applicable interaction
pattern when they do not: ARIA supplies no keyboard handling, focus management
or styling. The W3C
[ARIA practices introduction](https://www.w3.org/WAI/ARIA/apg/practices/read-me-first/)
explains this distinction and why examples still need browser and assistive-
technology testing.

For dialogs, choose modal versus nonmodal intentionally. Manage initial focus,
keyboard traversal, dismissal and a sensible destination afterward. That
destination may differ from the trigger if the trigger was removed or the
workflow advanced. Do not trap focus in content that is not modal.

Focus order must preserve meaning and operability; it need not mechanically
match pixel order when several logical orders work. Avoid CSS rearrangements
that make keyboard navigation jump between unrelated groups. See W3C's
[focus-order explanation](https://www.w3.org/WAI/WCAG22/Understanding/focus-order.html).

Provide alternatives to drag-only and gesture-only actions. Icon-only controls
need meaningful accessible names, and visible text when the action would
otherwise be guessed. Do not add a role that obscures useful native semantics.

## State ownership and concurrency

| State | Required design choice |
| --- | --- |
| Server data | Snapshot identity, freshness, invalidation and permission scope |
| Form draft | Dirty fields, validation, persistence and conflict behavior |
| Optimistic mutation | Operation identity, pending representation and reconciliation |
| Selection | Local versus cross-page scope, hidden selections and bulk-action meaning |
| Stream or background job | Durable identity, partial output, terminal result and return path |
| Route | Shareable meaning, history behavior and restoration |

Do not make a copied server object a second source of truth without a reason.
When a newer remote version arrives while a draft is open, decide how it is
compared or merged with the user's edits rather than which one silently wins.

Client abort stops the corresponding browser operation; it is not proof that a
server-side effect was canceled. The browser contract is described by
[AbortController.abort](https://developer.mozilla.org/en-US/docs/Web/API/AbortController/abort).
For uncertain writes, use the server's operation identity, idempotency or status
contract rather than blindly submitting again.

Keep pending distinct from confirmed. A rollback may need to compensate only
the fields changed by that attempt so that later edits survive. Payments,
publication and permissions often need stronger server confirmation than a
local preference toggle.

## The interaction around a transition

A background refresh need not blank a usable page. Keep correct form values
after validation or service failure. Show actionable field errors, and a
summary when the form's size makes locating them difficult. Do not rely on
color alone.

Disabled, hidden and unavailable have different meanings. Withhold irrelevant
actions; explain unavailable actions when the reason helps users proceed.
An inert control that looks enabled is a broken promise, not a harmless mockup.

Navigation or reload during background work requires a product decision: does
the work continue, where is its result, and how does the user find it again?
A spinner disappearing is not a terminal state.

## Visual structure and content

Rails express navigation; panels group independently manipulated units; badges
encode compact meaning. Decoration should not obscure that structure, and a
universal ban on a visual technique is no more a rationale than a generic house
style.

Preserve content hierarchy when text wraps or a value needs truncation. If
truncation is necessary, give the complete value an accessible route.

## Responsive and inclusive behavior

Reorder by task priority, not loyalty to desktop columns. For a table on a
narrow screen, choose explicitly between scrolling comparison, priority
columns, row detail or another representation; do not discard the relationship
people need to inspect.

Keep fixed or sticky regions from occluding content and focus. Account for
zoom, text enlargement, safe areas and software keyboards where applicable.
Pointer-dense controls and touch targets have different costs; support the
actual input context rather than adding empty space everywhere.

Exercise the affected keyboard path. Inspect accessible names, roles, values,
focus and announcements for custom or asynchronous interaction. Automated
accessibility checks find some defects, not complete usability or conformance,
and the browser and assistive-technology combination matters.

## Performance at the point of use

Preserve useful content during refetch, reserve media dimensions to avoid
layout shift, and defer work that is not yet needed. Virtualization complicates
focus, measurement, find-in-page and nonvisual traversal; use it for an actual
scale problem and keep access to the collection's meaning. Debounce
queries where appropriate; do not debounce a consequential action into
ambiguous delivery.

Measure the affected interaction with representative data. A fast initial page
can still have a slow first action, and a development preview's timing may not
represent a production build.

## Rendered checks

Inspect the real route and the transitions that changed. Choose the viewport,
input, content and failure cases that can expose a defect rather than a generic
matrix, and look for occlusion, layout shift, unexpected scroll regions,
clipped content, focus loss, stale state and broken history.
