import omni.replicator.core as rep
import numpy as np

greenhouse_node = rep.get.prim_at_path("/World/Greenhouse")
sun_node = rep.get.prim_at_path("/World/DistantLight") #DistantLight
# ---------------------------------------------------------
# 1. Configuration
# ---------------------------------------------------------
# VarA~VarE
WEED_VARIANTS = [f"C:/Assets/farm/weeds/Bog_Marshcress_theqfivr_High_theqfivr_Var{l}_LOD0.usd" for l in ["A", "B", "C", "D", "E"]]

farm_width, farm_length = 5.0, 15.0
res = 0.2
ridge_height, row_spacing = 0.2, 7.0

# ---------------------------------------------------------
# 2. (Ground Pool)
# ---------------------------------------------------------
# Calculated coordinates for weeds in advance.
def generate_ground_pool(count=5000):
    rows, cols = int(farm_width / res), int(farm_length / res)
    x_range = np.linspace(0, farm_width, cols)
    y_range = np.linspace(0, farm_length, rows)
    X, Y = np.meshgrid(x_range, y_range)
    mask = np.power(np.outer(np.sin(np.pi * np.linspace(0, 1, rows)), np.sin(np.pi * np.linspace(0, 1, cols))), 0.3)
    Z_matrix = ((np.sin(X * row_spacing) + 1.0) * 0.5 * ridge_height + 0.015) * mask
    
    pool = []
    for _ in range(count):
        rx = np.random.uniform(-farm_width/2 + 0.5, farm_width/2 - 0.5)
        ry = np.random.uniform(-farm_length/2 + 0.5, farm_length/2 - 0.5)
        c_idx = int(((rx + farm_width/2) / farm_width) * (cols - 1))
        r_idx = int(((ry + farm_length/2) / farm_length) * (rows - 1))
        rz = Z_matrix[np.clip(r_idx, 0, rows-1), np.clip(c_idx, 0, cols-1)] - 0.005
        pool.append((float(rx), float(ry), float(rz)))
    return pool

GROUND_POSITIONS = generate_ground_pool(5000)

# ---------------------------------------------------------
# 3. Replicator Pipeline
# ---------------------------------------------------------
# A. Summon Assets
def add_weeds():
    weed_list = []
    for path in WEED_VARIANTS:
        weeds = rep.create.from_usd(path, count=300)
        with weeds:
            rep.modify.semantics([('class', 'weed')])
        weed_list.append(weeds)
    
    return rep.create.group(weed_list)

weed_group = add_weeds()

with rep.trigger.on_frame(num_frames=1):
    with weed_group:
        rep.modify.pose(
            position=rep.distribution.choice(GROUND_POSITIONS),
            rotation=rep.distribution.uniform((90, 0, 0), (90, 0, 360)),
            scale=rep.distribution.uniform(0.002, 0.005)
        )

print("SDG Pipeline Ready: Space bar (Step) to randomize 30 scattered weeds.")

import omni.replicator.core as rep
prim_paths=["/World/Camera"]
prim_node=rep.get.prim_at_path(prim_paths)
with rep.trigger.on_frame():
	with prim_node:
		rep.modify.pose(position=rep.distribution.uniform((-1,-7,1),(1,7,1)),
		rotation=rep.distribution.uniform((0,0,180),(0,0,180)))
	
	with greenhouse_node:
		# 'inherited' means ON.
		rep.modify.attribute("visibility", rep.distribution.choice(["inherited", "invisible"]))
		
	with sun_node:
		rep.modify.pose(
		rotation=rep.distribution.uniform((0,-89,0),(0,89,0)))
		
		rep.modify.attribute("color", rep.distribution.uniform((1.0,1.0, 1.0), (2.0, 2.0,2.0)))
		

rep.orchestrator.run()

