"""Build the invented SALÓN RECREATIVO frontage: one directed render, one default.

blender --background --factory-startup --python-exit-code 1 --python this_file -- --output /new/directory --renders
The destination must be absent or empty. --renders writes directed.jpg,
default.jpg and the sheet directed-and-default.jpg; the lossless renders the
sheet is composed from live in a temporary folder and are not kept.

The materials and mesh parts are in arcade_frontage_parts.py, which must stay
beside this file. The lettering uses the SIL Open Font License typefaces
bundled beside the study (assets/arcade-frontage-study/fonts) and dot glyphs
drawn in that module; nothing is downloaded and no add-on is needed.

The frontage documents no real place. Its particulars are invented from what
seaside arcades of this kind accumulate: sign bands added over decades and
never removed, tubes and bulbs that have died, wet paving that takes the
colour, and a neighbour's roller shutter left half down.
"""

import argparse
import math
import random
import sys
import tempfile
from pathlib import Path

import bpy
import OpenImageIO as oiio
from mathutils import Vector

# Blender's --python leaves the script's folder off the module path, and its
# Python would otherwise write a bytecode cache into the package on import.
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.dont_write_bytecode = True
from arcade_frontage_parts import (  # noqa: E402
    LED_GLYPHS,
    box,
    bulb,
    bulb_meshes,
    cabinet_faces,
    cabinet_mesh,
    cable,
    galvanised,
    gooseneck,
    gresite,
    lightbox_face,
    link,
    mesh_object,
    principled,
    railing,
    ribbed_shutter,
    screen_material,
    stucco,
    text,
    wall_with_openings,
    wet_paving,
    worn_paint,
)

FONTS = Path(__file__).resolve().parent.parent / "assets" / "arcade-frontage-study" / "fonts"
FONT_FILES = {
    "tilt_neon": "tiltneon/TiltNeon-XROT-YROT.ttf",
    "neonderthaw": "neonderthaw/Neonderthaw-Regular.ttf",
    "racing_sans": "racingsansone/RacingSansOne-Regular.ttf",
    "alfa_slab": "alfaslabone/AlfaSlabOne-Regular.ttf",
    "bebas": "bebasneue/BebasNeue-Regular.ttf",
}
# The arcade's frontage runs from x -5.7 to 5.7 on the facade plane y = 0; the
# promenade is y < 0. The neighbouring unit with the half-down shutter is to
# its left, nearest a visitor walking in from that side.
ARCADE = (-5.7, 5.7)
NEIGHBOUR = (-10.6, -6.4)
OPENING_TOP = 2.85
GROUND_FLOOR = 5.0
LIGHTBOX = (-4.1, 2.5, 3.12, 4.08)  # x0, x1, z0, z1
JUEGOS_BLADE = (-5.45, 2.3, 4.6, -1.35, -0.25)  # x, z0, z1, y0, y1
BAR_BLADE = (5.45, 3.05, 3.8, -1.15, -0.25)
WINDOW_X = [-24.75 + 3.5 * k for k in range(15)]
DIRECTED_CAMERA = {"location": (-13.0, -7.6, 1.5), "target": (0.3, 0.0), "lens": 35.0, "shift_y": 0.06}
DIRECTED_EXPOSURE = 0.3
# Emission, scene-linear, before exposure. Saturated tubes and printed acrylic
# stay near 1 so the AgX view keeps their colour; the white acrylic, the bulb
# run and the arcade's fluorescent interior do most of the lighting.
NEON_PINK = (1.0, 0.02, 0.28)
NEON_GREEN = (0.05, 1.0, 0.18)
TUBE_STRENGTH = 0.75
LIGHTBOX_STRENGTH = 2.6
LIGHTBOX_PRINT_STRENGTH = 1.0
BULB_STRENGTH = 70.0
FLUORESCENT_STRENGTH = 20.0
LED_STRENGTH = 1.2
SEED = 1986
# The bundled stills are JPEG at this quality with full-resolution colour.
# Below it, inspected at 4x, the LED dots begin to merge and the sheet's text
# gains halos (assets/arcade-frontage-study/SOURCE.md).
JPEG_QUALITY = 85

DEAD = []  # what is broken, recorded into the scene for inspection


def arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--renders", action="store_true")
    parser.add_argument("--preview", action="store_true", help="half size, fewer samples")
    return parser.parse_args(sys.argv[sys.argv.index("--") + 1 :])


def build_model(collection, fonts):
    rnd = random.Random(SEED)
    mats = {
        "paving": wet_paving(),
        "kerb": principled("Granite kerb, wet", (0.11, 0.105, 0.10), 0.22),
        "road": principled("Asphalt, wet", (0.035, 0.035, 0.037), 0.16),
        "stucco": stucco("Render, faded salmon paint", (0.50, 0.33, 0.25)),
        "stucco upper": stucco("Render upper floors, faded salmon paint", (0.47, 0.32, 0.25), damp=1.0),
        "stucco far": stucco("Render, next block, ochre", (0.45, 0.36, 0.22), damp=1.0),
        "plinth": principled("Stone plinth", (0.16, 0.15, 0.14), 0.55),
        "gresite": gresite(),
        "step": principled("Granite threshold", (0.20, 0.19, 0.18), 0.3),
        "glass": principled("Window glass", (0.02, 0.02, 0.025), 0.03),
        "frame": principled("Painted window frames", (0.30, 0.28, 0.25), 0.5),
        "railing": principled("Balcony railings, black paint", (0.02, 0.02, 0.02), 0.4, metal=0.6),
        "slab": principled("Balcony slab, concrete", (0.32, 0.30, 0.28), 0.8),
        "roof": principled("Roof", (0.25, 0.23, 0.22), 0.9),
        "curtain lit": principled("Lit curtain", (0.6, 0.5, 0.4), 0.9, emit=(1.0, 0.72, 0.45), strength=1.2),
        "curtain tv": principled("Curtain lit by a television", (0.4, 0.45, 0.6), 0.9, emit=(0.55, 0.7, 1.0), strength=0.5),
        "paint panel": worn_paint("Painted panel, faded ochre, 1958", (0.55, 0.40, 0.18), (0.50, 0.33, 0.25)),
        "paint letters": worn_paint("Sign-writer's black, 1958", (0.025, 0.03, 0.028), (0.55, 0.40, 0.18)),
        "paint shadow": worn_paint("Sign-writer's oxide red shadow, 1958", (0.30, 0.05, 0.03), (0.55, 0.40, 0.18)),
        "lightbox frame": principled("Lightbox frame, anodised bronze", (0.06, 0.045, 0.035), 0.35, metal=0.8),
        "lightbox face": lightbox_face("Lightbox acrylic, 1986", (1.0, 0.93, 0.80), LIGHTBOX_STRENGTH, LIGHTBOX[1]),
        "lightbox red": lightbox_face("Lightbox print, red", (1.0, 0.03, 0.02), LIGHTBOX_PRINT_STRENGTH, LIGHTBOX[1]),
        "lightbox blue": lightbox_face("Lightbox print, blue shadow", (0.04, 0.10, 0.9), LIGHTBOX_PRINT_STRENGTH * 0.8, LIGHTBOX[1]),
        "blade blue": principled("Blade sign box, faded blue enamel, 1972", (0.035, 0.08, 0.20), 0.45),
        "blade black": principled("Bar sign box, black", (0.012, 0.012, 0.012), 0.35),
        "tube pink": principled("Neon tube, pink", (0.6, 0.2, 0.4), 0.1, emit=NEON_PINK, strength=TUBE_STRENGTH),
        "tube green": principled("Neon tube, green", (0.3, 0.6, 0.35), 0.1, emit=NEON_GREEN, strength=TUBE_STRENGTH),
        "tube dead": principled("Neon tube, dead (unlit glass)", (0.42, 0.36, 0.40), 0.12),
        "bulb lit": principled("Bulb, lit", (1.0, 0.8, 0.6), 0.1, emit=(1.0, 0.56, 0.22), strength=BULB_STRENGTH),
        "bulb dead": principled("Bulb, dead", (0.30, 0.27, 0.24), 0.08),
        "bulb channel": principled("Bulb channel, chrome-yellow paint", (0.45, 0.30, 0.02), 0.4, metal=0.3),
        "led": principled("LED dot, red", (0.3, 0.02, 0.02), 0.2, emit=(1.0, 0.012, 0.006), strength=LED_STRENGTH),
        "led board": principled("LED board", (0.01, 0.01, 0.01), 0.3),
        "fluorescent": principled("Fluorescent diffuser", (0.9, 0.95, 1.0), 0.4, emit=(0.86, 0.95, 1.0), strength=FLUORESCENT_STRENGTH),
        "ceiling": principled("Ceiling tiles", (0.55, 0.55, 0.53), 0.9),
        "terrazzo": principled("Terrazzo floor", (0.42, 0.40, 0.38), 0.22),
        "interior wall": principled("Interior wall, mirror-tiled", (0.18, 0.12, 0.20), 0.15, metal=0.4),
        "cabinet": principled("Cabinet, black laminate", (0.02, 0.02, 0.022), 0.35),
        "dark room": principled("Empty shop, bare", (0.10, 0.095, 0.09), 0.85),
        "poster": principled("Paper poster, damp", (0.62, 0.62, 0.6), 0.6),
        "poster ink": principled("Poster ink, red", (0.5, 0.02, 0.02), 0.5),
        "door": principled("Portal door, varnished wood", (0.12, 0.05, 0.025), 0.35),
        "metal": principled("Painted steel", (0.08, 0.08, 0.08), 0.5, metal=0.5),
        "cable": principled("Cable, black", (0.01, 0.01, 0.01), 0.4),
        "ac": principled("Air-conditioning unit", (0.55, 0.55, 0.53), 0.5),
        "shutter": galvanised(),
        "gooseneck": principled("Gooseneck lamps, bottle-green enamel", (0.02, 0.07, 0.04), 0.3, metal=0.5),
        "lamp lit": principled("Gooseneck lamp, lit", (1.0, 0.9, 0.8), 0.2, emit=(1.0, 0.72, 0.45), strength=12.0),
        "fanlight": principled("Portal fanlight, stair light on", (0.8, 0.8, 0.7), 0.1, emit=(1.0, 0.78, 0.5), strength=1.4),
    }
    screens = [
        screen_material(f"Cabinet screen {i}", c1, c2, 3.0 + 2 * i)
        for i, (c1, c2) in enumerate([((0.1, 0.4, 1.0), (0.02, 0.02, 0.15)), ((1.0, 0.25, 0.05), (0.2, 0.0, 0.3)),
                                      ((0.3, 1.0, 0.4), (0.0, 0.1, 0.3)), ((0.9, 0.1, 0.8), (0.1, 0.6, 1.0)),
                                      ((1.0, 0.85, 0.2), (0.6, 0.05, 0.05))])
    ]
    bulb_meshes(mats)
    c = collection
    ax0, ax1 = ARCADE
    ix0, ix1 = ax0 + 0.5, ax1 - 0.5

    # Ground: wet promenade flags, kerb and road.
    mesh_object("Promenade flags", [(-60, -10, 0), (90, -10, 0), (90, 0, 0), (-60, 0, 0)], [(0, 1, 2, 3)], mats["paving"], c)
    box("Kerb", (-60, -10.3, -0.15), (90, -10, 0.0), mats["kerb"], c)
    mesh_object("Road", [(-60, -30, -0.15), (90, -30, -0.15), (90, -10.3, -0.15), (-60, -10.3, -0.15)], [(0, 1, 2, 3)], mats["road"], c)

    # The block: ground-floor openings, three floors of balconied windows.
    bx0, bx1, depth, height = -27.0, 27.5, 12.0, 14.2
    neighbours = [(-16.6, -11.8), (-22.6, -17.8), (8.4, 13.4), (14.2, 19.2), (20.0, 25.0)]
    shops = [(ix0, ix1, 0.0, OPENING_TOP), (NEIGHBOUR[0], NEIGHBOUR[1], 0.0, 2.8), (6.5, 7.9, 0.0, 2.9)]
    shops += [(x0, x1, 0.0, 2.8) for x0, x1 in neighbours]
    wall_with_openings("Ground floor wall", bx0, bx1, 0.0, GROUND_FLOOR, shops, 0.3, mats["stucco"], c)
    floors = [GROUND_FLOOR + 0.05 + f * 3.2 for f in range(3)]
    windows = [(x - 0.6, x + 0.6, z0, z0 + 2.25) for z0 in floors for x in WINDOW_X]
    wall_with_openings("Upper floors wall", bx0, bx1, GROUND_FLOOR, height, windows, 0.25, mats["stucco upper"], c)
    box("Roof", (bx0, 0, height), (bx1, depth, height + 0.15), mats["roof"], c)
    box("Parapet", (bx0, -0.05, height), (bx1, 0.2, height + 0.9), mats["stucco upper"], c)
    mesh_object("Side wall left", [(bx0, 0, 0), (bx0, depth, 0), (bx0, depth, height + 0.9), (bx0, 0, height + 0.9)], [(0, 1, 2, 3)], mats["stucco upper"], c)
    mesh_object("Side wall right", [(bx1, depth, 0), (bx1, 0, 0), (bx1, 0, height + 0.9), (bx1, depth, height + 0.9)], [(0, 1, 2, 3)], mats["stucco upper"], c)
    box("Stone plinth", (bx0, -0.04, 0), (bx1, 0.0, 0.35), mats["plinth"], c)
    lit = {(8, 0): "curtain lit", (10, 0): "curtain tv", (9, 1): "curtain lit", (4, 1): "curtain lit", (13, 0): "curtain tv", (6, 2): "curtain lit"}
    for f, z0 in enumerate(floors):
        for i, x in enumerate(WINDOW_X):
            pane = box(f"Window {i}/{f}", (x - 0.6, 0.2, z0), (x + 0.6, 0.23, z0 + 2.25), mats["glass"], c)
            box(f"Window mullion {i}/{f}", (x - 0.03, 0.18, z0), (x + 0.03, 0.2, z0 + 2.25), mats["frame"], c)
            if (i, f) in lit:
                # The room's back wall, wide enough to be seen through the window at an angle.
                box(f"Lit room {i}/{f}", (x - 1.5, 0.6, z0), (x + 2.5, 0.62, z0 + 2.25), mats[lit[(i, f)]], c)
                pane.data.materials[0] = principled(f"Window glass, lit room {i}/{f}", (0.8, 0.8, 0.8), 0.05, transmission=1.0)
            slab_z = z0 - 0.05
            box(f"Balcony {i}/{f}", (x - 0.95, -0.75, slab_z - 0.14), (x + 0.95, 0, slab_z), mats["slab"], c)
            railing(f"Railing {i}/{f}", x, slab_z, mats["railing"], c)
    ac_x = WINDOW_X[7]
    box("Air-conditioning unit", (ac_x - 0.85, -0.62, floors[0] - 0.05), (ac_x - 0.05, -0.3, floors[0] + 0.55), mats["ac"], c)

    # The next block across a side street, receding into the dusk.
    far_windows = [(x - 0.55, x + 0.55, z, z + 1.9) for z in (3.6, 6.4, 9.2) for x in range(36, 88, 3)]
    wall_with_openings("Next block", 33.0, 90.0, 0.0, 12.0, far_windows, 0.2, mats["stucco far"], c)
    box("Next block roof", (33.0, 0, 12.0), (90.0, 12, 12.2), mats["roof"], c)
    mesh_object("Next block side", [(33.0, 12, 0), (33.0, 0, 0), (33.0, 0, 12.0), (33.0, 12, 12.0)], [(0, 1, 2, 3)], mats["stucco far"], c)
    for k, x in enumerate(range(36, 88, 3)):
        for z in (3.6, 6.4, 9.2):
            key = rnd.random()
            mat = mats["curtain lit"] if key < 0.18 else mats["curtain tv"] if key < 0.24 else mats["dark room"]
            box(f"Next block window {x}/{z}", (x - 0.55, 0.18, z), (x + 0.55, 0.2, z + 1.9), mat, c)

    # ---- The arcade. 1958 billiard hall; refitted 1972, 1986, 1994 and 2015.
    box("Arcade floor", (ix0, 0.0, -0.02), (ix1, 10.0, 0.0), mats["terrazzo"], c)
    box("Arcade ceiling", (ix0, 0.3, 3.0), (ix1, 10.0, 3.05), mats["ceiling"], c)
    mesh_object("Arcade back wall", [(ix0, 10, 0), (ix1, 10, 0), (ix1, 10, 3), (ix0, 10, 3)], [(0, 1, 2, 3)], mats["interior wall"], c)
    mesh_object("Arcade right wall", [(ix1, 0.3, 0), (ix1, 10, 0), (ix1, 10, 3), (ix1, 0.3, 3)], [(0, 1, 2, 3)], mats["interior wall"], c)
    mesh_object("Arcade left wall", [(ix0, 10, 0), (ix0, 0.3, 0), (ix0, 0.3, 3), (ix0, 10, 3)], [(0, 1, 2, 3)], mats["interior wall"], c)
    for row, x in enumerate((-3.2, -0.2, 2.8)):
        for k in range(4):
            y = 1.6 + k * 2.2
            box(f"Fluorescent troffer {row}.{k}", (x - 0.6, y - 0.15, 2.97), (x + 0.6, y + 0.15, 3.0), mats["fluorescent"], c)
    body = cabinet_mesh(mats["cabinet"])
    sides = [principled(f"Cabinet side art, {name}", col, 0.3) for name, col in
             (("purple", (0.08, 0.015, 0.14)), ("red", (0.20, 0.015, 0.01)), ("blue", (0.01, 0.04, 0.16)),
              ("yellow", (0.28, 0.18, 0.01)), ("black", (0.02, 0.02, 0.02)), ("black", (0.02, 0.02, 0.02)))]
    marquees = [principled(f"Cabinet marquee, {name}", col, 0.3, emit=col, strength=1.0) for name, col in
                (("amber", (1.0, 0.55, 0.12)), ("cyan", (0.1, 0.7, 1.0)), ("magenta", (1.0, 0.1, 0.6)),
                 ("white", (0.95, 0.9, 0.8)))]
    for row, x in enumerate((-2.6, 0.6, 3.6)):
        for k in range(5):
            y = 1.5 + k * 1.55
            cab = link(bpy.data.objects.new(f"Cabinet {row}.{k}", body), c)
            cab.location = (x, y, 0)
            cab.material_slots[1].link = "OBJECT"
            cab.material_slots[1].material = rnd.choice(sides)
            cabinet_faces(f"Cabinet {row}.{k}", (x, y), rnd.choice(screens), rnd.choice(marquees), c)
    # A claw machine just inside the door: lit hood, glass case, a heap of prizes.
    box("Claw machine base", (-4.9, 0.6, 0), (-3.9, 1.6, 0.85), mats["cabinet"], c)
    box("Claw machine hood", (-4.9, 0.6, 1.95), (-3.9, 1.6, 2.3),
        principled("Claw machine hood", (0.8, 0.6, 0.2), 0.3, emit=(1.0, 0.35, 0.6), strength=1.5), c)
    box("Claw machine glass", (-4.9, 0.6, 0.85), (-3.9, 1.6, 1.95),
        principled("Claw machine glass", (0.9, 0.9, 0.9), 0.02, transmission=1.0), c)
    prize_mats = [principled(f"Plush {name}", col, 0.9) for name, col in
                  (("pink", (0.8, 0.1, 0.3)), ("blue", (0.1, 0.4, 0.8)), ("yellow", (0.9, 0.7, 0.1)), ("green", (0.2, 0.7, 0.3)))]
    prize_mesh = bpy.data.meshes.new("Plush prize")
    bm_verts, bm_faces = [], []
    for i in range(7):
        phi = math.pi * i / 6
        for j in range(10):
            th = math.tau * j / 10
            bm_verts.append((math.sin(phi) * math.cos(th), math.sin(phi) * math.sin(th), math.cos(phi)))
    for i in range(6):
        for j in range(10):
            a, b = i * 10 + j, i * 10 + (j + 1) % 10
            bm_faces.append((a, b, b + 10, a + 10))
    prize_mesh.from_pydata(bm_verts, [], bm_faces)
    for poly in prize_mesh.polygons:
        poly.use_smooth = True
    prize_mesh.materials.append(prize_mats[0])
    for k in range(26):
        prize = link(bpy.data.objects.new(f"Prize {k}", prize_mesh), c)
        prize.scale = (rnd.uniform(0.06, 0.11),) * 3
        prize.location = (rnd.uniform(-4.8, -4.0), rnd.uniform(0.7, 1.5), 0.9 + rnd.uniform(0, 0.12))
        prize.material_slots[0].link = "OBJECT"
        prize.material_slots[0].material = rnd.choice(prize_mats)
    box("Threshold", (ix0, -0.35, 0), (ix1, 0.0, 0.06), mats["step"], c)
    box("Arcade shutter box", (ix0, 0.0, OPENING_TOP - 0.25), (ix1, 0.3, OPENING_TOP), mats["metal"], c)
    # Piers and two slim columns, clad in the 1972 gresite.
    for name, x0, x1 in (("left pier", ax0, ix0), ("right pier", ix1, ax1), ("column a", -1.95, -1.65), ("column b", 1.65, 1.95)):
        box(f"Gresite {name}", (x0 - 0.01, -0.03, 0.35 if "pier" in name else 0.0), (x1 + 0.01, 0.3, OPENING_TOP), mats["gresite"], c)

    # 1958: BILLARES in sign-writer's paint on a painted panel across the fascia.
    # The 1986 lightbox was screwed over the panel's lower part and never removed.
    lb_x0, lb_x1, lb_z0, lb_z1 = LIGHTBOX
    panel = (lb_x0 - 0.1, lb_x1 + 0.35, lb_z1 - 0.4, lb_z1 + 0.7)
    box("1958 painted panel", (panel[0], -0.003, panel[2]), (panel[1], 0.0, panel[3]), mats["paint panel"], c)
    paint_z = (lb_z1 + panel[3]) / 2
    for label, mat, dx, dz, dy in (("shadow", "paint shadow", 0.035, -0.03, -0.004), ("letters", "paint letters", 0.0, 0.0, -0.006)):
        text(f"1958 painted BILLARES · FUTBOLINES, {label}", "BILLARES · FUTBOLINES", fonts["alfa_slab"], mats[mat], c,
             width=5.6, location=((panel[0] + panel[1]) / 2 - 0.15 + dx, dy, paint_z + dz))
    # Its gooseneck lamps, still wired; the right-hand one has blown.
    for k, x in enumerate((-2.8, -1.5, -0.2, 1.1, 2.6)):
        gooseneck(f"1958 gooseneck lamp {k}", x, panel[3], k != 4, mats, c)
    DEAD.append("1958 gooseneck lamps: the right-hand one of five blown")

    # 1986: the backlit lightbox, its right-hand tube dead.
    box("1986 lightbox housing", (lb_x0, -0.27, lb_z0), (lb_x1, 0.0, lb_z1), mats["lightbox frame"], c)
    mesh_object("1986 lightbox face", [(lb_x0 + 0.06, -0.272, lb_z0 + 0.06), (lb_x1 - 0.06, -0.272, lb_z0 + 0.06),
                                       (lb_x1 - 0.06, -0.272, lb_z1 - 0.06), (lb_x0 + 0.06, -0.272, lb_z1 - 0.06)],
                [(0, 1, 2, 3)], mats["lightbox face"], c)
    DEAD.append("1986 lightbox: right-hand fluorescent tube dead")
    lb_mid = ((lb_x0 + lb_x1) / 2, (lb_z0 + lb_z1) / 2 - 0.03)
    lb_w = lb_x1 - lb_x0 - 0.5
    text("1986 SALÓN RECREATIVO, blue shadow", "SALÓN RECREATIVO", fonts["racing_sans"], mats["lightbox blue"], c,
         width=lb_w, location=(lb_mid[0] + 0.045, -0.274, lb_mid[1] - 0.04))
    text("1986 SALÓN RECREATIVO", "SALÓN RECREATIVO", fonts["racing_sans"], mats["lightbox red"], c,
         width=lb_w, location=(lb_mid[0], -0.276, lb_mid[1]))

    # 1972: double-sided blade sign on the left pier, JUEGOS in pink tube, the E dead.
    bx, bz0, bz1, by0, by1 = JUEGOS_BLADE
    box("1972 blade sign box", (bx - 0.09, by0, bz0), (bx + 0.09, by1, bz1), mats["blade blue"], c)
    box("1972 blade sign bracket, top", (bx - 0.03, by1, bz1 - 0.2), (bx + 0.03, 0.0, bz1 - 0.12), mats["metal"], c)
    box("1972 blade sign bracket, foot", (bx - 0.03, by1, bz0 + 0.12), (bx + 0.03, 0.0, bz0 + 0.2), mats["metal"], c)
    letters = "JUEGOS"
    pitch = (bz1 - bz0 - 0.3) / len(letters)
    for i, ch in enumerate(letters):
        z = bz1 - 0.15 - pitch * (i + 0.5)
        dead = ch == "E"
        for side, xface, rot in (("street", bx - 0.11, (math.pi / 2, 0, -math.pi / 2)), ("far", bx + 0.11, (math.pi / 2, 0, math.pi / 2))):
            text(f"1972 JUEGOS {ch} ({side} face)", ch, fonts["tilt_neon"], mats["tube dead" if dead else "tube pink"], c,
                 height=pitch * 0.72, location=(xface, (by0 + by1) / 2, z), rotation=rot, extrude=0.006, bevel=0.007, offset=-0.004)
    DEAD.append("1972 blade sign: the E of JUEGOS dead")
    perimeter = []
    n_side, n_top = 16, 7
    for k in range(n_side + 1):
        zk = bz0 + 0.06 + (bz1 - bz0 - 0.12) * k / n_side
        perimeter += [(by0 + 0.06, zk), (by1 - 0.06, zk)]
    for k in range(1, n_top):
        yk = by0 + 0.06 + (by1 - by0 - 0.12) * k / n_top
        perimeter += [(yk, bz0 + 0.06), (yk, bz1 - 0.06)]
    dead_blade = {5, 6, 19, 31}
    for k, (y, z) in enumerate(perimeter):
        bulb(f"1972 blade bulb {k}", (bx - 0.09, y, z), k not in dead_blade, mats, c, normal=(-1, 0, 0))
    DEAD.append(f"1972 blade sign: {len(dead_blade)} of {len(perimeter)} border bulbs dead")

    # 1994: bulb run on a painted channel round the opening; a few dead.
    box("1994 bulb channel, head", (ix0 - 0.05, -0.08, OPENING_TOP + 0.02), (ix1 + 0.05, 0.0, OPENING_TOP + 0.12), mats["bulb channel"], c)
    count = 46
    dead_run = set(rnd.sample(range(count), 5))
    for k in range(count):
        x = ix0 + 0.1 + (ix1 - ix0 - 0.2) * k / (count - 1)
        bulb(f"1994 bulb run {k}", (x, -0.08, OPENING_TOP + 0.07), k not in dead_run, mats, c)
    dead_jambs = {("right", 2), ("right", 3), ("left", 6)}
    for side, x in (("left", ax0 + 0.25), ("right", ax1 - 0.25)):
        box(f"1994 bulb channel, {side} jamb", (x - 0.05, -0.08, 0.6), (x + 0.05, -0.03, OPENING_TOP + 0.02), mats["bulb channel"], c)
        for k in range(10):
            z = 0.75 + (OPENING_TOP - 0.85) * k / 9
            bulb(f"1994 bulb run, {side} jamb {k}", (x, -0.08, z), (side, k) not in dead_jambs, mats, c)
    DEAD.append(f"1994 bulb run: {len(dead_run) + len(dead_jambs)} of {count + 20} bulbs dead")

    # A later neon "Bar" on a black blade, right pier, green tube.
    gx, gz0, gz1, gy0, gy1 = BAR_BLADE
    box("Bar blade box", (gx - 0.08, gy0, gz0), (gx + 0.08, gy1, gz1), mats["blade black"], c)
    box("Bar blade bracket", (gx - 0.03, gy1, gz1 - 0.15), (gx + 0.03, 0.0, gz1 - 0.08), mats["metal"], c)
    for side, xface, rot in (("street", gx - 0.11, (math.pi / 2, 0, -math.pi / 2)), ("far", gx + 0.11, (math.pi / 2, 0, math.pi / 2))):
        text(f"Neon Bar ({side} face)", "Bar", fonts["neonderthaw"], mats["tube green"], c, width=0.72,
             location=(xface, (gy0 + gy1) / 2, (gz0 + gz1) / 2), rotation=rot, extrude=0.004, bevel=0.004, offset=-0.002)

    # 2015: red LED dot-matrix ABIERTO hung inside the left bay.
    dot, gap, word = 0.016, 0.022, "ABIERTO"
    led_w = (len(word) * 6 - 1) * gap
    lx0, lz1, ly = -1.25, 2.5, 0.12
    box("2015 LED board", (lx0 - 0.05, ly, lz1 - 7 * gap - 0.04), (lx0 + led_w + 0.05, ly + 0.03, lz1 + 0.05), mats["led board"], c)
    verts, faces = [], []
    for li, ch in enumerate(word):
        for row, bits in enumerate(LED_GLYPHS[ch]):
            for col, bit in enumerate(bits):
                if bit == "1":
                    x, z = lx0 + (li * 6 + col) * gap, lz1 - row * gap
                    b = len(verts)
                    verts.extend([(x, ly - 0.002, z), (x + dot, ly - 0.002, z), (x + dot, ly - 0.002, z - dot), (x, ly - 0.002, z - dot)])
                    faces.append((b, b + 1, b + 2, b + 3))
    mesh_object("2015 LED ABIERTO", verts, faces, mats["led"], c)["lettering"] = word

    # Cables added with every sign and never taken down.
    for k, pts in enumerate([
        [(bx, -0.02, bz1 - 0.1), (ax0 + 0.9, -0.03, 4.25), (lb_x0 - 0.05, -0.03, 4.15)],
        [(lb_x0, -0.02, 4.1), (-1.0, -0.03, 4.22), (1.5, -0.03, 4.16), (ax1 - 0.3, -0.03, 4.22)],
        [(gx, -0.02, gz1 - 0.05), (gx + 0.15, -0.03, 4.0), (gx + 0.6, -0.03, 4.22), (8.0, -0.03, 4.2)],
    ]):
        cable(f"Cable {k}", pts, mats["cable"], c)

    # ---- The neighbour: closed, its shutter left half down, a SE ALQUILA bill on it.
    nx0, nx1 = NEIGHBOUR
    box("Neighbour, empty shop floor", (nx0, 0, -0.02), (nx1, 6, 0.0), mats["dark room"], c)
    mesh_object("Neighbour, back wall", [(nx0, 6, 0), (nx1, 6, 0), (nx1, 6, 2.8), (nx0, 6, 2.8)], [(0, 1, 2, 3)], mats["dark room"], c)
    box("Neighbour, ceiling", (nx0, 0.3, 2.8), (nx1, 6, 2.85), mats["dark room"], c)
    for x in (nx0 + 0.6, nx1 - 1.4):
        box(f"Left-behind carton {x:.1f}", (x, 3.5, 0), (x + 0.6, 4.1, 0.45), principled(f"Cardboard {x:.1f}", (0.25, 0.17, 0.10), 0.9), c)
    ribbed_shutter("Neighbour roller shutter, half down", nx0, nx1, 1.32, 2.8, mats["shutter"], c)
    box("Neighbour shutter bottom bar", (nx0, -0.075, 1.27), (nx1, -0.03, 1.34), mats["metal"], c)
    box("Neighbour shutter box", (nx0 - 0.1, -0.2, 2.8), (nx1 + 0.1, 0.0, 3.15), mats["shutter"], c)
    for x in (nx0 - 0.06, nx1):
        box(f"Neighbour shutter guide {x:.2f}", (x, -0.07, 0), (x + 0.06, 0.0, 2.8), mats["metal"], c)
    bill_x = nx1 - 0.9
    box("SE ALQUILA bill", (bill_x - 0.36, -0.07, 1.62), (bill_x + 0.36, -0.066, 2.1), mats["poster"], c)
    text("SE ALQUILA", "SE ALQUILA", fonts["bebas"], mats["poster ink"], c, width=0.62, location=(bill_x, -0.072, 1.86))

    # The rest of the ground floor: a residential portal and closed shops.
    box("Portal door", (6.5, 0.25, 0), (7.9, 0.3, 2.4), mats["door"], c)
    box("Portal fanlight", (6.5, 0.24, 2.45), (7.9, 0.26, 2.9), mats["fanlight"], c)
    for k, (x0, x1) in enumerate(neighbours):
        ribbed_shutter(f"Closed shop shutter {k}", x0, x1, 0.0, 2.8, mats["shutter"], c, y=0.05)
    return mats


# --------------------------------------------------------------------------- scenes


def use_gpu(scene):
    """Ask Cycles for a GPU itself; a headless process does not do it at start-up."""
    prefs = bpy.context.preferences.addons["cycles"].preferences
    prefs.refresh_devices()
    for kind in ("METAL", "OPTIX", "CUDA", "HIP", "ONEAPI"):
        try:
            prefs.compute_device_type = kind
        except TypeError:
            continue
        prefs.refresh_devices()
        gpus = [d for d in prefs.devices if d.type == kind]
        if gpus:
            for device in gpus:
                device.use = True
            scene.cycles.device = "GPU"
            scene.cycles.denoising_use_gpu = True
            return
    print("No GPU device available; Cycles renders on the CPU.")


def render_settings(scene, preview):
    scene.render.engine = "CYCLES"
    use_gpu(scene)
    scene.cycles.samples = 256 if preview else 1024
    scene.cycles.adaptive_threshold = 0.02 if preview else 0.008
    scene.cycles.use_denoising = True
    scene.cycles.max_bounces = 8
    scene.cycles.glossy_bounces = 4
    scene.cycles.transmission_bounces = 6
    scene.cycles.caustics_reflective = False
    scene.cycles.caustics_refractive = False
    scene.render.resolution_x, scene.render.resolution_y = 1920, 1080
    scene.render.resolution_percentage = 50 if preview else 100
    scene.view_settings.view_transform = "AgX"
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_depth = "8"
    scene.render.use_stamp_filename = False
    scene.render.use_stamp_hostname = False


def aim(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat("-Z", "Y").to_euler()


def dusk_sky():
    """Blue hour: deep blue overhead, a faint mauve band at the horizon."""
    world = bpy.data.worlds.new("Dusk sky")
    nodes, links = world.node_tree.nodes, world.node_tree.links
    coord = nodes.new("ShaderNodeTexCoord")
    sep = nodes.new("ShaderNodeSeparateXYZ")
    links.new(coord.outputs["Generated"], sep.inputs[0])
    ramp = nodes.new("ShaderNodeValToRGB")
    els = ramp.color_ramp.elements
    els[0].position, els[0].color = 0.0, (0.250, 0.150, 0.220, 1)
    els[1].position, els[1].color = 1.0, (0.020, 0.040, 0.160, 1)
    for pos, col in ((0.06, (0.150, 0.130, 0.300, 1)), (0.3, (0.055, 0.090, 0.275, 1))):
        els.new(pos).color = col
    links.new(sep.outputs["Z"], ramp.inputs["Fac"])
    links.new(ramp.outputs["Color"], nodes["Background"].inputs["Color"])
    return world


def directed_scene(scene, model, preview):
    scene.name = "Directed — dusk, on foot"
    lens = DIRECTED_CAMERA["lens"]
    cam = bpy.data.objects.new("Eye height 1.5 m, 35 mm", bpy.data.cameras.new("Eye height 1.5 m, 35 mm"))
    scene.collection.objects.link(cam)
    cam.location = DIRECTED_CAMERA["location"]
    aim(cam, (*DIRECTED_CAMERA["target"], cam.location.z))  # level: verticals stay vertical
    cam.data.lens, cam.data.sensor_width, cam.data.sensor_fit = lens, 36, "HORIZONTAL"
    cam.data.shift_y = DIRECTED_CAMERA["shift_y"]
    cam.data.clip_end = 400
    scene.camera = cam
    scene.world = dusk_sky()
    render_settings(scene, preview)
    scene.view_settings.look = "AgX - Punchy"
    scene.view_settings.exposure = DIRECTED_EXPOSURE
    return cam


def default_variant(mat, cache):
    if mat in cache:
        return cache[mat]
    copy = mat.copy()
    copy.name = mat.name + " · default"
    for n in copy.node_tree.nodes:
        if n.type == "BSDF_PRINCIPLED":
            for key, value in (("Roughness", 0.5), ("Emission Strength", 0.0)):
                socket = n.inputs[key]
                for old in list(socket.links):
                    copy.node_tree.links.remove(old)
                socket.default_value = value
    cache[mat] = copy
    return copy


def default_scene(model, preview):
    """Same meshes and curves, linked; every material at roughness 0.5, signs unlit."""
    scene = bpy.data.scenes.new("Default — factory camera, studio light")
    collection = bpy.data.collections.new("FRONTAGE MODEL — default materials (linked geometry)")
    scene.collection.children.link(collection)
    cache = {}
    for obj in model.objects:
        if obj.type == "LIGHT":
            continue  # sign lamps are part of the signs, and the signs are unlit
        twin = obj.copy()  # shares the mesh or curve data: the same geometry
        collection.objects.link(twin)
        for slot in twin.material_slots:
            if slot.material:
                mat = slot.material
                slot.link = "OBJECT"
                slot.material = default_variant(mat, cache)
    # A grey studio sweep under and behind the block.
    profile = [(-80.0, -0.16)]
    profile += [(40 + 25 * math.sin(math.pi / 2 * i / 16), -0.16 + 25 * (1 - math.cos(math.pi / 2 * i / 16))) for i in range(17)]
    profile += [(65.0, 120.0)]
    verts, faces = [], []
    for y, z in profile:
        verts.extend([(-150, y, z), (180, y, z)])
    for i in range(len(profile) - 1):
        faces.append((2 * i, 2 * i + 1, 2 * i + 3, 2 * i + 2))
    mesh_object("Grey sweep", verts, faces, principled("Sweep, grey", (0.18, 0.18, 0.18), 0.5), scene.collection, smooth=True)
    cam = bpy.data.objects.new("Factory camera, 50 mm", bpy.data.cameras.new("Factory camera, 50 mm"))
    scene.collection.objects.link(cam)
    cam.data.lens, cam.data.sensor_width, cam.data.sensor_fit = 50, 36, "HORIZONTAL"
    cam.data.clip_end = 1000
    cam.location = (7.358891487121582, -6.925790786743164, 4.958309173583984)  # Blender's factory camera
    cam.rotation_euler = (1.1093189716339111, 0.0, 0.8149281740188599)
    scene.camera = cam
    render_settings(scene, preview)
    # The factory position frames a 2 m cube; keep its orientation and pull back
    # along that axis until the frontage fits, as "view selected" would.
    corners = [(x, y, z) for x in (NEIGHBOUR[0] - 0.3, ARCADE[1] + 0.3) for y in (-1.4, 0.0) for z in (0.0, GROUND_FLOOR + 1.0)]
    previous = bpy.context.window.scene
    bpy.context.window.scene = scene
    bpy.context.view_layer.update()
    location, _ = cam.camera_fit_coords(bpy.context.evaluated_depsgraph_get(), [v for p in corners for v in p])
    cam.location = location
    bpy.context.window.scene = previous
    for name, color, energy, size, az, el in (
        ("Broad warm key", (1.0, 0.80, 0.58), 34000, 24, -140, 42),
        ("Cool fill", (0.60, 0.74, 1.0), 10000, 30, -35, 18),
    ):
        data = bpy.data.lights.new(name, "AREA")
        data.shape, data.size, data.energy, data.color = "DISK", size, energy, color
        light = bpy.data.objects.new(name, data)
        scene.collection.objects.link(light)
        a, e = math.radians(az), math.radians(el)
        light.location = Vector((math.cos(a) * math.cos(e), math.sin(a) * math.cos(e), math.sin(e))) * 60 + Vector((0, 0, 2))
        aim(light, (0, 0, 2))
    scene.world = bpy.data.worlds.new("Studio grey")
    scene.world.node_tree.nodes["Background"].inputs[0].default_value = (0.18, 0.18, 0.18, 1)
    scene.world.node_tree.nodes["Background"].inputs[1].default_value = 0.5
    scene.view_settings.look = "None"
    scene.view_settings.exposure = 0.0
    return scene, cam


def camera_facts(cam, look_at):
    """Height, horizontal distance to look_at and horizontal angle of view."""
    loc = cam.location
    flat = math.hypot(loc.x - look_at[0], loc.y - look_at[1])
    fov = math.degrees(2 * math.atan(cam.data.sensor_width / 2 / cam.data.lens))
    return loc.z, flat, fov


SHEET_GROUND = (0.25, 0.25, 0.25)
SHEET_INK = (0.006, 0.006, 0.006)


def sheet(folder, directed_cam, default_cam):
    """Both lossless renders in folder, side by side at 1920 x 1080 with the
    decisions that differ; written beside them as directed-and-default.png."""
    width, height, margin, gap = 1920, 1080, 48, 48
    tile_w = (width - 2 * margin - gap) // 2
    tile_h = tile_w * 9 // 16
    top = 164
    door = (0.0, 0.0)
    dh, dd, dfov = camera_facts(directed_cam, door)
    fh, fd, ffov = camera_facts(default_cam, door)
    angle = math.degrees(math.atan2(-directed_cam.location.y, -directed_cam.location.x))
    cells = [
        ("directed", "Directed: arriving on foot at dusk", [
            f"Camera: eye height {dh:.1f} m, {dd:.0f} m from the door, {angle:.0f}° to the frontage",
            f"Field of view: 35 mm lens, {dfov:.0f}° across",
            "Light: its own signs, bulbs and fluorescent interior; dusk sky",
            "Values: dark, cool street and upper floors; warm light pooled at the signs",
            "Materials: wet paving, glossy mosaic, galvanised shutter, worn paint, each its own roughness",
        ]),
        ("default", "Default: the same model as Blender sets it up", [
            f"Camera: Blender's factory angle, pulled back along it to fit: {fh:.0f} m up, {fd:.0f} m away",
            f"Field of view: 50 mm lens, {ffov:.0f}° across",
            "Light: one broad warm key and a cool fill; signs unlit",
            "Values: the whole frontage at one even middle value",
            "Materials: every surface at roughness 0.5",
        ]),
    ]
    scene = bpy.data.scenes.new("Sheet — directed beside default")
    render_settings(scene, preview=False)
    scene.cycles.samples = 32
    scene.cycles.use_denoising = False
    scene.cycles.filter_width = 1.0
    scene.render.resolution_x, scene.render.resolution_y = width, height
    scene.render.resolution_percentage = 100
    scene.view_settings.view_transform = "Standard"
    scene.view_settings.look = "None"
    scene.render.dither_intensity = 0
    scene.world = bpy.data.worlds.new("Sheet ground")
    scene.world.node_tree.nodes["Background"].inputs[0].default_value = (*SHEET_GROUND, 1)
    camera = bpy.data.objects.new("Sheet camera", bpy.data.cameras.new("Sheet camera"))
    scene.collection.objects.link(camera)
    camera.data.type, camera.data.ortho_scale, camera.data.sensor_fit = "ORTHO", width / 100, "HORIZONTAL"
    camera.location = (width / 200, -height / 200, 10)
    scene.camera = camera
    ink = bpy.data.materials.new("Sheet ink")
    ink.node_tree.nodes.clear()
    emission = ink.node_tree.nodes.new("ShaderNodeEmission")
    emission.inputs["Color"].default_value = (*SHEET_INK, 1)
    ink.node_tree.links.new(emission.outputs[0], ink.node_tree.nodes.new("ShaderNodeOutputMaterial").inputs[0])
    # Inter, the plain sans Blender ships for its interface (SIL OFL 1.1).
    inter = Path(bpy.utils.system_resource("DATAFILES")) / "fonts" / "Inter.woff2"
    font = bpy.data.fonts.load(str(inter)) if inter.is_file() else None

    def label(body, x, y, size):
        data = bpy.data.curves.new("label", "FONT")
        data.body, data.size, data.align_y = body, size / 100, "TOP"
        data.space_line = 1.25
        if font:
            data.font = font
        data.materials.append(ink)
        obj = bpy.data.objects.new("label", data)
        scene.collection.objects.link(obj)
        obj.location = (x / 100, -y / 100, 0)

    label("One invented frontage, set up twice: what the default leaves out", margin, 100, 30)
    for column, (stem, title, lines) in enumerate(cells):
        left = margin + column * (tile_w + gap)
        image = bpy.data.images.load(str(folder / f"{stem}.png"), check_existing=False)
        mat = bpy.data.materials.new(stem)
        nodes = mat.node_tree.nodes
        nodes.clear()
        texture = nodes.new("ShaderNodeTexImage")
        texture.image = image
        glow = nodes.new("ShaderNodeEmission")
        mat.node_tree.links.new(texture.outputs[0], glow.inputs["Color"])
        mat.node_tree.links.new(glow.outputs[0], nodes.new("ShaderNodeOutputMaterial").inputs[0])
        x0, y0 = left / 100, -top / 100
        x1, y1 = (left + tile_w) / 100, -(top + tile_h) / 100
        mesh = bpy.data.meshes.new(stem)
        mesh.from_pydata([(x0, y1, 0), (x1, y1, 0), (x1, y0, 0), (x0, y0, 0)], [], [(0, 1, 2, 3)])
        mesh.uv_layers.new().data.foreach_set("uv", [0, 0, 1, 0, 1, 1, 0, 1])
        mesh.materials.append(mat)
        scene.collection.objects.link(bpy.data.objects.new(stem, mesh))
        label(title, left, top + tile_h + 28, 24)
        label("\n".join(lines), left, top + tile_h + 72, 20)
    label("When the default is right: for inspecting or cataloguing this model, where every part "
          "should be visible at one even value.", margin, top + tile_h + 266, 22)
    scene.render.filepath = str(folder / "directed-and-default.png")
    bpy.ops.render.render(write_still=True, scene=scene.name)


def scrub_file_browsers():
    """Blender's default Shading workspace keeps a file browser opened on the
    author's home folder, and the native file saves that fixed-size field
    whole: fill it before pointing it at the file's own folder, so no tail of
    the earlier path survives the save."""
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type == "FILE_BROWSER" and space.params:
                    space.params.directory = b"/" * 4096
                    space.params.directory = b"//"


def write_jpeg(lossless, target):
    """Encode a lossless render as a bundled JPEG with the OpenImageIO that ships
    inside Blender, keeping full-resolution colour: Blender's own JPEG output
    halves it (4:2:0), which smears small saturated detail."""
    rgb = oiio.ImageBufAlgo.channels(oiio.ImageBuf(str(lossless)), (0, 1, 2))
    rgb.specmod().attribute("Compression", f"jpeg:{JPEG_QUALITY}")
    rgb.specmod().attribute("jpeg:subsampling", "4:4:4")
    if not rgb.write(str(target), "uint8"):
        raise RuntimeError(f"{target}: {rgb.geterror()}")


def build(dest, renders, preview):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    fonts = {}
    for key, rel in FONT_FILES.items():
        font = bpy.data.fonts.load(str(FONTS / rel))
        font.pack()  # the native file carries its lettering
        # The path field is saved whole: fill it so no tail of the absolute
        # load path survives, then name where the bundled copy sits.
        font.filepath = "/" * 1024
        font.filepath = f"//fonts/{rel}"
        fonts[key] = font
    scene = bpy.context.scene
    model = bpy.data.collections.new("FRONTAGE MODEL — invented, directed materials")
    scene.collection.children.link(model)
    build_model(model, fonts)
    directed_cam = directed_scene(scene, model, preview)
    default, default_cam = default_scene(model, preview)
    bpy.context.window.scene = scene
    scene["broken"] = "; ".join(DEAD)
    script = Path(__file__).resolve()
    source = bpy.data.texts.new("BUILD SOURCE — edit the external script to regenerate")
    source.write(script.read_text())
    parts = bpy.data.texts.new("BUILD SOURCE — arcade_frontage_parts.py, imported")
    parts.write(script.with_name("arcade_frontage_parts.py").read_text())
    unused = bpy.data.fonts.get("Bfont Regular")
    if unused and unused.users == 0:
        bpy.data.fonts.remove(unused)  # every new text curve starts on it
    scrub_file_browsers()
    bpy.ops.wm.save_as_mainfile(filepath=str(dest / "arcade-frontage-study.blend"), compress=True)
    if renders:
        with tempfile.TemporaryDirectory(prefix="arcade-frontage-") as temporary:
            lossless = Path(temporary)
            for name, s in (("directed", scene), ("default", default)):
                s.render.filepath = str(lossless / f"{name}.png")
                bpy.ops.render.render(write_still=True, scene=s.name)
            if not preview:
                sheet(lossless, directed_cam, default_cam)
            for png in sorted(lossless.glob("*.png")):
                write_jpeg(png, dest / f"{png.stem}.jpg")


def main():
    if not bpy.app.background:
        raise SystemExit("Use a separate Blender --background process; this script owns its scenes.")
    args = arguments()
    dest = args.output.expanduser().resolve()
    if dest.exists() and (not dest.is_dir() or any(dest.iterdir())):
        raise SystemExit(f"Refusing a nonempty or non-directory destination: {dest}")
    missing = [rel for rel in FONT_FILES.values() if not (FONTS / rel).is_file()]
    if missing:
        raise SystemExit(f"Missing bundled fonts under {FONTS}: {missing}")
    dest.mkdir(parents=True, exist_ok=True)
    build(dest, args.renders, args.preview)


if __name__ == "__main__":
    main()
