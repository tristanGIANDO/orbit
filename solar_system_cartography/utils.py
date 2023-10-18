import json

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

def read_json(path):
    """Reads json file

    :param path: the path of the json file
    :type path: str
    :return: the data
    :rtype: dict
    """
    with open(path, 'r') as openfile:
        dct = json.load(openfile)

    return dct