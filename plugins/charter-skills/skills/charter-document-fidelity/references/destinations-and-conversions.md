# Destinations and Conversions

Choose the document path by the property that must survive. A file extension identifies a
container; it does not define what the recipient can do with the file.

## Fixed versus editable

PDF normally favors stable page appearance, distribution, printing and annotation. DOCX, ODT,
PPTX, ODP, XLSX and ODS normally favor continued editing through structured objects. Either class
can be misused: a PDF may hold inaccessible scanned pages, and an office file may be a single
flattened image with no useful editability.

When recipients need both stable reading and future editing, keep one declared editable master
and derive the fixed distribution copy from it. Two independently edited masters diverge.

## Local file versus hosted-native document

Google Docs, Slides and Sheets, and comparable hosted formats, are not remote storage for office
files. Import can reinterpret styles, masters, formulas, charts, comments, permissions and media.
Decide whether the imported native object or the local file becomes canonical, then inspect the
conversion boundary in each direction users will traverse. An upload receipt shows transfer, not
successful editing or rendering; a clean local preview says nothing about the imported object.

## Screen, print, projection and editing

The same document can need different treatment by destination:

- print depends on page boxes, bleed, margins, color handling, image resolution and physical size;
- screen reading depends on zoom, reflow expectations, links, bookmarks, search and reading order;
- projection depends on contrast, minimum type size, safe areas, aspect ratio and media playback;
- editing depends on native structures, available fonts, compatibility and save behavior.

Name the dominant destination before settling trade-offs such as page density, font embedding,
image compression, animation or spreadsheet scaling. Page size and number, date and currency
formats follow the recipient's locale rather than the generating library's defaults.

## Appearance versus machine access

Rendered appearance, text extraction, OCR and accessibility semantics are distinct layers:

- rendering reveals clipping, pagination, crop, glyph and composition defects;
- extraction reveals whether software can recover text and tables;
- OCR infers text from pixels and carries language, segmentation and confidence errors;
- tags, headings, labels, alt text and reading order support assistive navigation and reuse.

A page can succeed in one layer and fail in another, so inspect the layers the recipient's use
depends on.

## Construction versus content

Writing, data and visual specialists may own the content, the analysis or the art direction. The
format skill or plugin supplies construction mechanics. Fidelity work owns the choices that decide
whether the result survives its path: template, styles, sections, masters, workbook model, page
geometry, accessibility structure and export route.

When a defect originates in a template, style, master, workbook model or generator, repair that
canonical owner and regenerate the recipient artifact rather than patching a derivative. Bring in
another specialist only when an unresolved content or design decision changes the document.

## Compound packages and attachments

Documents may contain embedded spreadsheets, linked charts, fonts, media, macros, signatures,
annotations or external relationships. Decide whether each must remain live, become embedded or
be replaced with a safe static representation. Broken external relationships often stay invisible
until the artifact moves to another machine or account.

Provenance and active content are not incidental: a security or privacy policy may need its own
handling decision, and fidelity work identifies the feature and what removing or keeping it does
to the document.
