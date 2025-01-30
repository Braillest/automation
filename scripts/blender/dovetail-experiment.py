import bpy

# Define the vertex positions for the trapezoidal prism
vertices = [
    ( 0.0,  0.0,  0.0),  # Bottom face
    ( 2.0,  0.0,  0.0),
    ( 1.5,  2.0,  0.0),
    ( 0.5,  2.0,  0.0),
    ( 0.0,  0.0,  1.0),  # Top face
    ( 2.0,  0.0,  1.0),
    ( 1.5,  2.0,  1.0),
    ( 0.5,  2.0,  1.0),
]

# Define faces using the vertex indices
faces = [
    (0, 1, 2, 3),  # Bottom face
    (4, 5, 6, 7),  # Top face
    (0, 1, 5, 4),  # Side 1
    (1, 2, 6, 5),  # Side 2
    (2, 3, 7, 6),  # Side 3
    (3, 0, 4, 7),  # Side 4
]

# Create a new mesh and object
mesh = bpy.data.meshes.new(name="TrapezoidalPrism")
obj = bpy.data.objects.new("TrapezoidalPrism", mesh)

# Link the object to the scene
bpy.context.collection.objects.link(obj)

# Create mesh from given vertices and faces
mesh.from_pydata(vertices, [], faces)

# Update mesh with new geometry
mesh.update()
