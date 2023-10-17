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

# # Maintenant, vous pouvez utiliser l'argument du périhélie pour calculer l'orientation de l'axe semi-majeur comme précédemment.

# # Les éléments orbitaux
# inclinaison_degrees = 162.238  # Inclinaison de l'orbite en degrés
# argument_du_perihelie_degrees = get_perihelion()
# noeud_ascendant_degrees = 58

# # Conversion des angles en radians
# inclinaison_radians = math.radians(inclinaison_degrees)
# argument_du_perihelie_radians = math.radians(argument_du_perihelie_degrees)
# noeud_ascendant_radians = math.radians(noeud_ascendant_degrees)

# # Calcul de l'orientation de l'axe semi-majeur par rapport à l'axe vertical Nord du Soleil
# orientation_radians = argument_du_perihelie_radians + noeud_ascendant_radians
# orientation_degrees = math.degrees(orientation_radians)

# print("L'orientation de l'axe semi-majeur par rapport à l'axe vertical Nord du Soleil est de", orientation_degrees, "degrés.")

print(get_semi_minor_axis(30.0699, 0.00859))