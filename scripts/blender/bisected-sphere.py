import bpy

def create_dome(location, radius=2):
    # Create a UV sphere
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=location)
    dome = bpy.context.object
    
    # Enter Edit Mode
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    
    # Switch to vertex selection mode
    bpy.ops.mesh.select_mode(type="VERT")
    
    # Select vertices below the equator
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.bisect(plane_co=(0, 0, location[2]), plane_no=(0, 0, -1), clear_inner=True)
    
    # Return to Object Mode
    bpy.ops.object.mode_set(mode='OBJECT')

def main():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()  # Clear existing objects

    create_dome(location=(0, 0, 1))  # Create dome at origin

    # Export to STL
    # bpy.ops.export_mesh.stl(filepath="/tmp/dome.stl")

if __name__ == "__main__":
    main()
