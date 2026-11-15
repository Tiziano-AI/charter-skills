# SALÓN RECREATIVO frontage: source, licences and render settings

## The scene is invented

The frontage documents no real place. There is no SALÓN RECREATIVO at this
address or any other that the study refers to; the street, the block, the
neighbouring shops and the history of refits (a 1958 billiard hall, signs added
in 1972, 1986, 1994 and 2015) were made up for this study. Its particulars come
from what seaside arcades of this kind accumulate, not from photographs or
measurements of one.

The model, procedural materials, builder script, renders and comparison sheet
were authored for Charter. No photographs, image textures, HDRIs, downloaded
models or generated imagery are used: every surface is a Blender node material
built by [the script](../../scripts/build_arcade_frontage_study.py). The only
third-party material is the typefaces below.

## Typefaces

The five lettering typefaces are under the SIL Open Font License 1.1. They are
bundled unmodified in `fonts/`, each with its licence text, and packed into the
native file so it opens with its lettering. They were taken from the
`ofl/<family>/` folders of the [google/fonts](https://github.com/google/fonts)
repository. Tilt Neon's upstream file name, `TiltNeon[XROT,YROT].ttf`, is
shortened here to `TiltNeon-XROT-YROT.ttf`; its bytes are unchanged.

| Typeface | File | Copyright | Used for |
| --- | --- | --- | --- |
| Alfa Slab One | `fonts/alfaslabone/AlfaSlabOne-Regular.ttf` | Copyright 2016 The Alfa Slab One Project Authors, with Reserved Font Name "Alfa Slab" | 1958 painted BILLARES · FUTBOLINES |
| Tilt Neon | `fonts/tiltneon/TiltNeon-XROT-YROT.ttf` | Copyright 2019 The Tilt Project Authors | 1972 JUEGOS tubes |
| Racing Sans One | `fonts/racingsansone/RacingSansOne-Regular.ttf` | Copyright (c) 2012, Pablo Impallari, Rodrigo Fuenzalida, with Reserved Font Name Racing Sans | 1986 lightbox SALÓN RECREATIVO |
| Neonderthaw | `fonts/neonderthaw/Neonderthaw-Regular.ttf` | Copyright 2014-2021 The Neonderthaw Project Authors | Bar tube |
| Bebas Neue | `fonts/bebasneue/BebasNeue-Regular.ttf` | Copyright © 2010 by Dharma Type | SE ALQUILA bill |

The 2015 ABIERTO sign uses 5 × 7 dot glyphs drawn in the script, not a font.
The sheet's labels use Inter as shipped inside Blender (SIL Open Font License
1.1, Copyright 2020 The Inter Project Authors); it is loaded from the Blender
installation and not bundled here.

SHA-256 of the bundled bytes:

| File | SHA-256 |
| --- | --- |
| `alfaslabone/AlfaSlabOne-Regular.ttf` | `28664afa698a3393bd5a29eec750230a0645c5301d62200e5f2d3a027fb2299d` |
| `alfaslabone/OFL.txt` | `e315abc82a78710c7242e2f2e6529651fd631d4d50e6ad98ea194f9b54c3d701` |
| `bebasneue/BebasNeue-Regular.ttf` | `08e4623805102d819f58601e46e345648846075e363b2ceb23313c2d1c83ec73` |
| `bebasneue/OFL.txt` | `72082f6cb4d04be2ecf7cc7d9e1e7d73787f0af8a5a278a47cade70c16b78341` |
| `neonderthaw/Neonderthaw-Regular.ttf` | `15a72ab630eb73ee922ad653783b81053cf381ef53bcc17a536f3c7fa8097184` |
| `neonderthaw/OFL.txt` | `1b6b1362683d5bb1f864615e723b4323a3c05de5dd020e0e448546135bab75de` |
| `racingsansone/RacingSansOne-Regular.ttf` | `8b5cada83e3e4692f624f1b583a069b34e457e07a4210ceddbb1133b3383673e` |
| `racingsansone/OFL.txt` | `cdcc959c42ab255b4cea4bd82f2db5c24a2da7ecabe615d02d5a5dba3716e446` |
| `tiltneon/TiltNeon-XROT-YROT.ttf` | `c22333dfd1cd14c2a612b36ea1c50ea13e5e9244181e5129a63c944a165823a0` |
| `tiltneon/OFL.txt` | `97941703cd5fb1d5e86a062c9463ed12a613dbfbab9961c333699bdb2d277321` |

## Render settings and device

The bundled renders came from Blender 5.2.2 LTS (build hash d13f752e3b9c) with
Cycles. Cycles' own device report (`--debug-cycles`) for every render read
"Path tracing on: Apple M4 Max (GPU - 40 cores) (Metal)"; for the two scene
renders it also read "Denoising on: Apple M4 Max (GPU - 40 cores) (Metal)".

| Setting | Directed | Default |
| --- | --- | --- |
| Resolution | 1920 × 1080 | 1920 × 1080 |
| Samples | up to 1024, adaptive threshold 0.008 | same |
| Denoiser | OpenImageDenoise on the GPU | same |
| Bounces (total, diffuse, glossy, transmission) | 8, 4, 4, 6; caustics off | same |
| View transform | AgX, look AgX - Punchy, exposure +0.3 | AgX, no look, exposure 0 |
| Camera | 1.5 m eye height at (-13.0, -7.6), level, aimed at (0.3, 0); 35 mm lens on a 36 mm sensor (54° across); lens shift 0.06 up | Blender's factory camera rotation (1.1093, 0, 0.8149 rad) and 50 mm lens on a 36 mm sensor (40° across), moved back along that axis to (17.25, -16.75, 14.56) to frame the frontage |
| Light | Only sources that belong to the place: lightbox, bulbs, tubes, LED, fluorescent interior, cabinet screens and marquees, lit windows, the portal's stair light, four lit gooseneck spot lamps (60 W each; the fifth is blown) and a dusk-sky world | One 24 m warm disc key (34 000 W, colour 1.0, 0.80, 0.58; azimuth -140°, elevation 42°, 60 m away), one 30 m cool disc fill (10 000 W, colour 0.60, 0.74, 1.0; azimuth -35°, elevation 18°), grey world 0.18 at strength 0.5, grey sweep |
| Materials | As authored, each with its own roughness | Linked copies of the same geometry; every material at roughness 0.5 with emission 0; the gooseneck lamps are left out with the other sign light |

Scene-linear emission strengths in the directed scene, before exposure: neon
tubes 0.75; lightbox white acrylic 2.6 and its printed lettering 1.0; bulbs 70;
fluorescent troffers 20; LED dots 1.2; cabinet screens 1.2 and marquees 1.0;
lit windows 1.2 (warm) and 0.5 (television). In the lossless directed render,
before JPEG encoding, no tube, LED or lightbox-lettering pixel reached 255 in
any channel. In the bundled `directed.jpg`, 2 of the 18,971 such pixels
sampled reach 255 in red alone, at edges beside a bulb and the white acrylic
where the encoding overshoots: (223, 149, 155) became (255, 156, 177) and
(227, 173, 166) became (255, 155, 140). Neither is white. Per-channel medians
in the bundled file: JUEGOS pink (196, 86, 121), Bar green (91, 160, 89),
lightbox lettering red (211, 72, 60), LED red (168, 21, 13).

The sheet is a separate Blender render: Cycles, Standard view transform, 32
samples without denoising, labels in Inter on a mid-grey ground (linear 0.25).
It is composed from the lossless renders, so its pictures are encoded once.

## Bundled files

`directed.jpg`, `default.jpg` and `directed-and-default.jpg` are JPEG at
quality 85 with full-resolution colour (4:4:4). The builder writes them from
lossless PNG renders, which it keeps in a temporary folder only while the sheet
is composed, using the OpenImageIO module that ships inside Blender (3.1.13 in
Blender 5.2.2). Blender's own JPEG output stores colour at half resolution
(4:2:0), which smeared the LED dots at any quality. The quality was chosen
against the lossless renders at 1:1, 2× and 4×. No quality from 70 to 95 showed
a difference at 1:1 or 2×; at 4× the LED dots begin to merge and halos form
around the sheet's text from 80 down, and 85 is the lowest that shows no more
than a faint trace there.

The bundled JPEGs were encoded, with the builder's own encoding function, from
the renders described above; the native file was rebuilt from the current
builder without rendering. A fresh run renders again, so its images differ from
these by sampling noise.

## Rebuild

From the package directory, with a new or empty output folder:

```sh
blender --background --factory-startup --python-exit-code 1 \
  --python scripts/build_arcade_frontage_study.py -- \
  --output /absolute/path/to/new-frontage --renders
```

It writes `arcade-frontage-study.blend`, `directed.jpg`, `default.jpg` and
`directed-and-default.jpg`. `--preview` renders both scenes at half size with
fewer samples and skips the sheet.
