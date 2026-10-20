# Icons And Symbols

Use this file when the task touches app icons, toolbar symbols, menu symbols, or icon-versus-text decisions.

## App Icons

Primary sources:

- <https://developer.apple.com/design/whats-new/>
- <https://developer.apple.com/videos/play/wwdc2025/220/>
- <https://developer.apple.com/videos/play/wwdc2025/361/>
- <https://developer.apple.com/design/human-interface-guidelines/app-icons>

Rules:

- Use the current Icon Composer release appropriate to the shipping toolchain for the final
  material-aware build. Check whether the chosen format and features are supported by the shipping
  toolchain; a beta listing is not a stable availability guarantee.
- For layered, material-aware icons, keep reflections, highlights and shadows
  that the system should supply out of the artwork. Flatter, frontal layers
  help that construction; they do not forbid illustrative or dimensional
  identity when the subject depends on it.
- Keep overlaps bold and silhouettes readable at small sizes.
- Judge background color and gradient by separation under the supported icon
  appearances. A softened background can help material layers read; it is not
  a universal replacement for a deliberate high-contrast identity.
- Keep the artwork optically balanced inside the current grid and mask.

## SF Symbols And Action Semantics

Primary sources:

- <https://developer.apple.com/design/whats-new/>
- <https://developer.apple.com/videos/play/wwdc2025/356/>
- <https://developer.apple.com/videos/play/wwdc2025/337/>
- <https://developer.apple.com/design/human-interface-guidelines/sf-symbols>

Use a symbol when:

- the action is standard and recognition speed matters;
- the meaning stays stable across platforms;
- the surrounding context makes the verb obvious.

Use text when:

- the action could be misread;
- the action changes mode or scope;
- the label carries legal, destructive, or confirming meaning.

Rules:

- Use the same symbol for the same meaning across surfaces.
- Do not create families of near-duplicate icons for closely related menu actions.
- Keep symbol weight and scale aligned with surrounding typography and control density.
- Use expressive or animated symbol features only when they reinforce state or task feedback.
- Verify the deployment target and symbol availability before depending on a
  new symbol or effect; current tool availability is not OS availability.

## Menus And Toolbars

- Put symbols where recognition speed matters.
- Do not force symbols into every text action.
- Keep the same symbol semantics between menus, toolbars, and context surfaces.
- If a toolbar button would be clearer as text, let it remain text instead of inventing a weak icon.
- Separate symbol-only quick actions from text-labeled confirmatory actions instead of blending them into one cluster.
- Use an icon-only status action only when its meaning and destination are
  understandable; otherwise add a label or contextual explanation.
