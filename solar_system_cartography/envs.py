import os
from solar_system_cartography import utils

PRESETS = utils.read_json(os.path.join(os.path.dirname(__file__), "presets.json"))
AU = 149597870700 # meters

G = 6.67430e-11 # Newton's gravitational constant

SOLAR_MASS = 1.989e30 # Solar mass in kilograms