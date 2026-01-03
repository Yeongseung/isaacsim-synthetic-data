# GUI setup
![GUI](images/GUI_setup.png)
---

```python
import omni.replicator.core as rep

shape_paths = ["/World/Cone", "/World/Cube"]
camera_path = ["/World/Camera"]

shapes = rep.get.prim_at_path(shape_paths)
camera = rep.get.prim_at_path(camera_path)

with rep.trigger.on_frame():
    with shapes:
        rep.modify.pose(
            position=rep.distribution.uniform((-100, -100, -100), (200, 200, 100)),
            # Scale from 50% to 200% of original size
            scale=rep.distribution.uniform(0.5, 1.0) 
        )
    
    with camera:
        rep.modify.pose(
            position=rep.distribution.uniform((350, 350, 350), (400, 400, 400))
        )
```