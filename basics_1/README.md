# GUI setup
![GUI](images/GUI_setup.png)
---

```python
import omni.replicator.core as rep

# Separate camera node to maintain a distant perspective.
shape_paths = ["/World/Cone", "/World/Cube"]
camera_path = ["/World/Camera"]

shapes = rep.get.prim_at_path(shape_paths)
camera = rep.get.prim_at_path(camera_path)

with rep.trigger.on_frame():
    with shapes:
        rep.modify.pose(
            position=rep.distribution.uniform((-100, -100, -100), (200, 200, 100)),
            # Scale from 50% to 100% of original size
            scale=rep.distribution.uniform(0.5, 1.0) 
        )
    
    with camera:
        rep.modify.pose(
            position=rep.distribution.uniform((350, 350, 350), (400, 400, 400)),
            # I add 'look_at' to ensure the camera doesn't just stare into the void
            look_at="/World/Cube" # Or point at a central Xform/Null
        )
```
![Semantics_Editor](images/Semantics_schema_Editor.png)
Click Add to define the semantic labeling for your objects. This allows you to control the segmentation data captured in your renders.