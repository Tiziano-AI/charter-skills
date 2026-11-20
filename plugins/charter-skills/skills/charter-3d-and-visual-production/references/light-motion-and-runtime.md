# Light, motion and runtime cost

## Choose the view and value structure together

The camera chooses the relation among depths before the light describes their
surfaces. Judge the distance-and-framing pair, not “wide” or “long” as a style
label; an orthographic view keeps size constant with depth, so only its
direction and crop compose.

| Relationship the scene needs | Lever and condition that changes it |
| --- | --- |
| A near mass should intrude while distant space recedes | Move the eye closer and choose a field of view that keeps the needed context. If measured proportions or an unexaggerated comparison matter, stand back and frame from there instead. |
| Weight or dominance should read from a low view | Lower the eye so mass rises above it. Raise it when the top plane, internal layout or a fragile connection is the important information; a low view can conceal all three. |
| A chosen interval should hold through movement | Compose the camera path against overlap and negative space, not merely a constant radius around a centre. A turntable remains useful when repeatable all-around inspection is the purpose. |
| A form merges with its surroundings | Separate its large light/dark group from the background, or change the contour's overlap. Increasing saturation alone may leave the luminance collision intact; intentional camouflage or uncertainty can call for the merge. |
| A dense scene needs a legible rhythm | Group related bright and dark areas and control their intervals. Quiet support can clarify a focal relation; a deliberately all-over pattern instead needs consistent scale and rhythm, not an imposed single accent. |
| Colour should belong to this place or graphic world | Work from its pigments, emitting sources, reflected light and designed colour relationships. Test the area and saturation of each group in the final transform. A limited muted palette and a loud multicolour one can both cohere; warm/cool separation earns its place through the chosen sources or graphic logic. |

## Light reveals both substance and composition

A reflective surface needs something meaningful to reflect. A dark metal in
an empty environment may be behaving correctly; brightening its colour can
damage it without supplying the missing environment. A narrow bright source
can describe curvature where uniform illumination cannot. Broad light can
reveal a soft surface while flattening the relief that matters elsewhere.
Choose light for the form and mood, not because a standard light rig is called
professional.

Key position and source quality solve different problems. Move the key relative
to the camera to choose which planes, relief and shadows are visible. A side
or rear source can separate a turning form; a frontal source can retain an
intentionally flat, legible graphic face. The source's apparent size at the
subject governs shadow softness. Increase that apparent size for broader
shadow transitions; use a smaller one when a crisp shadow or sharper source
image is part of the design. Raising energy changes exposure, not softness.

Choose the shadow-side value rather than automatically filling it. A dark flag
that blocks returning bounce is negative fill; it can maintain a chosen dark
plane in a bright setting. A dark card visible in a polished surface instead
supplies a dark reflection shape. The same object may do both, but their
effects are different. Add fill when the scene needs information in that
plane; leave it withheld when that loss is the intended reading.

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

### Place a reflection boundary on the form

For a polished curved housing, fix camera, geometry, roughness and exposure.
Give it a broad bright source to reflect, then move the source so its light/dark
boundary travels across the shoulder. To isolate position, keep source size
and distance consistent. Watch where the reflection begins, bends and leaves:
covering the whole face in white can hide the turn, while a boundary across it
can explain the curvature. Place a dark reflected region where adjacent bright
planes need separation, rather than dirtying the base colour to manufacture it.

Then vary source size separately. A narrow reflected strip exposes local
curvature changes; a broad one can describe the overall belly with fewer sharp
events. If the strip repeatedly kinks at a junction, inspect the surface and
normals there. Increasing roughness may hide the kink without repairing it.
For a matte subject or shallow relief, shadow direction and diffuse falloff may
carry more of the form than the reflection boundary. A painted graphic face
may need neither test. Judge the final material/light relationship after the
diagnostic contrast, not the most dramatic inspection image. The
[worked vessel](form-construction-study.md#move-the-reflection-not-the-form)
runs this test on one glazed form: the source moved, resized and cut by a dark
card, with a matte counterpart.

## Motion is part of the material

Anticipation can make a watched performance legible or express a deliberately
designed windup. Inserted before an action that promises immediate response,
the same anticipation reads as input lag. Preserve the interaction's timing
while giving trailing parts their own follow-through when the subject calls
for it. A held graphic pose or mechanical stop may need no overshoot; a
measured display must not acquire invented lag or oscillation. Camera motion
can reinforce an action, conceal it or make interaction uncomfortable; compose
within the experience's control and comfort requirements.

Timing chooses when events occur; spacing distributes positions between them.
Compare the same path and overall action length with different equal-time
positions. A close cluster before release can hold tension, wide gaps can make
the release decisive, and narrowing gaps can bring it to rest. A perfectly
constant-speed carriage instead needs equal spacing over its constant-speed
span. These are different intentions, not bad linear motion versus good easing.

For a carried weight, choose where support transfers, which mass lags and what
settles last. For an abrupt rigid stop, preserve the stop and let only parts
with a reason to flex continue. A tentative character can hold before contact;
a proud one can attack and hold after it. Offset starts and stops where they
reveal force or temperament, not simply to make all channels different. Inspect
the silhouette and contact in the blocked sequence before polishing curves.

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

- [Fujifilm, Understanding Lens Compression](https://www.fujifilm-x.com/en-gb/learning-centre/understanding-lens-compression/):
  distinguishes perspective due to camera position from the lens used to frame
  it. The principle transfers to perspective rendering; an orthographic camera
  has a different projection.
- [ARRI Lighting Handbook](https://www.arri.com/resource/blob/83996/409091c612f371b0c68b41d9dcb636db/arri-lighting-handbook-english-data.pdf):
  source extent, hard/soft shadows and reflected source images explain the
  light-quality choices. Its live-action equipment does not prescribe a CG rig.
- [Sony, Scene Deconstruction with Chris Ross BSC](https://pro.sony/en_PK/insight/cinematography-tips/scene-deconstruction-chris-ross):
  a worked use of negative fill and key position, alongside deliberately flatter
  lighting for another scene. It demonstrates a choice, not a universal demand
  for contrast or backlight.
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
