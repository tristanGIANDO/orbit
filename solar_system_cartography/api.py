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

if __name__ == "__main__":
    print(get_semi_minor_axis(17.9, 0.96727))