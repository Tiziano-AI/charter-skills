# Reference assets

These are unmodified upstream assets, retained for material, lighting and
export inspection. Their licenses permit redistribution. Neither is authored
by Charter, and their presence does not establish that a renderer supports
their features.

## Toy Car

[ToyCar.glb](toy-car/ToyCar.glb) is the exported Khronos glTF sample by
Guido Odendahl (initial car model) and Eric Chadwick (extensions and scene
composition). It provides clearcoat,
transmission, sheen and texture-transform examples, three meshes, three
materials and eight cameras. Its images and buffer data are embedded.

This GLB is a finished asset reference, **not modeling history**: it does not
retain the original DCC modifier stack, construction process or editable
authoring project. An importer's reconstruction is not that original project.

- Upstream repository revision: `edc7c9e67c639d230715049ee31f9a96a6babbbe`.
- [Pinned asset download](https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Assets/edc7c9e67c639d230715049ee31f9a96a6babbbe/Models/ToyCar/glTF-Binary/ToyCar.glb).
- [Pinned authorship and license metadata](https://github.com/KhronosGroup/glTF-Sample-Assets/blob/edc7c9e67c639d230715049ee31f9a96a6babbbe/Models/ToyCar/metadata.json).
- [Pinned upstream license](https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Assets/edc7c9e67c639d230715049ee31f9a96a6babbbe/Models/ToyCar/LICENSE.md), preserved unchanged as [LICENSE.upstream.md](toy-car/LICENSE.upstream.md).
- GLB license: **CC0-1.0**. The upstream license notice itself is
  **CC-BY-4.0**, attributed here to KhronosGroup/glTF-Sample-Assets and linked
  to its exact source. Logos and trademarks are excluded by that notice.
- Git blob SHA-1 verified against GitHub:
  `6b3eaab83218894ab27bcf48fcc9a0f7a04be45e`.

## Studio Small 09

[studio_small_09_1k.exr](studio-small-09/studio_small_09_1k.exr) is the
1024 × 512 HDR environment by **Sergej Majboroda**, published by Poly Haven.
It supplies a compact studio-lighting reference. The 1k variant retains HDR
values but cannot supply the background detail of the higher-resolution
variants; no tone mapping or format conversion has been applied here.

- [Asset and author](https://polyhaven.com/a/studio_small_09).
- [Exact variant download](https://dl.polyhaven.org/file/ph-assets/HDRIs/exr/1k/studio_small_09_1k.exr).
- License: **CC0-1.0**, established by the asset page and
  [Poly Haven's asset license](https://polyhaven.com/license).
- [File metadata](https://api.polyhaven.com/files/studio_small_09): upstream
  MD5 `d85346bc4f0d041d27393d5f9aee211c`, verified against the downloaded bytes.
- [Asset metadata](https://api.polyhaven.com/info/studio_small_09): observed
  `files_hash` `ffa1de6f4c30e34f97f33af13411c4b4a08543d1`. This is upstream's
  asset-file-set identifier, not a claimed Git commit. Poly Haven exposes no
  immutable revision in this download URL; the SHA-256 below pins this copy.

## Retained bytes and license texts

The upstream files are retained byte-for-byte, including the notice and canonical
Creative Commons legal texts. The legal texts apply as described above, not
as one blanket license for this directory.

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `toy-car/ToyCar.glb` | 5,422,412 | `01a60862de55cd4b9f3acfab0b0def86451800f9c42467fcd61052c16cb9838c` |
| `studio-small-09/studio_small_09_1k.exr` | 1,319,434 | `44dcbed056512ecd8afd2a3d7ba73d2dd4c24694d0c72005fafcb2469bbc8fd4` |
| `toy-car/LICENSE.upstream.md` | 911 | `6e7c41dba03a561a67197a5aba92219bcc462806d69d13d8aba1c0ccbe183253` |
| `licenses/CC0-1.0.txt` | 7,048 | `a2010f343487d3f7618affe54f789f5487602331c0a8d03f49e9a7c547cf0499` |
| `licenses/CC-BY-4.0.txt` | 18,657 | `9ba9550ad48438d0836ddab3da480b3b69ffa0aac7b7878b5a0039e7ab429411` |

- [Local CC0-1.0 legal text](licenses/CC0-1.0.txt), downloaded from
  [Creative Commons](https://creativecommons.org/publicdomain/zero/1.0/legalcode.txt).
- [Local CC-BY-4.0 legal text](licenses/CC-BY-4.0.txt), downloaded from
  [Creative Commons](https://creativecommons.org/licenses/by/4.0/legalcode.txt).

Header inspection confirms glTF 2.0 framing and embedded resources for the
GLB, and a 1024 × 512 data/display window for the EXR. These structural checks
are not a visual render or an import/export round-trip test.
