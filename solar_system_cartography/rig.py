from maya import cmds
import math
from solar_system_cartography.api import ObjectInOrbit
from solar_system_cartography import envs, utils

class Rig():
    def __init__(self, obj:ObjectInOrbit, create_sun:bool=True) ->None:
        self._obj = obj
        self._name = obj.get_name()
        self.build()

    def get_inclination(self) ->float:
        """Converts the inclination of an orbit in maya units.

        Args:
            inclination (float): orbit inclination

        Returns:
            float: The converted inclination
        """
        inclination = self._obj.get_inclination()
        if inclination > 90:
            inclination = -(180 - inclination)
        
        return inclination

    def get_eccentricity(self) ->float:
        """In Maya, eccentricity is the center of a Nurbscurve. Attribute is r*2 (obsolete ?)

        Args:
            eccentricity (float): the eccentricity in degrees

        Returns:
            float: the converted eccentricity
        """
        eccentricity = self._obj.get_eccentricity()
        if self._obj.get_inclination() > 90:
            eccentricity = eccentricity

        return eccentricity # / 2

    def get_radius(self) ->float:
        return self._obj.get_radius() / envs.AU

    def cr_barycenter(self) ->str:
        name = "barycenter"
        if not cmds.objExists(name):
            cmds.spaceLocator(n=name)[0]
        return name

    def cr_orbit(self) ->str:
        """Creates the orbit of the object

        Args:
        semi major axis : radius
        eccentricity : center Z
        argument periapsis : rotate Y
        inclination : rotate Z
        ascending node : rotate Y from sun

        Returns:
            str: The created orbit DAG node
        """
        # create orbit offset
        offset = cmds.group(n=f"{self._name}_orbit_offset", em=True)
        # create circle
        orbit = cmds.circle(nr=(0, 1, 0),
                            c=(0, 0, 0),
                            sw=360,
                            r=1,
                            d=3,
                            ut=0,
                            tol=0.01,
                            s=100,
                            n=f"{self._name}_orbit")[0]
        cmds.parent(orbit, offset)

        # set size
        cmds.setAttr(f"{orbit}.scaleZ", self._obj.get_semi_major_axis())
        cmds.setAttr(f"{orbit}.scaleX", self._obj.get_semi_minor_axis())
        # set inclination
        cmds.setAttr(f"{orbit}.rotateZ", self.get_inclination())
        # set eccentricity
        orbit_node = cmds.listHistory(orbit)[-1]
        cmds.setAttr(f"{orbit_node}.centerZ", self.get_eccentricity())
        # set orientations
        cmds.setAttr(f"{orbit}.rotateY", self._obj.get_arg_periapsis())
        cmds.setAttr(f"{offset}.rotateY", self._obj.get_ascending_node())

        return orbit

    def cr_hierarchy(self, orbit:str, offset:str) ->str:
        group = cmds.group(n=f"{self._name}_group", em=True)
        cmds.parent(f"{orbit}_offset", group)
        cmds.parent(offset, group)
        return group

    def cr_offset(self) ->str:
        return cmds.spaceLocator(n=f"{self._name}_follow")[0]

    def cr_control(self, offset:str) ->str:
        control = cmds.spaceLocator(n=f"{self._name}_control")[0]
        cmds.parent(control, offset)
        cmds.matchTransform(control, offset)
        return control

    def cr_geo(self, control:str) ->str:
        obj = cmds.polySphere(n=f"{self._name}_geo", radius=0.5)[0]
        cmds.parent(obj,control)
        cmds.matchTransform(obj, control)
        return obj

    def cstr_offset_orbit(self, orbit_name:str, offset_name):
        poc = cmds.createNode("pointOnCurveInfo", n=f"{self._name}_POC")
        curve_attr = f"{orbit_name}.worldSpace[0]"
        
        cmds.connectAttr(curve_attr, f"{poc}.inputCurve")
        cmds.connectAttr(f"{poc}.position", f"{offset_name}.translate")

        return poc

    def cstr_orbit_barycenter(self, orbit:str, barycenter:str) ->None:
        cmds.connectAttr(f"{barycenter}.worldMatrix[0]", f"{orbit}.offsetParentMatrix", f=True)
    
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
            
    def anim_orbit(self, poc:str) ->None:
        for t, v in self._obj.get_covered_distance_each_day().items():
            print(t, v)
            cmds.setKeyframe(f"{poc}.parameter", v=v, t=t)

        cmds.keyTangent(f"{poc}.parameter", itt="spline", ott="spline")
        cmds.setInfinity(f"{poc}.parameter", pri="cycle", poi="cycle")

    def anim_offset(self, control:str, offset:str) ->None:
        cmds.setAttr(f"{offset}.rotateX", self._obj.get_axis_inclination())

        cmds.setKeyframe(f"{control}.rotateY", v=0, t=0)
        cmds.setKeyframe(f"{control}.rotateY", v=359, t=self._obj.get_rotation_period())

        cmds.keyTangent(f"{control}.rotateY", itt="spline", ott="spline")
        cmds.setInfinity(f"{control}.rotateY", pri="cycle", poi="cycle")

    def build(self) ->None:
        barycenter = self.cr_barycenter()
        orbit = self.cr_orbit()
        offset = self.cr_offset()
        control = self.cr_control(offset)
        geo = self.cr_geo(control)
        group = self.cr_hierarchy(orbit,offset)

        poc = self.cstr_offset_orbit(orbit, offset)
        self.cstr_orbit_barycenter(orbit, barycenter)

        self.anim_orbit(poc)
        self.anim_offset(control, offset)

if __name__ == "__main__":
    pass