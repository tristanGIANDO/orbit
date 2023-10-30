from maya import cmds
import math
from solar_system_cartography.api import ObjectInOrbit
from solar_system_cartography import envs

class File():
    def __init__(self) -> None:
        pass
    
    def new_file(self) ->None:
        cmds.file(new=True, force=True) 

    def open_file(self, path:str) ->None:
        self.new_file()
        cmds.file(path, open=True)

class Rig():
    def __init__(self, obj:ObjectInOrbit, color:list=None) ->None:
        self._obj = obj
        self._name = self.conform_name()
        
        self._type = self._obj.get_type()

        self._color = []
        if not color:
            self._color = [0.5,0.5,0.5]
        for c in color:
            if c > 1 :
                c = c / 255
            self._color.append(c)

        # not used yet
        self._barycenter = "barycenter"
        self._group = f"{self._name}_group"
        self._offset = f"{self._name}_orbit_offset"
        self._orbit = f"{self._name}_orbit"
        self._control = f"{self._name}_control"
        self._follow = f"{self._name}_follow"

    def conform_name(self) ->str:
        "Removes all invalid characters from name"
        name = self._obj.get_name()
        if "/" in name:
            name = name.replace("/","_")
        for i in range(0,9):
            if name.startswith(str(i)):
                name = name.replace(str(i),"")

        return name

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
        if not cmds.objExists(self._barycenter):
            cmds.spaceLocator(n=self._barycenter)[0]
        return self._barycenter

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
        offset = cmds.group(n=self._offset, em=True)
        # create circle
        orbit = cmds.circle(nr=(0, 1, 0),
                            c=(0, 0, 0),
                            sw=360,
                            r=1,
                            d=3,
                            ut=0,
                            tol=0.01,
                            s=100,
                            n=self._orbit)[0]

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

        # color orbit
        shape = cmds.listRelatives(orbit, s=True)[0]
        cmds.setAttr(f"{shape}.overrideEnabled", True)
        cmds.setAttr(f"{shape}.overrideRGBColors", True)
        cmds.setAttr(f"{shape}.overrideColorRGB", *self._color)

        return orbit

    def cr_hierarchy(self) ->str:
        self._group = cmds.group(n=self._group, em=True)
        cmds.parent(self._offset, self._group)
        cmds.parent(self._follow, self._group)
        return self._group

    def cr_offset(self) ->str:
        return cmds.spaceLocator(n=self._follow)[0]

    def cr_control(self) ->str:
        cmds.spaceLocator(n=self._control)
        cmds.parent(self._control, self._follow)
        cmds.matchTransform(self._control, self._follow)
        return self._control

    def cr_geo(self, suffix:str="object", radius:float=0.1) ->str:
        # obj = cmds.polySphere(n=f"{self._name}_geo", radius=0.05)[0]
        cmds.select(self._control)
        obj = cmds.joint(n=f"{self._name}_{suffix}", rad=radius)
        return obj

    def cr_annotation(self) ->str:
        shape = cmds.annotate(self._follow, tx=self._name, p=(0, .5, .5) )
        transform = cmds.listRelatives(shape, p=True)[0]
        cmds.parent(transform,self._follow)

        # color
        cmds.setAttr(f"{shape}.overrideEnabled", True)
        cmds.setAttr(f"{shape}.overrideRGBColors", True)
        cmds.setAttr(f"{shape}.overrideColorRGB", *self._color)

    def cstr_offset_orbit(self):
        poc = cmds.createNode("pointOnCurveInfo", n=f"{self._name}_POC")
        curve_attr = f"{self._orbit}.worldSpace[0]"
        
        cmds.connectAttr(curve_attr, f"{poc}.inputCurve")
        cmds.connectAttr(f"{poc}.position", f"{self._follow}.translate")

        return poc

    def cstr_orbit_barycenter(self) ->None:
        cmds.connectAttr(f"{self._barycenter}.worldMatrix[0]",
                         f"{self._orbit}.offsetParentMatrix",
                         f=True)

    def cstr_star(self, star:str) ->None:
        obj_suffix = "_object"
        names = [obj.split(f"{obj_suffix}")[0] for obj in cmds.ls(f"*{obj_suffix}", typ="joint")]
        influences = self._obj.get_influences()
        names.insert(0, self._barycenter)

        for obj,value in zip(names,influences):
            if obj != self._barycenter:
                obj = f"{obj}{obj_suffix}"
            cmds.parentConstraint(obj,
                                star,
                                mo=False,
                                w=value)

    def cstr_obj_to_parent(self, obj:str, parent:str) ->None:
        # cmds.connectAttr(f"{parent}.worldMatrix[0]", f"{obj}.offsetParentMatrix", f=True)
        cmds.parentConstraint(parent, obj, mo=False)

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
            cmds.setKeyframe(f"{poc}.parameter", v=v, t=t)

        cmds.keyTangent(f"{poc}.parameter", itt="spline", ott="spline")
        cmds.setInfinity(f"{poc}.parameter", pri="cycle", poi="cycle")

    def anim_offset(self) ->None:
        cmds.setAttr(f"{self._follow}.rotateX", self._obj.get_axis_inclination())

        cmds.setKeyframe(f"{self._control}.rotateY", v=0, t=0)
        cmds.setKeyframe(f"{self._control}.rotateY", v=359, t=self._obj.get_rotation_period())

        cmds.keyTangent(f"{self._control}.rotateY", itt="spline", ott="spline")
        cmds.setInfinity(f"{self._control}.rotateY", pri="cycle", poi="cycle")

    def delete(self) ->None:
        for node in [self._group, self._offset, self._control, self._follow, self._orbit]:
            if cmds.objExists(node):
                cmds.delete(node)

    def build(self) ->None:
        if self._type == envs.T_STAR:
            self.build_star()
        else:
            self.build_object_in_orbit()

    def build_object_in_orbit(self) ->None:
        # delete the old one if exists
        self.delete()
        # create new one
        
        self.cr_orbit()
        self.cr_offset()
        self.cr_control()
        self.cr_geo()
        self.cr_annotation()
        self.cr_hierarchy()
        poc = self.cstr_offset_orbit()
        parent = self._obj.get_parent()

        self.anim_orbit(poc)
        self.anim_offset()

        if parent == envs.ORIGIN:
            self._barycenter = self.cr_barycenter()
            self.cstr_obj_to_parent(self._offset, self._barycenter)
        else:
            parent = f"{parent}_follow"
            self.cstr_obj_to_parent(self._offset, parent)
    
    def build_star(self) ->None:
        self.delete()
        self.cr_barycenter()
        self.cr_offset()
        self.cr_control()
        geo = self.cr_geo("star", 0.5)
        self.cstr_star(geo)

    def _exists(self) ->bool:
        return cmds.objExists(self._group)
    
if __name__ == "__main__":
    pass