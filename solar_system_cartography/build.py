from solar_system_cartography.database import Database
from solar_system_cartography.api import ObjectInOrbit, Star
from solar_system_cartography import envs
try:
    from solar_system_cartography.rig import Rig, File
    STANDALONE = False
except:
    STANDALONE = True

class Build():
    def __init__(self, project_path:str) -> None:
        self._db = Database(project_path)
        self._project_path = project_path

        if not STANDALONE:
            self._file = File()

        self.reload(new_file=True)

    def reload(self, new_file:bool=True) ->None:
        self.init_elements()
        if not STANDALONE:
            if new_file:
                self.new_file()
            # self.all(rebuild=False)

    def init_elements(self):
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

    def all(self, rebuild:bool=True) ->None:
        for elem in self._elements:
            self.element(elem, rebuild)

    def element(self, elem:list, rebuild:bool=True) ->None:
        if elem[1] == envs.T_STAR: #type
            obj = Star(elem[0], elem[3], elem[2], self._children)
        else:
            parent = self._db.find_object(elem[2])
            if parent:
                parent_mass = parent[0][3]
            else:
                parent_mass = envs.SOLAR_MASS
            
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
                        random_perihelion_day = elem[11],
                        parent_mass = parent_mass
                        )
            
        self._db.insert_object(obj.read())

        if not STANDALONE:
            rig = Rig(obj, color=envs.COLORS[obj.get_type()])
            if rebuild == False:
                if rig._exists():
                    return
            rig.build()

    def open_file(self, path:str) ->None:
        self._file.open_file(path)

    def new_file(self) ->None:
        self._file.new_file()

    def close(self) ->None:
        self._db.close()

    def read(self) ->list:
        return self._db.read()
    
    def delete_item(self, name:str) ->None:
        self._db.delete_object(name)
        self.reload()
        self.all(rebuild=False)
    
if __name__ == "__main__":
    b = Build(r"C:\Users\giand\Videos\demo")