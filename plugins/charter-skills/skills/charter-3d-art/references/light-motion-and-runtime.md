# Light, motion and runtime cost

## Light reveals both substance and composition

A reflective surface needs something meaningful to reflect. A dark metal in
an empty environment may be behaving correctly; brightening its colour can
damage it without supplying the missing environment. A narrow bright source
can describe curvature where uniform illumination cannot. Broad light can
reveal a soft surface while flattening the relief that matters elsewhere.
Choose light for the form and mood, not because a standard light rig is called
professional.

Separate the questions a light or approximation answers: which plane faces
the source, what blocks it, what reflects in the surface, and what indirect
illumination reaches a recess. Ambient occlusion cannot supply all of these.
Excess occlusion can turn joins into soot; too little separation can make an
assembly float. A local solution may be better geometry, a different light,
baked indirect illumination or a screen-space technique, depending on what
moves and what the renderer supports.

Exposure and tone mapping determine how those relationships reach the display.
Compare a reference under a declared transform rather than repeatedly pushing
material values to counter an unknown one. Specular shape, midtone separation
and highlight compression matter alongside nominal brightness. Atmosphere can
organize depth or dissolve it; preserve distant information when the viewer
depends on it.

Transparency is several different visual problems. A thin protective sheet
may be conveyed through reflection, tint and controlled opacity in a given
viewing range. A thick coloured vessel may depend on refraction, absorption
and thickness. Layered leaves need a different treatment again. Blending is
not physical transmission, and physically richer optics are not automatically
worth their cost or free of sorting and sampling artifacts. Keep the effects
that define the subject and name a consequential approximation when judging it.

## Motion is part of the material

Anticipation can make a watched performance legible or express a deliberately
designed windup. Inserted before an action that promises immediate response,
the same anticipation reads as input lag. Preserve the interaction's timing
while giving trailing parts their own follow-through when the subject calls
for it. A held graphic pose or mechanical stop may need no overshoot; a
measured display must not acquire invented lag or oscillation. Camera motion
can reinforce an action, conceal it or make interaction uncomfortable; compose
within the experience's control and comfort requirements.

Temporal quality is more than average frame rate. Subpixel edges, high-frequency
normal detail, shadow changes, transparency and level-of-detail transitions can
flicker while frames arrive regularly. Observe the actual movement and viewing
distance. Filtering, roughness treatment, silhouette-preserving LOD or less
contrast in fine detail may improve both stability and appearance. A temporal
filter may introduce trails; evaluate the moving result, not just the sharper
still.

## Spend resources on what survives to the viewer

The useful performance question is which work limits this scene on this target,
and what visible contribution that work buys. Triangle count alone cannot
answer it. Draw submission, shading, overdraw, shadow rendering, texture
bandwidth, memory residency and simulation can limit different scenes.
Pixel-bound work can rise strongly with render-buffer area; transparent layers
may shade the same area repeatedly. A light's cost depends on its renderer,
shadowing and affected objects, not simply on the existence of a light node.

Use a controlled change when attribution matters: hold view, motion, resolution
and scene state fixed while changing the suspected feature. Lower render
resolution can probe pixel cost; reducing submissions can probe another cause.
These are diagnostic contrasts, not promises that one number uniquely proves
a bottleneck. Read the profiler and renderer's actual passes alongside them.

Preserve the defining cues when changing representation. Instancing can help
repeated objects; merging can damage culling or independent movement. Baking
can replace stable illumination; it can contradict moving parts. LOD can shed
unseen detail; it can also remove a character's distinctive contour. A cheaper
reflection may be adequate for a scuffed prop and wrong for a mirror that is
the subject.

A real budget includes the other work the scene must do. Judge a hero asset
among its neighbours and during interaction, rather than spending the entire
target on an isolated turntable. Also distinguish loading and residency from
steady-state rendering: a compressed download does not establish small GPU
memory use, and a smooth warmed scene says little about a streaming hitch.
Judge the effect at the target view, buffer size and device; a headless
software-rendered loop does not establish the visual performance the viewer
receives.

## Primary references and limits

- [Meta, Art Direction for All-in-One VR Performance](https://developers.meta.com/horizon/documentation/unreal/po-art-direction/):
  makes art direction and resource allocation a joined problem. Mobile VR's
  constraints do not set desktop, browser or other devices' budgets.
- [John Lasseter, Principles of Traditional Animation Applied to 3D Computer Animation](https://www.provideocoalition.com/wp-content/uploads/p35-lasseter.pdf):
  authored by Pixar's animator; timing, secondary action and exaggeration
  communicate weight and intention. This film-animation account does not
  settle input response, simulation correctness or user-controlled cameras.
- [Babylon.js, Optimizing Your Scene](https://doc.babylonjs.com/features/featuresDeepDive/scene/optimize_your_scene/):
  a renderer-specific route to inspect when Babylon is the target. Confirm the
  current feature behavior and visual effect rather than importing its switches
  into another renderer or adopting every suggested optimization.
