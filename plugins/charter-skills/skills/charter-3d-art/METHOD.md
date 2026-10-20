# Charter · 3D Art

A 3D scene is a visual idea given form in space. Interactive work lets the
viewer inhabit it; a rendered still or film fixes the view and spends render
time instead of frame time. Either way, its character comes from relationships
among forms, surfaces, light, space and movement, not from the number of
assets or effects it contains. Technical art preserves those relationships as
the view moves, the object acts and the renderer spends its finite resources.
The intended result can be photographic, graphic, painterly, abstract or
deliberately strange; realism is one direction, not the quality scale.

Start with what the viewer should perceive and the views in which it must
survive. For existing work, look at the actual scene at its ordinary viewing
size before selecting a repair. A beautiful close-up can conceal a confused
composition, unreadable mechanism or lifeless character in use.

For new work, make the defining visual relationship concrete early: mass
against space, surface against light, pose against movement. When the look is
still open, start with a few generated concept takes in distinct directions
and put them before the person; `charter-visual-asset-production` says when
they help and how to make them. Then show the chosen direction as a fragment
in the target renderer: a concept settles a direction without proving its
realization. A representative fragment can settle the defining relationship;
it cannot establish the quality of an unseen whole. For an animated piece that
whole includes timing and camera movement, which need not wait for the look:
put the complete sequence in motion with stand-in parts and a rough camera
path while the direction is being chosen, then reframe the shots to the chosen
take and swap detail in as it lands.

## Direct the eye before adding detail

Translate broad adjectives into visible choices. Monumental might mean a low
eye, an uninterrupted mass and sparse scale cues; delicate might mean slender
connections, space around them and small controlled highlights. Neither
description dictates a preset. Decide which relationships express this subject
and which must remain exact. A measured product replica owes fidelity that an
expressive landscape does not.

Use references to understand causes as well as appearances: what carries the
weight, where a surface changes substance, how light describes curvature, what
the gesture suggests. Distinguish construction, material, mood and composition
references. When a chosen picture governs a fixed frame, construct through that
frame: establish the camera and large shapes against it, using projected size,
overlap, negative space and light/dark grouping to guide the scene. Camera
position, field of view and geometry may need to change together. The
[reference-to-scene study](references/reference-to-scene-study.md) makes this
working comparison and its controls concrete.

A generated image may contain incompatible perspectives or invented mechanisms.
Preserve the intended reading while resolving what the actual commission
requires; mechanical plausibility must not silently replace the selected
composition. Conversely, measured fidelity or required movement can rule out a
single-view construction. A mood reference does not bind every contour, and
interactive work needs the relationship to survive its permitted views, not
just match one picture.

Give the scene a hierarchy of large forms, supporting forms and accents.
Proportion, silhouette, negative space and grouped light/dark areas establish
the reading that texture elaborates. If every edge is bright and every surface
is busy, attention has nowhere to settle. Repair an undistinguished primary
shape in the model or composition rather than covering it with scratches,
bloom or expensive materials. Conversely, ornament can be the subject: organize
its richness instead of stripping away its identity.

Coherence does not mean sameness. Related objects can share a construction
logic, palette or rhythm while differing in age, role and emphasis. Deliberate
contrast makes a focal object important; an unrelated asset-pack style merely
makes it foreign. Quiet areas can make a subject easier to find; dense or
oppressive compositions may instead depend on a rhythm the eye can learn.

## Construct the causes of the appearance

Choose a representation by the visual behavior it must carry. Geometry can
change silhouette, parallax, occlusion, contact and deformation. A normal map
changes the shading response but cannot make a cutout open or a thin profile
exist. Painting a seam does not by itself create independently moving parts.
Use actual depth where the viewer can discover it, and simpler
representations where they preserve what the work needs. A distant painted
skyline can be exactly right; the same treatment fails a freely inspected
sculpture.

Choose a construction route that can change the defining form. A profile and
sweep give control over a vessel's body and reach; a sculpting or subdivision
surface can sustain broader continuous transitions. Joining primitives can
establish masses without resolving their junctions. If the result still reads
as attached pieces when the aim is one incised or flowing volume, change the
shared surface, root transition and negative space. More light or texture
cannot make those geometric relationships exist. The
[worked vessel](references/form-construction-study.md) carries an editable
source, form revisions and an interactive export for this seam; the separate
finished-asset and HDRI references serve surface and light, not construction
history.

A manufactured object reads as made when its features meet the way casting and
machining make them meet: a fillet where a boss or foot grows out of a wall, a
crisp break where a cutter passed, a finish that follows each operation. A solid
modelled in CAD, an exact boundary representation whether scripted or drawn,
finds the exact edge where features intersect and rolls a fillet of a chosen
radius along it, knows where shading should break and where it should flow,
keeps each face's identity (its surface type and, where the modeller records it,
the feature that made it) so a finish can follow the operation, and holds
measured fits and clearances exactly. A modifier or node stack driven by numbers
is parametric too, but it works on the mesh: its blends follow the tessellation
rather than the exact intersection, and its faces carry no surface type, only
the labels you assign before each operation. Hand-built
meshes suit turned and prismatic parts; intersecting castings built that way
tend to look assembled from primitives. Soft or deforming forms need other
routes. Before turning a solid into render meshes, open [construction and
interchange](references/construction-and-materials.md) for tessellation, shading
breaks, per-face finishes and where to check fits.

Specificity comes from a chosen design logic. Physical construction can express
assembly, thickness, growth or erosion; graphic construction can express a
shape alphabet, edge quality and repetition; a performed character can turn on
line of action and expressive extremes. These logics can combine. A seamless
product may communicate its construction through gaps and finish rather than
visible fasteners. Choose which causes to expose, compress or invent instead
of decorating every subject with physical traces. An impossible object can be
coherent on its own terms.

Materials and illumination act together. In a relit scene, distinguish surface
properties from the lighting already present in a photograph or generated
image. A convincing picture of polished metal is not automatically a usable
metal material. A highlight painted into colour may stay attached when the
light moves; a plausible base colour under the wrong reflection environment
can still look wrong. Design the material response and the light that reveals
it, rather than compensating for one by distorting the other. Intentionally
painted illumination can define a graphic treatment even under a moving camera;
choose a shader that preserves that treatment rather than decomposing it into
physical channels and expecting the style to return.

Light also composes: it can separate depth, reveal gesture, guide attention or
withhold information. Exposure, atmosphere and tone mapping change that
composition. Neutral inspection light helps diagnose a surface; it is not
necessarily the final art direction. Neither physical accuracy nor dramatic
contrast excuses losing something the viewer must read.

## Make the idea survive movement and scale

The camera participates in the design. Eye height, field of view, distance and
framing change apparent proportion and intimacy. In interactive work, establish
them with the intended interaction; do not save a weak asset with a beauty-shot
camera the user never gets. User-controlled views require a range of
successful compositions, not one frozen frame. In a rendered film the authored
camera path is the composition, and every frame of it is seen.

Movement reveals substance. Timing, contact, flex and settling can communicate
weight or temperament; connected parts need not respond identically. A rigid
instrument should not wobble like a creature, and an expressive character need
not obey literal mechanics. Visual follow-through should enrich the action
without delaying the response or falsifying a measurement that the experience
depends on.

Fine detail has to survive projection into pixels. Thin bright edges, tight
patterns and sharp specular highlights can sparkle or disappear in motion even
when a still looks crisp. More texture resolution or triangles may intensify
that failure. Shape the frequencies, filtering and transitions for the actual
viewing range. Preserve the identity, pose, material reading and important
information when simplifying; uniform reduction is not visual judgment.

## Treat the runtime as the artistic medium

When the scene ships to a runtime, the authoring viewport, export format and
target renderer are different interpreters. A successful export does not show
that a node network, tangent basis, animation, light or optical effect
survived. Bring the defining material and mechanism into the target while
their construction can still change. Use its supported capabilities
deliberately rather than treating an offline image as a rendering promise.

Design appearance and cost together. Ask what a costly feature contributes,
what causes its cost in this renderer, and whether another representation can
preserve that contribution. This may mean retaining geometry and changing a
pass, or retaining an optical effect and simplifying its surroundings. It does
not mean reducing everything until the frame counter is green. Nor does a
fast hero-object scene establish the budget of its populated environment.

## Rendered stills and films

Render time is the budget of a rendered piece: it sets how many times you can
see the whole of it before the final render.

- From the first render in the kind of process the final will use, make the
  renderer report the device each stage ran on, denoising included. Fallbacks
  can be silent and a default log may name no device, so raise its logging
  and confirm that the device lines actually appear; a filter that matches
  nothing proves nothing. Device preferences need not travel with the scene
  file into another process, a stage such as denoising can stay on the CPU
  unless enabled, and one stage on the CPU can multiply the budget.
- Measure seconds per frame on the hardest shot, at the samples and
  resolution you intend for the final, as soon as it has its final materials
  and light: time several consecutive frames in that same kind of process,
  apart from one-off start-up. Do this before
  committing samples and resolution and before promising frame rate and
  length; when the person's own numbers do not fit, show them the
  measurement.
- Before the long render, push a short span through the whole chain (render,
  master, grade, encode) and check the decoded file as
  `charter-visual-asset-production` describes for derivation. Choose a span
  with the darkest gradient, a fade and the fastest motion. A setting whose
  output is identical with it switched off is doing nothing.
- Render into durable storage in units a restart can skip once complete. A
  unit counts as complete only when it reads back whole, or was written under
  a temporary name and renamed when finished; the presence of a file does not
  prove it, and a renderer's own skip-existing option may not check.
- When exposure or grade may still change after rendering, keep a scene-linear
  master in a floating-point format, so values above display white survive,
  and finish it through the same view transform you judged the look in.
  Written linear, an integer file clips those values; written through the
  display transform, it bakes the tone curve, and at 8 bits its steps too.
  Only a log encoding lets an integer file carry them, and the grade must
  decode the same curve.
- Sampling noise moves differently from the scene. With a fixed seed it stays
  put on the screen while the scene slides under it; with an animated seed it
  boils; a per-frame denoiser turns either into shifting blotches. Where the
  camera is locked, a fixed seed keeps still areas that see no moving part
  identical before denoising, though a denoiser or adaptive sampler that looks
  at neighbouring pixels can still carry change in from a nearby moving part.
  Render one frame with two seeds, denoised as the final will be: the
  difference shows how much the noise will change wherever the image under it
  changes, which with an animated seed or a moving camera is everywhere.
  Where it shows at playback size, the remedy is
  more samples or a lower noise threshold, the same every frame, which a time
  cap does not keep.
- A repeated feature such as gear teeth, spokes or a hex socket that moves more
  than half its spacing per frame appears to stand still, run slow or reverse,
  and it judders well before that. Motion blur hides this only once the
  shutter smears each feature across a full repeat; between those rates it
  strobes even when blurred; a high-contrast feature keeps a faint drift
  beyond a full repeat, fading only slowly as the smear lengthens; and an
  eased spin-up or stop passes through that band.
  Check peak rates, not averages.
- When you cannot watch the motion, measure the scene as the renderer
  evaluates it, frame by frame, rather than the curves you authored: the
  on-screen speed in pixels per frame of each moving part, and of the subject
  and background as the camera move sweeps them across the frame (too fast
  reads as debris, too slow as nothing); each repeated feature's peak step
  against its spacing; and evaluated positions against their intended values,
  which exposes jitter a still hides. The motion section of
  `charter-visual-asset-production` covers the decoded file and when motion
  counts as watched.

## Find the first wrong relationship

Before calling the work finished, compare it with the intended reference at
comparable view, scale and motion. Renderer and authoring defaults are not an
art direction: anonymous primitives, one roughness everywhere, an empty
reflection environment or unexamined tone mapping can produce a generic look
even when every feature is present. Keep a default because it serves the idea,
not because it escaped a decision. Find the first visual relationship that is
wrong. A proportion problem, a material response problem and a
colour-management problem can all be described as “plastic”; they need
different interventions. Isolate a suspected cause with a useful temporary
view or material, then return to the intended scene. Diagnostic wireframes
and neutral renders are instruments for making the art, not substitutes for
delivering it.

## Depth and neighbouring work

- [Art direction and visual diagnosis](references/art-direction-and-diagnosis.md):
  open when a scene is generic, incoherent, noisy or merely technically
  correct, or when translating a reference into a different medium.
- [Construction, materials and interchange](references/construction-and-materials.md):
  open when choosing geometry versus surface treatment, turning a CAD
  solid into render meshes, authoring texture channels, preparing moving
  assets or repairing DCC-to-runtime differences.
- [Worked form construction](references/form-construction-study.md): open when
  a hollow body, integrated appendage or root transition needs making rather
  than another verbal diagnosis; use its editable source and comparison to
  understand the construction, not as a universal silhouette or recipe.
- [Light, motion and runtime cost](references/light-motion-and-runtime.md):
  open when lighting obscures the subject, detail fails in movement, or
  appearance and performance seem to demand incompatible choices.

`charter-visual-asset-production` directs and finishes image/video sources,
including concepts and texture imagery; this skill owns their interpretation
inside a 3D scene. For a still or film rendered from a 3D scene, this skill
owns the scene, its motion, its render and its master and grade, and Visual
Asset Production owns the finished asset: placement, playback, derivation and
encode. `charter-game-design` owns what the player needs to notice, what a
response communicates about a rule, and what may remain ambiguous. Where camera
behavior, response timing or routes through space affect control or play,
Game Design decides that behavior; this skill composes its visual expression.
Platform interface skills own surrounding controls and navigation. Engine
setup, API usage and general application correctness stay with their
technical owners. The renderer and the artistic problem, rather than the
work's label as a game, viewer, exhibit, configurator or film, determine
whether this expertise applies.
