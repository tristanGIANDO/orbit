from maya import cmds
from solar_system_cartography import api

MAYA_AU = 0.000000001

def convert_meters_to_maya_au(meters:int) ->float:
    if not meters:
        raise
    return meters * MAYA_AU

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
    cmds.setAttr(f"{orbit}.rotateX", inclination)
    # set eccentricity
    construction_node = cmds.listHistory(orbit)[-1]
    cmds.setAttr(f"{construction_node}.centerX", eccentricity)

    return orbit

if __name__ == "__main__":
    create_orbit(
        name="mercury",
        semi_major_axis=convert_meters_to_maya_au(57909050000),
        semi_minor_axis=convert_meters_to_maya_au(56669796330),
        inclination=7.004,
        eccentricity=0.2056
    )