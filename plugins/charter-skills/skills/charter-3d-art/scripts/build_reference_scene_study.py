"""Build the original, diagrammatic reference-to-scene study in Blender.

blender --background --factory-startup --python-exit-code 1 --python this_file -- --output /new/directory --renders
For supplied PNGs: --output /new/directory --compare reference.png candidate.png
The destination must be absent or empty. No downloads or external add-ons.
"""

import argparse
import json
import math
import struct
import sys
import zlib
from array import array
from pathlib import Path

import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector

WIDTH, HEIGHT = 1000, 625
# Authored image-space design, not coordinates recovered from a generated image.
# Rectangles use left/top/right/bottom fractions; depth is from the hero camera.
PARTS = {
    "near_lintel": {"rect": [-0.16, -0.08, 0.62, 0.30], "depth": 3, "length": 2},
    "near_pier": {"rect": [0.03, 0.22, 0.20, 1.08], "depth": 3, "length": 2},
    "far_lintel": {"rect": [0.57, 0.27, 0.91, 0.32], "depth": 9, "length": 1.5},
    "far_left": {"rect": [0.57, 0.32, 0.62, 0.74], "depth": 9, "length": 1.5},
    "far_right": {"rect": [0.86, 0.32, 0.91, 0.74], "depth": 9, "length": 1.5},
}
COLORS = {
    "sky": "d5cbbb",
    "floor": "9e9b88",
    "front": "273536",
    "side": "53605b",
    "top": "6f7769",
    "far": "64736c",
    "ember": "e48445",
}


def arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--renders", action="store_true")
    parser.add_argument("--compare", nargs=2, type=Path, metavar=("REFERENCE", "CANDIDATE"))
    return parser.parse_args(sys.argv[sys.argv.index("--") + 1 :])


def rgb(hex_color):
    return tuple(int(hex_color[i : i + 2], 16) / 255 for i in (0, 2, 4))


def linear(value):
    return value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4


def material(name, color):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    mat.node_tree.nodes.clear()
    out = mat.node_tree.nodes.new("ShaderNodeOutputMaterial")
    emission = mat.node_tree.nodes.new("ShaderNodeEmission")
    rgba = (*map(linear, rgb(color)), 1)
    emission.inputs["Color"].default_value = rgba
    mat.node_tree.links.new(emission.outputs[0], out.inputs["Surface"])
    mat.diffuse_color = rgba
    return mat


def png(path, pixels, width, height):
    def chunk(kind, data):
        return (
            struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))
        )

    rows = b"".join(b"\0" + pixels[y * width * 3 : (y + 1) * width * 3] for y in range(height))
    path.write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(rows, 9))
        + chunk(b"IEND", b"")
    )


def authored_reference(output):
    """Write an editable SVG and matching raster without a font or SVG engine."""
    shapes = []

    def polygon(points, color):
        shapes.append((points, color))

    polygon([(0, 0), (1, 0), (1, 1), (0, 1)], COLORS["sky"])
    polygon([(0, 0.51), (1, 0.51), (1, 1), (0, 1)], COLORS["floor"])
    # The circle is a drawn distant marker, not a recovered physical object.
    polygon(
        [
            (0.75 + 0.02 * math.cos(i * math.tau / 96), 0.532 + 0.032 * math.sin(i * math.tau / 96))
            for i in range(96)
        ],
        COLORS["ember"],
    )
    # Back-to-front layers. The two lintels visually merge at the left far pier;
    # the image deliberately supplies no joint or unique spatial interpretation.
    for name in ("far_left", "far_right", "far_lintel", "near_pier", "near_lintel"):
        p = PARTS[name]
        left, top, right, bottom = p["rect"]
        ratio = p["depth"] / (p["depth"] + p["length"])

        def back(x, y):
            return (0.5 + (x - 0.5) * ratio, 0.5 + (y - 0.5) * ratio)

        polygon(
            [(left, bottom), (right, bottom), back(right, bottom), back(left, bottom)],
            COLORS["front"],
        )
        polygon(
            [(right, top), (right, bottom), back(right, bottom), back(right, top)], COLORS["side"]
        )
        polygon([(left, top), (right, top), back(right, top), back(left, top)], COLORS["top"])
        polygon(
            [(left, top), (right, top), (right, bottom), (left, bottom)],
            COLORS["far"] if name.startswith("far") else COLORS["front"],
        )
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">',
        "<title>Aperture / distant ember — original diagrammatic concept</title>",
    ]
    raster = bytearray(WIDTH * HEIGHT * 3)
    for points, color in shapes:
        coords = [(x * WIDTH, y * HEIGHT) for x, y in points]
        svg.append(
            '<polygon points="'
            + " ".join(f"{x:.3f},{y:.3f}" for x, y in coords)
            + f'" fill="#{color}"/>'
        )
        channels = bytes(round(v * 255) for v in rgb(color))
        for y in range(
            max(0, math.floor(min(p[1] for p in coords))),
            min(HEIGHT, math.ceil(max(p[1] for p in coords))),
        ):
            scan = y + 0.5
            crossings = []
            for a, b in zip(coords, coords[1:] + coords[:1]):
                if (a[1] <= scan < b[1]) or (b[1] <= scan < a[1]):
                    crossings.append(a[0] + (scan - a[1]) * (b[0] - a[0]) / (b[1] - a[1]))
            crossings.sort()
            for start, end in zip(crossings[::2], crossings[1::2]):
                start, end = max(0, math.ceil(start - 0.5)), min(WIDTH, math.ceil(end - 0.5))
                if end > start:
                    raster[(y * WIDTH + start) * 3 : (y * WIDTH + end) * 3] = channels * (
                        end - start
                    )
    (output / "reference.svg").write_text("\n".join(svg) + "\n</svg>\n")
    png(output / "reference.png", raster, WIDTH, HEIGHT)


def box(scene, name, low, high, materials):
    x, y, z = low
    X, Y, Z = high
    vertices = [
        (x, y, z),
        (X, y, z),
        (X, y, Z),
        (x, y, Z),
        (x, Y, z),
        (X, Y, z),
        (X, Y, Z),
        (x, Y, Z),
    ]
    faces = [(0, 1, 2, 3), (1, 5, 6, 2), (3, 2, 6, 7), (4, 7, 6, 5), (0, 3, 7, 4), (0, 4, 5, 1)]
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    scene.collection.objects.link(obj)
    obj["study_role"] = name
    for mat in materials:
        mesh.materials.append(mat)
    for face, index in zip(mesh.polygons, (0, 1, 2, 0, 1, 0)):
        face.material_index = index
    return obj


def camera(scene, reference, location=(0, -8, 2), target=(0, 0, 2), lens=24):
    data = bpy.data.cameras.new(scene.name + " camera")
    obj = bpy.data.objects.new(data.name, data)
    scene.collection.objects.link(obj)
    obj.location = location
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat("-Z", "Y").to_euler()
    data.lens, data.sensor_width, data.sensor_fit = lens, 36, "HORIZONTAL"
    data.clip_end = 500
    data.show_background_images = True
    background = data.background_images.new()
    background.image, background.alpha = reference, 0.35
    background.display_depth = "FRONT"
    background.frame_method = "FIT"
    scene.camera = obj
    return obj


def scene_base(name, mats):
    scene = bpy.data.scenes.new(name)
    scene.render.engine = "CYCLES"
    scene.cycles.samples = 8
    scene.cycles.use_denoising = False
    scene.render.resolution_x, scene.render.resolution_y = WIDTH, HEIGHT
    scene.render.resolution_percentage = 100
    scene.render.dither_intensity = 0
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGB"
    # Render metadata must not disclose the author's native-project location.
    scene.render.use_stamp_filename = False
    scene.render.use_stamp_hostname = False
    scene.view_settings.view_transform = "Standard"
    scene.view_settings.look = "None"
    scene.world = bpy.data.worlds.new(name + " world")
    scene.world.use_nodes = True
    scene.world.node_tree.nodes["Background"].inputs["Color"].default_value = (
        *map(linear, rgb(COLORS["sky"])),
        1,
    )
    scene.world.node_tree.nodes["Background"].inputs["Strength"].default_value = 1
    # A real, broad floor rather than a picture filling the frame.
    box(scene, "ground", (-200, -200, -0.08), (200, 200, -0.05), [mats["floor"]] * 3)
    return scene


def screen_point(u, v, depth):
    """Top-left image fractions to world at a chosen hero-camera depth."""
    return ((u - 0.5) * depth * 1.5, -8 + depth, 2 + (0.5 - v) * depth * 0.9375)


def marker(scene, mats, center=(9.375, 17, 1.25), radius=0.75):
    # A distant upright disc in the world: not a pasted reference-image plane.
    vertices = [center] + [
        (
            center[0] + radius * math.cos(i * math.tau / 96),
            center[1],
            center[2] + radius * math.sin(i * math.tau / 96),
        )
        for i in range(96)
    ]
    mesh = bpy.data.meshes.new("distant disc")
    mesh.from_pydata(vertices, [], [(0, i + 1, (i + 1) % 96 + 1) for i in range(96)])
    obj = bpy.data.objects.new("distant disc", mesh)
    scene.collection.objects.link(obj)
    mesh.materials.append(mats["ember"])


def reference_geometry(scene, mats, flatten=False):
    for name, p in PARTS.items():
        left, top, right, bottom = p["rect"]
        low = screen_point(left, bottom, p["depth"])
        high = screen_point(right, top, p["depth"])
        high = (high[0], high[1] + p["length"], high[2])
        palette = [
            mats["far"] if name.startswith("far") else mats["front"],
            mats["side"],
            mats["top"],
        ]
        obj = box(scene, name, low, high, [mats["flat"]] * 3 if flatten else palette)
        obj["authored_rectangle"] = p["rect"]
        obj["hero_camera_depth"] = p["depth"]
    marker(scene, mats)


def connector(scene, mats):
    # A visible spatial return joins the previously disconnected near/far caps.
    # It is geometric continuity, not a structural-engineering calculation.
    obj = box(
        scene,
        "continuous return",
        (0.24, -3.15, 2.65),
        (0.64, 1.3, 3.45),
        [mats["front"], mats["side"], mats["top"]],
    )
    obj["changed_commission"] = "Walk around: the apparently continuous strip must really meet."
    box(
        scene,
        "raised far joint",
        (0.24, 1.0, 2.65),
        (1.05, 1.4, 3.95),
        [mats["far"], mats["side"], mats["top"]],
    )


def projection_report(scene):
    scene.view_layers[0].update()
    report = {}
    for obj in scene.objects:
        if obj.type != "MESH" or obj.get("study_role") == "ground":
            continue
        points = [
            world_to_camera_view(scene, scene.camera, obj.matrix_world @ Vector(p))
            for p in obj.bound_box
        ]
        report[obj.name] = {
            "projected_bbox_xy": [
                [min(p[i] for p in points), max(p[i] for p in points)] for i in (0, 1)
            ],
            "camera_depth_range": [min(p.z for p in points), max(p.z for p in points)],
        }
    return {
        "origin": "bottom-left",
        "range": "0..1 is the frame; values outside are retained",
        "meaning": "Projected 3D bounding-box corners, not visible silhouette, occlusion, material or quality.",
        "objects": report,
    }


def comparison(reference_path, candidate_path, output, stem="comparison"):
    """Contain, never stretch. Background/overlay are derivative inspection PNGs."""
    images = [
        bpy.data.images.load(str(p.resolve()), check_existing=False)
        for p in (reference_path, candidate_path)
    ]
    dimensions = [list(image.size) for image in images]
    width, height = max(p[0] for p in dimensions), max(p[1] for p in dimensions)
    frames = []
    for image in images:
        ratio = min(width / image.size[0], height / image.size[1])
        fitted = (round(image.size[0] * ratio), round(image.size[1] * ratio))
        image.scale(*fitted)
        pixels = array("f", [0]) * (fitted[0] * fitted[1] * 4)
        image.pixels.foreach_get(pixels)
        frame = array("f", [0.16, 0.16, 0.16, 1]) * (width * height)
        ox, oy = (width - fitted[0]) // 2, (height - fitted[1]) // 2
        for row in range(fitted[1]):
            start = ((row + oy) * width + ox) * 4
            frame[start : start + fitted[0] * 4] = pixels[
                row * fitted[0] * 4 : (row + 1) * fitted[0] * 4
            ]
        frames.append(frame)
    pair = array("f", [0]) * (width * height * 8)
    overlay = array("f", [0]) * (width * height * 4)
    for row in range(height):
        for index in (0, 1):
            pair[
                (row * width * 2 + index * width) * 4 : (row * width * 2 + (index + 1) * width) * 4
            ] = frames[index][row * width * 4 : (row + 1) * width * 4]
    for i in range(len(overlay)):
        overlay[i] = (frames[0][i] + frames[1][i]) / 2
    for suffix, data, size in (
        ("paired", pair, (width * 2, height)),
        ("overlay", overlay, (width, height)),
    ):
        image = bpy.data.images.new(f"{stem}-{suffix}", *size)
        image.pixels.foreach_set(data)
        image.filepath_raw = str(output / f"{stem}-{suffix}.png")
        image.file_format = "PNG"
        image.save()
        bpy.data.images.remove(image)
    (output / f"{stem}.json").write_text(
        json.dumps(
            {
                "reference": reference_path.name,
                "candidate": candidate_path.name,
                "source_dimensions": dimensions,
                "panel_dimensions": [width, height],
                "placement": "reference left; candidate right; contain with gray letterbox, no stretch",
                "overlay": "50% stored-sample blend of display images; diagnostic only, not a candidate",
            },
            indent=2,
        )
        + "\n"
    )
    for image in images:
        bpy.data.images.remove(image)


def build(output, renders):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    authored_reference(output)
    # Start with a fresh relative identity: setting a shorter filepath after
    # loading an absolute one leaves its old tail and packed-file path in .blend.
    content = (output / "reference.png").read_bytes()
    reference = bpy.data.images.new("reference.png", width=WIDTH, height=HEIGHT)
    reference.source = "FILE"
    reference.filepath = "//reference.png"
    reference.pack(data=content, data_len=len(content))
    mats = {name: material(name, color) for name, color in COLORS.items()}
    mats["flat"] = material("equalized values", "a6ad9f")
    scenes = {}
    for name in (
        "reference-informed",
        "equalized-values",
        "inferred-side",
        "continuous-side",
        "continuous-hero",
        "distant-camera",
        "short-lintel",
    ):
        scene = scene_base(name, mats)
        reference_geometry(scene, mats, flatten=name == "equalized-values")
        if name.startswith("continuous"):
            connector(scene, mats)
            # The cropped fixed frame did not require this concealed base.
            pier = next(obj for obj in scene.objects if obj.get("study_role") == "near_pier")
            bottom = min(vertex.co.z for vertex in pier.data.vertices)
            for vertex in pier.data.vertices:
                if abs(vertex.co.z - bottom) < 1e-6:
                    vertex.co.z = -0.05
        if name == "short-lintel":
            lintel = next(obj for obj in scene.objects if obj.get("study_role") == "near_lintel")
            for vertex in lintel.data.vertices:
                if vertex.co.x > 0:
                    vertex.co.x = 0
        if name.endswith("side"):
            camera(scene, reference, (13, -13, 8), (0, 0, 1.5), 40)
            scene.camera.data.show_background_images = False
        elif name == "distant-camera":
            camera(scene, reference, (0, -14, 2), (0, 0, 2), 43.2)
        else:
            camera(scene, reference)
        scenes[name] = scene
    inventory = scene_base("literal-inventory", mats)
    palette = [mats["front"], mats["side"], mats["top"]]
    for name, low, high in (
        ("near_pier", (-3, -3, 0), (-2, -2, 4)),
        ("near_lintel", (-3, -3, 4), (1, -2, 5)),
        ("far_left", (2, 2, 0), (2.6, 3, 3)),
        ("far_right", (5.4, 2, 0), (6, 3, 3)),
        ("far_lintel", (2, 2, 3), (6, 3, 3.6)),
    ):
        box(inventory, name, low, high, palette)
    marker(inventory, mats, (4, 6, 0.8), 0.8)
    camera(inventory, reference, (12, -18, 9), (1, 1, 2), 40)
    scenes[inventory.name] = inventory
    engineered = scene_base("engineered-gate", mats)
    for name, low, high in (
        ("left_pier", (-3, -2, 0), (-2, 3, 4)),
        ("right_pier", (2, -2, 0), (3, 3, 4)),
        ("joined_cap", (-3, -2, 4), (3, 3, 5)),
        ("far_left", (-2, 4, 0), (-1.4, 5, 3)),
        ("far_right", (1.4, 4, 0), (2, 5, 3)),
        ("far_lintel", (-2, 4, 3), (2, 5, 3.6)),
    ):
        box(engineered, name, low, high, palette)
    marker(engineered, mats, (0, 8, 1.4), 0.8)
    camera(engineered, reference, (0, -15, 3.8), (0, 1, 2.4), 34)
    scenes[engineered.name] = engineered
    reports = {name: projection_report(scene) for name, scene in scenes.items()}
    center = world_to_camera_view(
        scenes["reference-informed"], scenes["reference-informed"].camera, Vector((0, 0, 2))
    )
    assert abs(center.x - 0.5) < 1e-6 and abs(center.y - 0.5) < 1e-6
    (output / "controls.json").write_text(
        json.dumps(
            {
                "reference_rectangles": PARTS,
                "hero_camera": {
                    "location": [0, -8, 2],
                    "target": [0, 0, 2],
                    "lens_mm": 24,
                    "sensor_width_mm": 36,
                },
                "pixel_dimensions": [WIDTH, HEIGHT],
                "projection": reports,
                "technical_check": "Known camera-axis point projects to (0.5, 0.5); not artistic acceptance.",
            },
            indent=2,
        )
        + "\n"
    )
    # Keep only authored scenes. This is a background-only generator, not an
    # operator that clears the user's current interactive scene.
    for scene in list(bpy.data.scenes):
        if scene not in scenes.values():
            bpy.data.scenes.remove(scene)
    bpy.context.window.scene = scenes["reference-informed"]
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type == "VIEW_3D":
                area.spaces.active.region_3d.view_perspective = "CAMERA"
    text = bpy.data.texts.new("BUILD SOURCE — edit the external script to regenerate")
    text.write(Path(__file__).read_text())
    bpy.ops.wm.save_as_mainfile(filepath=str(output / "reference-scene-study.blend"), compress=True)
    if renders:
        for name, scene in scenes.items():
            scene.render.filepath = str(output / f"{name}.png")
            bpy.ops.render.render(write_still=True, scene=scene.name)
        for candidate in ("literal-inventory", "engineered-gate", "reference-informed"):
            comparison(output / "reference.png", output / f"{candidate}.png", output, candidate)


def main():
    if not bpy.app.background:
        raise SystemExit(
            "Use a separate Blender --background process; this script owns its scenes."
        )
    args = arguments()
    output = args.output.expanduser().resolve()
    if output.exists() and (not output.is_dir() or any(output.iterdir())):
        raise SystemExit(f"Refusing nonempty or non-directory destination: {output}")
    if args.compare:
        for path in args.compare:
            if not path.expanduser().resolve().is_file():
                raise SystemExit(f"Not a readable image file: {path}")
    output.mkdir(parents=True, exist_ok=True)
    if args.compare:
        comparison(*(path.expanduser().resolve() for path in args.compare), output)
    else:
        build(output, args.renders)


if __name__ == "__main__":
    main()
