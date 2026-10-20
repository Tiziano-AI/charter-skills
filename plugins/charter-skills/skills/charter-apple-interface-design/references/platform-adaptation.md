# Platform Adaptation

Use this file when the task spans multiple Apple platforms or specifically targets watchOS or tvOS.

## Source Anchors

- HIG root:
  <https://developer.apple.com/design/human-interface-guidelines/>
- HIG Designing for watchOS:
  <https://developer.apple.com/design/human-interface-guidelines/designing-for-watchos>
- HIG Designing for tvOS:
  <https://developer.apple.com/design/human-interface-guidelines/designing-for-tvos>
- HIG Designing for visionOS:
  <https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos>
- Apple new design gallery:
  <https://developer.apple.com/design/new-design-gallery/>
- tvOS What's New:
  <https://developer.apple.com/tvos/whats-new/>

## Shared meaning, different action costs

Carry recognizable identity and task meaning across platforms. Density,
navigation and input should change when viewing distance, precision, reach or
available attention changes. Pixel parity can create interaction disparity.

## watchOS

A glance has little time for interpretation. Make the current state and useful
action recognizable without sustained reading; move richer comparison to a
surface that supports it. The crown and system controls can provide precise
input without demanding tiny touch targets. A crowded command cluster spends
attention locating an action rather than completing it, while a phone's full
navigation structure can overwhelm the occasion.

## tvOS

Focus is the navigation model, not a decoration added to a touch layout.
Grouping should make the next directional move predictable and preserve a
useful focus position on return. Viewing distance increases the cost of small
text and subtle state cues. Clear spacing and emphasis help when they make the
focus path legible; translucency cannot compensate for an unpredictable path.
Phone toolbar density generally carries the wrong assumptions about proximity
and input precision.

## Cross-Platform Review Questions

- Did the design keep the same meaning while adapting layout and interaction model per platform?
- Is the densest platform dictating the design for the others?
- Did any surface import the wrong platform's chrome out of convenience?
