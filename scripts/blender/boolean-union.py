import bpy

# Delete all existing objects (optional)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Create two cubes at different locations
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
cube1 = bpy.context.object

bpy.ops.mesh.primitive_cube_add(location=(1, 0, 0))  # Slight offset to overlap
cube2 = bpy.context.object

# Make sure we are in object mode
bpy.ops.object.mode_set(mode='OBJECT')

# Add Boolean Modifier to first cube
bool_mod = cube1.modifiers.new(name="Union", type='BOOLEAN')
bool_mod.operation = 'UNION'
bool_mod.object = cube2

# Apply the modifier
bpy.context.view_layer.objects.active = cube1  # Ensure active object
bpy.ops.object.modifier_apply(modifier=bool_mod.name)

# Remove the second object after union
bpy.data.objects.remove(cube2, do_unlink=True)

print("Objects unioned successfully!")