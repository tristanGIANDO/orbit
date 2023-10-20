from solar_system_cartography.api import ObjectInOrbit
from solar_system_cartography import rig
from solar_system_cartography.envs import PRESETS

object_name = "Mercury"
    
data = PRESETS.get(object_name)
obj = ObjectInOrbit(object_name, data["mass"], data["semi_major_axis"], data["inclination"], data["eccentricity"])
print(obj)

rig.build_all(obj)