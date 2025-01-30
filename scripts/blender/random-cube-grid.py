import bpy
import random

def create_material(color):
    mat = bpy.data.materials.new(name="Mat")
    mat.diffuse_color = (*color, 1.0)  # RGBA
    return mat

def create_cube(x, y):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, 0))
    cube = bpy.context.object
    
    # Random scaling
    scale_factor = random.uniform(0.5, 2.0)
    cube.scale.z = scale_factor
    
    # Assign material
    mat = create_material((random.random(), random.random(), random.random()))
    cube.data.materials.append(mat)

def main():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()  # Clear existing objects
    
    for i in range(10):
        for j in range(10):
            create_cube(i * 2, j * 2)  # Space out cubes

if __name__ == "__main__":
    main()
