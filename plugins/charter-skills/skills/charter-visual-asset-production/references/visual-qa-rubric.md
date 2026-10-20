# Visual Quality Rubric

Use this to select, repair, or reject visual assets in their intended product context.

When many candidates compete, turn the brief into yes-or-no checks before judging taste: one
subject, the named action, no logo, the exact wording, the safe area clear. Ask a dependent
question only when its premise holds; there is no point checking the hand's pose on a candidate
with the wrong subject. Judge the whole at its intended display size and background. Use zoomed
crops to inspect suspected defects in faces, hands, text or edges, then return to the whole;
a corrected detail does not settle the asset's fitness for its role.

## Creative fitness

- The subject, action, mood, and visual hierarchy serve the product role.
- Composition and negative space accommodate crop, text, controls, or neighboring content.
- Palette, material, lighting, texture, and detail level match the intended register.
- The image has a deliberate focal point rather than uniform generated detail.
- Unwanted text, logos, watermarks, props, limbs, panels, shadows, or background subjects are absent.

## Identity and family coherence

- Subject silhouette, proportions, face, markings, wardrobe, object design, and palette remain
  stable where identity is required.
- Variants share a coherent world, camera, lighting, material, outline, and texture language.
- State and direction changes are meaningful without accidental redesign.
- Mirroring or cropping preserves handedness, logos, text, asymmetrical markings, light direction,
  and semantic direction.

## Geometry and edges

- Perspective, anatomy, joints, hands, faces, straight lines, circles, and repeated structures are
  plausible for the style.
- Crops preserve the focal subject and safe area at every required aspect ratio.
- Masks and transparent edges are clean on relevant backgrounds, without matte halos or missing
  translucent detail.
- Alignment, padding, baseline, optical weight, and occupied area are consistent across icon or
  sprite families.

## Technical fitness

- Dimensions, density, format, color space, alpha mode, duration, frame rate, and file-size budget
  match the receiving pipeline.
- Compression does not create banding, ringing, block artifacts, color shifts, or unreadable detail.
- The target application decodes, renders, animates, and loops the asset correctly.
- Filenames and variants map unambiguously to product roles.
- The delivered file's credential state has been checked against the preservation requirement,
  and its placement carries the required audience-facing disclosure.

## Small assets and chrome

Inspect icons, thumbnails, badges, screenshots, and package chrome at their actual small and large
sizes. Check contrast, optical balance, recognizability, safe padding, masked rendering, and both
light and dark contexts. Screenshots should show current real product state rather than generic
marketing decoration.

## Motion

- Movement has coherent timing, continuity, weight, easing, and camera behavior.
- Loops do not pop, drift, or duplicate frames unless intentional.
- Subject identity and geometry remain stable across frames.
- Captions, audio, speech, and visual events remain synchronized.
- Poster frames represent the asset honestly and crop well.

## Decision

- **select:** visually and technically fit for the intended role;
- **repair:** one bounded defect can be corrected without redesigning the source;
- **reject:** the creative source, identity, or composition is wrong enough that repair is wasteful;
- **uninspected:** no suitable target-size or playback inspection occurred.

Name concrete defects by location and consequence. Reinspect repaired assets and adjacent variants;
a local fix can drift the family.
