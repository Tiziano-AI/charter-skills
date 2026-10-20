# From creative source to product asset

Production joins creative selection with transformations. The distinction
matters because the same defect can call for a better source, a different crop,
a local repair or a change to the receiving layout. Start at the relationship
that fails rather than passing every candidate through the same finishing line.

## A brief describes what the visual must do

The role and placement establish the constraints worth resolving: audience,
display size and density, aspect ratios, background and alpha, motion, duration,
variants, format, file-size budget and receiving pipeline. These are not equal
priorities for every asset.

A small character sprite must keep identity in silhouette and motion. An
editorial portrait can depend on expression and lighting. An illustration under
text needs a deliberate quiet region. Translate the role into a visual register:
subject, hierarchy, palette, material, texture and camera. Mention unwanted
lettering, logos, props or extra subjects when they would be plausible but wrong
additions, not as a universal negative-prompt incantation.

Assign references by what they control. An identity reference and a lighting
reference should not be blended into two half-identities. A layout guide can
constrain negative space without owning style. Source footage, audio and timing
guides can govern different parts of a motion piece. Inspect original geometry
when thumbnails or prior derivatives have lost the needed detail.

## Source quality and repairability are different

A candidate's fitness comes from its subject, silhouette, expression,
perspective, anatomy, focal hierarchy, palette and placement. A tiny asset may
need less detail and stronger shape; a wide crop may need a different camera
rather than stretching the subject.

Compare these nearby cases:

- A strong portrait with a distracting object at the edge may benefit from a
  crop, if the target frame keeps its balance.
- The same portrait with the wrong expression needs a creative change; tighter
  crop and sharper encoding will not create the intended emotion.
- A damaged hand may be locally repairable when pose and lighting are coherent.
  Repeated anatomy patches across a fundamentally wrong pose suggest rejecting
  the source.
- A beautiful landscape that leaves no space for essential text may need a new
  composition, not increasingly heavy text shadows.

Choose a canonical base capable of supporting the family. Independent generation
is appropriate for independent images; dependent states, poses and themes need
enough shared source or reference control to remain the same subject.

## Derivation preserves options by being repeatable

Keep original selected output separate from crops, resized images, masks,
compressed files, posters and atlases. A flattened derivative cannot recover
detail that its processing removed. Record parameters when later reproduction
or family consistency depends on them.

Different transformations threaten different properties:

| Transformation | Typical failure | Useful observation |
| --- | --- | --- |
| Crop or aspect-ratio adaptation | Focal subject or text-safe area lost | Actual receiving frame |
| Resize and density | Thin features vanish or optical weight changes | Intended display size |
| Alpha cleanup | Matte halo, missing translucency, jagged silhouette | Relevant light and dark mattes |
| Color conversion | Skin, brand color or gradients shift | Color-managed receiving context |
| Compression | Ringing, banding, blocks, illegible detail | Target-size view and affected detail |
| Mirroring | Text, handedness, markings or semantic direction reverse | Comparison with canonical identity |
| Atlas packing | Wrong padding, bleed or frame mapping | Runtime rendering and animation |
| Transcoding | Timing, looping, audio or caption drift; colour tags read differently by the receiving player | Full playback in the receiver |
| Any export or re-encode without C2PA support | Content Credentials and embedded source type dropped or invalidated | The delivered file's manifest, for example `c2patool <file>` |

Avoid repeated lossy recompression and uncontrolled variant-by-variant manual
transforms. A format can decode correctly while still being a poor choice for
the visual: line art, gradients, transparency and footage stress codecs
differently.

## A family is judged together

Numeric consistency is only a starting point. Compare occupied area, baseline,
silhouette, outline, light direction, texture and optical weight across variants.
A dark-mode icon can need a deliberate contrast adjustment rather than simple
inversion. Localized text can alter the frame. State changes should remain
recognizable without accidentally redesigning the subject.

For motion, compare continuity through time: posture, geometry, camera,
acceleration, easing, loop seam and entry/exit. Match captions and audio to actual
events. A contact sheet can reveal identity drift; what it and a poster frame
cannot show, and how to judge motion you cannot play, is in the skill's motion
section.

## Package the chosen work, not the production mess

One canonical filename per receiving role makes integration intelligible.
Include the required themes, states, densities, locales or aspect ratios and
the source relationships needed to maintain them. Rejected candidates and
repair intermediates are useful during production but do not belong in runtime
paths unless the product explicitly consumes them.

[Provenance and labelling](provenance-and-labelling.md) supports rights,
disclosure, reproduction and diagnosis, and ends with a bundle-manifest example
for many variants or several contributors; a one-off asset usually needs a
source note rather than a bundle manifest.
The [quality rubric](visual-qa-rubric.md) supplies concrete fault lines when
selection is difficult. The receiving product remains the judge of fitness.
