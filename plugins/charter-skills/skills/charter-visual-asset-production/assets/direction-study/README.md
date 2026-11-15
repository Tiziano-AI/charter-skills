# Bell foundry: directions and grades

Every image is AI-generated concept work for a fictional, unnamed magazine
commission, not a record of any foundry. The commission is a 3:2 landscape
cover for a long feature on a working bell foundry; the picture's idea is open.

[The comparison plate](plate.jpg) offers three different pictures in its upper
row and repeats one picture in three colour treatments below. The lower row
is useful when the picture is already chosen and only its treatment is open.
One bare-prompt generation supplies that row; it is a sample, not evidence of
how often a generator chooses this scene.

The [direction sheets](../../references/direction-study.md) explain the
propositions and their relationship to foundry practice.

## Files and editability

- [plate.jpg](plate.jpg): 2304 × 1568 px, with each picture at 720 × 480 px.
  The JPEG is the reference render, encoded at quality 89 with 4:4:4 sampling.
- [plate.svg](plate.svg): editable source, with relative image links and live
  text. Its stylesheet references `fonts/IBMPlexSans-Regular.ttf` through a
  relative `@font-face` URL, without an embedded copy. The images and `fonts/`
  directory stay beside the SVG when it moves. SVG applications differ in
  support for linked web fonts.
- [pour.jpg](pour.jpg), [form.jpg](form.jpg) and [sound.jpg](sound.jpg): the
  three selected directions.
- [expected-source.jpg](expected-source.jpg): the untinted bare-prompt image.
- [expected-blue.jpg](expected-blue.jpg),
  [expected-gold.jpg](expected-gold.jpg) and
  [expected-teal.jpg](expected-teal.jpg): three grades of that same image.
- [derive-grades.py](derive-grades.py): the reproducible colour operation.

All seven picture JPEGs are 1080 × 720 px and under 282 KB (decimal). The
selected native PNGs are uniformly reduced from 1536 × 1024 px with Pillow's
Lanczos resampler, without cropping, retouching or generative editing. JPEG
encoding uses quality 88, 4:4:4 sampling, optimisation and progressive scans.
These compact derivatives are not untouched generation masters.

The plate uses a cool steel-grey ground, dark ink and one sans face, IBM Plex
Sans, with plain sentence-case captions. These support a working comparison
sheet rather than imitating a finished magazine's identity.

## What the pictures settle

The takes settle propositions, framing, manner, light and palette. They do not
establish the design of a mould, a lifting system or a tuning machine.

- **Pour:** the ladle, inlet and refractory surfaces are invented. The crop
  does not establish the full crane suspension, mould assembly or protective
  arrangement; it is not a safety illustration.
- **Form:** the print abstracts the strickle's working clearance and linkage.
  It shows an external contour, not the internal masonry, cope lining or
  assembled casting cavity. Its profile is illustrative, not a measured bell
  or tool pattern.
- **Sound:** the crop hides much of the bell's clamping and tool support. The
  bell profile and turning bands are invented; the bands do not prescribe
  where metal is removed to adjust a particular partial. A mallet and a
  listening pose do not establish which partial is being tested.
- **Expected picture:** the composition assembles a pour, workers and finished
  bells into workshop spectacle. It does not resolve a complete mould inlet
  or lifting arrangement, and the decorative detail is generated invention.

None is an audited account of a specific foundry. A feature about a real
foundry uses photographs made there. A generated photograph published as that
foundry claims a fidelity it cannot have.

## Generation record

The route is the native `image_gen.imagegen` tool. All four retained source
generations date from 15 November 2026. Each call is a fresh generation with
`transparent_background: false` and no reference images. Only original prompts
are transferred; no foundry photographs or third-party artwork are inputs.

The tool exposes no model, seed, quality or pixel-dimension control. It returns
no exact model ID, rewritten prompt or seed. Each output is a 1536 × 1024 PNG.
The times below are UTC clock readings taken before the respective calls, not
completion times. The exact submitted prompts follow without rewording.

### Pour → pour.jpg

Candidate `pour-3`; pre-call reading `2026-11-15 18:14:47 UTC`.
Native output `exec-3a31d59d-77b4-45d9-aa85-5eccc1bc62a5.png`.
Original SHA-256:
`b2605d4cf6c526109578304245628ab8b4aa977895166407ce214ae0ccd8ad99`.

```text
Use case: photorealistic-natural.
Asset type: horizontal 3:2 magazine cover concept, fictional unnamed bell foundry, AI-generated image without lettering.
Primary request: the weight above the bright thread. A close lateral view from the safe side of a casting pit, about 2.5 metres from the pour, with the dark refractory-lined bowl of a crane-carried ladle occupying the upper half of the frame. Its stout steel trunnion and hanging bail visibly carry the load. A slender white-hot bronze stream crosses the darkness down to a small pouring cup on the crown of a closed iron bell mould bedded in sand. The bell is being cast mouth down inside; there is no visible liquid bell silhouette. A single worker's shield and shoulder, small and cropped at the far side, catch the low reflected light.
Light: night inside a working shop; the liquid in the ladle and falling stream are the sources. Their orange light grazes the blackened cup, the ladle lip and a thin patch of sand; shadows remain deep neutral black. Little smoke, no sunbeams.
Matter: refractory grit, soot, rough black iron, grey work clothes and brilliant liquid bronze. Camera at the worker's chest height; the industrial containment feels more important than spectacle. No text, logos, spurious decorative mechanisms or spark shower.
```

### Form → form.jpg

Candidate `form-1`; pre-call reading `2026-11-15 18:17:28 UTC`.
Native output `exec-9a7fde62-a45f-4186-87b7-ea7e0c604e34.png`.
Original SHA-256:
`0f678c8a890fc92f6ed95ab667f4cfb0130b77db6c74a4ad515d0a25a26018f6`.

```text
Use case: illustration-story.
Asset type: a horizontal 3:2 cover concept for a long magazine feature about a fictional unnamed working bell foundry; AI-generated editorial illustration, image only.
Primary request: a bell begins as earth and a measured curve. Make a forceful two-ink relief print, using carved-edge silhouettes, flat ink masses, economical hatching and the small irregular gaps of an actual cut block, not a photograph with paper texture. A large mouth-down bell-mould core of dry loam on a square baseplate is seen square-on from the moulder's eye height, two metres away. It has no hollow mouth or clapper: this is the solid earthen form for a bell's inside. Beside its right-hand contour, a flat dark strickle template on a simple pivoting arm describes that same concave-to-flared profile. A straight vertical spindle at the centre line and the template's curved cutting edge make the geometry evident. A second iron cope shell is a quiet cropped half-shape at the far edge.
Light logic: a workshop doorway at mid-morning gives one hard left-to-right raking shadow; translate it into solid ink shapes rather than rendered shading.
Palette: graphite-black ink for iron and shadow, burnt-red iron-oxide ink for loam, cool light-grey unprinted stock. The earthen core is large and asymmetric in the landscape, the measured contour is the decisive sharp line. Tool marks follow the curved sweep, the ground remains mostly empty. No writing, lettering, measurement marks, gradients, glow or decorative musical notes.
```

### Sound → sound.jpg

Candidate `sound-3`; pre-call reading `2026-11-15 18:19:20 UTC`.
Native output `exec-eec2e500-bd69-48d2-aafa-ed433aaa46f2.png`.
Original SHA-256:
`6afab751994e2ed56bfdba1a7ba16334249e343db394c0a76fbd5d574dcb24d4`.

```text
Use case: photorealistic-natural.
Asset type: horizontal 3:2 magazine cover concept, AI-generated, fictional unnamed working bell foundry.
Primary request: listening to the missing metal. From a safe raised position about two metres away, look steeply down into a large bronze church bell mounted mouth UP on the circular table of a stopped vertical tuning lathe. Its inner concentric cutting rings and thick lip make a huge off-centre near-circle cropped by the bottom and left edges of the landscape. A small soft-faced striking mallet rests in the tuner's bare hand just beyond the far lip; only the sleeve, hand and a little profile are seen at upper right as the tuner listens. At upper left, the dark solid side-mounted tool carriage and retracted boring bar stand clear. A modest scatter of short bronze chips in an oily tray at right shows what was removed. No central shaft through the bell and no second bell inside it.
Light: broad cool noon skylight falling from upper left into the bronze cavity; the interior is pale metallic ochre and shadow, no furnace or glow. Keep the cutting marks as the most legible fine detail, not every background bolt.
Materials and manner: an unembellished editorial photograph with real worn machine paint, quiet grey wall, faded indigo sleeve and hard bell bronze; a felt pause rather than workshop spectacle. No labels, lettering, numbers, sparks, musical graphics or decorative inscriptions.
```

### Bare request → expected-source.jpg and all three grades

Candidate `expected`; pre-call reading `2026-11-15 18:13:33 UTC`.
Native output `exec-6deb79e1-5b1c-432e-b27a-8766ae01798d.png`.
Original SHA-256:
`83cdc2b67b95fb805edee96b5c5d09c1fecadeb84e865227c07dfdc2d29d39a2`.

```text
A cover image for a feature about a bell foundry. Landscape 3:2. Image only, without lettering.
```

The blue, gold and teal files inherit this single generation record. There
are no separate prompts, seeds or generation calls for these three files.

### Provenance signals before and after derivation

Each of the four native PNGs contains a `caBX` chunk with `c2pa` and `jumb`
markers: embedded Content Credentials/JUMBF data. This is a binary-container
observation, not signature or trust validation. No C2PA verification tool is
available in this run. Readable assertion data in the pour original names
`ChatGPT`, a generic `gpt-image` version label, `OpenAI Media Service API` and
an AI-media source type. It does not identify an exact generation model.
It also includes `c2pa.watermarked.unbound`; the watermark itself is not
detected or verified here.

All seven picture JPEGs contain JFIF data, but no detected C2PA/JUMBF,
EXIF or XMP provenance payload. Resizing and re-encoding do not carry the
native credential container into these files. Absence of that metadata does
not establish absence of an invisible watermark. The SVG and JPEG plate do
not assert a signed derivation chain; their disclosure is visible text.
The generation records here preserve attribution but do not replace signed
Content Credentials.

## Deterministic grades

`derive-grades.py` reads the saved untinted JPEG once, converts its RGB pixels
to one 8-bit luminance plane, then maps that same plane through each palette.
Pillow's `ImageOps.colorize` uses stops at 0, 128 and 255:

| Grade | Shadow (0) | Middle (128) | Highlight (255) |
| --- | --- | --- | --- |
| Blue | `#102331` | `#617d9d` | `#dbe9f7` |
| Gold | `#261e14` | `#8d7642` | `#f6e5b7` |
| Teal | `#10292a` | `#467d7c` | `#d7f0e7` |

No crop, warp, retouching or further generation occurs. The palette lookup
changes colour, not the position of any feature. JPEG encoding can slightly
alter decoded colour values. Reproduction with Python 3 and Pillow 13.0.0 on
macOS on Apple silicon produces grade files byte-identical to the bundled
ones:

```sh
python3 /path/to/derive-grades.py /absolute/path/to/new-folder
```

The script reads its source beside itself and writes only to the new or empty
folder it is given, so it works from any working directory and leaves the
bundled grades in place for comparison. Reproduction across other
Pillow/JPEG-library versions need not be byte-identical.

## Sources for the practice

These sources inform the directions, not the invented architecture or
machinery. No source image is reproduced or sent to the generator.

- [Central Council of Church Bell Ringers: Bells and bellringing](https://archive.cccbr.org.uk/services/pr/bells-and-bellringing/)
  describes loam shaped by a strickle rotating around an axis, the inner core
  and outer cope, drying, assembly, pouring and interior tuning. Its account
  supplies the relation between measured contour and earthen form.
- [B. A. Sunderlin Bellfoundry: Bell Tuning](https://sunderlinfoundry.com/bell-tuning/)
  describes selective interior metal removal on a lathe and the hum, prime,
  tierce, quint and nominal partials. Its account supplies the quiet tuning
  direction: a note depends on removing material, not adding decoration.
- [John Taylor & Co: Drinkstone, Suffolk, All Saints Parish Church](https://taylorbells.co.uk/drinkstone-suffolk-all-saints-parish-church/)
  records casting, fettling, facing and tuning as distinct stages. Fettling
  belongs between casting and tuning even though this plate does not show it.
- [Heritage Crafts: Bell founding](https://heritagecrafts.org.uk/craft/bell-founding/)
  describes mouth-down casting, dry moulds, the pouring header and variation
  in mould materials. Its practitioner account notes self-setting sand in
  modern Taylor's cores and loam in outer moulds. Loam moulding is one real
  method, not a universal account of all present-day foundries.

## Fonts and licence

The unmodified IBM Plex Sans Regular file is bundled under [fonts/](fonts/).
Copyright © 2017 IBM Corp., with Reserved Font Name “Plex”; the font uses the
SIL Open Font License 1.1. The complete licence is
[fonts/OFL.txt](fonts/OFL.txt), from the
[IBM Plex repository licence](https://raw.githubusercontent.com/IBM/plex/master/LICENSE.txt).
The [IBM Plex project](https://github.com/IBM/plex) is the font's source home.
