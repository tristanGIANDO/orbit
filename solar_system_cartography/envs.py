import os
from solar_system_cartography import utils

# PRESETS = utils.read_json(os.path.join(os.path.dirname(__file__), "presets.json"))
AU = 149597870700 # meters

G = 6.67430e-11 # Newton's gravitational constant

SOLAR_MASS = 1.989e30 # Solar mass in kilograms

# Main names
E_NAME = "name"
E_TYPE = "type"
E_PARENT = "parent"
E_MASS = "mass"
E_PERIOD = "rotation_period"
E_INCLINATION = "axis_inclination"
O_SEMI_MAJOR_AXIS = "semi_major_axis"
O_INCLINATION = "inclination"
O_ECCENTRICITY = "eccentricity"
O_ASCENDING_NODE = "ascending_node"
O_ARG_PERIAPSIS = "arg_periapsis"
O_PERIHELION_DAY = "perihelion_day"

# Additional names
O_SEMI_MINOR_AXIS = "semi_minor_axis"
O_PERIOD = "period"
O_CIRCUMFERENCE = "circumference"
O_PERIHELION_D = "distance_at_perihelion"
O_PERIHELION_V = "velocity_at_perihelion"
O_APHELION_D = "distance_at_aphelion"
O_APHELION_V = "velocity_at_aphelion"

# Types
T_PLANET = "Planet"
T_STAR = "Star"
T_COMET = "Comet"
T_NAT_SAT = "Natural Satellite"
T_ART_SAT = "Artificial Satellite"
T_ASTEROID = "Asteroid"
T_RANDOM = "Random"

TYPES = [
    T_PLANET,
    T_STAR,
    T_COMET,
    T_NAT_SAT,
    T_ART_SAT,
    T_ASTEROID,
    T_RANDOM
]

# Types colors
COLORS = {
    T_PLANET : [255,255,255],
    T_STAR : [0,0,0],
    T_COMET : [0,0,255],
    T_NAT_SAT : [255,0,0],
    T_ART_SAT : [0,255,0],
    T_ASTEROID : [80,20,255],
    T_RANDOM : [50,50,50]
}

# Parents
ORIGIN = "Origin"