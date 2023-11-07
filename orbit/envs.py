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
T_TELLURIC_PLANET = "Telluric Planet"
T_GIANT_PLANET = "Giant Planet"
T_PLANET_DWARF = "Dwarf Planet"
T_STAR = "Star"
T_COMET = "Comet"
T_NAT_SAT = "Natural Satellite"
T_ART_SAT = "Artificial Satellite"
T_ASTEROID = "Asteroid"
T_RANDOM = "Random"
T_OORT_CLOUD = "Oort Cloud"
T_TRANSNEPTUNIAN = "Trans_Neptunian object"
T_CENTAUR = "Centaur"
T_KUIPER = "Kuiper Belt Object"

TYPES = [
    T_PLANET,
    T_PLANET_DWARF,
    T_TELLURIC_PLANET,
    T_GIANT_PLANET,
    T_STAR,
    T_COMET,
    T_NAT_SAT,
    T_ART_SAT,
    T_ASTEROID,
    T_RANDOM,
    T_OORT_CLOUD,
    T_TRANSNEPTUNIAN,
    T_CENTAUR,
    T_KUIPER
]

# Types colors
COLORS = {
    T_PLANET : [255,255,255],
    T_PLANET_DWARF : [255,0,0],
    T_TELLURIC_PLANET : [255,128,0],
    T_GIANT_PLANET : [255,128,128],
    T_STAR : [255,255,0],
    T_COMET : [128,255,0],
    T_NAT_SAT : [0,255,255],
    T_ART_SAT : [128,128,128],
    T_ASTEROID : [0,128,255],
    T_RANDOM : [255,0,255],
    T_OORT_CLOUD : [45,0,45],
    T_TRANSNEPTUNIAN : [160,25,255],
    T_CENTAUR : [80,128,0],
    T_KUIPER : [128,128,0]
}

# Parents
ORIGIN = "Origin"

ME = "https://www.linkedin.com/in/tristan-giandoriggio/"