from solar_system_cartography.database import Database
from solar_system_cartography.api import ObjectInOrbit, Star
from solar_system_cartography import envs
try:
    from solar_system_cartography.rig import Rig
    STANDALONE = False
except:
    STANDALONE = True

class Build():
    def __init__(self, project_path:str) -> None:
        self._db = Database(project_path)
        self._project_path = project_path

        # sort elements (goal is to create parents before children)
        unparented = []
        parented = []
        stars = []
        for elem in self.read():
            if not elem[1] == envs.T_STAR: # type
                if elem[2] == envs.ORIGIN: # parent
                    unparented.append(elem)
                else:
                    parented.append(elem)
            else:
                stars.append(elem)

        self._elements = unparented + parented + stars
        self._children = unparented + parented

    def all(self) ->None:
        for elem in self._elements:
            self.element(elem)

    def element(self, elem:list) ->None:
        print(elem)
        if elem[1] == envs.T_STAR: #type
            obj = Star(elem[0], elem[3], elem[2], self._children)
        else:
            obj = ObjectInOrbit(
                        object_name = elem[0],
                        object_type = elem[1],
                        object_parent = elem[2],
                        object_mass = elem[3],
                        rotation_period = elem[4],
                        axis_inclination = elem[5],
                        semi_major_axis = elem[6],
                        inclination = elem[7],
                        eccentricity = elem[8],
                        ascending_node = elem[9],
                        arg_periapsis = elem[10],
                        random_perihelion_day = elem[11]
                        )
            
        self._db.insert_object(obj.read())

        if not STANDALONE:
            rig = Rig(obj, color=envs.COLORS[obj.get_type()])

    def read(self) ->list:
        return self._db.read()
    
if __name__ == "__main__":
    b = Build(r"C:\Users\giand\Videos\demo")