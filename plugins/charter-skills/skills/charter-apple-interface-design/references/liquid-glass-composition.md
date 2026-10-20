# Liquid Glass composition

Use material to clarify controls and their relation to content. A request for
richer translucency does not imply that every surface should become glass.

## Material and sampling

Start with the system component that owns the interaction. Standard bars and
presentations already coordinate appearance, geometry and accessibility.
Custom glass is useful for an elevated control or group not served by them.
Apple's HIG places Liquid Glass in the functional layer of controls and
navigation above content; standard materials differentiate within content.
That distinction does not require a task-focused content surface to become
translucent.

Consider what the material samples, not just the foreground color. Dynamic
media, text behind controls and adjacent glass can change legibility. Related
custom elements may need a shared container so sampling and merging are
coherent; unrelated actions should not become one visual group merely because
morphing is possible.

- Regular glass suits ordinary elevated controls.
- Clear glass can keep media visible behind a compact overlay, but needs
  inspection against the actual range of content.
- Tint can signal emphasis or state. Choose emphasis by meaning; there is no
  universal numerical quota for tinted controls.

Avoid stacking independent blur and glass layers to imitate a native material.
When content or grouping is unclear, another effect usually amplifies the
problem. A stable contrasting support may be more useful than maximum
transparency.

## Grouping and continuity

Keep persistent commands, contextual actions and transient presentations
distinguishable. Shape, spacing and placement should establish the relationship
before motion does. Container-relative corners can preserve nesting as sizes
change.

Choose motion for the transition: appearing, expanding, replacing or moving.
Source-anchored motion helps when the origin explains the destination.
A detached presentation can still be appropriate when it has no meaningful
source control. Avoid motion chains that compete with the work.

Custom interaction needs visible rest, focus, activation and disabled states
where applicable, but not an identical four-state animation protocol for every
control. Reduced motion and transparency should preserve meaning rather than
become a degraded afterthought.

## Reading the result

Inspect the changed material over representative backgrounds and at the
relevant size and appearance. Look at label contrast, grouping, control
affordance, content occlusion and perceived stability. Distinguish static
visual calibration from working interaction.

If the design feels detached, fix placement and grouping. If contrast fails,
fix foreground/background separation. If motion disorients, simplify the
transition. Do not keep adjusting tint to compensate for the wrong hierarchy.

## Official foundations

- <https://developer.apple.com/design/human-interface-guidelines/materials>
- <https://developer.apple.com/videos/play/wwdc2025/219/>
- <https://developer.apple.com/videos/play/wwdc2025/356/>
- <https://developer.apple.com/videos/play/wwdc2025/323/>
- <https://developer.apple.com/videos/play/wwdc2025/284/>
- <https://developer.apple.com/videos/play/wwdc2025/310/>
- <https://developer.apple.com/design/human-interface-guidelines/accessibility>

Consult the current framework authority in [official sources](official-sources.md)
for implementation and availability. The [linked official examples](visual-reference.md)
illustrate older material examples, not current API behavior.
