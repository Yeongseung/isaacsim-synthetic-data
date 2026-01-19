import numpy as np
import omni.usd
import omni.kit.commands
from pxr import UsdGeom, Gf, Sdf, UsdPhysics, UsdShade

import isaacsim.core.utils.stage as stage_utils
import isaacsim.core.utils.nucleus as nucleus_utils
import isaacsim.core.utils.prims as prim_utils

# ---------------------------------------------------------
# 1. Configuration
# ---------------------------------------------------------
farm_path = "/World/AgriculturalTerrain"
ground_path = "/World/OuterGround"
material_path = "/World/Looks/Cardboard_Low_Quality_Dirt"

# Terrain Settings
farm_width, farm_length = 5.0, 15.0   
res = 0.2         
outer_size = 80.0 
ridge_height, row_spacing, bumpiness = 0.2, 7.0, 0.03

# ---------------------------------------------------------
# 2. Function: Create Mesh with Material
# ---------------------------------------------------------
def create_mesh_with_material(name_path, points, uvs, face_counts, face_indices, mat_path):
    stage = stage_utils.get_current_stage()
    if stage.GetPrimAtPath(name_path):
        stage.RemovePrim(name_path)
        
    mesh = UsdGeom.Mesh.Define(stage, name_path)
    mesh.CreatePointsAttr(points)
    mesh.CreateFaceVertexCountsAttr(face_counts)
    mesh.CreateFaceVertexIndicesAttr(face_indices)
    
    primvars_api = UsdGeom.PrimvarsAPI(mesh.GetPrim())
    texCoords = primvars_api.CreatePrimvar("st", Sdf.ValueTypeNames.TexCoord2fArray, UsdGeom.Tokens.varying)
    texCoords.Set(uvs)
    
    UsdPhysics.CollisionAPI.Apply(mesh.GetPrim())
    UsdPhysics.MeshCollisionAPI.Apply(mesh.GetPrim())
    mesh.GetPrim().CreateAttribute("physics:approximation", Sdf.ValueTypeNames.Token).Set("meshSimplification")
    
    mat_prim = stage.GetPrimAtPath(mat_path)
    if mat_prim:
        UsdShade.MaterialBindingAPI(mesh.GetPrim()).Bind(UsdShade.Material(mat_prim))
    return mesh

# ---------------------------------------------------------
# 3. Terrain Generation
# ---------------------------------------------------------
rows, cols = int(farm_width / res), int(farm_length / res)
x, y = np.linspace(0, farm_width, cols), np.linspace(0, farm_length, rows)
X, Y = np.meshgrid(x, y)

mask = np.power(np.outer(np.sin(np.pi * np.linspace(0, 1, rows)), np.sin(np.pi * np.linspace(0, 1, cols))), 0.3)
Z = ((np.sin(X * row_spacing) + 1.0) * 0.5 * ridge_height + (np.random.rand(rows, cols) * bumpiness)) * mask

farm_points = [Gf.Vec3f(float(X[i,j] - farm_width/2), float(Y[i,j] - farm_length/2), float(Z[i,j])) for i in range(rows) for j in range(cols)]
farm_uvs = [Gf.Vec2f(float(j)/(cols-1), float(i)/(rows-1)) for i in range(rows) for j in range(cols)]
farm_face_indices = []
for i in range(rows - 1):
    for j in range(cols - 1):
        idx = i * cols + j
        farm_face_indices.extend([idx, idx + 1, idx + cols + 1, idx + cols])

create_mesh_with_material(farm_path, farm_points, farm_uvs, [4]*((rows-1)*(cols-1)), farm_face_indices, material_path)

h = outer_size / 2
create_mesh_with_material(ground_path, 
    [Gf.Vec3f(-h,-h,0), Gf.Vec3f(h,-h,0.02), Gf.Vec3f(h,h,0.02), Gf.Vec3f(-h,h,0.02)],
    [Gf.Vec2f(0,0), Gf.Vec2f(10,0), Gf.Vec2f(10,10), Gf.Vec2f(0,10)], [4], [0,1,2,3], material_path)











