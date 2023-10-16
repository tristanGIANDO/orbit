import math
from solar_system_cartography import envs

def get_revolution_time(semi_major_axis:int) ->float:
    """
    Calculate the time in days that it takes for a star to make a complete revolution around the Sun from its distance from the Sun.
    semi_major_axis : The semi-major axis of the ellipse formed by the star around the Sun
    """
    # Using Kepler's law to calculate the orbital period (T)
    orbital_period = 2 * math.pi * math.sqrt((semi_major_axis**3) / (envs.GRAVITATIONAL_CONSTANT * envs.SOLAR_MASS))
    
    # Conversion to days
    orbital_period_days = orbital_period / (60 * 60 * 24)
    
    return orbital_period_days
    
print(get_revolution_time(envs.JUPITER_SEMI_MAJOR_AXIS))
