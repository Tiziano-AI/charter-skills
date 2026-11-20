---
name: charter-document-fidelity
description: 'Make document properties survive export, import and editing in the recipient''s
  application: Word pagination, slide masters, spreadsheet formulas, PDF reading order
  or extraction. Routine single-format authoring uses its format tool.'
metadata:
  content_version: charter-document-fidelity@2026.11.20.0
---
# Charter · Document Fidelity

Start with how the recipient will use the file. Is it a DOCX read in Word,
a template whose styles must survive another edit, a workbook imported into
Google Sheets, a PDF searched by machine or a deck extended from its masters?
The answer determines which transformations and properties matter.

For routine construction in one format, use the available DOCX, PPTX, XLSX or
PDF authoring tool and its own render check. That suffices when the recipient
uses the target app, there is no template or existing structure to preserve,
no conversion, hosted import or save-back, and the render uses the recipient's
fonts. Return the file and name anything material you could not confirm.

When a transformation can change the result, choose an available native app,
library, format skill or connector that observes the property in question.
This skill bundles none of them: `pdffonts` and `pdftoppm` are options, not
prerequisites. Extracted text cannot substitute for layout. If no equivalent
observation is available, keep the artifact and name what remains unconfirmed;
do not claim fidelity or install tools without authority.

## First moves when fidelity is at stake

Name the recipient's application, the property that must survive (page
appearance, continued editing, calculation, search and extraction,
accessibility, print) and every transformation on the way: export, conversion,
hosted import, download, save-back. That chain decides the canonical master and
the derived copies. When editing and fixed layout both matter, an editable
master plus a PDF reading copy usually serves better than one compromised file
or two independently edited masters.

A renderer using different fonts or metrics can move a table onto a new page.
Before judging pagination, check the font actually used and compare it with
the named font. Read [destination and font differences](references/destinations-and-conversions.md#font-substitution-and-reflow)
when the render and recipient application differ; leave slack and name the
pagination still unconfirmed if the target cannot be inspected.

Set page size and locale before producing pages, because library defaults
belong to someone else: python-docx's default template uses US Letter, while
ReportLab ships with A4. Use the recipient's template or actual paper and locale
conventions for dates, decimals and currency, not their nationality as a proxy.
Correcting page size after the fact reflows every page.

Then build one difficult representative unit (the densest table, the longest
formula chain, the chart slide, the landscape exhibit) and carry it through the
actual chain before producing the rest. It shows whether the construction
survives before repetition multiplies the wrong structure.

## Encode the intent where future changes can find it

A file extension identifies a container, not a guarantee. A slide can be one
flattened image inside a presentation file; a PDF can show words it cannot
search; a spreadsheet can display correct cached numbers while its formulas are
broken. Hosted import is another transformation, not storage, and a re-export
is a new artifact.

For Word, slides and workbooks, keep structure that the next editor can
actually use: styles and fields, themes and editable chart data, formulas
and input types. A displayed number and a recalculated formula make different
promises. Read [editable documents](references/editable-documents.md) before
choosing structures that must survive import, editing or save-back.

PDFs preserve a page description. Geometry, font metrics, glyph mapping,
resources and export determine appearance; tags and text order carry separate
semantics. A scanned page adds OCR's language and segmentation uncertainty, and
a plausible recognized name or amount is not established by confidence alone.

## Diagnose the property, then repair its generator

A render answers layout questions: overflow, missing glyphs, crop, hierarchy,
table rhythm and page balance. Native object inspection answers structure
questions. Calculation answers value questions. Extraction answers search and
reading-order questions. Edit, save and reopen shows whether a recipient can
continue the work. None substitutes for the others.

Follow the fault to its owner. Fix a recurring table split at the layout
source; rotate a misoriented assembled page at its page operation; replace an
unsupported feature when the destination cannot preserve it. Shrinking
everything, flattening review objects, pasting formula values or rasterizing
text trades away capability and hides the cause.

For example, a font substitution changes metrics, which moves a table, which
creates a blank spill page. Deleting the blank page treats the last symptom;
correcting the font or the layout rule repairs the chain and may move
neighboring pages. Conversely, rebuilding an entire master to fix one page's
rotation introduces loss the defect never required.

For a repeated exporter defect, give `charter-test-design` the failing round
trip and the actual destination observation: for a formula, the result after
recalculation, not its cached display. A second renderer helps when the recipient's viewer is known to differ or a
defect may be renderer-specific, not as a routine vote. Cover distinct and
consequential layouts rather than equating page count with inspection. After a
repair, inspect the affected units and the neighbors whose pagination,
references or calculations can change.

## Craft and delivery belong to the same artifact

Preserving bytes or objects is not enough. Typography, hierarchy, whitespace,
table rhythm, chart legibility and balance help the recipient read and use the
document. If a revision must also change the message for its audience, use
`charter-adaptive-communication` for the wording without detaching conditions,
then check that wording in the final layout. Repair lost meaning, wrong
values, missing content and unusable
interaction first, then make the surviving structure look deliberate rather
than merely unbroken.

Linked charts, embedded files, review history, macros, signatures and metadata
change both what is shared and what survives conversion; treat them according
to the actual handoff. A repair to the master does not repair an older export
still waiting to be sent.

Return the recipient forms and the editable source. Name material conversion
losses and any property you could not observe where the recipient will use it,
such as Word pagination checked only through a substituted font.

## Depth by subproblem

- [Destinations and conversions](references/destinations-and-conversions.md):
  open when choosing between fixed and editable forms, crossing a hosted import,
  targeting print or projection, or handing off embedded and linked content.
- [PDF construction and repair](references/pdf-construction-and-repair.md):
  open when producing, inspecting or repairing a PDF: its type, page selection,
  rendering and fonts, structure and accessibility validation, extraction, OCR
  and direct repair.
- [Word, slides and workbooks](references/editable-documents.md): open when an
  editable file must keep styles, masters or formulas through editing, save and
  round trip: per-format structure and fault lines, inspection layers, and the
  edit/save/reopen and round-trip exercises.
