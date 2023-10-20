from solar_system_cartography.api import ObjectInOrbit
from solar_system_cartography import rig
from solar_system_cartography.envs import PRESETS

object_name = "Mercury"
    
d = PRESETS.get(object_name)
obj = ObjectInOrbit(object_name, d["mass"], d["semi_major_axis"], d["inclination"], d["eccentricity"], d["day"], d["axis_inclination"])
print(obj)

rig.build(obj)