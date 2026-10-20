# Charter · Document Fidelity

A document is structured meaning passing through transformations: authoring,
export, font substitution, calculation, import, save and print. Fidelity means
that the properties the recipient needs survive that path. A file that looks
right where it was made can still fail where it is used.

## When the format skill is enough

Most document requests are construction in one format: a report as DOCX, a
deck, a workbook, a PDF. An available format skill or document plugin (docx,
pptx, xlsx, pdf or their equivalents) owns that construction and its own
render check. Use it alone when the recipient opens the file in the application
the format targets, no template or existing file has to keep its structure, no
conversion, hosted import or save-back sits between you and the recipient, and
the render you can see uses the fonts the recipient has. The answer is then the
file, with one line on anything you could not confirm.

This package earns its place when something between the file and its use can
change it: a client template whose styles must survive, a DOCX judged through a
LibreOffice render while the recipient uses Word, a workbook headed for Google
Sheets, a PDF that must stay searchable or accessible, a deck that someone will
keep extending from its masters.

The skill does not bundle an office suite, fonts, authoring libraries, renderers
or format plugins. Use the capabilities actually available in the current
environment, whether a native application, format skill, connector or library.
`pdffonts`, `pdftoppm` and the reference tools below are options, not installed
prerequisites for every document job. An equivalent tool must observe the same
property; extracted text cannot replace a layout render. If that observation is
unavailable, keep the artifact and name the property still unconfirmed rather
than claiming fidelity or installing a tool without authority.

## First moves when fidelity is at stake

Name the recipient's application, the property that must survive (page
appearance, continued editing, calculation, search and extraction,
accessibility, print) and every transformation on the way: export, conversion,
hosted import, download, save-back. That chain decides the canonical master and
the derived copies. When editing and fixed layout both matter, an editable
master plus a PDF reading copy usually serves better than one compromised file
or two independently edited masters.

Your renderer is not the recipient's application. LibreOffice substitutes any
font it lacks, as a PDF viewer does for fonts the PDF does not embed, and a
substitute with different widths moves line breaks, table rows and page breaks.
Before judging pagination, overflow or a spill page, inspect the PDF's fonts
with `pdffonts` or an equivalent and compare them with the ones the document
names. Carlito is designed as a metric-compatible alternative to Calibri;
Liberation Sans, Serif and Mono target Arial, Times New Roman and Courier New.
That reduces reflow risk, but the actual font version, style and glyph fallback
still matter, and another suite's layout can differ even with matching metrics.
Do not rule out font substitution from the family name alone. An Aptos document,
for example, may render in an unrelated installed face when Aptos is absent.
Confirm consequential layout in the recipient's application, or leave slack
and name the pagination that remains unconfirmed.

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

In word processing, named styles carry repeated hierarchy, sections carry page
geometry, and lists, fields and references carry relationships. Direct
formatting can be the right exception; repeating the same manual nudge usually
signals a broken style, section or table rule.

In presentations, themes, masters and layouts make recurring structures
reproducible. Custom art direction can remain editable without forcing every
slide into identical placeholders. An editable chart needs its data
relationship, not separate vector shapes that resemble a chart.

In workbooks, inputs, formulas, references, tables and calculation settings
carry the analytical model. Formula text, cached values and recalculated
results are different layers. Missing, blank, zero and error mean different
things; locale, leading zeroes and date interpretation can silently corrupt
that meaning.

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

A second renderer helps when the recipient's viewer is known to differ or a
defect may be renderer-specific, not as a routine vote. Cover distinct and
consequential layouts rather than equating page count with inspection. After a
repair, inspect the affected units and the neighbors whose pagination,
references or calculations can change.

## Craft and delivery belong to the same artifact

Preserving bytes or objects is not enough. Typography, hierarchy, whitespace,
table rhythm, chart legibility and balance help the recipient read and use the
document. Repair lost meaning, wrong values, missing content and unusable
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
