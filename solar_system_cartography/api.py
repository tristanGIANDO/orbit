import math

from solar_system_cartography import envs

def convert_meters_to_au(meters:int) ->float:
    """Converts a distance in meters to astronomical unit

    Args:
        meters (int): Meters

    Returns:
        float: The same distance but in astronomical unit
    """
    if not meters:
        raise
    return meters / envs.AU

def convert_au_to_meters(au:float) ->float:
    """Converts a distance in astronomical unit to meters

    Args:
        au (float): astronomical unit distance

    Returns:
        float: The same distance but in astronomical unit
    """
    if not au:
        raise
    return au * envs.AU

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

def get_semi_minor_axis(semi_major_axis:float, eccentricity:float) ->float:
    """Calculates the semi minor axis of an ellipse.

    Args:
        semi_major_axis (float): semi major axis, unit does not matter
        eccentricity (float): eccentricity in degrees converted to float

    Returns:
        float: The semi minor axis of the ellipse
    """
    return semi_major_axis * math.sqrt(1 - eccentricity ** 2)

def get_perihelion():
    inclinaison_degrees = 162.238  # Inclinaison de l'orbite en degrés
    longitude_du_noeud_ascendant_degrees = 58  # Longitude du nœud ascendant en degrés

    # Conversion des angles en radians
    inclinaison_radians = math.radians(inclinaison_degrees)
    longitude_du_noeud_ascendant_radians = math.radians(longitude_du_noeud_ascendant_degrees)

    # Calcul de l'argument du périhélie (ω) en radians
    argument_du_perihelie_radians = math.atan2(-math.cos(inclinaison_radians) * math.sin(longitude_du_noeud_ascendant_radians), math.cos(longitude_du_noeud_ascendant_radians))

    # Conversion de l'angle résultant en degrés
    argument_du_perihelie_degrees = math.degrees(argument_du_perihelie_radians)

    return argument_du_perihelie_degrees

if __name__ == "__main__":
    # print(get_semi_minor_axis(30.0699, 0.00859))
    print(get_revolution_time(convert_au_to_meters(0.38709808989279954)))