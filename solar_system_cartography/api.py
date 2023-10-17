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

def est_ascendante(element_orbital_inclinaison, element_orbital_argument_perigee):
    # Convertir l'inclinaison et l'argument du périgée de degrés en radians
    inclinaison_rad = math.radians(element_orbital_inclinaison)
    argument_perigee_rad = math.radians(element_orbital_argument_perigee)

    # Calculer la longitude du nœud ascendant
    longitude_noeud_ascendant = (argument_perigee_rad + math.pi) % (2 * math.pi)
    print(longitude_noeud_ascendant)

    # Une orbite est ascendante si la longitude du nœud ascendant est entre 0 et pi radians
    if 0 <= longitude_noeud_ascendant <= math.pi:
        return "Ascendante"
    else:
        return "Descendante"
    
import math

def argument_perigee(excentricite, angle_noeud_ascendant_perigee):
    # Convertir l'angle entre le nœud ascendant et le périgée en radians
    angle_noeud_ascendant_perigee_rad = math.radians(angle_noeud_ascendant_perigee)

    # Utilisez la formule pour calculer l'argument du périgée
    argument_perigee_rad = angle_noeud_ascendant_perigee_rad - math.pi

    # Assurez-vous que l'argument du périgée est dans la plage [0, 2*pi] radians
    argument_perigee_rad = argument_perigee_rad % (2 * math.pi)

    # Convertir l'argument du périgée en degrés
    argument_perigee_deg = math.degrees(argument_perigee_rad)

    return argument_perigee_deg

if __name__ == "__main__":
    # element_orbital_inclinaison = 162.238  # Inclinaison en degrés
    # element_orbital_argument_perigee = 111.84652  # Argument du périgée en degrés

    # resultat = est_ascendante(element_orbital_inclinaison, element_orbital_argument_perigee)
    # print(f"L'orbite est {resultat}.")

    # Exemple d'utilisation
    excentricite = 0.3
    angle_noeud_ascendant_perigee = 60  # Angle en degrés

    argument_p = argument_perigee(excentricite, angle_noeud_ascendant_perigee)
    print(f"L'argument du périgée est de {argument_p} degrés.")
