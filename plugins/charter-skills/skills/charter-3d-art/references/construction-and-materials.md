# Construction, materials and interchange

## The required behavior chooses the representation

Think of a feature under a moving eye and changing light. Does it alter the
outline, expose another surface, separate from its neighbour, bend or transmit
light through thickness? Those behaviors decide what must be represented.

| Needed behavior | Useful representation and its limit |
| --- | --- |
| A visible opening, profile or moving component | Geometry with meaningful thickness and pivots; a dark painted patch cannot expose the space behind it. |
| Shallow relief whose silhouette is unimportant | Normal or height-based treatment; grazing angles, close views and self-occlusion can reveal its limits. |
| Pigment, lettering, stain or a broad colour pattern | Texture or decal; its sampling, orientation and edges must remain correct in the intended view. |
| A fixed distant composition | Cards, impostors or baked imagery can preserve the reading; a freely moving eye may expose their lack of depth. |
| A deforming surface | Geometry and deformation that preserve the intended volumes and seams; continuous skin, cloth and a hinged puppet require different constructions. |

These are choices, not ranks of quality. Reconstructing every fibre in a distant
coat can waste resources and create noise; a close embroidered crest may need
real relief. A graphic world can deliberately flatten space. The requirement is
for the approximation to hold across the views and behavior the work promises.

Separate the visible structure from the authoring technique. A script can
build a beautifully proportioned object or repeat anonymous primitives. Manual
sculpting can reveal character or produce detail without design. Choose the
means by the shape and revision control needed; procedural construction is not
an excuse to accept a primitive-looking result.

Assembly logic helps manufactured objects read: parts meet, clearances exist,
edges finish and movement has an axis. Organic design needs its own logic of
growth, tension and articulation. Model the relationships that are visible or
functional; hidden detail earns its cost only when it affects shadows,
reflection, deformation or later views.

## Build continuity through the junction

A union removes an internal overlap; it does not choose a pleasing junction.
Two tangent surfaces can still meet with an abrupt curvature change, producing
a hard highlight break that makes an appendage read as glued on. A broader root
can carry force or growth into a body, while a narrower free span keeps the
appendage light. That relationship is different from uniformly inflating the
whole handle. A visible assembly may need the opposite: a clear seam and
separate edge treatments to explain how its parts meet.

Read the negative space as a designed contour too. Moving one attachment
changes the opening, the bridge above it and the distribution of body mass.
For a hollow object, the inner wall, lip and floor form another profile; a
thin-looking outer silhouette does not establish plausible thickness inside.
An actual cut removes volume and exposes a wall, while a separate plate adds
another contour and shadow. Repeated incisions preserve the body's continuity
through the material left between them. Repeated detached panels express an
assembly, even when their overall envelope matches the original mass.

The [vessel construction study](form-construction-study.md) makes these
relationships editable: two profiles, variable-radius handle controls,
localized root blending, exported meshes and the same forms under different
surface/light treatments. Its voxel union is suitable for this soft volume.
For a crisp manufactured fillet, deformation-ready edge flow or exact wall
dimensions, explicit topology or a CAD solid provides controls this
method does not retain.

## Carry a CAD solid into the scene

A CAD solid holds exact surfaces and the features that produced them;
the renderer receives only their tessellation. Set the tessellation of each
face from its size on screen at the closest view it reaches. One chord
tolerance in model units either leaves a small foreground fillet faceted or,
made fine enough for it, spends triangles on large curved faces and curved
boundaries that read the same either way. An angular limit per segment keeps
small radii round whatever their size. Keep shading split where faces meet at
a real edge and continuous across a fillet's tangent joins. Welding the whole
mesh and smoothing by angle can soften a crisp break or crease a shallow
blend, because an angle threshold does not know which joins the solid made
tangent. An interchange that carries only triangles drops both the shading
splits and the face types; choose one that keeps them, or bring them across
by script.

Carry each face's surface type, and the feature that created it where the
modeller records one, into the scene as a material slot or attribute. A bore,
a faced flat and a cast wall can then take the finish of the operation that
made them without hand selection, and keep it when a dimension changes and the
meshes are regenerated. Check fits, clearances and interference on the solid,
where they are exact; a gap or overlap in the tessellated mesh can come from
chord error rather than from the design. Where a chord-error overlap or gap
shows in the picture, tighten the tessellation of those mating faces.

## Author surfaces, not photographs of surfaces

Choose the shading language before channel authoring. A relit or finish-compared
object usually needs pigment separated from illumination. A painted or graphic
world may instead depend on value shapes, ramps and drawn light that its shader
must preserve. Walking through that world does not make its painted light
wrong; promising a changing illumination response can. Mixed treatments need
an intentional visual relationship rather than accidental differences between
assets.

Non-physical shading is constructed too. Cel/ramp shading turns surface-normal
changes into visible bands, so the normal field and ramp thresholds shape the
face or garment as much as polygon count. An expanded-hull outline depends on
normals and extrusion, whereas a screen-space outline depends on its sampled
boundaries; inspect thickness and breaks at the intended distances. In unlit
painted work, the texture carries the value modelling. Its implied illumination
and palette must belong to the same world. Flat-colour work places more of that
burden on silhouette and shape. The physical-channel guidance below applies
where physically lit response is intended.

For a physically based material, identify the substance before adjusting its
numbers. Conductive metal, dielectric coating, exposed substrate and dirt do
not share one response merely because they occupy one object. Roughness
controls the distribution of reflected light; normal detail changes surface
orientation; colour specifies a different property. Use the material model's
actual semantics rather than treating each channel as a contrast slider.

A photograph or generated image mixes these properties with illumination,
perspective and processing. Ask for a source suited to the intended channel,
then inspect what was produced. A generated “seamless PBR texture” label proves
neither seamlessness nor a calibrated set of maps. Do not derive roughness by
blindly desaturating colour: a dark printed mark can be as smooth as the pale
coating around it. Height, normal, roughness and colour need coherent surface
features without being copies of one another.

Keep colour transforms separate from data-map interpretation. A roughness or
normal map is data, not a colour photograph to make pleasing through a display
transform. The authoring application, exporter and renderer must agree on
channel packing, colour space and normal convention. A normal-map inversion
can make a recess appear raised; additional resolution will not repair it.

Use generated or sourced imagery where it contributes variation, atmosphere
or surface character. Exact recurring symbols, markings and designed patterns
often benefit from controlled drawing and layout rather than repeated
generative repair. Baked light is legitimate for a fixed graphic treatment or
supported baked-lighting workflow; it becomes a defect when it contradicts
the relighting or motion the object is supposed to support.

## Make the maps work on the object

UV layout distributes finite samples. Give important visible areas enough
coverage, avoid stretching that changes material scale, and allow padding so
filtered mip levels do not pull in unrelated islands. Equal texel density is a
useful baseline across comparable surfaces, not a requirement to spend the
same resolution on a hidden underside and an inspected face.

Baking transfers detail from a dense source onto a lighter surface. Projection
distance and direction must reach the intended source without picking up a
neighbour or skewing the feature. Tangent-space normal maps also depend on
agreement among the bake, mesh normals, UVs and renderer's tangent basis; a
mismatch is not repaired by higher resolution. Inspect shading seams and
projection errors in the target before painting around them. For glTF's exact
tangent-generation rules, use its current specification rather than assuming
every exporter and renderer makes the same choice.

Tiling and atlases solve different needs. Tiling sustains surface density but
can reveal repetition; an atlas reduces some binding overhead while coupling
sampling and residency. Unique accents can break repetition without making
every surface unique. A larger atlas may increase resident memory or weaken
independent loading. Choose around actual use rather than a universal
one-material or one-texture rule.

Thin text and lines need shape as well as resolution. Check their contrast and
coverage after projection, filtering and motion. Adjust stroke weight,
spacing, representation or placement when necessary. A symbol important to
operation must remain interpretable, not merely present in the source image.

## Export is a translation between models

An authoring scene can contain capabilities that the delivery format or loader
does not express. Establish which transforms, material features, animation
channels and extensions reach this renderer. Export a representative difficult
part while the construction is still flexible; exporting only a plain cube
does not answer whether the defining material survives.

Preserve the units, coordinate system, pivots and hierarchy that runtime
motion consumes. Inspect hard/soft shading boundaries, tangent continuity,
negative scale, culling and deformation in the imported object. Mesh counts
inside the DCC and exported vertex counts need not agree: attribute boundaries
can split shared vertices. Generated assets and hand-authored assets face the
same translation.

Keep the editable source and a reproducible route to the shipped derivative.
An engine-side material adjustment is part of that route when the exporter
cannot express the desired result; it must not be a mystery fix lost on the
next export. Asset provenance belongs with the source and its useful usage
constraints, not with a claim that export validation makes the art correct.

## Sources for deeper work

- [Sébastien Lagarde, Feeding a physically based shading model](https://seblagarde.wordpress.com/2011/08/17/feeding-a-physical-based-lighting-mode/):
  useful causal discussion of material/light compensation and judging surface
  response in-engine. Its encodings and numerical advice depend on the
  rendering pipeline; they are not cross-renderer defaults.
- [Khronos, Real-time Asset Creation Guidelines](https://github.com/KhronosGroup/3DC-Asset-Creation/blob/main/asset-creation-guidelines/RealtimeAssetCreationGuidelines.md):
  geometry, material, texture and delivery guidance for interoperable assets.
  Use the relevant chapters; product-commerce fidelity does not dictate a
  game's artistic style.
- [Blender, glTF 2.0 exporter manual](https://docs.blender.org/manual/en/latest/addons/scene_gltf2.html):
  recognized material arrangements and export features. Read the documentation
  matching the actual exporter and target loader; arbitrary DCC shader graphs
  and optional glTF extensions are not automatically portable.
- [Marmoset, Toolbag Baking Tutorial](https://marmoset.co/posts/toolbag-baking-tutorial/):
  projection direction, distance and grouping explain skewed or contaminated
  bakes. Its tool-specific controls and example settings are not universal.
- [Khronos, glTF 2.0 specification, Using Primitive Data](https://github.com/KhronosGroup/glTF/blob/main/specification/2.0/Specification.adoc):
  the format's normal/tangent interpretation, not a guarantee that a particular
  imported mesh matches its authoring viewport.
- [Unity Toon Shader, Outline Settings](https://github.com/Unity-Technologies/com.unity.toonshader/blob/master/com.unity.toonshader/Documentation~/Outline.md)
  and [Normal Map Settings](https://docs.unity3d.com/Packages/com.unity.toonshader@0.11/manual/NormalMap.html):
  concrete examples of controlling cel-shaded regions and outline extrusion.
  These demonstrate construction choices, not a required shader or engine.
- [Babylon.js, Planning Your Assets for Real-Time Rendering](https://doc.babylonjs.com/preparingArtForBabylon/planningRealTimeAssets/):
  practical links among intended style, silhouette, materials and texture
  allocation. Example budgets are not format limits or measurements of another
  device.
