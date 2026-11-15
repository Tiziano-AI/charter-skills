"""Build the authored vessel comparison in Blender; no external add-ons.

Run with Blender --background --factory-startup --python-exit-code 1
--python this_file -- --output /new/output.
The output directory must be absent or empty. --renders adds Cycles stills:
the four comparison PNGs and, in reflection-plate/, the plate's seven frames
and labelled contact sheet as JPEG. The lossless plate renders the sheet is
composed from live in a temporary folder and are not kept.
The saved .blend retains editable profile/handle source, evaluated meshes and
one named scene per plate frame.
"""

import argparse
import json
import math
import sys
import tempfile
from pathlib import Path

import bpy
import OpenImageIO as oiio
from mathutils import Vector


def arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--renders", action="store_true")
    return parser.parse_args(sys.argv[sys.argv.index("--") + 1 :])


def bezier(points, count=20):
    a, b, c, d = map(Vector, points)
    return [
        (1 - t) ** 3 * a + 3 * (1 - t) ** 2 * t * b + 3 * (1 - t) * t * t * c + t**3 * d
        for t in [i / count for i in range(count)]
    ] + [d]


def revolve(name, profile, collection, segments=96):
    vertices, rings = [], []
    for r, z in profile:
        ring = []
        for j in range(1 if r == 0 else segments):
            ring.append(len(vertices))
            vertices.append(
                (
                    r * math.cos(j * math.tau / segments),
                    r * math.sin(j * math.tau / segments),
                    z,
                )
            )
        rings.append(ring)
    faces = []
    for i, ring in enumerate(rings):
        next_ring = rings[(i + 1) % len(rings)]
        if len(ring) == len(next_ring) == 1:
            continue
        for j in range(segments):
            if len(ring) == 1:
                faces.append((ring[0], next_ring[(j + 1) % segments], next_ring[j]))
            elif len(next_ring) == 1:
                faces.append((ring[j], ring[(j + 1) % segments], next_ring[0]))
            else:
                faces.append(
                    (
                        ring[j],
                        ring[(j + 1) % segments],
                        next_ring[(j + 1) % segments],
                        next_ring[j],
                    )
                )
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)
    return obj


def outer_profile(p):
    # Outer wall rises from the foot, swells low, then tightens into the lip.
    h, w = p["height"], p["width"]
    curves = [
        [(0.53, 0.03), (0.72, 0.03), (0.97, 0.15), (1.0, 0.37)],
        [(1.0, 0.37), (1.04, 0.60), (0.94, 0.75), (0.82, 0.84)],
        [(0.82, 0.84), (0.75, 0.90), (0.73, 0.94), (0.73, 0.99)],
    ]
    outer = []
    for curve in curves:
        samples = bezier(curve, 16)
        outer.extend(samples if not outer else samples[1:])
    return [(r * w, z * h) for r, z in outer]


def shell(name, p, collection):
    w, wall = p["width"], p["wall"]
    outer = outer_profile(p)
    profile = list(outer)
    # A semicircular lip joins wall and cavity; thickness is geometry.
    lip_r, lip_z = profile[-1]
    for i in range(1, 13):
        angle = i * math.pi / 12
        profile.append(
            (
                lip_r - wall / 2 + math.cos(angle) * wall / 2,
                lip_z + math.sin(angle) * wall / 2,
            )
        )
    profile.extend([(r - wall, max(z, wall + 0.055)) for r, z in reversed(outer[:-1])])
    # Rounded interior floor, then the enclosed underside.
    profile.extend(
        [(0.40 * w, wall + 0.055), (0, wall + 0.055), (0, 0.035), (0.40 * w, 0.035)]
    )
    obj = revolve(name, profile, collection)
    obj["section"] = "Closed shell: exterior, round lip, interior, floor, underside"
    return obj


def cavity(name, p, collection):
    # Keep the interior an intentional surface. Overlapping handle roots may
    # penetrate it during union; this volume restores the original cavity
    # after exterior blending instead of leaving a hidden internal wedge.
    wall = p["wall"]
    floor = wall + 0.055
    inner = [(r - wall, max(z, floor)) for r, z in outer_profile(p)]
    above_lip = p["height"] + wall
    profile = [(0, floor), (0.40 * p["width"], floor)] + inner
    profile.extend([(inner[-1][0], above_lip), (0, above_lip)])
    obj = revolve(name, profile, collection)
    obj.display_type = "WIRE"
    obj.hide_render = True
    obj["purpose"] = (
        "Subtract after outer-root blending to retain the smooth inner wall"
    )
    return obj


def handle(name, p, collection):
    w, h = p["width"], p["height"]
    reach = p["reach"]
    curves = [
        [
            (0.70 * w, 0.86 * h),
            (1.04 * w, 0.87 * h),
            (reach, 0.87 * h),
            (reach, 0.64 * h),
        ],
        [
            (reach, 0.64 * h),
            (reach, 0.39 * h),
            (1.05 * w, 0.28 * h),
            (0.88 * w, 0.28 * h),
        ],
    ]
    data = bpy.data.curves.new(name, "CURVE")
    data.dimensions = "3D"
    data.resolution_u = 24
    data.bevel_depth = p["handle_radius"]
    data.bevel_resolution = 6
    data.use_fill_caps = True
    spline = data.splines.new("BEZIER")
    spline.bezier_points.add(2)
    anchors = [curves[0][0], curves[0][3], curves[1][3]]
    for point, (x, z) in zip(spline.bezier_points, anchors):
        point.co = (x, 0, z)
        point.handle_left_type = "FREE"
        point.handle_right_type = "FREE"
    a, b, c = spline.bezier_points
    a.handle_left = a.co
    a.handle_right = (curves[0][1][0], 0, curves[0][1][1])
    b.handle_left = (curves[0][2][0], 0, curves[0][2][1])
    b.handle_right = (curves[1][1][0], 0, curves[1][1][1])
    c.handle_left = (curves[1][2][0], 0, curves[1][2][1])
    c.handle_right = c.co
    # Broader roots carry the handle into the body; the outer reach stays light.
    a.radius = p["root_scale"]
    b.radius = 0.87
    c.radius = p["root_scale"]
    obj = bpy.data.objects.new(name, data)
    collection.objects.link(obj)
    return obj


def material(name, color, roughness):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1)
    mat.use_nodes = True
    node = mat.node_tree.nodes.get("Principled BSDF")
    node.inputs["Base Color"].default_value = (*color, 1)
    node.inputs["Roughness"].default_value = roughness
    return mat


def evaluated(name, body, grip, interior, p, collection):
    objects = []
    for source in (body, grip):
        obj = source.copy()
        obj.data = source.data.copy()
        collection.objects.link(obj)
        objects.append(obj)
    bpy.ops.object.select_all(action="DESELECT")
    for obj in objects:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = objects[0]
    bpy.ops.object.convert(target="MESH")
    bpy.ops.object.join()
    result = bpy.context.object
    result.name = name
    # Voxel union changes overlapping pieces into one volume. Its scale sets
    # resolution, not the design fillet. Smooth iterations control the blend.
    mod = result.modifiers.new("Union body and swept handle", "REMESH")
    mod.mode = "VOXEL"
    mod.voxel_size = 0.021
    mod.use_smooth_shade = True
    bpy.ops.object.modifier_apply(modifier=mod.name)
    mod = result.modifiers.new("Root continuity and lip finish", "SMOOTH")
    mod.factor = 0.75
    mod.iterations = p["fillet_passes"]
    bpy.ops.object.modifier_apply(modifier=mod.name)
    if p["root_blend"]:
        roots = [
            (p["width"] * 0.80, 0, p["height"] * 0.85),
            (p["width"] * 0.96, 0, p["height"] * 0.28),
        ]
        group = result.vertex_groups.new(name="Fillets — local root influence")
        for vertex in result.data.vertices:
            distance = min((vertex.co - Vector(root)).length for root in roots)
            weight = math.exp(-((distance / 0.42) ** 4))
            if weight > 0.005:
                group.add([vertex.index], weight, "REPLACE")
        mod = result.modifiers.new(
            "Broad root fillets without softening the rim", "SMOOTH"
        )
        mod.vertex_group = group.name
        mod.factor, mod.iterations = 0.82, 90
        bpy.ops.object.modifier_apply(modifier=mod.name)
    mod = result.modifiers.new("Restore the continuous inner wall", "BOOLEAN")
    mod.operation = "DIFFERENCE"
    mod.solver = "EXACT"
    mod.object = interior
    bpy.ops.object.modifier_apply(modifier=mod.name)
    # Retessellate the Boolean boundary before smoothing its joins. The light
    # finish is separate from the broad exterior-root intervention above.
    mod = result.modifiers.new("Retessellate the retained cavity", "REMESH")
    mod.mode = "VOXEL"
    mod.voxel_size = 0.016
    mod.use_smooth_shade = True
    bpy.ops.object.modifier_apply(modifier=mod.name)
    mod = result.modifiers.new("Cavity and lip finish", "SMOOTH")
    mod.factor, mod.iterations = 0.55, 3
    bpy.ops.object.modifier_apply(modifier=mod.name)
    mod = result.modifiers.new(
        "Curvature interpolation before delivery triangulation", "SUBSURF"
    )
    mod.levels = 1
    bpy.ops.object.modifier_apply(modifier=mod.name)
    mod = result.modifiers.new("Delivery simplification", "DECIMATE")
    mod.ratio = 0.04
    bpy.ops.object.modifier_apply(modifier=mod.name)
    for polygon in result.data.polygons:
        polygon.use_smooth = True
    result["construction"] = (
        "Profile shell + variable-radius Bezier handle; voxel union, root blend, cavity subtraction, remesh, subdivision, decimate"
    )
    for key, value in p.items():
        result[key] = value
    return result


def aim(obj, target):
    obj.rotation_euler = (
        (Vector(target) - obj.location).to_track_quat("-Z", "Y").to_euler()
    )


def area(name, location, energy, size, color=(1, 1, 1)):
    data = bpy.data.lights.new(name, "AREA")
    data.energy, data.shape, data.size, data.color = energy, "DISK", size, color
    obj = bpy.data.objects.new(name, data)
    bpy.context.scene.collection.objects.link(obj)
    obj.location = location
    aim(obj, (0.2, 0, 1.1))
    return obj


# Reflection-placement plate on the low-bellied form. The orthographic camera,
# geometry, glaze roughness, exposure and view transform stay fixed; only the
# one neutral white source (or a dark card, or the roughness for the matte
# counterpart) changes. Sources sit 14 units from the vessel, behind the
# camera plane, so a card between source and vessel stays out of frame.
PLATE_SOURCE = {"distance": 14.0, "elevation": 35.0, "power": 5200.0, "aspect": 2.0}
PLATE_FRAMES = [
    # file stem, scene name, azimuth (deg), source width, roughness, dark card
    ("source-left", "Plate · source left", -125, 3.0, 0.20, False),
    ("source-middle", "Plate · source middle", -72, 3.0, 0.20, False),
    ("source-handle-side", "Plate · source handle side", -25, 3.0, 0.20, False),
    ("source-small", "Plate · small source", -72, 0.6, 0.20, False),
    ("source-broad", "Plate · broad source", -72, 9.0, 0.20, False),
    ("broad-dark-card", "Plate · broad source and dark card", -72, 9.0, 0.20, True),
    ("matte-middle", "Plate · matte, middle source", -72, 3.0, 0.90, False),
]
PLATE_CENTER = Vector((0.2, 0, 1.1))
SHEET_GROUND = (0.25, 0.25, 0.25)  # linear; a neutral mid-grey on screen
# The plate is bundled as JPEG at this quality with full-resolution colour.
# Below it, inspected at 4x, halos form around the contact sheet's labels; at
# this quality the reflection edges and the smooth grey grounds show nothing.
JPEG_QUALITY = 85
SHEET_INK = (0.006, 0.006, 0.006)


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


def direction(azimuth, elevation):
    a, e = math.radians(azimuth), math.radians(elevation)
    return Vector((math.cos(a) * math.cos(e), math.sin(a) * math.cos(e), math.sin(e)))


def plate_scenes(vessel, camera):
    """One named scene per plate frame, sharing camera, stage and world."""
    common = bpy.data.collections.new("PLATE · camera and neutral stage")
    common.objects.link(camera)
    bpy.ops.mesh.primitive_plane_add(size=200, location=(0, 0, 0.02))
    stage = bpy.context.object
    for collection in list(stage.users_collection):
        collection.objects.unlink(stage)
    common.objects.link(stage)
    stage.name = "Plate stage — neutral grey"
    stage.data.materials.append(material("Plate stage • neutral grey", (0.16,) * 3, 0.9))
    world = bpy.data.worlds.new("Plate world — dark neutral")
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs[0].default_value = (1, 1, 1, 1)
    world.node_tree.nodes["Background"].inputs[1].default_value = 0.02
    subjects = {}
    for roughness in sorted({frame[4] for frame in PLATE_FRAMES}):
        collection = bpy.data.collections.new(f"PLATE · low-bellied, roughness {roughness:.2f}")
        obj = vessel.copy()  # linked duplicate: the delivery mesh itself
        obj.name = f"Plate vessel • roughness {roughness:.2f}"
        obj.hide_render = False
        collection.objects.link(obj)
        obj.material_slots[0].link = "OBJECT"
        obj.material_slots[0].material = material(
            f"Plate glaze • neutral dark • roughness {roughness:.2f}", (0.02,) * 3, roughness
        )
        subjects[roughness] = collection
    scenes = {}
    for stem, name, azimuth, width, roughness, card in PLATE_FRAMES:
        scene = bpy.data.scenes.new(name)
        scene.collection.children.link(common)
        scene.collection.children.link(subjects[roughness])
        scene.camera = camera
        scene.world = world
        data = bpy.data.lights.new(f"Source • neutral white • {width:g} × {width * 2:g}", "AREA")
        data.shape = "RECTANGLE"
        data.size, data.size_y = width, width * PLATE_SOURCE["aspect"]
        data.energy, data.color = PLATE_SOURCE["power"], (1, 1, 1)
        light = bpy.data.objects.new(data.name, data)
        scene.collection.objects.link(light)
        light.location = PLATE_CENTER + PLATE_SOURCE["distance"] * direction(
            azimuth, PLATE_SOURCE["elevation"]
        )
        aim(light, PLATE_CENTER)
        light["azimuth_deg"] = azimuth
        if card:
            mesh = bpy.data.meshes.new("Dark card")
            mesh.from_pydata(
                [(-0.65, -9, 0), (0.65, -9, 0), (0.65, 9, 0), (-0.65, 9, 0)], [], [(0, 1, 2, 3)]
            )
            obj = bpy.data.objects.new("Dark card — between source and vessel, out of frame", mesh)
            scene.collection.objects.link(obj)
            obj.location = PLATE_CENTER + 11.8 * direction(azimuth, PLATE_SOURCE["elevation"])
            obj.rotation_euler = (PLATE_CENTER - obj.location).to_track_quat("Z", "Y").to_euler()
            mesh.materials.append(material("Dark card • matte black", (0.01,) * 3, 0.9))
        render_settings(scene, samples=128)
        scenes[stem] = scene
    return scenes


def render_settings(scene, samples):
    scene.render.engine = "CYCLES"
    use_gpu(scene)
    scene.cycles.samples = samples
    scene.cycles.use_denoising = True
    scene.render.resolution_x = 1080
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100
    scene.view_settings.view_transform = "AgX"
    scene.view_settings.look = "None"
    scene.view_settings.exposure = 0
    # Render metadata must not disclose the author's native-project location.
    scene.render.use_stamp_filename = False
    scene.render.use_stamp_hostname = False


def contact_sheet(folder, renders):
    """Lay the unblended plate renders out with plain sentence-case labels;
    written into folder as contact-sheet.png."""
    tile, gap, margin, head, foot = 540, 24, 40, 64, 70
    rows = [
        (
            "One source moved; same size, distance and power",
            [
                ("source-left", "Left"),
                ("source-middle", "Middle"),
                ("source-handle-side", "Handle side: at the lower inner return\nthe reflection pinches to a tight spot"),
            ],
        ),
        (
            "One position, three sizes; same power",
            [
                ("source-small", "Small, 0.6 × 1.2"),
                ("source-middle", "Medium, 3 × 6 (the middle render above)"),
                ("source-broad", "Broad, 9 × 18"),
            ],
        ),
        (
            "Dark card in the reflection; matte counterpart",
            [
                ("broad-dark-card", "Broad source with a dark card\nbetween it and the vessel"),
                ("matte-middle", "Matte, roughness 0.90,\nmiddle source"),
            ],
        ),
    ]
    width = 2 * margin + 3 * tile + 2 * gap
    height = 2 * margin + 3 * (head + tile + foot)
    scene = bpy.data.scenes.new("Plate · contact sheet")
    render_settings(scene, samples=64)
    scene.cycles.use_denoising = False
    scene.cycles.filter_width = 1.0
    scene.render.resolution_x, scene.render.resolution_y = width, height
    scene.view_settings.view_transform = "Standard"
    scene.render.dither_intensity = 0
    scene.world = bpy.data.worlds.new("Sheet ground")
    scene.world.use_nodes = True
    scene.world.node_tree.nodes["Background"].inputs[0].default_value = (*SHEET_GROUND, 1)
    camera = bpy.data.objects.new("Sheet camera", bpy.data.cameras.new("Sheet camera"))
    scene.collection.objects.link(camera)
    camera.data.type, camera.data.ortho_scale = "ORTHO", width / 100
    camera.data.sensor_fit = "HORIZONTAL"
    camera.location = (width / 200, -height / 200, 10)
    scene.camera = camera
    ink = bpy.data.materials.new("Sheet ink")
    ink.use_nodes = True
    ink.node_tree.nodes.clear()
    emission = ink.node_tree.nodes.new("ShaderNodeEmission")
    emission.inputs["Color"].default_value = (*SHEET_INK, 1)
    ink.node_tree.links.new(
        emission.outputs[0], ink.node_tree.nodes.new("ShaderNodeOutputMaterial").inputs[0]
    )

    # Inter, the plain sans Blender ships for its interface (SIL OFL 1.1).
    inter = Path(bpy.utils.system_resource("DATAFILES")) / "fonts" / "Inter.woff2"
    font = bpy.data.fonts.load(str(inter)) if inter.is_file() else None

    def label(text, x, y, size):
        data = bpy.data.curves.new("label", "FONT")
        data.body, data.size, data.align_y = text, size / 100, "TOP"
        if font:
            data.font = font
        data.materials.append(ink)
        obj = bpy.data.objects.new("label", data)
        scene.collection.objects.link(obj)
        obj.location = (x / 100, -y / 100, 0)

    for row, (title, cells) in enumerate(rows):
        top = margin + row * (head + tile + foot)
        label(title, margin, top + 18, 26)
        for column, (stem, caption) in enumerate(cells):
            left = margin + column * (tile + gap)
            image = bpy.data.images.load(str(renders[stem]), check_existing=False)
            mat = bpy.data.materials.new(stem)
            mat.use_nodes = True
            nodes = mat.node_tree.nodes
            nodes.clear()
            texture = nodes.new("ShaderNodeTexImage")
            texture.image = image
            emission = nodes.new("ShaderNodeEmission")
            mat.node_tree.links.new(texture.outputs[0], emission.inputs["Color"])
            mat.node_tree.links.new(
                emission.outputs[0], nodes.new("ShaderNodeOutputMaterial").inputs[0]
            )
            x0, y0 = left / 100, -(top + head) / 100
            x1, y1 = (left + tile) / 100, -(top + head + tile) / 100
            mesh = bpy.data.meshes.new(stem)
            mesh.from_pydata([(x0, y1, 0), (x1, y1, 0), (x1, y0, 0), (x0, y0, 0)], [], [(0, 1, 2, 3)])
            mesh.uv_layers.new().data.foreach_set("uv", [0, 0, 1, 0, 1, 1, 0, 1])
            mesh.materials.append(mat)
            scene.collection.objects.link(bpy.data.objects.new(stem, mesh))
            label(caption, left, top + head + tile + 14, 21)
    held = (
        "Held in every frame: orthographic camera,\nlow-bellied geometry, neutral dark glaze,\n"
        "exposure 0, AgX view transform.\n\nSource: one neutral white rectangle, 1:2,\n"
        "14 units from the vessel at 35° elevation,\n5200 W in every frame."
    )
    top = margin + 2 * (head + tile + foot)
    label(held, margin + 2 * (tile + gap), top + head + 20, 21)
    scene.render.filepath = str(folder / "contact-sheet.png")
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


def main():
    if not bpy.app.background:
        raise SystemExit(
            "Use a separate Blender --background process; this script owns its scene."
        )
    args = arguments()
    dest = args.output.expanduser().resolve()
    if dest.exists() and (not dest.is_dir() or any(dest.iterdir())):
        raise SystemExit(
            "Output must be a new or empty directory; existing assets are not overwritten."
        )
    dest.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    source = bpy.data.collections.new("EDITABLE CONSTRUCTION — hidden from renders")
    scene.collection.children.link(source)
    display = bpy.data.collections.new("DELIVERY — select a version")
    scene.collection.children.link(display)
    neutral = material(
        "Inspection • warm white • roughness 0.42", (0.64, 0.61, 0.55), 0.42
    )
    glaze = material("Teal glaze • roughness 0.20", (0.025, 0.18, 0.165), 0.20)
    variants = {
        "upright": {
            "height": 2.95,
            "width": 0.94,
            "wall": 0.19,
            "reach": 1.68,
            "handle_radius": 0.21,
            "root_scale": 1.02,
            "fillet_passes": 3,
            "root_blend": False,
        },
        "low-bellied": {
            "height": 2.40,
            "width": 1.15,
            "wall": 0.12,
            "reach": 1.96,
            "handle_radius": 0.165,
            "root_scale": 1.5,
            "fillet_passes": 12,
            "root_blend": True,
        },
    }
    meshes = []
    for name, params in variants.items():
        body = shell(name + " • section", params, source)
        grip = handle(name + " • handle controls", params, source)
        interior = cavity(name + " • retained cavity", params, source)
        obj = evaluated(name, body, grip, interior, params, display)
        obj.data.materials.append(neutral)
        meshes.append(obj)
        bpy.ops.object.select_all(action="DESELECT")
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.export_scene.gltf(
            filepath=str(dest / (name + ".glb")),
            export_format="GLB",
            use_selection=True,
            export_extras=True,
        )
    source.hide_render = True
    source.hide_viewport = True
    for obj in meshes:
        obj.hide_render = True
        obj.hide_set(True)
    meshes[1].hide_render = False
    meshes[1].hide_set(False)
    bpy.ops.mesh.primitive_plane_add(size=200, location=(0, 0, 0.02))
    ground = bpy.context.object
    ground.name = "Stage — not exported"
    ground.data.materials.append(material("Stage", (0.23, 0.215, 0.19), 0.85))
    bpy.ops.object.camera_add(location=(5.2, -8.2, 5.0))
    camera = bpy.context.object
    camera.name = "Three-quarter • orthographic"
    camera.data.type = "ORTHO"
    camera.data.ortho_scale = 5.15
    aim(camera, (0.35, 0, 1.30))
    scene.camera = camera
    key = area("Neutral broad key", (-3, -4, 7), 1050, 5)
    fill = area("Neutral fill", (4, 1, 4), 500, 4)
    scene.world = bpy.data.worlds.new("Studio world")
    scene.world.use_nodes = True
    scene.world.node_tree.nodes["Background"].inputs[0].default_value = (
        0.18,
        0.18,
        0.18,
        1,
    )
    scene.world.node_tree.nodes["Background"].inputs[1].default_value = 0.35
    render_settings(scene, samples=48)
    plates = plate_scenes(meshes[1], camera)
    bpy.context.window.scene = scene
    # Text block keeps the rebuilding source reachable inside the native file.
    text = bpy.data.texts.new("BUILD SOURCE — edit the external script to regenerate")
    text.write(Path(__file__).read_text())
    scrub_file_browsers()
    bpy.ops.wm.save_as_mainfile(
        filepath=str(dest / "vessel-study.blend"), compress=True
    )
    stats = {
        obj.name: {
            "vertices": len(obj.data.vertices),
            "triangles": sum(len(f.vertices) - 2 for f in obj.data.polygons),
            "dimensions": list(obj.dimensions),
            "parameters": variants[obj.name],
        }
        for obj in meshes
    }
    (dest / "geometry.json").write_text(json.dumps(stats, indent=2) + "\n")
    if args.renders:
        for obj in meshes:
            for other in meshes:
                other.hide_render = other != obj
            scene.render.filepath = str(dest / (obj.name + "-neutral.png"))
            bpy.ops.render.render(write_still=True)
        key.location = (-3, 1, 5)
        key.data.size = 2
        key.data.energy = 1100
        key.data.color = (1, 0.77, 0.52)
        aim(key, (0.2, 0, 1))
        fill.data.energy = 180
        fill.data.color = (0.55, 0.73, 1)
        for obj in meshes:
            for other in meshes:
                other.hide_render = other != obj
            obj.data.materials[0] = glaze
            scene.render.filepath = str(dest / (obj.name + "-glaze.png"))
            bpy.ops.render.render(write_still=True)
        plate_dir = dest / "reflection-plate"
        plate_dir.mkdir()
        with tempfile.TemporaryDirectory(prefix="vessel-plate-") as temporary:
            lossless = Path(temporary)
            renders = {}
            for stem, plate in plates.items():
                renders[stem] = lossless / f"{stem}.png"
                plate.render.filepath = str(renders[stem])
                bpy.ops.render.render(write_still=True, scene=plate.name)
            contact_sheet(lossless, renders)
            for png in sorted(lossless.glob("*.png")):
                write_jpeg(png, plate_dir / f"{png.stem}.jpg")


if __name__ == "__main__":
    main()
