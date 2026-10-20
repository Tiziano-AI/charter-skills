# Pepper&Carrot composition study

An editable study in adapting an existing illustration to square, wide and
vertical reading invitations. The copy and layouts are new illustrative
work, not official Pepper&Carrot campaign material.

## Original and rights

The unchanged [original JPEG](pepper-carrot-e26-p01-original.jpg) is the
artwork-only rendering of **Pepper&Carrot, episode 26: Books Are Great,
page 1**, by **David Revoy**, licensed under
[Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).
It is 2481 × 3503 pixels; SHA-256:
`6e8c77960393e55bf52915b13ee12346a3409bff50b83953bf68e6caec21db4b`.

- [Episode source and credits](https://www.peppercarrot.com/en/webcomic-sources/ep26_Books-Are-Great.html)
- [Original artwork-only download](https://www.peppercarrot.com/0_sources/ep26_Books-Are-Great/hi-res/gfx-only/gfx_Pepper-and-Carrot_by-David-Revoy_E26P01.jpg)
- [Author's attribution guidance](https://www.peppercarrot.com/en/documentation/120_License_best_practices.html)
- [External Krita art archive](https://www.peppercarrot.com/0_sources/ep26_Books-Are-Great/zip/ep26_Books-Are-Great_art-pack.zip)

The Krita archive is a pointer for a task that actually needs painting layers;
it is not bundled, inspected or required to edit these layouts. The supplied
JPEG is flattened artwork, not a layered painting.

The artwork's applicable creator credit is David Revoy. The source episode
also credits his scenario; script-doctor Craig Maloney; beta-readers Jihoon
Kim, Jookia, Midgard, Nicolas Artance, Popolon, R J Quiralta, Valvin, xHire and
Zeograd; and English proofreading by Craig Maloney and CalimeroTeknik. The
study uses neither original dialogue nor translated lettering. Hereva was
created by David Revoy, with Craig Maloney as lead maintainer; writing
contributions by Craig Maloney, Nicolas Artance, Scribblemaniac and Valvin;
corrections by Alex Gryson, CGand, Hali, Marno van der Maas, Moini and Willem
Sonke. These credits identify the source, not endorsement of this study.

## Editable derivatives

Charter's study adds copy, typography, backgrounds, panel extraction, uniform
scaling and, for the vertical version, a new panel sequence. It does not
repaint the artwork, generate replacement pixels, isolate subjects, or use
the original dialogue. Attribution remains on the rendered study images.
Keep this source-and-change note with reused files.

| Source | Rendered preview | Canvas | Composition |
| --- | --- | --- | --- |
| [square.svg](square.svg) | [square.png](square.png) | 1200 × 1200 | Journey above a separate headline area |
| [wide.svg](wide.svg) | [wide.png](wide.png) | 1600 × 900 | Copy and intact journey in adjacent columns |
| [vertical.svg](vertical.svg) | [vertical.png](vertical.png) | 1080 × 1920 | Reader beside copy, then the intact journey |
| [crop-comparison.svg](crop-comparison.svg) | [crop-comparison.png](crop-comparison.png) | 1600 × 1000 | Two rejected crops for this brief, with their source windows |

The three layout SVGs have named `art`, `copy`, `paper` and `credit` groups,
also labelled as Inkscape layers. Text remains text; the art layer links the
unchanged local JPEG. Keep it beside the SVG. The `journey-panel` and
`reader-panel` nested SVGs define the viewports in original-image coordinates:

- Journey: `104 104 2276 1536`.
- Reader: `104 1710 744 1690`.

Changing a viewport changes the visible panel, not the source pixels.
Changing its output dimensions with `preserveAspectRatio="xMidYMid meet"`
keeps proportions rather than stretching the art. Text uses Georgia and
Arial with generic serif/sans-serif fallbacks; inspect line fit after a font
substitution. A flattened PNG is for viewing, not for recovering this
editability. A browser's HTML `img` embedding may block an SVG's linked JPEG;
use the PNG for that placement or open the SVG as a document.

## Render

From this directory, with librsvg's `rsvg-convert` installed:

```sh
rsvg-convert square.svg -o square.png
rsvg-convert wide.svg -o wide.png
rsvg-convert vertical.svg -o vertical.png
rsvg-convert crop-comparison.svg -o crop-comparison.png
```

The PNGs are retained visual references rendered from these SVGs. Rendering
does not add C2PA signing or establish watermark state. This resource teaches
layout composition and derivation from finished art; it does not demonstrate
painting construction, layered subject editing or motion production.
