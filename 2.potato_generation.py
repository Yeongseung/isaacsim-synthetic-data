import omni.usd
from pxr import UsdGeom, Gf, Sdf
import numpy as np
import omni.kit.commands
import omni.replicator.core as rep

# ---------------------------------------------------------
# 1. Configuration
# ---------------------------------------------------------
assets = [
    "C:/Assets/farm/Potatoes/Potato_01.usd",
    "C:/Assets/farm/Potatoes/Potato_02.usd",
    "C:/Assets/farm/Potatoes/Potato_03.usd",
    "C:/Assets/farm/Potatoes/Potato_04.usd"
]
offsets = [0.25, 0.20, 0.15, 0.10]

row_spacing = 7.0 
farm_width = 5.0
farm_length = 15.0
base_z_height = 0.10

# ---------------------------------------------------------
# 2. Cleanup & Parent Setup
# ---------------------------------------------------------
stage = omni.usd.get_context().get_stage()
parent_path = "/World/PotatoField"

# Cleanup previous planting to avoid overlapping
if stage.GetPrimAtPath(parent_path):
    omni.kit.commands.execute("DeletePrims", paths=[parent_path])

UsdGeom.Xform.Define(stage, parent_path)

# ---------------------------------------------------------
# 3. Planting Logic (Standard API)
# ---------------------------------------------------------
def plant_static_potatoes():
    ridge_x_positions = []
    for n in range(-20, 20):
        peak = (np.pi / 2) / row_spacing + (n * 2 * np.pi / row_spacing)
        if -farm_width/2 + 0.5 < peak < farm_width/2 - 0.5:
            ridge_x_positions.append(peak)

    instance_id = 0
    for usd_path, x_off in zip(assets, offsets):
        for x_pos in ridge_x_positions:
            for _ in range(60):
                # Random variation
                y_pos = np.random.uniform(-farm_length/2 + 0.5, farm_length/2 - 0.5)
                x_pos_final = x_pos + x_off + np.random.uniform(-0.02, 0.02)
                z_pos_final = base_z_height + np.random.uniform(0, 0.005)

                prim_path = f"{parent_path}/Potato_{instance_id:04d}"
                prim = stage.DefinePrim(prim_path, "Xform")
                prim.GetReferences().AddReference(usd_path)
                
                # Transform operations
                xformable = UsdGeom.Xformable(prim)
                xformable.AddTranslateOp().Set(Gf.Vec3d(x_pos_final, y_pos, z_pos_final))
                xformable.AddRotateXYZOp().Set(Gf.Vec3f(90, 0, np.random.uniform(0, 360)))
                xformable.AddScaleOp().Set(Gf.Vec3f(np.random.uniform(0.005, 0.015)))

                # This applies the 'potato' class to the prim path string directly
                rep.modify.semantics([('class', 'potato')], str(prim_path))

                instance_id += 1

    print(f"Successfully planted {instance_id} static potatoes.")

plant_static_potatoes()
