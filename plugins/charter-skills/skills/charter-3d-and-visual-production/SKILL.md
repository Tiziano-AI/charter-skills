---
name: charter-3d-and-visual-production
description: Build or repair a 3D model or scene, produce an image or texture, or
  finish a still or film for its placement. Includes art direction, animation, render
  cost, crops, transparent assets, and playback. Not engine setup, gameplay rules,
  or designing the interface around the art.
metadata:
  content_version: charter-3d-and-visual-production@2026.11.20.0
---
# Charter · 3D Art & Visual Production

A museum pump that visitors can turn, a diagram of how it works and a film
of its first stroke owe different things. Look at the existing work at the
distance, size and speed at which it will be seen. What must the viewer be
able to discover by moving, what must read in a single frame, and what must
unfold over time? Build the part that carries that relationship.

**A model or scene.** Before choosing mesh, material, rig or camera, read the
[scene craft chapter](3d-art.md). Work from how the subject is made, moves or
is performed. The hole in a pump handle must stay open against the background
when it turns; a normal map can describe a shallow stamp, not that hole. A
weld and a cast junction meet the housing differently before either needs
scratches. In a fixed shot build the projected silhouette, overlaps and dark
and light masses against the chosen frame. A replica or a freely handled
model must also hold up from the other permitted views; a convincing hero
shot cannot hide a wrong fit. Use the [worked vessel](references/form-construction-study.md)
when two joined shapes need to read as one continuous surface. Open
[construction and interchange](references/construction-and-materials.md)
before choosing how to carry shape, finishes or motion into the target. If a
model stutters when visitors turn it, identify what costs frame time *in that
view* before reducing it. Retain the casting and the movement that explain
the mechanism; compare like views in the actual viewer, not just file size.
[Light, motion and runtime cost](references/light-motion-and-runtime.md)
separates costs that call for a different mesh from those that call for a
different material, light or pass.

**An image or a surface that needs new pixels.** Before making or deriving
the image, use [image and motion production](visual-asset-production.md) to
choose the medium, framing and source. A report documenting a damaged pump
needs a faithful capture; an illustration can cut through the casing to
explain an otherwise hidden stroke. A photograph of enamel includes the
reflection of the room. Project that reflection as base color and it will
travel with the paint as the object turns. For a relit surface, produce the
properties the material needs, then see them on the object under moving
light. For painted illumination, a shader that keeps the artist's painted
light may be exactly right. If the pixels are settled and a finish reads
wrong, change the surface response or reflection environment; no new image
is implied.

A masthead needs its real crop, copy area and background, not a 3D scene.
Select at placement size. Recompose when cropping breaks the relationship;
derive related variants from the chosen source when identity matters. For a
transparent edge inspect decoded alpha against light and dark: a checkerboard
can be part of the picture. Use the [production method](references/workflow.md)
when choosing between a local edit and a new source; for a difficult aspect
change the [derivation study](references/composition-and-derivation.md) shows
what rearranging the drawing can preserve that a crop loses. Compare
the [visual fault lines](references/visual-qa-rubric.md) across variants
before selecting what ships. A one-off illustration need not become a bundle.
When imagery will be published or reused, consult [provenance and labelling](references/provenance-and-labelling.md)
before choosing the source and check what rights, disclosures and credentials
travel with the delivered file.

**A film or a rendered still.** If light, material or movement is made in a
scene, use [rendered stills and films](references/rendered-stills-and-films.md)
before the first render in the final type of process. For motion, stage the
action with stand-ins: what leads, what holds, what follows, and from where
can the viewer see the change? A planted camera may reveal the play of a
linkage better than an orbit. Carry a short, difficult span through render,
master, grade and encode before committing to the long render. Keep a
scene-linear floating-point master when the grade still needs its range.
For a supplied film that only needs a new delivery, start instead at its
master. Inspect the decoded asset in its receiving player at its intended
pace; consecutive-frame measurements can locate jumps, but a contact sheet
cannot establish freedom from flicker or that anyone watched it.

When the look is open, take direction from the subject's making, use or
performance. Use [directing a look](references/directing-a-look.md) before
turning those particulars into a brief for new images or shots;
[scene diagnosis](references/art-direction-and-diagnosis.md) helps distinguish
a direction that was never chosen from one lost in construction. Show
comparable takes at delivery framing before building
expensively on a choice the person has yet to make. If the idea is open,
three grades of the same studio shot show just one idea; if only the grade is
open, holding the shot constant is what makes the choice intelligible.
Use the [direction study](references/direction-study.md) to separate those
cases, or the [reference-to-scene study](references/reference-to-scene-study.md)
when translating a chosen picture into space. A concept establishes a
direction; a fragment in the target renderer shows whether it survives
construction. A local repair keeps the settled look. For generated takes,
edits or finished media, consult the selected generator's operating guide
before calling it; supported source controls, transparency and output vary.

When an interface determines where artwork can sit, take the placements and
occlusion from `charter-web-apple-and-status-interfaces` and return the
finished variants at the sizes it uses. When the silhouette of a landing
craft is a cue, `charter-game-design` settles what the player must know and
at what distance or moment. Realize that reading in the scene and inspect it
in play. A standalone model needs neither an interface nor a game.
