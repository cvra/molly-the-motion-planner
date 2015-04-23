molly-the-motion-planner
========================

simple 2d motion planner with circle based obstacles

# Known Issues

* currently only available under python2 until acceptable hash functions are
  implemented for all classes that redefine ```__eq__```

# Usage

The principal functionality of molly is the ```get_path``` function in the
Pathplanner module:

```python
def get_path(settings,
             polygons,
             circles,
             start_pos,
             start_heading,
             start_v,
             target_pos)
```

* settings: collection of general settings of the environment (more detail below)
* polygons: list of polygonal obstacles to avoid (use class molly.Polygon)
* circles: list of circular obstacles to avoid (use class molly.Circle)
* start_pos: starting position from where to search path (molly.Vec2D)
* start_heading: heading of the robot at start in world coordinates (molly.Vec2D)
* start_v: initial velocity of robot (float)
* target_pos: target position you want robot to navigate to (molly.Vec2D)

The result of a call to ```get_path``` is a list of tuples ```(pos, speed, acc, time_stamp)```
where ```pos``` is a ```molly.Vec2D``` describing a point on the trajectory,
```speed``` is a ```molly.Vec2D``` describing robot velocity at ```pos```, 
```acc``` is a ```molly.Vec2D``` describing robot acceleration at ```pos``` and
```time_stamp``` is the time passed since the start of the trajectory.

**Note:** molly plans a path for a point object, so you have to add robot radius
to all obstacles you want to avoid.

```python
class Settings(object):
    "settings class memorizing settings for molly"

    def __init__(self,
                 max_acc=1.6,
                 max_v=0.6,
                 time_resolution=0.1,
                 static_poly_obs=[STAIRS],
                 static_circ_obs=[],
                 obs_min_r=0.1,
                 playground_dim=(3.0, 2.0)):

        ...
```

Content of a ```molly.Settings``` object:

* max_acc: maxmimum *tangential* acceleration of the robot (m/s^2)
* max_v: maximum velocity of the robot (m/s)
* time_resolution: time step used when discretizing trajectory (s)
* static_poly_obs: list of polygonal obstacles, that are always in the environment and don't move 
* static_circ_obs: list of circular obstacles, that are always in the environment and don't move
* obs_min_r: minimum radius an obstacle should have (currently not enforced; use robot radius)
* playground_dim: width and height of playground

defaults are set for use at the eurobot 2015 competition

