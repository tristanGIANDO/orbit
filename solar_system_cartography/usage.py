from solar_system_cartography.backend import ObjectInOrbit
from solar_system_cartography.envs import SOLAR_MASS
from solar_system_cartography.presets import PRESETS

mercury = PRESETS[0]

obj = ObjectInOrbit(*mercury, SOLAR_MASS)

print(obj)