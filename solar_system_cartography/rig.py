from maya import cmds

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

def constrain_planet_to_orbit(planet_name:str, revolution_time:int):
    offset = cmds.group(n=f"{planet_name}_offset", em=True)
    poc = cmds.createNode("pointOnCurveInfo", n=f"{planet_name}_POC")
    loc = cmds.spaceLocator()
    curve_attr = f"{planet_name}_ellipseShape.worldSpace[0]"
    
    cmds.parent(loc,offset)
    cmds.matchTransform(loc,offset)
    
    cmds.connectAttr(curve_attr, f"{poc}.inputCurve")
    cmds.connectAttr(f"{poc}.position", f"{offset}.translate")
    
    cmds.setKeyframe(f"{poc}.pr", v=0, t=0)
    cmds.setKeyframe(f"{poc}.pr", v=8, t=revolution_time)
    
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

if __name__ == "__main__":
    create_orbit(
        name="Neptune",
        semi_major_axis=30.0699,
        semi_minor_axis=30.06879057914001,
        inclination=1.77,
        eccentricity=0.00859
    )