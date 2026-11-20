"""Materials and mesh parts of the SALÓN RECREATIVO frontage study.

build_arcade_frontage_study.py imports this module and decides where each part
goes; nothing here places anything in the scene by itself or runs alone. The
builder saves both files into the native file as BUILD SOURCE texts.
"""

import math

import bpy
from mathutils import Vector

# --------------------------------------------------------------------------- materials


def principled(name, base, rough=0.5, metal=0.0, emit=None, strength=0.0, transmission=0.0):
    mat = bpy.data.materials.new(name)
    node = mat.node_tree.nodes["Principled BSDF"]
    node.inputs["Base Color"].default_value = (*base, 1)
    node.inputs["Roughness"].default_value = rough
    node.inputs["Metallic"].default_value = metal
    if emit:
        node.inputs["Emission Color"].default_value = (*emit, 1)
        node.inputs["Emission Strength"].default_value = strength
    if transmission:
        node.inputs["Transmission Weight"].default_value = transmission
    mat.diffuse_color = (*base, 1)
    return mat


def nodes_of(mat):
    tree = mat.node_tree
    return tree, tree.nodes, tree.links, tree.nodes["Principled BSDF"]


def node(nodes, kind, **inputs):
    n = nodes.new(kind)
    for key, value in inputs.items():
        if hasattr(n, key):
            setattr(n, key, value)
        else:
            n.inputs[key].default_value = value
    return n


def world_position(nodes):
    return nodes.new("ShaderNodeNewGeometry").outputs["Position"]


def wet_paving():
    """Square concrete flags, wet; water stands in the joints and in shallow dips."""
    mat = principled("Wet paving flags", (0.09, 0.088, 0.085), 0.2)
    tree, nodes, links, bsdf = nodes_of(mat)
    pos = world_position(nodes)
    brick = node(nodes, "ShaderNodeTexBrick", offset=0.0, squash=1.0)
    brick.inputs["Scale"].default_value = 1.0
    brick.inputs["Mortar Size"].default_value = 0.007
    brick.inputs["Mortar Smooth"].default_value = 0.3
    brick.inputs["Brick Width"].default_value = 0.4
    brick.inputs["Row Height"].default_value = 0.4
    brick.inputs["Color1"].default_value = (0.095, 0.092, 0.088, 1)
    brick.inputs["Color2"].default_value = (0.07, 0.07, 0.068, 1)
    brick.inputs["Mortar"].default_value = (0.03, 0.03, 0.03, 1)
    links.new(pos, brick.inputs["Vector"])
    # Puddles: low-frequency dips, sharpened into standing water.
    dips = node(nodes, "ShaderNodeTexNoise")
    dips.inputs["Scale"].default_value = 0.22
    dips.inputs["Detail"].default_value = 4.0
    dips.inputs["Roughness"].default_value = 0.55
    links.new(pos, dips.inputs["Vector"])
    water = node(nodes, "ShaderNodeMapRange")
    water.inputs["From Min"].default_value = 0.50
    water.inputs["From Max"].default_value = 0.56
    links.new(dips.outputs["Fac"], water.inputs["Value"])
    grain = node(nodes, "ShaderNodeTexNoise")
    grain.inputs["Scale"].default_value = 38.0
    grain.inputs["Detail"].default_value = 6.0
    links.new(pos, grain.inputs["Vector"])
    # Roughness: wet film 0.14-0.30, joints and puddles near mirror.
    rough = node(nodes, "ShaderNodeMapRange")
    rough.inputs["To Min"].default_value = 0.13
    rough.inputs["To Max"].default_value = 0.32
    links.new(grain.outputs["Fac"], rough.inputs["Value"])
    joint = node(nodes, "ShaderNodeMix", data_type="FLOAT")
    links.new(brick.outputs["Fac"], joint.inputs["Factor"])
    links.new(rough.outputs["Result"], joint.inputs["A"])
    joint.inputs["B"].default_value = 0.06
    puddle = node(nodes, "ShaderNodeMix", data_type="FLOAT")
    links.new(water.outputs["Result"], puddle.inputs["Factor"])
    links.new(joint.outputs["Result"], puddle.inputs["A"])
    puddle.inputs["B"].default_value = 0.015
    links.new(puddle.outputs["Result"], bsdf.inputs["Roughness"])
    darker = node(nodes, "ShaderNodeMix", data_type="RGBA", blend_type="MULTIPLY")
    links.new(water.outputs["Result"], darker.inputs["Factor"])
    links.new(brick.outputs["Color"], darker.inputs["A"])
    darker.inputs["B"].default_value = (0.45, 0.45, 0.47, 1)
    links.new(darker.outputs["Result"], bsdf.inputs["Base Color"])
    # Joints are grooves; standing water is flat.
    groove = node(nodes, "ShaderNodeMath", operation="MULTIPLY")
    links.new(brick.outputs["Fac"], groove.inputs[0])
    groove.inputs[1].default_value = -1.0
    flat = node(nodes, "ShaderNodeMath", operation="SUBTRACT")
    flat.inputs[0].default_value = 1.0
    links.new(water.outputs["Result"], flat.inputs[1])
    bump = node(nodes, "ShaderNodeBump")
    bump.inputs["Distance"].default_value = 0.004
    links.new(groove.outputs[0], bump.inputs["Height"])
    links.new(flat.outputs[0], bump.inputs["Strength"])
    fine = node(nodes, "ShaderNodeBump")
    fine.inputs["Strength"].default_value = 0.05
    fine.inputs["Distance"].default_value = 0.001
    links.new(grain.outputs["Fac"], fine.inputs["Height"])
    links.new(fine.outputs["Normal"], bump.inputs["Normal"])
    links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    return mat


def stucco(name, base, damp=0.55):
    """Painted render with a damp band at the foot and uneven repainting."""
    mat = principled(name, base, 0.86)
    tree, nodes, links, bsdf = nodes_of(mat)
    pos = world_position(nodes)
    blotch = node(nodes, "ShaderNodeTexNoise")
    blotch.inputs["Scale"].default_value = 0.9
    blotch.inputs["Detail"].default_value = 8.0
    links.new(pos, blotch.inputs["Vector"])
    shade = node(nodes, "ShaderNodeMapRange")
    shade.inputs["To Min"].default_value = 0.78
    shade.inputs["To Max"].default_value = 1.08
    links.new(blotch.outputs["Fac"], shade.inputs["Value"])
    sep = nodes.new("ShaderNodeSeparateXYZ")
    links.new(pos, sep.inputs[0])
    foot = node(nodes, "ShaderNodeMapRange")
    foot.inputs["From Min"].default_value = 0.15
    foot.inputs["From Max"].default_value = 0.75
    foot.inputs["To Min"].default_value = damp
    foot.inputs["To Max"].default_value = 1.0
    links.new(sep.outputs["Z"], foot.inputs["Value"])
    both = node(nodes, "ShaderNodeMath", operation="MULTIPLY")
    links.new(shade.outputs["Result"], both.inputs[0])
    links.new(foot.outputs["Result"], both.inputs[1])
    tint = node(nodes, "ShaderNodeMix", data_type="RGBA", blend_type="MULTIPLY")
    tint.inputs["Factor"].default_value = 1.0
    tint.inputs["A"].default_value = (*base, 1)
    links.new(both.outputs[0], tint.inputs["B"])
    links.new(tint.outputs["Result"], bsdf.inputs["Base Color"])
    bump = node(nodes, "ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.12
    bump.inputs["Distance"].default_value = 0.003
    grain = node(nodes, "ShaderNodeTexNoise")
    grain.inputs["Scale"].default_value = 60.0
    links.new(pos, grain.inputs["Vector"])
    links.new(grain.outputs["Fac"], bump.inputs["Height"])
    links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    return mat


def gresite():
    """2.5 cm glass mosaic of the 1970s refit, amber and brown, glossy."""
    mat = principled("Gresite mosaic, amber and brown", (0.35, 0.16, 0.05), 0.08)
    tree, nodes, links, bsdf = nodes_of(mat)
    pos = world_position(nodes)
    brick = node(nodes, "ShaderNodeTexBrick", offset=0.0, squash=1.0)
    brick.inputs["Scale"].default_value = 1.0
    brick.inputs["Brick Width"].default_value = 0.026
    brick.inputs["Row Height"].default_value = 0.026
    brick.inputs["Mortar Size"].default_value = 0.0025
    brick.inputs["Bias"].default_value = 0.0
    brick.inputs["Color1"].default_value = (0.40, 0.17, 0.045, 1)
    brick.inputs["Color2"].default_value = (0.16, 0.075, 0.03, 1)
    brick.inputs["Mortar"].default_value = (0.32, 0.30, 0.27, 1)
    # Use X+Y so the same texture runs round the pier's faces.
    sep = nodes.new("ShaderNodeSeparateXYZ")
    links.new(pos, sep.inputs[0])
    add = node(nodes, "ShaderNodeMath", operation="ADD")
    links.new(sep.outputs["X"], add.inputs[0])
    links.new(sep.outputs["Y"], add.inputs[1])
    comb = nodes.new("ShaderNodeCombineXYZ")
    links.new(add.outputs[0], comb.inputs["X"])
    links.new(sep.outputs["Z"], comb.inputs["Y"])
    links.new(comb.outputs[0], brick.inputs["Vector"])
    links.new(brick.outputs["Color"], bsdf.inputs["Base Color"])
    rough = node(nodes, "ShaderNodeMapRange")
    rough.inputs["To Min"].default_value = 0.07
    rough.inputs["To Max"].default_value = 0.8
    links.new(brick.outputs["Fac"], rough.inputs["Value"])
    links.new(rough.outputs["Result"], bsdf.inputs["Roughness"])
    bump = node(nodes, "ShaderNodeBump")
    bump.inputs["Distance"].default_value = 0.002
    inv = node(nodes, "ShaderNodeMath", operation="MULTIPLY")
    links.new(brick.outputs["Fac"], inv.inputs[0])
    inv.inputs[1].default_value = -1.0
    links.new(inv.outputs[0], bump.inputs["Height"])
    links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    return mat


def worn_paint(name, base, wall):
    """Sign-writer's paint on render, worn through where the render breathes."""
    mat = principled(name, base, 0.7)
    tree, nodes, links, bsdf = nodes_of(mat)
    pos = world_position(nodes)
    wear = node(nodes, "ShaderNodeTexNoise")
    wear.inputs["Scale"].default_value = 4.0
    wear.inputs["Detail"].default_value = 10.0
    wear.inputs["Roughness"].default_value = 0.65
    links.new(pos, wear.inputs["Vector"])
    edge = node(nodes, "ShaderNodeMapRange")
    edge.inputs["From Min"].default_value = 0.64
    edge.inputs["From Max"].default_value = 0.70
    links.new(wear.outputs["Fac"], edge.inputs["Value"])
    mix = node(nodes, "ShaderNodeMix", data_type="RGBA")
    links.new(edge.outputs["Result"], mix.inputs["Factor"])
    mix.inputs["A"].default_value = (*base, 1)
    mix.inputs["B"].default_value = (*wall, 1)
    links.new(mix.outputs["Result"], bsdf.inputs["Base Color"])
    return mat


def galvanised():
    mat = principled("Galvanised shutter, streaked", (0.42, 0.43, 0.44), 0.42, metal=0.85)
    tree, nodes, links, bsdf = nodes_of(mat)
    pos = world_position(nodes)
    streak = node(nodes, "ShaderNodeTexNoise")
    streak.inputs["Scale"].default_value = 3.0
    streak.inputs["Detail"].default_value = 6.0
    scale = node(nodes, "ShaderNodeVectorMath", operation="MULTIPLY")
    links.new(pos, scale.inputs[0])
    scale.inputs[1].default_value = (6.0, 6.0, 0.4)
    links.new(scale.outputs[0], streak.inputs["Vector"])
    ramp = node(nodes, "ShaderNodeMapRange")
    ramp.inputs["To Min"].default_value = 0.28
    ramp.inputs["To Max"].default_value = 0.62
    links.new(streak.outputs["Fac"], ramp.inputs["Value"])
    links.new(ramp.outputs["Result"], bsdf.inputs["Roughness"])
    rust = node(nodes, "ShaderNodeMix", data_type="RGBA")
    rust.inputs["A"].default_value = (0.42, 0.43, 0.44, 1)
    rust.inputs["B"].default_value = (0.16, 0.08, 0.04, 1)
    fac = node(nodes, "ShaderNodeMapRange")
    fac.inputs["From Min"].default_value = 0.62
    fac.inputs["From Max"].default_value = 0.75
    links.new(streak.outputs["Fac"], fac.inputs["Value"])
    links.new(fac.outputs["Result"], rust.inputs["Factor"])
    links.new(rust.outputs["Result"], bsdf.inputs["Base Color"])
    return mat


def lightbox_face(name, color, strength, right_edge):
    """Backlit acrylic. Its right-hand fluorescent tube has died, dimming the
    end that stops at right_edge (world x)."""
    mat = principled(name, color, 0.25, emit=color, strength=strength)
    tree, nodes, links, bsdf = nodes_of(mat)
    sep = nodes.new("ShaderNodeSeparateXYZ")
    links.new(world_position(nodes), sep.inputs[0])
    dead = node(nodes, "ShaderNodeMapRange")
    dead.inputs["From Min"].default_value = right_edge - 1.35
    dead.inputs["From Max"].default_value = right_edge - 0.75
    dead.inputs["To Min"].default_value = strength
    dead.inputs["To Max"].default_value = strength * 0.17
    links.new(sep.outputs["X"], dead.inputs["Value"])
    links.new(dead.outputs["Result"], bsdf.inputs["Emission Strength"])
    return mat


# --------------------------------------------------------------------------- geometry


def link(obj, collection):
    collection.objects.link(obj)
    return obj


def mesh_object(name, vertices, faces, mat, collection, smooth=False):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    if mat:
        mesh.materials.append(mat)
    if smooth:
        for poly in mesh.polygons:
            poly.use_smooth = True
    return link(bpy.data.objects.new(name, mesh), collection)


def box(name, low, high, mat, collection):
    x, y, z = low
    X, Y, Z = high
    v = [(x, y, z), (X, y, z), (X, Y, z), (x, Y, z), (x, y, Z), (X, y, Z), (X, Y, Z), (x, Y, Z)]
    f = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    return mesh_object(name, v, f, mat, collection)


def wall_with_openings(name, x0, x1, z0, z1, openings, depth, mat, collection, y=0.0):
    """Front face at y with rectangular openings and their reveals (depth into +y)."""
    xs = sorted({x0, x1, *[o[0] for o in openings], *[o[1] for o in openings]})
    zs = sorted({z0, z1, *[o[2] for o in openings], *[o[3] for o in openings]})
    verts, faces = [], []

    def quad(a, b, c, d):
        base = len(verts)
        verts.extend([a, b, c, d])
        faces.append((base, base + 1, base + 2, base + 3))

    for i in range(len(xs) - 1):
        for j in range(len(zs) - 1):
            cx, cz = (xs[i] + xs[i + 1]) / 2, (zs[j] + zs[j + 1]) / 2
            if any(o[0] < cx < o[1] and o[2] < cz < o[3] for o in openings):
                continue
            quad((xs[i], y, zs[j]), (xs[i + 1], y, zs[j]), (xs[i + 1], y, zs[j + 1]), (xs[i], y, zs[j + 1]))
    for ox0, ox1, oz0, oz1 in openings:
        d = y + depth
        quad((ox0, y, oz1), (ox1, y, oz1), (ox1, d, oz1), (ox0, d, oz1))  # head
        if oz0 > z0 + 1e-6:
            quad((ox0, d, oz0), (ox1, d, oz0), (ox1, y, oz0), (ox0, y, oz0))  # sill
        quad((ox0, y, oz0), (ox0, y, oz1), (ox0, d, oz1), (ox0, d, oz0))
        quad((ox1, d, oz0), (ox1, d, oz1), (ox1, y, oz1), (ox1, y, oz0))
    return mesh_object(name, verts, faces, mat, collection)


def text(name, body, font, mat, collection, *, height=None, width=None, size=None,
         location=(0, 0, 0), rotation=(math.pi / 2, 0, 0), align="CENTER", extrude=0.0,
         bevel=0.0, offset=0.0, spacing=1.0, shear=0.0):
    """Text set by its overall height, overall width or size, placed at location."""
    data = bpy.data.curves.new(name, "FONT")
    data.body, data.size = body, 1.0
    data.font = data.font_bold = data.font_italic = data.font_bold_italic = font
    data.align_x, data.align_y = align, "CENTER"
    data.space_character = spacing
    data.shear = shear
    data.materials.append(mat)
    obj = link(bpy.data.objects.new(name, data), collection)
    bpy.context.view_layer.update()
    dims = obj.dimensions
    scale = size or (width / dims.x if width else height / dims.y)
    data.size = scale
    data.extrude, data.bevel_depth, data.offset = extrude, bevel, offset
    data.bevel_resolution = 2
    obj.location, obj.rotation_euler = location, rotation
    obj["lettering"] = body
    return obj


def bulb(name, location, lit, mats, collection, normal=(0, -1, 0)):
    data = mats["bulb mesh lit" if lit else "bulb mesh dead"]
    obj = link(bpy.data.objects.new(name, data), collection)
    obj.location = location
    obj.rotation_euler = Vector(normal).to_track_quat("Z", "Y").to_euler()
    if not lit:
        obj["broken"] = "dead bulb"
    return obj


def bulb_meshes(mats):
    for key, mat in (("lit", mats["bulb lit"]), ("dead", mats["bulb dead"])):
        verts, faces = [], []
        rings, seg, r = 6, 10, 0.03
        verts.append((0, 0, 0.012))
        for i in range(1, rings + 1):
            phi = math.pi * i / (rings + 1)
            for j in range(seg):
                th = math.tau * j / seg
                verts.append((r * math.sin(phi) * math.cos(th), r * math.sin(phi) * math.sin(th), 0.042 - r * math.cos(phi) * 1.0))
        verts.append((0, 0, 0.042 + r))
        for j in range(seg):
            faces.append((0, 1 + j, 1 + (j + 1) % seg))
        for i in range(rings - 1):
            for j in range(seg):
                a = 1 + i * seg + j
                b = 1 + i * seg + (j + 1) % seg
                faces.append((a, b, b + seg, a + seg))
        top = len(verts) - 1
        last = 1 + (rings - 1) * seg
        for j in range(seg):
            faces.append((last + j, top, last + (j + 1) % seg))
        mesh = bpy.data.meshes.new(f"Bulb {key}")
        mesh.from_pydata(verts, [], faces)
        mesh.materials.append(mat)
        for poly in mesh.polygons:
            poly.use_smooth = True
        mats[f"bulb mesh {key}"] = mesh


def ribbed_shutter(name, x0, x1, z0, z1, mat, collection, y=-0.05):
    """Roller-shutter slats: a corrugated surface with a heavier bottom bar."""
    verts, faces = [], []
    pitch, depth = 0.075, 0.012
    rows = int((z1 - z0) / (pitch / 6))
    for i in range(rows + 1):
        z = z0 + (z1 - z0) * i / rows
        phase = ((z - z0) % pitch) / pitch
        dy = depth * (0.5 - abs(phase - 0.5)) * 2
        verts.extend([(x0, y - dy, z), (x1, y - dy, z)])
    for i in range(rows):
        a = 2 * i
        faces.append((a, a + 1, a + 3, a + 2))
    obj = mesh_object(name, verts, faces, mat, collection, smooth=True)
    return obj


# --------------------------------------------------------------------------- the model


def railing(name, x, slab_z, mat, collection):
    """Balcony railing: square bars on three sides and a top rail, one mesh."""
    bars = []
    for k in range(20):
        bx = x - 0.9 + k * 0.095
        bars.append(((bx - 0.008, -0.73, slab_z), (bx + 0.008, -0.715, slab_z + 1.0)))
    for k in range(8):
        by = -0.7 + k * 0.095
        bars.append(((x - 0.93, by - 0.008, slab_z), (x - 0.915, by + 0.008, slab_z + 1.0)))
        bars.append(((x + 0.915, by - 0.008, slab_z), (x + 0.93, by + 0.008, slab_z + 1.0)))
    bars.append(((x - 0.95, -0.75, slab_z + 0.98), (x + 0.95, -0.7, slab_z + 1.03)))
    verts, faces = [], []
    for (x0, y0, z0), (x1, y1, z1) in bars:
        b = len(verts)
        verts.extend([(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
                      (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)])
        faces.extend([(b, b + 1, b + 5, b + 4), (b + 1, b + 2, b + 6, b + 5), (b + 2, b + 3, b + 7, b + 6),
                      (b + 3, b, b + 4, b + 7), (b + 4, b + 5, b + 6, b + 7)])
    return mesh_object(name, verts, faces, mat, collection)


def cable(name, points, mat, collection):
    data = bpy.data.curves.new(name, "CURVE")
    data.dimensions, data.bevel_depth, data.bevel_resolution = "3D", 0.007, 2
    spline = data.splines.new("NURBS")
    spline.points.add(len(points) - 1)
    for p, co in zip(spline.points, points):
        p.co = (*co, 1)
    spline.use_endpoint_u = True
    data.materials.append(mat)
    return link(bpy.data.objects.new(name, data), collection)


LED_GLYPHS = {  # 5 x 7 dot glyphs for the 2015 sign
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "B": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    "I": ["11111", "00100", "00100", "00100", "00100", "00100", "11111"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
}


def gooseneck(name, x, panel_top, lit, mats, collection):
    """Sign lamp: an arm from above the panel and a shade aimed back down at it."""
    head = Vector((x, -0.5, panel_top - 0.08))
    aim_at = Vector((x, 0.0, panel_top - 0.75))
    d = (aim_at - head).normalized()
    apex = head - d * 0.15
    cable(f"{name}, arm", [(x, 0.0, panel_top + 0.04), (x, -0.3, panel_top + 0.06), tuple(apex)], mats["gooseneck"], collection)
    collection.objects[f"{name}, arm"].data.bevel_depth = 0.012
    u = d.orthogonal().normalized()
    v = d.cross(u)
    seg, verts, faces = 16, [tuple(apex)], []
    for j in range(seg):
        a = math.tau * j / seg
        verts.append(tuple(head + (u * math.cos(a) + v * math.sin(a)) * 0.09))
    for j in range(seg):
        faces.append((0, 1 + j, 1 + (j + 1) % seg))
    mesh_object(f"{name}, shade", verts, faces, mats["gooseneck"], collection, smooth=True)
    disc_c = head - d * 0.035
    disc = [tuple(disc_c)] + [tuple(disc_c + (u * math.cos(math.tau * j / seg) + v * math.sin(math.tau * j / seg)) * 0.055) for j in range(seg)]
    mesh_object(f"{name}, lamp", disc, [(0, 1 + (j + 1) % seg, 1 + j) for j in range(seg)],
                mats["lamp lit" if lit else "bulb dead"], collection)
    if lit:
        spot = bpy.data.lights.new(f"{name}, light", "SPOT")
        spot.energy, spot.color, spot.shadow_soft_size = 60.0, (1.0, 0.72, 0.45), 0.04
        spot.spot_size, spot.spot_blend = math.radians(130), 0.8
        lamp = link(bpy.data.objects.new(f"{name}, light", spot), collection)
        lamp.location = head - d * 0.02
        lamp.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    else:
        collection.objects[f"{name}, lamp"]["broken"] = "blown lamp"


def screen_material(name, c1, c2, scale):
    """A game's attract screen: two colours in bands, emitting."""
    mat = principled(name, (0.02, 0.02, 0.02), 0.1, emit=c1, strength=1.2)
    tree, nodes, links, bsdf = nodes_of(mat)
    coord = nodes.new("ShaderNodeTexCoord")
    wave = node(nodes, "ShaderNodeTexWave", wave_type="BANDS", bands_direction="DIAGONAL")
    wave.inputs["Scale"].default_value = scale
    wave.inputs["Distortion"].default_value = 3.0
    links.new(coord.outputs["Object"], wave.inputs["Vector"])
    mix = node(nodes, "ShaderNodeMix", data_type="RGBA")
    links.new(wave.outputs["Fac"], mix.inputs["Factor"])
    mix.inputs["A"].default_value = (*c1, 1)
    mix.inputs["B"].default_value = (*c2, 1)
    links.new(mix.outputs["Result"], bsdf.inputs["Emission Color"])
    return mat


# Cabinet side profile: (depth behind the front plane, height). It faces -x.
CABINET_PROFILE = [(0.75, 0.0), (0.0, 0.0), (0.0, 0.85), (-0.12, 0.92), (-0.05, 1.0), (0.08, 1.02),
                   (0.2, 1.52), (0.05, 1.6), (-0.03, 1.62), (-0.03, 1.88), (0.75, 1.88)]


def cabinet_mesh(body_mat):
    """An upright arcade cabinet: base, control deck, sloped screen, marquee."""
    half, n = 0.34, len(CABINET_PROFILE)
    verts = [(dx, -half, z) for dx, z in CABINET_PROFILE] + [(dx, half, z) for dx, z in CABINET_PROFILE]
    faces = [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
    faces += [tuple(range(n)), tuple(range(2 * n - 1, n - 1, -1))]
    mesh = bpy.data.meshes.new("Arcade cabinet")
    mesh.from_pydata(verts, [], faces)
    mesh.materials.append(body_mat)
    mesh.materials.append(body_mat)  # side art, set per cabinet
    for poly in mesh.polygons[n:]:
        poly.material_index = 1
    return mesh


def cabinet_faces(name, at, screen_mat, marquee_mat, collection):
    """The emitting screen on the sloped bezel and the lit marquee above it."""
    x, y = at
    half = 0.28
    (ax, az), (bx, bz) = (0.08, 1.02), (0.2, 1.52)
    off = Vector((-(bz - az), 0, bx - ax)).normalized() * 0.004
    quad = [Vector((x + ax, y - half, az)) + off, Vector((x + ax, y + half, az)) + off,
            Vector((x + bx, y + half, bz)) + off, Vector((x + bx, y - half, bz)) + off]
    mesh_object(f"{name} screen", [tuple(v) for v in quad], [(0, 1, 2, 3)], screen_mat, collection)
    mx = x - 0.034
    mesh_object(f"{name} marquee", [(mx, y - 0.3, 1.65), (mx, y + 0.3, 1.65), (mx, y + 0.3, 1.85), (mx, y - 0.3, 1.85)],
                [(0, 1, 2, 3)], marquee_mat, collection)
