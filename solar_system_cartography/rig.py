from maya import cmds
import math

def convert_inclination(inclination:float) ->float:
    """Converts the inclination of an orbit in maya units.

    Args:
        inclination (float): orbit inclination

    Returns:
        float: The converted inclination
    """
    if inclination > 90:
        inclination = -(180 - inclination)
    
    return inclination

def convert_eccentricity(eccentricity:float) ->float:
    """In Maya, eccentricity is the center of a Nurbscurve. Attribute is r*2

    Args:
        eccentricity (float): the eccentricity in degrees

    Returns:
        float: the converted eccentricity
    """
    return eccentricity / 2

def create_object(object_name:str) ->str:
    return cmds.spaceLocator(n=f"{object_name}_offset")

def attach_object_to_orbit(object_name:str, revolution_time:float):
    obj = f"{object_name}_offset"
    poc = cmds.createNode("pointOnCurveInfo", n=f"{object_name}_POC")
    orbit = f"{object_name}_orbit"
    curve_attr = f"{orbit}.worldSpace[0]"

    points_distances = get_distances(orbit)
    furthest_point = get_perihelion_point(points_distances)
    closest_point = get_aphelion_point(points_distances)
    
    cmds.connectAttr(curve_attr, f"{poc}.inputCurve")
    cmds.connectAttr(f"{poc}.position", f"{obj}.translate")
    
    cmds.setKeyframe(f"{poc}.pr", v=0, t=0)
    cmds.setKeyframe(f"{poc}.pr", v=100, t=revolution_time)
    
    cmds.keyTangent(poc, itt="linear", ott="linear")
    cmds.setInfinity(poc, poi="cycle")

def create_orbit(name, semi_major_axis:float,
                 semi_minor_axis:float, inclination:float,
                 eccentricity:float) ->str:
    """Creates the orbit of the object

    Args:
        name (str): The object name
        semi_major_axis (float): Orbit semi major axis
        semi_minor_axis (float): Orbit semi minor axis
        inclination (float): Orbit inclination
        eccentricity (float): Orbit eccentricity

    Returns:
        str: The created orbit DAG node
    """
    # create circle
    orbit = cmds.circle(nr=(0, 1, 0),
                        c=(0, 0, 0),
                        sw=360,
                        r=0.5,
                        d=3,
                        ut=0,
                        tol=0.01,
                        s=100,
                        n=f"{name}_orbit")[0]
    # set size
    cmds.setAttr(f"{orbit}.scaleX", semi_major_axis)
    cmds.setAttr(f"{orbit}.scaleZ", semi_minor_axis)
    # set inclination
    cmds.setAttr(f"{orbit}.rotateZ", convert_inclination(inclination))
    # set eccentricity
    orbit_node = cmds.listHistory(orbit)[-1]
    cmds.setAttr(f"{orbit_node}.centerX", convert_eccentricity(eccentricity))

    return orbit

def get_distances(orbit:str) ->dict:
    barycenter_pos = [0.0, 0.0, 0.0]
    positions = {}
    if cmds.objExists(orbit):
        for cv in cmds.ls(orbit + '.cv[*]', fl=True):
            cv_index = int(cv.split("[")[-1].split("]")[0])
            cv_pos = cmds.pointPosition(cv)
            distance = math.sqrt((cv_pos[0] - barycenter_pos[0]) ** 2 + (cv_pos[1] - barycenter_pos[1]) ** 2 + (cv_pos[2] - barycenter_pos[2]) ** 2)
            positions[cv_index] = distance

    return positions

def get_perihelion_point(positions:dict) ->str:
    max_distance = max(d for d in list(positions.values()))

    for i,d in positions.items():
        if d == max_distance:
            return i
        
def get_aphelion_point(positions:dict) ->str:
    min_distance = min(d for d in list(positions.values()))

    for i,d in positions.items():
        if d == min_distance:
            return i

if __name__ == "__main__":
    create_orbit(
        name="Neptune",
        semi_major_axis=30.0699,
        semi_minor_axis=30.06879057914001,
        inclination=1.77,
        eccentricity=0.00859
    )