# PDF Construction and Repair

A PDF preserves a page description, not the author's intent. Create or repair the canonical source,
produce the exact recipient PDF, and exercise the operations that matter to its use: render,
search, select, extract, annotate, fill, print, sign or archive. No single tool sees the whole
artifact, so combine the few that cover that use and keep their outputs tied to the exact bytes
being inspected.

## Know what kind of PDF it is

If the PDF exists, identify the exact bytes and where they came from: supplied artifact, export,
generated output, scan or converted copy. Then establish whether it is primarily:

- born-digital text and vector content;
- scanned page images;
- a hybrid of page images plus a text layer;
- interactive, annotated, signed or form-based;
- assembled from several sources.

Where print or crop behavior matters, read the page count and the MediaBox, CropBox, BleedBox,
TrimBox and rotation. Mixed sizes and orientations can be deliberate; unexpected variation often
signals a bad merge or export.

## Choose the construction path

Pick the owner of later changes from the document's future use:

- a native editable master when people must keep changing content, layout, formulas or review
  state;
- a structured document generator when repeatability, data binding or scale owns the output;
- a maintained PDF library used directly for bounded fixed-layout artifacts whose pagination,
  typography, links, forms and accessibility structure can be owned explicitly;
- scan assembly plus OCR when the source is physical or image-only, keeping the page image as the
  visual authority.

Direct PDF construction is not automatically simpler: hand-positioned generation must own font
metrics, line wrapping, pagination, table splitting, image scaling, links and accessibility
structure. Prefer the native authoring or generation pipeline when future change or complex flow
makes it the stronger owner.

Define the page geometry, typography, pagination, color, accessibility and interaction properties
the recipient needs before producing all pages. Build the shared structures first (page templates,
styles, repeated headers and footers, table and figure behavior, image placement, bookmarks and
links, tags and reading order, form fields, OCR settings) and carry one high-risk representative
page or spread through the destination before scaling.

When assembling scans or existing pages, normalize geometry, orientation, ordering, OCR language,
metadata and navigation without erasing meaningful source differences, and keep the canonical
inputs so the assembled file never becomes an accidental master.

Generate or modify into a new file, then reopen it. Incremental saves, encryption, signatures, forms
and object streams can make an apparently small rewrite consequential.

## Select pages by layout class and risk

For a page-appearance or print claim, inspect every distinct page class and every high-consequence
page. Typical candidates:

- cover, contents, first and last body pages;
- section starts and pages across a numbering transition;
- landscape, foldout, full-bleed or differently sized pages;
- dense tables, charts, equations, forms, footnotes and multi-column layouts;
- pages with repaired content, unusual fonts, transparency or large images;
- signature, legal, financial or instruction pages where small defects change meaning.

Inspect every page when variation makes sampling unreliable or the document is small enough that
selection saves little. Otherwise sample repeated classes and look directly at exceptions and
high-consequence pages. Page count alone does not set the coverage.

## Render and look

Rasterize selected pages with a mature renderer at a scale suited to the question. Poppler's
`pdftoppm` is a common choice:

```bash
pdftoppm -png -r 150 -f 1 -l 3 input.pdf renders/page
```

Moderate resolution serves page composition; small type, line art and print detail need more.
Keep page numbers in the output names. Look at full pages for composition, then at the affected
type, line art, images, tables and charts. Use a second renderer, or the recipient's viewer, when a
defect may be renderer-specific or that viewer is known to differ.

Run `pdffonts` before trusting line breaks. It lists each font with its type and whether it is
embedded (`emb`) and subset (`sub`). Subsets are normal when every used glyph is present; a
non-embedded font becomes consequential when another viewer, printer or later edit picks different
metrics or glyphs. A listed font can still lack a glyph, so look at symbols, currency signs,
diacritics and equations on the page.

What to look for:

- page count, order, size, orientation, crop, trim, bleed and rotation are intentional; blanks,
  duplicates, section starts and recto/verso behavior fall where expected;
- margins and live areas suit the screen or physical output; headers, footers, running titles and
  page numbers align and follow the right sequence;
- no clipping outside page or crop boxes; no changed line breaks, missing glyphs, tofu or
  substituted fonts; no text that overlaps, disappears or becomes an unresolved token;
- hyphenation, widows, orphans and page breaks keep the text easy to follow, and fine text stays
  legible at the intended size;
- table headers, cell boundaries, values, units and continuation across pages stay
  understandable; chart titles, axes, scales, legends and labels are readable and accurate;
- images have enough effective resolution, correct aspect ratio, intended crop, acceptable
  compression and clean alpha, without color shifts;
- transparency, masks, gradients, patterns and thin rules render without seams or disappearance;
- captions and in-text references point to the right visible object.

For print, embedded fonts, image resolution, color spaces, overprint, transparency and page boxes
must suit the print path. Whatever the destination, the file should open in the recipient's viewer
without repair warnings, and its size should be proportionate: optimization must not have destroyed
text, metadata, links, tags or image detail.

## Structure, navigation and accessibility

`pypdf` suits page structure, metadata, forms, outlines, merges and bounded transformations;
`pdfplumber` suits positioned text and table exploration; MuPDF and similar engines suit rendering,
text spans, images and object-level diagnostics. Structural presence does not prove correct
rendering: a font can be listed yet miss a glyph, and text can extract while columns read in the
wrong order.

Where use depends on them, check image pixel dimensions against placed size, internal destinations,
external links and their hit areas, bookmarks with a useful hierarchy, annotations, attachments,
layers, form field names, order, values and submit behavior, and signatures and permissions.

Tagged structure, document language, reading order, headings, lists, table headers, alternate text
and form labels need their own inspection; visual order does not make a PDF accessible. Decorative
content should stay out of the reading order, and meaningful content should not be marked
decorative. veraPDF formalizes the requirements of PDF/A-1 to PDF/A-4, PDF/UA-1, PDF/UA-2 and
WTPDF 1.0, but for PDF/UA it runs only the machine-verifiable checks. The Matterhorn Protocol's
human checkpoints, such as whether alt text is meaningful and the reading order is logical, still
need a person or a careful look, so a clean veraPDF report on PDF/UA is not a claim that the
document is accessible. Archived or signed variants must keep the conformance and immutability
their use requires; print preflight and signature validation have their own specialist validators.

## Extraction, tables and OCR

When search, extraction or machine reuse is part of use, extract the relevant text and tables and
compare a sample with the rendered page before scaling extraction to the whole document. Columns,
headers, footers, ligatures, equations, tables and hyphenation often carry the meaning that goes
wrong. Extraction can contain every word in an unusable order, duplicate a hidden OCR layer, or
omit visible text while the page looks right.

Keep page coordinates or cell relationships when order matters. Repeated headers, multi-line and
spanning cells, footnotes and aligned text without drawn borders defeat generic table extraction;
choose a tool or a custom region strategy from how the page was built rather than forcing every
page through one parser.

Use OCR when the text exists only as pixels or the existing text layer is unusable. Choose the
languages explicitly, deskew or rotate first, and pick segmentation for prose, columns, sparse
labels, forms or tables. OCR confidence is model-specific and can be high on a plausible but wrong
name, date or number: compare names, dates, amounts and identifiers with the page image, and keep
ambiguity visible instead of normalizing it away.

## Repair the source or the PDF mechanism

Regenerate from the editable source when the defect originates in layout, fonts, charts, tables,
links or structure. Repair the PDF directly for bounded page-box, rotation, metadata, merge,
annotation, form or object defects, or when the source is unavailable and regeneration would lose
more. Typical interventions:

- correct page size, margins, crop, bleed and export settings;
- embed or replace fonts and regenerate the affected text;
- replace low-resolution or wrongly transformed images;
- repair links, destinations, bookmarks, tags, reading order or form labels;
- split or repeat table headers and recut dense layouts at the source;
- rotate or deskew scans and rerun OCR with the right language;
- rebuild a corrupt merge from its ordered inputs.

After a repair, produce new bytes and repeat the rendering, structural, interaction, extraction or
accessibility observations on every affected page and on the neighbors whose pagination or object
flow may have moved.

## Order defects by consequence

Rank defects by what they do to the recipient: changed meaning, lost content, wrong value,
inaccessible path, blocked form or signature, print failure, navigation friction, cosmetic
variance. Repair in that order.
