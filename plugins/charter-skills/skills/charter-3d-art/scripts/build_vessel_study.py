"""Build the authored vessel comparison in Blender; no external add-ons.

Run with Blender --background --factory-startup --python-exit-code 1
--python this_file -- --output /new/output.
The output directory must be absent or empty. --renders adds Cycles stills.
The saved .blend retains editable profile/handle source and evaluated meshes.
"""

import argparse
import json
import math
import sys
from pathlib import Path

import bpy
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
    scene.render.engine = "CYCLES"
    scene.cycles.samples = 48
    scene.cycles.use_denoising = True
    scene.render.resolution_x = 1080
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100
    scene.view_settings.view_transform = "AgX"
    # Render metadata must not disclose the author's native-project location.
    scene.render.use_stamp_filename = False
    scene.render.use_stamp_hostname = False
    # Text block keeps the rebuilding source reachable inside the native file.
    text = bpy.data.texts.new("BUILD SOURCE — edit the external script to regenerate")
    text.write(Path(__file__).read_text())
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


if __name__ == "__main__":
    main()
