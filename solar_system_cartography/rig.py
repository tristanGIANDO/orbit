from maya import cmds
import math
from solar_system_cartography.api import ObjectInOrbit
from solar_system_cartography import envs

class Rig():
    def __init__(self, obj:ObjectInOrbit) ->None:
        self._obj = obj
        self._name = obj.get_name()
        self.build()

    def convert_inclination(self, inclination:float) ->float:
        """Converts the inclination of an orbit in maya units.

        Args:
            inclination (float): orbit inclination

        Returns:
            float: The converted inclination
        """
        if inclination > 90:
            inclination = -(180 - inclination)
        
        return inclination

    def convert_eccentricity(self, eccentricity:float) ->float:
        """In Maya, eccentricity is the center of a Nurbscurve. Attribute is r*2

        Args:
            eccentricity (float): the eccentricity in degrees

        Returns:
            float: the converted eccentricity
        """
        return eccentricity / 2

    def convert_radius(self, radius:float) ->float:
        return radius / envs.AU

    def create_object(self) ->str:
        return cmds.spaceLocator(n=f"{self._name}_follow")[0]

    def create_control(self, offset:str) ->str:
        control = cmds.spaceLocator(n=f"{self._name}_control")[0]
        cmds.parent(control, offset)
        cmds.matchTransform(control, offset)
        return control

    def create_geometry(self, control:str) ->str:
        obj = cmds.polySphere(n=f"{self._name}_geo", radius=self.convert_radius(self._obj.get_radius()))[0]
        cmds.parent(obj,control)
        cmds.matchTransform(obj, control)
        return obj

    def attach_object_to_orbit(self, orbit_name:str, offset_name):
        poc = cmds.createNode("pointOnCurveInfo", n=f"{self._name}_POC")
        curve_attr = f"{orbit_name}.worldSpace[0]"
        
        cmds.connectAttr(curve_attr, f"{poc}.inputCurve")
        cmds.connectAttr(f"{poc}.position", f"{offset_name}.translate")

        return poc

    def create_orbit(self) ->str:
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
                            n=f"{self._name}_orbit")[0]
        # set size
        cmds.setAttr(f"{orbit}.scaleX", self._obj.get_semi_major_axis())
        cmds.setAttr(f"{orbit}.scaleZ", self._obj.get_semi_minor_axis())
        # set inclination
        cmds.setAttr(f"{orbit}.rotateX", self.convert_inclination(self._obj.get_inclination()))
        # set eccentricity
        orbit_node = cmds.listHistory(orbit)[-1]
        cmds.setAttr(f"{orbit_node}.centerZ", self.convert_eccentricity(self._obj.get_eccentricity()))

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
            
    def create_orbit_animation(self, poc:str) ->None:
        # animation along the orbit
        values_to_key = {}
        values_to_key["0"] = 0
        total_v = 0
        for t, v in self._obj.get_covered_distance_each_day().items():
            total_v += v
            values_to_key[t+1] = total_v
            
        for t, v in values_to_key.items():
            cmds.setKeyframe(f"{poc}.parameter", v=v, t=t)

        cmds.keyTangent(f"{poc}.parameter", itt="spline", ott="spline")
        cmds.setInfinity(f"{poc}.parameter", pri="cycle", poi="cycle")

    def create_object_animation(self, control:str, offset:str) ->None:
        cmds.setAttr(f"{offset}.rotateX", self._obj.get_axis_inclination())

        cmds.setKeyframe(f"{control}.rotateY", v=0, t=0)
        cmds.setKeyframe(f"{control}.rotateY", v=359, t=self._obj.get_rotation_period())

        cmds.keyTangent(f"{control}.rotateY", itt="spline", ott="spline")
        cmds.setInfinity(f"{control}.rotateY", pri="cycle", poi="cycle")

    def build(self) ->None:
        orbit = self.create_orbit()
        offset = self.create_object()
        control = self.create_control(offset)
        geo = self.create_geometry(control)
        poc = self.attach_object_to_orbit(orbit, offset)
        self.create_orbit_animation(poc)
        self.create_object_animation(control, offset)

if __name__ == "__main__":
    pass