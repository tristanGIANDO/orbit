from solar_system_cartography.api import ObjectInOrbit
# from solar_system_cartography.rig import create_orbit
from solar_system_cartography.envs import PRESETS

object_name = "Earth"
    
data = PRESETS.get(object_name)
object = ObjectInOrbit(object_name, data["semi_major_axis"], data["inclination"], data["eccentricity"])
print(object)

# create_orbit(object_name,
#              object.get_semi_major_axis(),
#              object.get_semi_minor_axis(),
#              object.get_inclination(),
#              object.get_eccentricity()
#              )

revolution_time = object.get_revolution_time()

v_max = object.get_perihelion_velocity()
d_max = object.get_perihelion_distance()

v_min = object.get_aphelion_velocity()
d_min = object.get_aphelion_distance()

print(v_max, d_max)