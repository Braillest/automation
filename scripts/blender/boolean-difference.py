import bpy

# Clear scene
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete()

# Create a base cube as "line"
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
line = bpy.context.object  # The newly created cube

# Create a custom object with from_pydata()
mesh = bpy.data.meshes.new(name="CustomNegative")
negative_alignment_tab_obj = bpy.data.objects.new(name="NegativeObject", object_data=mesh)
bpy.context.collection.objects.link(negative_alignment_tab_obj)

# Example mesh data for the custom object (ensure it has faces!)
verts = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1)]
faces = [(0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4), (2, 3, 7, 6), (0, 3, 7, 4), (1, 2, 6, 5)]
mesh.from_pydata(verts, [], faces)
mesh.update()

# Ensure the object is a proper mesh
bpy.ops.object.select_all(action='DESELECT')
bpy.context.view_layer.objects.active = negative_alignment_tab_obj
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.normals_make_consistent(inside=False)  # Fix normals
bpy.ops.object.mode_set(mode='OBJECT')

# Apply transforms to avoid Boolean issues
#bpy.context.view_layer.objects.active = negative_alignment_tab_obj
#bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

# Ensure Boolean target is visible
#negative_alignment_tab_obj.hide_viewport = False
#negative_alignment_tab_obj.hide_render = False

# Create and configure Boolean modifier
bool_modifier = line.modifiers.new(name="Negative Removal", type="BOOLEAN")
bool_modifier.operation = "DIFFERENCE"
bool_modifier.solver = "EXACT"
bool_modifier.object = negative_alignment_tab_obj

# Ensure we are in Object Mode before applying modifier
#bpy.ops.object.mode_set(mode='OBJECT')

# Set active object and apply modifier
#bpy.context.view_layer.objects.active = line
#line.select_set(True)

# Apply modifier
bpy.ops.object.modifier_apply(modifier=bool_modifier.name)
