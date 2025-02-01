import bpy
import math

# Define global vars
scaling_factor = 1.005

alignment_hole_w = 1.1
alignment_hole_h = 4.6
alignment_hole_d = 1.4

alignment_pin_w = 1
alignment_pin_h = 4.5
alignment_pin_d = 1.2

braille_dot_diameter = 1.5
braille_dot_spacing = 2.5
braille_dot_d = 0.6

braille_hole_diameter = 1.9
braille_hole_d = 0.8

paper_w = 216
paper_h = 280
paper_d = 0.2

cell_padding_x = 1.75
cell_padding_y = 2.5
cell_w = 6
cell_x_count = math.floor(216 / 6) - 2
cell_h = 10
cell_y_count = math.floor(280 / 10) - 2

content_w = cell_x_count * cell_w
content_h = cell_y_count * cell_h

paper_margin_x = 0.1
paper_padding_x = (paper_w - content_w) / 2
paper_padding_y = (paper_h - content_h) / 2

mold_interface_d = 0.2
mold_negative_d = alignment_hole_d + mold_interface_d

negative_tab_w = 6.1
negative_tab_h = 6

positive_tab_w = 6
positive_tab_h = 6

puzzle_w = 10
puzzle_h = 10

line_w = paper_w + (2 * paper_margin_x) + alignment_pin_w + puzzle_w
line_h = 10
line_d = mold_negative_d

# Clear scene
bpy.ops.object.mode_set(mode="OBJECT")
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete()

positive_alignment_tab_vertices = [
    (0.0, 0.0, 0.0),
    (positive_tab_w / 2, positive_tab_h, 0.0),
    (-positive_tab_w / 2, positive_tab_h, 0.0),
    (0.0, 0.0, mold_negative_d),
    (positive_tab_w / 2, positive_tab_h, mold_negative_d),
    (-positive_tab_w / 2, positive_tab_h, mold_negative_d),
]
positive_alignment_tab_faces = [
    (0, 1, 2),
    (3, 4, 5),
    (0, 1, 4, 3),
    (1, 2, 5, 4),
    (2, 0, 3, 5),
]
positive_alignment_tab_mesh = bpy.data.meshes.new(name="Positive Alignment Tab")
positive_alignment_tab_mesh.from_pydata(positive_alignment_tab_vertices, [], positive_alignment_tab_faces)
positive_alignment_tab_obj = bpy.data.objects.new("Positive Alignment Tab", object_data=positive_alignment_tab_mesh)
bpy.context.collection.objects.link(positive_alignment_tab_obj)
bpy.ops.object.select_all(action="DESELECT")
bpy.context.view_layer.objects.active = positive_alignment_tab_obj
bpy.ops.object.mode_set(mode="EDIT")
bpy.ops.mesh.normals_make_consistent(inside=False)
bpy.ops.object.mode_set(mode="OBJECT")

# Negative tab
negative_alignment_tab_vertices = [
    (0.0, 0.0, 0.0),
    (negative_tab_w / 2, negative_tab_h, 0.0),
    (-negative_tab_w / 2, negative_tab_h, 0.0),
    (0.0, 0.0, mold_negative_d),
    (negative_tab_w / 2, negative_tab_h, mold_negative_d),
    (-negative_tab_w / 2, negative_tab_h, mold_negative_d),
]
negative_alignment_tab_faces = [
    (0, 1, 2),
    (3, 4, 5),
    (0, 1, 4, 3),
    (1, 2, 5, 4),
    (2, 0, 3, 5),
]
negative_alignment_tab_mesh = bpy.data.meshes.new(name="Negaative Alignment Tab")
negative_alignment_tab_mesh.from_pydata(negative_alignment_tab_vertices, [], negative_alignment_tab_faces)
negative_alignment_tab_obj = bpy.data.objects.new("Negative Alignment Tab", object_data=negative_alignment_tab_mesh)
bpy.context.collection.objects.link(negative_alignment_tab_obj)
bpy.ops.object.select_all(action="DESELECT")
bpy.context.view_layer.objects.active = negative_alignment_tab_obj
bpy.ops.object.mode_set(mode="EDIT")
bpy.ops.mesh.normals_make_consistent(inside=False)
bpy.ops.object.mode_set(mode="OBJECT")

# Alignment pin
bpy.ops.mesh.primitive_cube_add(scale=(alignment_pin_w / 2, alignment_pin_h / 2, alignment_pin_d / 2))
alignment_pin_obj = bpy.context.object

# Alignment hole
bpy.ops.mesh.primitive_cube_add(scale=(alignment_hole_w / 2, alignment_hole_h / 2, alignment_hole_d))
alignment_hole_obj = bpy.context.object

def main():

    draw_paper()

    for y in range(cell_y_count):
        draw_line(y)
        for x in range(cell_x_count):
            pass

    # Remove persistent tools
    bpy.data.objects.remove(positive_alignment_tab_obj, do_unlink=True)
    bpy.data.objects.remove(negative_alignment_tab_obj, do_unlink=True)
    bpy.data.objects.remove(alignment_pin_obj, do_unlink=True)
    bpy.data.objects.remove(alignment_hole_obj, do_unlink=True)

def draw_paper():

    paper_x = paper_w / 2
    paper_y = paper_h / 2
    paper_z = mold_negative_d + braille_dot_d + (paper_d / 2)
    paper_location = (paper_x, paper_y, paper_z)
    paper_scale = (paper_w / 2, paper_h / 2, paper_d / 2)
    paper_mesh = bpy.ops.mesh.primitive_cube_add(scale=paper_scale, location=paper_location)
    paper_obj = bpy.context.object
    paper_obj.name = "Paper"
    paper_obj.data.name = "Paper mesh"
    paper_mat = bpy.data.materials.new(name="Paper material")
    paper_mat.diffuse_color = (0.8, 0.9, 0.9, 1.0) # RGBA
    paper_obj.data.materials.append(paper_mat)

def draw_line(line_number):

    # Line
    line_x = (paper_w / 2)
    line_y = ((cell_y_count - line_number - 1) * cell_h) + (cell_h / 2) + paper_padding_y
    line_z = (mold_negative_d / 2)
    line_location = (line_x, line_y, line_z)
    line_scale = (line_w / 2, line_h / 2, line_d / 2)
    line_mesh = bpy.ops.mesh.primitive_cube_add(location=line_location, scale=line_scale)
    line_obj = bpy.context.object
    line_obj.name = f"Line {line_number:03}"
    line_obj.data.name = "Line {line_number:03} mesh"

    # Left negative tab and difference
    negative_alignment_tab_obj.location.x = -paper_margin_x - (alignment_pin_w / 2)
    negative_alignment_tab_obj.location.y = line_y - line_h + 0.5
    left_negative_alignment_tab_obj = negative_alignment_tab_obj.copy()
    bool_modifier = line_obj.modifiers.new(name="Negative Removal", type="BOOLEAN")
    bool_modifier.operation = "DIFFERENCE"
    bool_modifier.solver = "EXACT"
    bool_modifier.object = left_negative_alignment_tab_obj
    bpy.ops.object.modifier_apply(modifier=bool_modifier.name)

    # Left positive tab and union
    positive_alignment_tab_obj.location.x = -paper_margin_x - (alignment_pin_w / 2)
    positive_alignment_tab_obj.location.y = line_y + 0.5
    left_positive_alignment_tab_obj = positive_alignment_tab_obj.copy()
    bpy.context.collection.objects.link(left_positive_alignment_tab_obj)
    union_modifier = line_obj.modifiers.new(name="Tab Union", type="BOOLEAN")
    union_modifier.operation = "UNION"
    union_modifier.solver = "EXACT"
    union_modifier.object = left_positive_alignment_tab_obj
    bpy.ops.object.modifier_apply(modifier=union_modifier.name)

    # Right negative tab and difference
    negative_alignment_tab_obj.location.x = paper_w + paper_margin_x + (alignment_pin_w / 2)
    right_negative_alignment_tab_obj = negative_alignment_tab_obj.copy()
    bool_modifier = line_obj.modifiers.new(name="Negative Removal", type="BOOLEAN")
    bool_modifier.operation = "DIFFERENCE"
    bool_modifier.solver = "EXACT"
    bool_modifier.object = right_negative_alignment_tab_obj
    bpy.ops.object.modifier_apply(modifier=bool_modifier.name)

    # Right positive tab and union
    positive_alignment_tab_obj.location.x = paper_w + paper_margin_x + (alignment_pin_w / 2)
    right_positive_alignment_tab_obj = positive_alignment_tab_obj.copy()
    bpy.context.collection.objects.link(right_positive_alignment_tab_obj)
    union_modifier = line_obj.modifiers.new(name="Tab Union", type="BOOLEAN")
    union_modifier.operation = "UNION"
    union_modifier.solver = "EXACT"
    union_modifier.object = right_positive_alignment_tab_obj
    bpy.ops.object.modifier_apply(modifier=union_modifier.name)

    # Left alignment pin
    alignment_pin_obj.location.x = -paper_margin_x - (alignment_pin_w / 2)
    alignment_pin_obj.location.y = line_y + (1.5 / 2)
    alignment_pin_obj.location.z = mold_negative_d + (alignment_pin_d / 2)
    left_alignment_pin_obj = alignment_pin_obj.copy()
    bpy.context.collection.objects.link(left_alignment_pin_obj)
    union_modifier = line_obj.modifiers.new(name="Pin Union", type="BOOLEAN")
    union_modifier.operation = "UNION"
    union_modifier.solver = "EXACT"
    union_modifier.object = left_alignment_pin_obj
    bpy.ops.object.modifier_apply(modifier=union_modifier.name)

    # Right alignment pin
    alignment_pin_obj.location.x = paper_w + paper_margin_x + (alignment_pin_w / 2)
    right_alignment_pin_obj = alignment_pin_obj.copy()
    bpy.context.collection.objects.link(right_alignment_pin_obj)
    union_modifier = line_obj.modifiers.new(name="Pin Union", type="BOOLEAN")
    union_modifier.operation = "UNION"
    union_modifier.solver = "EXACT"
    union_modifier.object = right_alignment_pin_obj
    bpy.ops.object.modifier_apply(modifier=union_modifier.name)

    # Left alignment hole
    alignment_hole_obj.location.x = -paper_margin_x - (alignment_hole_w / 2)
    alignment_hole_obj.location.y = line_y + (1.5 / 2)
    alignment_hole_obj.location.z = 0
    left_alignment_hole_obj = alignment_hole_obj.copy()
    bpy.context.collection.objects.link(left_alignment_hole_obj)
    bool_modifier = line_obj.modifiers.new(name="Negative Removal", type="BOOLEAN")
    bool_modifier.operation = "DIFFERENCE"
    bool_modifier.solver = "EXACT"
    bool_modifier.object = left_alignment_hole_obj
    bpy.ops.object.modifier_apply(modifier=bool_modifier.name)

    # Right alignment hole
    alignment_hole_obj.location.x = paper_w + paper_margin_x + (alignment_hole_w / 2)
    right_alignment_hole_obj = alignment_hole_obj.copy()
    bpy.context.collection.objects.link(right_alignment_hole_obj)
    bool_modifier = line_obj.modifiers.new(name="Negative Removal", type="BOOLEAN")
    bool_modifier.operation = "DIFFERENCE"
    bool_modifier.solver = "EXACT"
    bool_modifier.object = right_alignment_hole_obj
    bpy.ops.object.modifier_apply(modifier=bool_modifier.name)

    # Remove tools
    bpy.data.objects.remove(left_positive_alignment_tab_obj, do_unlink=True)
    bpy.data.objects.remove(right_positive_alignment_tab_obj, do_unlink=True)
    bpy.data.objects.remove(left_negative_alignment_tab_obj, do_unlink=True)
    bpy.data.objects.remove(right_negative_alignment_tab_obj, do_unlink=True)
    bpy.data.objects.remove(left_alignment_pin_obj, do_unlink=True)
    bpy.data.objects.remove(right_alignment_pin_obj, do_unlink=True)
    bpy.data.objects.remove(left_alignment_hole_obj, do_unlink=True)
    bpy.data.objects.remove(right_alignment_hole_obj, do_unlink=True)

if __name__ == "__main__":
    main()
