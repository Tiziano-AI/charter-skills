# Charter · Visual Asset Production

A visual asset succeeds through a relationship: subject and treatment, frame
and placement, still image and motion, source and variants. Obtaining a bitmap
is only one production act. Art direction, selection and derivation determine
whether it becomes a compelling asset for the intended use.

When a look is still open, a few quick generated takes in genuinely different
directions are often the cheapest way to settle it. Make them at the delivery
framing and put them before the person before building anything expensive
that depends on the look. This holds for a 3D scene or film, a website or an
app screen as much as for an image asset, and it keeps the first look that
came to mind from becoming the direction by default. The takes settle look,
palette, light and mood, and for a picture or a shot its composition; the
receiving skill says what else carries over. They invent structure, text and
mechanisms, so construction still follows the real subject. No takes are
needed for a defect fix, a screen inside an established design system, work
whose look carries little of the result (such as an internal tool or a
functional prototype), or a look the person has already set: an image or
description of the intended look, a brand or a chosen take. A reference for
what the subject is or how it is built does not set its look, and a broad
adjective or genre such as real, premium, clean or product photography leaves
the look open, because several looks satisfy it. For a single image with no
placement constraints the takes are simply its candidates: choose one and
deliver.

Art direction and production do not replace a generator's operating guidance.
For image or video generation, concept takes included, and for generative
editing, identify a suitable capability this session can use, respecting any
route specified by the task: a generator tool, a collaborator agent that can
make images or a local image service. Before calling it, find and read its
native skill or other operating guide when provided, together with its
current callable contract. That guidance supplies generator-specific prompting
and reference conventions, supported inputs and edits, alpha options, output
handling and fallback routes; do not impose a universal prompt recipe. Apply
the production reasoning here to direction, selection, consistency,
derivation and fitness for the receiving placement. A successful call does not
establish those properties.

When the result depends on exact structure or continued editability, construct
that structure in an editable source; generated imagery can be a component of
that source.

For 3D work, this skill can direct concepts and produce texture imagery.
`charter-3d-art` owns the model, the interpretation of texture channels,
material response, lighting and appearance in the target renderer. For a still
or film rendered from a 3D scene, `charter-3d-art` owns the scene, its motion,
its render and its master and grade; this skill owns the finished asset:
placement, playback, derivation and encode. A finished picture of a surface is
not automatically a material for a relit object. Produce source imagery for its
receiving role: separated surface properties for relighting, or painted
illumination where the graphic treatment depends on it. Concepts can explore
either direction without first settling the final material construction.

A single image with no placement constraints, such as an illustration for a
reply or a placeholder in a draft, needs no bundle or variant apparatus:
direct it well, look at it at the size it will be seen, and deliver the file.
The method below matters when the asset has a place to fit, siblings to match,
transformations to survive or an audience to be published to.

## The placement changes what a good image is

Decide what the image contributes: recognition, explanation, atmosphere,
evidence, persuasion, navigation or another specific role. A hero with overlaid
text needs negative space and crop tolerance; a tiny icon needs a readable
silhouette and optical weight; evidence needs fidelity more than embellishment.
The most detailed candidate may be the weakest at the actual display size.

Frame the creative intent through subject, action, gesture, expression,
composition, lighting, palette, material and texture. Give the image a focal
hierarchy rather than uniform intensity. Technical dimensions and format
constrain the work, but cannot make an undirected visual idea compelling.

Generate at the delivery aspect ratio and orientation when supported, because
composition is decided within that frame. Generators may offer presets or
dimensions bounded by per-axis limits, alignment and total pixel area. Set the
canvas through supported geometry controls; ratio prose does not replace them.
Use prose for subject placement and scale, margins and negative space. When
delivery geometry is unsupported, choose the supported canvas and an explicit
resize, fit, padding or crop treatment, then compose for it rather than assuming
a crop from a square.

Each reference controls something. Separate identity, style, material, palette,
composition, existing geometry and timing, and when you pass several images,
identify each using the selected capability's reference convention and say
what it governs. When references conflict, choose which relationship matters
rather than averaging them into two half-identities.
Exact identity may require the original source; an already-cropped thumbnail
can hide the very feature that needs preserving.

Text changes the route. Short exact wording that belongs to the image can be
generated: put it in quotes, spell unusual words out, and check every letter in
the output. Long, localized or frequently changing text stays out of the bitmap
and is set live by the layout over a quiet region, so a translation does not
require a new image.

## Select a source capable of carrying the work

Judge the candidate in its intended role before expensive finishing. Wrong
identity, gesture or composition needs a new source or a creative edit;
compression, upscaling and edge cleanup cannot repair those failures.
Conversely, a strong image with one damaged edge deserves a local repair rather
than a fresh generation that loses everything that works.

Selection sets the foundation for a family. Independent generations of every
pose, theme or crop can produce a different subject each time. Derive
dependent variants from a selected base where identity matters; allow
meaningful variation where roles differ. Locale can alter reading direction,
text area and composition, not merely lettering.

Compare optical rather than numeric consistency. Equal dimensions do not make
icons equally heavy, subjects equally large or padding equally balanced.
Mirroring can break handedness, asymmetrical markings, light direction, text and
semantic motion. A family should share a world without forcing every member
into the same pose.

## Repair at the scale of the defect

Choose among a local generative edit, a deterministic correction, another
candidate and a different placement. A defect is local when changing it can
preserve the rest of the composition; a cropped face may be a placement
problem, not a generation problem.

Generative edits can change details outside the region you name, and repeated
passes accumulate that drift in faces, lighting and texture. Ask for one change
per pass and restate what must stay the same. A prompt-only edit cannot
guarantee pixel-identical preservation. Where exact preservation is required,
retain those pixels from the original and composite only the approved change
through a permitted deterministic operation. Repeated patching of a
fundamentally wrong pose erodes anatomy and coherence; that source should be
rejected.

Transparency must be real alpha. Use the generator's transparent-background
option with PNG or WebP output, then inspect the decoded alpha channel at hair,
glass, shadows and edges. A checkerboard in the pixels is a painting of
transparency, not an alpha channel. If the generator has no transparent
option, a flat background that contrasts with the subject can support matte
extraction through a permitted editing route; inspect the decoded alpha the
same way.

Derivation translates the selected source into the receiving pipeline: crop,
resize, density, color space, alpha, compression, transcoding, posters and atlas
packing. Repeatable transformations keep a family consistent. Keep the source
distinct, because repeated lossy recompression and resizing destroy options for
later repair. A generative upscaler invents detail, so compare faces, text and
markings with the source rather than trusting sharper pixels.

Inspect the property each transform can damage. Alpha cleanup can leave a halo
on dark backgrounds; compression can destroy thin lines or gradients; a color
conversion can shift skin or brand color; a density change can blur small
symbols; a resize or re-encode in a tool that does not carry C2PA forward
drops or invalidates embedded Content Credentials. A video encode carries
colour tags (primaries, transfer, matrix, range) that players interpret
differently: compare the encoded file as the receiving players show it with
the master, because a decoder used only for the check can read or ignore those
tags differently. The tags describe the pixels and convert nothing: the
pixels must already be in the primaries and transfer the tags declare, and the
conversion that writes them has to use the declared matrix and range.
Correct dimensions reveal none of these.

## Motion is composition through time

Timing, weight, easing, camera behavior and continuity make action
intelligible. A still can look convincing while neighboring frames drift in
identity or geometry. A loop needs a coherent seam, not matching filenames or
duration. Entry, exit, poster-to-play transition, sound and caption
synchronization belong to the asset's experience.

Choose a shot sequence when the story needs cuts; use extension when a
continuous shot matters and the selected capability supports it. Maintain
identity and style through its supported reference or frame controls rather
than repeatedly re-describing the subject. Duration limits, first/last-frame
conditioning and whether audio is retained or regenerated depend on the
selected operation; read its contract before planning around them. Describe
each shot's framing, subject, action, setting, lighting and camera movement.

Watch the clip at its intended pace in its receiving context. If you cannot
play it yourself, you have not watched it: stills and contact sheets hide
stutter, flicker and rhythm. Measure what playback would show from the decoded
file: jumps, duplicated or dropped frames, and frame-to-frame change where the
image should hold still. Read its frames at their own timestamps, without rate
conversion, and compare their count and timing with the source sequence,
because extraction at a fixed rate can turn a dropped frame into a duplicate
or add duplicates the file lacks. Look at consecutive frames around the
fastest moments. Call the motion uninspected until a person has watched it,
and put a short playable clip before them as soon as one exists. A repair to
one frame can create a new discontinuity. Choose regeneration or a bounded
edit according to how much of the temporal relationship is wrong.

## Provenance and disclosure travel with the file

Generator provenance is file-specific. OpenAI supports C2PA and SynthID signals
for supported outputs, but coverage depends on product, model, format and date;
Google documents SynthID for Veo video. Transformations can remove credentials
or weaken watermarks. Plan credential preservation and check the delivered
file. No detected signal does not establish human authorship or absence of AI
editing.

Audience-facing disclosure is a separate decision. In the EU, Article 50(4)
requires deployers to disclose qualifying deepfakes: resemblance to a real or
plausible subject and a false appearance of authenticity or truthfulness matter
together, in the actual publication context. Photorealism alone is insufficient;
stylization or fictional intent is not a universal exemption. For qualifying
deepfakes in evidently artistic works, the manner of disclosure is reduced,
not removed. Platform rules have their own scope. The
[provenance reference](references/provenance-and-labelling.md) supplies the
classification, personal-use exclusion, verification limits and current dates.

## Finish with a deliberate selection

Inspect at the intended display size and background, then use native-resolution
detail to diagnose defects. Compare variants together. The useful decision is
select, repair or reject for this role, not a generic aesthetic score.

Package one canonical file per role with the needed variants. Keep enough
source and transformation lineage to revise the work: reference roles, selected
output, creator or generation identity, settings when available,
transformations, credentials and usage constraints. Do not promise a
reproducible seed or a rights grant that does not exist.

A single asset needs only its file and a source note. A large bundle benefits
from a manifest, because relationships otherwise become hard to retain.
Rejected candidates, contact sheets and intermediates stay out of runtime paths
unless the product uses them.

- [Production reasoning](references/workflow.md): open when briefing a set of
  assets, assigning references, deciding between crop, repair and a new source,
  or checking what each transformation can damage.
- [Composition and derivation study](references/composition-and-derivation.md):
  open when existing artwork must carry copy or change aspect ratio. Editable
  SVGs and rendered comparisons show how hierarchy and panel arrangement retain
  a relationship that a crop loses; this is layout practice, not a painting or
  motion lesson.
- [Visual fault lines](references/visual-qa-rubric.md): open when selecting
  among many candidates or reviewing a family: identity, geometry, edges,
  optical balance, motion and receiving-product fitness.
- [Provenance and labelling](references/provenance-and-labelling.md): open when
  an asset will be published or reused: source classes, lineage, Content
  Credentials, platform labels, EU AI Act Article 50, and a bundle-manifest
  example.
