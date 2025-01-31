import bpy
import math

# Define global vars
scaling_factor = 1.005

alignment_hole_x = 1 * scaling_factor
alignment_hole_y = 4.5 * scaling_factor
alignment_hole_z = 1.4

alignment_pin_x = 1 * scaling_factor
alignment_pin_y = 4.5 * scaling_factor
alignment_pin_z = 1.2

braille_dot_diameter = 1.5 * scaling_factor
braille_dot_spacing = 2.5 * scaling_factor
braille_dot_z = 0.6

braille_hole_diameter = 1.9 * scaling_factor
braille_hole_z = 0.8

paper_x = 216 * scaling_factor
paper_y = 280 * scaling_factor
paper_z = 0.2

cell_padding_x = 1.75 * scaling_factor
cell_padding_y = 2.5 * scaling_factor
cell_x = 6 * scaling_factor
cell_x_count = math.floor(216 / 6) - 2
cell_y = 10 * scaling_factor
cell_y_count = math.floor(280 / 10) - 2

content_x = cell_x_count * cell_x
content_y = cell_y_count * cell_y

paper_margin_x = 0.1
paper_padding_x = (paper_x - content_x) / 2
paper_padding_y = (paper_y - content_y) / 2

mold_interface_z = 0.2
mold_negative_z = alignment_hole_z + mold_interface_z

negative_tab_x = 6.1 * scaling_factor
negative_tab_y = 1.5 * scaling_factor

positive_tab_x = 6 * scaling_factor
positive_tab_y = 1.5 * scaling_factor

puzzle_x = 10 * scaling_factor
puzzle_y = 10 * scaling_factor

line_x = paper_x + paper_margin_x + (alignment_pin_x / 2) + (puzzle_x / 2)
line_y = 10 * scaling_factor

# Clear scene
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete()

# Positive tab
positive_alignment_tab_vertices = [
    ( 0.0,  0.0,  0.0),  # Bottom face
    ( positive_tab_x,  0.0,  0.0),
    ( positive_tab_x - positive_tab_y,  -positive_tab_y,  0.0),
    ( positive_tab_y,  -positive_tab_y,  0.0),
    ( 0.0,  0.0,  mold_negative_z),  # Top face
    ( positive_tab_x,  0.0,  mold_negative_z),
    ( positive_tab_x - positive_tab_y,  -positive_tab_y,  mold_negative_z),
    ( positive_tab_y,  -positive_tab_y,  mold_negative_z),
]
positive_alignment_tab_faces = [
    (0, 1, 2, 3),  # Bottom face
    (4, 5, 6, 7),  # Top face
    (0, 1, 5, 4),  # Side 1
    (1, 2, 6, 5),  # Side 2
    (2, 3, 7, 6),  # Side 3
    (3, 0, 4, 7),  # Side 4
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
    ( 0.0,  0.0,  0.0),  # Bottom face
    ( negative_tab_x,  0.0,  0.0),
    ( negative_tab_x - negative_tab_y,  -negative_tab_y,  0.0),
    ( negative_tab_y,  -negative_tab_y,  0.0),
    ( 0.0,  0.0,  mold_negative_z),  # Top face
    ( negative_tab_x,  0.0,  mold_negative_z),
    ( negative_tab_x - negative_tab_y,  -negative_tab_y,  mold_negative_z),
    ( negative_tab_y,  -negative_tab_y,  mold_negative_z),
]
negative_alignment_tab_faces = [
    (0, 1, 2, 3),  # Bottom face
    (4, 5, 6, 7),  # Top face
    (0, 1, 5, 4),  # Side 1
    (1, 2, 6, 5),  # Side 2
    (2, 3, 7, 6),  # Side 3
    (3, 0, 4, 7),  # Side 4
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
bpy.ops.mesh.primitive_cube_add(scale=(alignment_pin_x / 2, alignment_pin_y / 2, alignment_pin_z / 2))
alignment_pin = bpy.context.object

def main():

    draw_paper()

    for y in range(cell_y_count):
        draw_line(y)
        for x in range(cell_x_count):
            pass

    bpy.data.objects.remove(positive_alignment_tab_obj, do_unlink=True)
    bpy.data.objects.remove(negative_alignment_tab_obj, do_unlink=True)

def draw_paper():

    bpy.ops.mesh.primitive_cube_add(location=(paper_x / 2 , paper_y / 2, mold_negative_z + braille_dot_z + (paper_z / 2)))
    paper = bpy.context.object
    paper.scale.x = paper_x / 2
    paper.scale.y = paper_y / 2
    paper.scale.z = paper_z / 2
    paper_mat = bpy.data.materials.new(name="Paper Material")
    paper_mat.diffuse_color = (0.8, 0.9, 0.9, 1.0) # RGBA
    paper.data.materials.append(paper_mat)

def draw_line(line_number):

    # Line
    x = (paper_x / 2)
    y = ((cell_y_count - line_number - 1) * cell_y) + (cell_y / 2)
    z = (mold_negative_z / 2)
    bpy.ops.mesh.primitive_cube_add(location=(x , y, z))
    line = bpy.context.object
    line.scale.x = (content_x / 2) + paper_padding_x + paper_margin_x + (alignment_pin_x / 2) + (puzzle_x / 2)
    line.scale.y = cell_y / 2
    line.scale.z = mold_negative_z / 2

    # Left negative tab and difference
    negative_alignment_tab_obj.location.x = paper_margin_x - (alignment_pin_x / 2) - (negative_tab_x / 2)
    negative_alignment_tab_obj.location.y = y - (line_y / 2) + negative_tab_y
    bool_modifier = line.modifiers.new(name="Negative Removal", type="BOOLEAN")
    bool_modifier.operation = "DIFFERENCE"
    bool_modifier.solver = "EXACT"
    bool_modifier.object = negative_alignment_tab_obj
    bpy.ops.object.modifier_apply(modifier=bool_modifier.name)

    # Left positive tab and union
    positive_alignment_tab_obj.location.x = paper_margin_x - (alignment_pin_x / 2) - (positive_tab_x / 2)
    positive_alignment_tab_obj.location.y = y + (line_y / 2) + positive_tab_y
    left_positive_alignment_tab_obj = positive_alignment_tab_obj.copy()
    bpy.context.collection.objects.link(left_positive_alignment_tab_obj)
    union_modifier = line.modifiers.new(name="Tab Union", type="BOOLEAN")
    union_modifier.operation = "UNION"
    union_modifier.solver = "EXACT"
    union_modifier.object = left_positive_alignment_tab_obj
    bpy.ops.object.modifier_apply(modifier=union_modifier.name)

    # Right negative tab and difference
    negative_alignment_tab_obj.location.x = paper_x + paper_margin_x + (alignment_pin_x / 2) - (negative_tab_x / 2)
    bool_modifier = line.modifiers.new(name="Negative Removal", type="BOOLEAN")
    bool_modifier.operation = "DIFFERENCE"
    bool_modifier.solver = "EXACT"
    bool_modifier.object = negative_alignment_tab_obj
    bpy.ops.object.modifier_apply(modifier=bool_modifier.name)

    # Right positive tab and union
    positive_alignment_tab_obj.location.x = paper_x + paper_margin_x + (alignment_pin_x / 2) - (positive_tab_x / 2)
    right_positive_alignment_tab_obj = positive_alignment_tab_obj.copy()
    bpy.context.collection.objects.link(right_positive_alignment_tab_obj)
    union_modifier = line.modifiers.new(name="Tab Union", type="BOOLEAN")
    union_modifier.operation = "UNION"
    union_modifier.solver = "EXACT"
    union_modifier.object = right_positive_alignment_tab_obj
    bpy.ops.object.modifier_apply(modifier=union_modifier.name)

    # Alignment pin
    alignment_pin.location.x = -paper_margin_x - (alignment_hole_x / 2)
    alignment_pin.location.y = y + (negative_tab_y / 2)
    alignment_pin.location.z = mold_negative_z + (alignment_pin_z / 2)
    left_alignment_pin = alignment_pin.copy()
    bpy.context.collection.objects.link(left_alignment_pin)
    alignment_pin.location.x = paper_x + paper_margin_x + (alignment_hole_x / 2)
    right_alignment_pin = alignment_pin.copy()
    bpy.context.collection.objects.link(right_alignment_pin)

    # Alignment hole

    # Remove unlinked left and right tabs
    bpy.data.objects.remove(left_positive_alignment_tab_obj, do_unlink=True)
    bpy.data.objects.remove(right_positive_alignment_tab_obj, do_unlink=True)

if __name__ == "__main__":
    main()
