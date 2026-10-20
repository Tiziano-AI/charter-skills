---
name: charter-functional-design
description: 'Design the substantive work of a new or incomplete product: turn inputs
  into usable findings, decisions or actions and assign each transformation. Not ordinary
  implementation of a clear function, market strategy or the journey through the product.'
metadata:
  content_version: charter-functional-design@2026.10.08.0
---
# Charter · Functional Design

A functional design explains how the product does the work its user came for.
It connects the information available at the start to the result someone can
use, including the interpretation, judgment and action between them. A system
can store documents, retrieve passages and expose an API while leaving the
assessment it promises entirely unspecified. In a new product, specify that
substantive work before the component list hardens; in an incomplete one,
locate the transformation its pieces still leave undone.

The useful design unit is a transformation with meaning: supplier evidence
becomes a finding against a criterion; a finding becomes a recommended action;
an authorized action becomes a changed business state. Screens, services and
model calls may implement these transformations, but naming them does not
explain the work.

When the function is already clear, as in an ordinary implementation, build it
directly; this design is for a promised result whose substantive work nobody
has specified yet.

## Work through a representative case

Use an actual or clearly illustrative input and work toward the promised
result. An example reveals omissions that component diagrams conceal: which
criterion applies, how conflicting sources affect a conclusion, what a missing
answer means, or who can authorize a change. The result should contain the
substance the real recipient needs, not just the shape of a response object.

Separate three kinds of incompleteness. **Missing information** needs retrieval,
acquisition or a useful question. **Missing transformation** needs a method for
interpreting or combining information already present. **Missing policy or
preference** needs the person or authority that owns that choice. Adding search
does not define judgment, and routing every judgment to a human can hide an
unimplemented product behind an approval button.

Read the output backward when a design looks complete but feels hollow. For a
recommendation to be usable, what findings support it? For each finding, which
evidence and criteria would produce it? Follow those dependencies until they
reach available inputs or an explicit acquisition function. A box labeled
"analyze" deserves decomposition when its internal work decides the product's
value; a mature calculation with a known contract may need none.

## Allocate functions by the work they require

Function allocation decides what a person, deterministic code, model, service
or existing workflow actually contributes. The distinction is consequential:

- Deterministic transformations fit explicit rules, exact arithmetic,
  normalization and mechanical validity. A model can propose a mapping without
  becoming the authority for arithmetic or a mandatory field rule.
- Model-mediated work fits interpretation, synthesis and candidate judgments
  where the inputs vary in language or structure. Specify the evidence it can
  use, the criterion it applies, the result it must produce and how ambiguity
  changes that result. "Call the model" leaves all four undefined.
- People supply preferences, authority, tacit expertise or genuinely necessary
  judgment. Design the information they receive and the effect of their answer;
  an unexplained review queue is merely a transfer of unfinished work.
- Existing systems may already own facts, decisions or actions. Reuse their
  function when its actual contract fits, rather than building a competing
  calculation or asking the user to repeat a decision already recorded there.

One component can perform several functions, and one function can span several
components. Keep the functional decomposition independent of deployment until
a real boundary changes it. Otherwise the current technology accidentally
defines what the product is allowed to do.

## Handoffs carry meaning, not only fields

A preparation product may extract and organize evidence while a consuming
product decides what it implies. Their handoff needs enough semantics for that
decision: the identity being discussed, scope, source location, applicable
version, uncertainty and the distinction between absent evidence and a negative
finding. Carry only the distinctions the receiver needs, but carry them intact.

The same principle applies to actions. A proposed amendment, an approved
amendment, a submitted amendment and a confirmed change are different functional
states. Define what advances the state and what the user can do when the result
is partial or unresolved. These are product functions when the user must recover
work; they need not become an elaborate workflow engine.

## Deliver complete input-to-result slices

A useful slice closes a meaningful input-to-result path for a stated use case.
It may use a narrow input family or a deliberate manual handoff, provided that
the resulting capability and remaining work are explicit. An ingestion-only
slice can be necessary infrastructure, but it is not an assessment slice.

Keep the whole promised capability in view when sequencing. A representative
case guides the first implementation; it does not silently replace the other
agreed use cases. Shared functions become clearer by comparing cases with
different inputs, judgments or actions. Cases that differ only in presentation
may share the same functional core; apparently similar cases may need different
criteria or authority.

Put the missing functional content into the design or implementation that owns
it. A worked input-to-result example and the decisive allocations often suffice;
a separate specification system is useful only when actual consumers need it.
[Worked cases and allocation](references/worked-cases-and-allocation.md) develops
evidence interpretation, human handoffs and slice boundaries.

## Neighboring jobs

Product strategy chooses the occasion and value worth serving. Product
experience designs how the person encounters and uses the capability. This
skill designs the substantive work that makes that experience possible.
Architecture simplification decides how much machinery the functions need;
cross-layer change design carries a settled behavior through source owners.
