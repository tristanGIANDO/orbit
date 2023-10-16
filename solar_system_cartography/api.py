from solar_system_cartography import envs

def convert_meters_to_au(meters:int) ->float:
    if not meters:
        raise
    return meters / envs.AU