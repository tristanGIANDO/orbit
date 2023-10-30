AU = 149597870700 # meters

G = 6.67430e-11 # Newton's gravitational constant

SOLAR_MASS = 1.989e30 # Solar mass in kilograms

# Main names
E_NAME = "Name"
E_TYPE = "Type"
E_PARENT = "Parent"
E_MASS = "Mass (kg)"
E_PERIOD = "Rotation Period (d)"
E_INCLINATION = "Axis Inclination (°)"
O_SEMI_MAJOR_AXIS = "Semi Major Axis (AU)"
O_INCLINATION = "Inclination (°)"
O_ECCENTRICITY = "Eccentricity"
O_ASCENDING_NODE = "Ascending Node (°)"
O_ARG_PERIAPSIS = "Periapsis Argument (°)"
O_PERIHELION_DAY = "Perihelion or Perigee Date"

# Additional names
O_SEMI_MINOR_AXIS = "Semi Minor Axis (AU)"
O_PERIOD = "Orbital Period (d)"
O_CIRCUMFERENCE = "Circumference (m)"
O_PERIHELION_D = "Perihelion Distance (AU)"
O_PERIHELION_V = "Perihelion Speed (m/s)"
O_APHELION_D = "Aphelion Distance (AU)"
O_APHELION_V = "Aphelion Speed (m/s)"

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