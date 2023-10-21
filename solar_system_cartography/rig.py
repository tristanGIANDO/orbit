from maya import cmds
import math
from solar_system_cartography.api import ObjectInOrbit
from solar_system_cartography import envs

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

def convert_radius(radius:float) ->float:
    return radius / envs.AU

def create_object(object_name:str) ->str:
    return cmds.spaceLocator(n=f"{object_name}_follow")[0]

def create_control(object_name:str, offset:str) ->str:
    control = cmds.spaceLocator(n=f"{object_name}_control")[0]
    cmds.parent(control,offset)
    cmds.matchTransform(control,offset)
    return control

def create_geometry(object_name:str, control:str, radius:float) ->str:
    obj = cmds.polySphere(n=f"{object_name}_geo", radius=convert_radius(radius))[0]
    cmds.parent(obj,control)
    cmds.matchTransform(obj, control)
    return obj

def attach_object_to_orbit(object_name:str, orbit_name:str, revolution_time:float):
    poc = cmds.createNode("pointOnCurveInfo", n=f"{object_name}_POC")
    curve_attr = f"{orbit_name}.worldSpace[0]"
    
    cmds.connectAttr(curve_attr, f"{poc}.inputCurve")
    cmds.connectAttr(f"{poc}.position", f"{object_name}.translate")

    return poc

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
    cmds.setAttr(f"{orbit}.rotateX", convert_inclination(inclination))
    # set eccentricity
    orbit_node = cmds.listHistory(orbit)[-1]
    cmds.setAttr(f"{orbit_node}.centerZ", convert_eccentricity(eccentricity))

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
        
def create_orbit_animation(poc:str, percentage_dict:dict) ->None:
    # animation along the orbit
    values_to_key = {}
    values_to_key["0"] = 0
    total_v = 0
    for t, v in percentage_dict.items():
        total_v += v
        values_to_key[t+1] = total_v
        
    for t, v in values_to_key.items():
        cmds.setKeyframe(f"{poc}.parameter", v=v, t=t)

    cmds.keyTangent(f"{poc}.parameter", itt="spline", ott="spline")
    cmds.setInfinity(f"{poc}.parameter", pri="cycle", poi="cycle")

def create_object_animation(control:str, offset:str, axis_inclination:float, rotation_period:float) ->None:
    cmds.setAttr(f"{offset}.rotateX", axis_inclination)

    cmds.setKeyframe(f"{control}.rotateY", v=0, t=0)
    cmds.setKeyframe(f"{control}.rotateY", v=359, t=rotation_period)

    cmds.keyTangent(f"{control}.rotateY", itt="spline", ott="spline")
    cmds.setInfinity(f"{control}.rotateY", pri="cycle", poi="cycle")

def build(obj:ObjectInOrbit) ->None:
    name = obj.get_name()

    orbit = create_orbit(name,
                 obj.get_semi_major_axis(),
                 obj.get_semi_minor_axis(),
                 obj.get_inclination(),
                 obj.get_eccentricity())
    
    offset = create_object(name)
    control = create_control(name, offset)
    geo = create_geometry(name, control, obj.get_radius())
    poc = attach_object_to_orbit(offset, orbit, obj.get_orbital_period())

    create_orbit_animation(poc, obj.get_covered_distance_each_day())
    create_object_animation(control, offset, obj.get_axis_inclination(), obj.get_rotation_period())

if __name__ == "__main__":
    create_orbit(
        name="Neptune",
        semi_major_axis=30.0699,
        semi_minor_axis=30.06879057914001,
        inclination=1.77,
        eccentricity=0.00859
    )