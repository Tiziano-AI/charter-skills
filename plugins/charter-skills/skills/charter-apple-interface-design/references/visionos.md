# visionOS

Use this file when the task includes windowed visionOS UI, ornaments, or glass-backed controls in a spatial context.

## Source Anchors

- HIG Designing for visionOS:
  <https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos>
- `ornament(visibility:attachmentAnchor:contentAlignment:ornament:)`:
  <https://developer.apple.com/documentation/swiftui/view/ornament(visibility:attachmentanchor:contentalignment:ornament:)>
- `glassBackgroundEffect(in:displayMode:)`:
  <https://developer.apple.com/documentation/swiftui/view/glassbackgroundeffect(in:displaymode:)>
- `glassBackgroundEffect(displayMode:)`:
  <https://developer.apple.com/documentation/swiftui/view/glassbackgroundeffect(displaymode:)>

## Windowed spatial structure

- Start from the window, ornament, and system container model.
- Keep primary content spatially stable and place controls near the content they affect.
- Use glass-backed surfaces for interface chrome and support UI, not for volumetric content itself.
- Test legibility, hover states, comfortable spacing, and orientation against varied surroundings.

## Strong Defaults

- Prefer ornaments for persistent control clusters that belong near window content.
- Use glass background effects to separate interface surfaces from the scene when structure needs help.
- Keep controls compact, grouped, and context-bound.
- Do not transplant iPhone tab bars or macOS toolbar density into space without a spatial reason.
- If the task becomes immersive or volumetric, acknowledge that the problem has moved beyond this skill's primary 2D-first scope.

## Review Questions

- Are ornaments attached to the content they control?
- Does the window remain legible against varied surroundings?
- Are hover and focus cues clear without motion overload?
- Is the UI still fundamentally a windowed app surface, or does it require a broader spatial redesign?
