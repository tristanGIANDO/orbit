from orbit.backend import ObjectInOrbit
from orbit.envs import SOLAR_MASS
from orbit.presets import PRESETS

mercury = PRESETS[0]

obj = ObjectInOrbit(*mercury, SOLAR_MASS)

print(obj)