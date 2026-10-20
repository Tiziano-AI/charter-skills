# Word, Slides and Workbooks

Editable formats carry several independent fidelity layers. Rendering settles layout, edit/save/
reopen settles practical editability, and a round trip settles a conversion boundary the recipient
actually crosses. Choose the layers from how the recipient will use the file.

## Resolve the destination and the canonical master

Identify the file the recipient will open and the application that will open it. A `.docx` edited
in Word, imported into Google Docs, previewed in Finder and exported back to `.docx` has four
different behavior surfaces. If the artifact does not exist yet, choose the native or generated
format that best preserves the required structures and declare it the canonical master; note the
format version and every conversion or import between source and destination.

Decide which properties matter, and leave the rest alone even when the format supports them:

- continued editing and style reuse;
- stable visual layout or pagination;
- formulas, chart ranges, validation or recalculation;
- review features such as comments and tracked changes;
- accessibility and reading order;
- printing, projection or distribution as a fixed derivative;
- extraction or automation against document structure.

When fixed layout and editability conflict, keep the editable source and produce a
destination-safe fixed derivative rather than flattening the only master.

Keep the objects apart when more than one exists: authoring source, generated editable file,
converted or imported copy, downloaded or re-exported copy, fixed PDF or image derivative, and the
copy the recipient opens. Paths, stable names, hashes or application identifiers prevent repairing
one file while delivering another.

## Inspection layers

| Layer | What it can reveal | What it cannot establish alone |
| --- | --- | --- |
| Package structure | Styles, relationships, formulas, masters, media, comments, metadata | Actual layout in the destination renderer |
| Native object model | Destination-recognized editable objects and warnings | Appearance after export, print or another suite |
| Render or preview | Pagination, crop, clipping, glyphs, hierarchy, chart readability | Whether objects, formulas and styles remain editable |
| Edit/save/reopen | Practical editability and persistence | Compatibility with an application not exercised |
| Import/export round trip | Conversion losses and format substitutions | Behavior on paths not traversed |
| Text or table extraction | Searchability and semantic presence | Visual order, layout and structural editability |

When repairing an existing file, inspect the package or object model at the structures that carry
the required meaning rather than inventorying every feature or reading only extracted text.

## Word-processing documents

Establish page geometry, named styles, heading hierarchy, lists, sections and navigation before
laying out the body. The structures that carry meaning are paragraph and character styles; heading
hierarchy, lists, fields, cross-references, footnotes and citations; sections with their page size,
margins, columns, headers, footers and numbering; tables, anchored or floating media, captions and
wrapping; comments, tracked changes, content controls and embedded objects; language, fonts, alt
text and document properties.

Judge styles by stable name and use, not by how many exist. Direct formatting can be a deliberate
exception; widespread direct formatting makes every future edit fragile. A sound document has:

- headings that drive navigation, lists that continue correctly, fields that update and
  references that resolve;
- styles that produce repeatable formatting without a parallel system of exceptions;
- sections that own their page size, margins, columns, headers, footers and numbering;
- tables that repeat headers where useful, fit their page and hide no cell content;
- floating and anchored media attached to the intended passage, with useful alt text;
- tracked changes, comments, content controls and hidden text matching the recipient's review
  needs;
- search, navigation, copy and paste, and printing that remain usable.

Floating media, tables near page boundaries, footnotes, tracked changes and mixed page orientations
are frequent conversion fault lines and deserve explicit render and edit exercises.

## Presentations

Establish slide size, theme, masters, layouts, placeholders and recurring hierarchy before building
individual slides. The structures that carry meaning are masters, layouts, theme fonts, theme
colors and placeholders; editable text, shapes, charts, diagrams, tables and groups; crops,
transparency, media relationships and fallback images; builds, transitions, speaker notes, comments
and hidden slides; slide size, safe margins and projection contrast.

Separate master and layout structure from copied shapes that merely look alike. Repeated hierarchy
belongs in layouts and themes, while one-off art direction can still use custom objects. A sound
deck has:

- a new slide from the intended layout that needs no manual rebuilding;
- text, charts, tables, diagrams and shapes that stay editable where editing matters;
- coherent titles, body hierarchy, spacing and rhythm across slide classes;
- no object unintentionally cropped, hidden, stretched, off-canvas or too small for projection;
- chart axes, legends, labels, units and data sources that communicate without the presenter;
- builds, transitions, media, links, notes, comments and hidden slides that behave as intended in
  the presentation application.

Charts, grouped objects, masks, media, animations, notes and hidden slides often survive preview and
fail on import or in presentation mode; exercise the features the presenter will use.

## Workbooks

Separate inputs, model, references and outputs, and establish tables, formulas, named ranges,
validations, number formats and chart ownership before filling presentation sheets. The structures
that carry meaning are formulas, array behavior, named ranges, tables, pivots, connections and
calculation mode; chart sources, series labels, number formats, dates, currencies and locale; data
validation, conditional formatting, filters, freeze panes and protection; hidden rows, columns and
sheets, external links, macros and refresh dependencies; print areas, page breaks and scaling.

Read formula text as well as displayed values, because cached values can make a broken workbook
look right until recalculation. Follow precedents and dependents around repaired cells, check
relative references after inserting rows or columns, and keep blanks, empty strings, zeroes,
errors and missing data distinct. A sound workbook has:

- derived values that remain formulas when recalculation is part of use;
- formula ranges, structured references, named ranges, pivots, connections and chart sources that
  cover the intended data and refresh as expected;
- dates, currencies, percentages, identifiers, leading zeroes and locale-sensitive values that
  keep their meaning;
- inputs, outputs, protected regions, validations and error states that are visibly distinct;
- conditional formatting, filters, sorting, freeze panes, hidden regions and print areas that
  survive the recipient's path;
- sheets readable at realistic zoom and print scaling, without clipped rows, columns, charts or
  repeated headings.

For CSV or TSV inputs, settle encoding, delimiter, quoting, decimal and date locale, leading zeroes
and identifiers before office software guesses their types.

## Render when layout or appearance matters

Render or preview every distinct layout class and every high-risk unit; sample repeated low-risk
units. Look for what structural inspection cannot reveal:

- font substitution, missing glyphs and changed line breaks;
- clipping, overlap, orphaned headings, blank spill pages or table splits;
- low-contrast text, unreadable chart labels, stretched media or changed crops;
- placeholders, field codes, error values, stale calculations or hidden content becoming visible;
- footer, page-number, master or theme drift.

Use realistic long values, alternate locales or dense data where they can change the behavior you
are about to rely on.

## Edit, save and reopen when editing continues

When the recipient must keep editing, make a small representative edit in a working copy, never
the only original, then save, reopen and observe. Touch the structure at risk: apply a heading
style, add a list item, resize a table, edit a chart source, change a formula input, add a slide
from the intended layout, resolve a comment or update a field. Then check whether:

- the intended style or master is still available;
- neighboring layout reflows sensibly;
- formulas and charts update from their real sources;
- comments, notes, tracked changes and object relationships survive;
- accessibility properties stay attached to the right object;
- saving changed metadata, compatibility mode or unsupported features, or raised corruption or
  compatibility warnings on reopening.

## Follow the round trip the recipient will traverse

When import, conversion or cross-suite editing is part of use, follow that exact path:

1. preserve the source artifact;
2. import or open it in the destination application;
3. read warnings, substitutions and changed features;
4. edit one representative structure;
5. save or export in the format the recipient will keep;
6. reopen the result and render the affected units;
7. compare structure, values and appearance with the source intent.

Common losses are theme remapping, floating-object movement, missing fonts, field flattening,
chart conversion, unsupported formulas, comments becoming notes, animation changes and lost
accessibility metadata. Unsupported features should be replaced deliberately, not silently
flattened, and a fixed derivative should stay distinguishable from the editable master.

Hosted-native import is a transformation: inspect its warnings and the native result for the
features that matter, then decide whether the local file or the hosted document is canonical; two
active masters diverge. When exporting back from a hosted editor, inspect the new local file
instead of assuming the original format round-tripped unchanged.

## Repair at the owning structure

Prefer one structural correction over many local nudges:

- repair styles, masters, themes or layouts before formatting each instance;
- fix section geometry before inserting manual page breaks;
- fix table width, cell margins and repeat-header behavior before shrinking type;
- correct formula, range or number-format ownership before pasting displayed values;
- embed or substitute fonts deliberately rather than accepting silent fallback;
- replace unsupported objects with the simplest destination-safe editable form;
- rasterize only content that needs neither future editing nor semantic access.

Then regenerate the recipient artifact and repeat only the render, edit, round-trip, extraction or
accessibility observations the repair can affect. A corrected source does not repair an older
export already on its way to the recipient.

## Order defects by consequence

Rank defects by what they do to the recipient: changed meaning or values, blocked editing,
concealed review history, broken navigation, damaged accessibility, a misleading presentation,
then polish. A small visual difference is acceptable when it does not undermine the artifact's use.
