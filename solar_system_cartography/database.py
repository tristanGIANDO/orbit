import os, sqlite3
from solar_system_cartography import envs

class Database():
    def __init__(self, project_path:str) -> None:
        self._path = project_path
        self._name = os.path.basename(self._path)

        self._db = self.connect()
        self._cursor = self._db.cursor()

        self.create()

    def connect(self):
        return sqlite3.connect(os.path.join(self._path, f"{self._name}_database.db"))

    def _row_exists(self, name:str) ->bool:
        for file in self.read():
            if file[0] == name:
                return True
            
    def create(self) ->None:
        self._cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {self._name}
                (
                    [{envs.E_NAME}] TEXT,
                    [{envs.E_TYPE}] TEXT,
                    [{envs.E_PARENT}] TEXT,
                    [{envs.E_MASS}] REAL,
                    [{envs.E_PERIOD}] REAL,
                    [{envs.E_INCLINATION}] REAL,
                    [{envs.O_SEMI_MAJOR_AXIS}] REAL,
                    [{envs.O_INCLINATION}] REAL,
                    [{envs.O_ECCENTRICITY}] REAL,
                    [{envs.O_ASCENDING_NODE}] REAL,
                    [{envs.O_ARG_PERIAPSIS}] REAL,
                    [{envs.O_PERIHELION_DAY}] TEXT,
                    [{envs.O_SEMI_MINOR_AXIS}] REAL,
                    [{envs.O_PERIOD}] REAL,
                    [{envs.O_CIRCUMFERENCE}] REAL,
                    [{envs.O_PERIHELION_D}] REAL,
                    [{envs.O_PERIHELION_V}] REAL,
                    [{envs.O_APHELION_D}] REAL,
                    [{envs.O_APHELION_V}] REAL  
                )
                """)

    def insert_object(self, data:dict) ->None:
        object_name = data[envs.E_NAME]
        if self._row_exists(object_name):
            self.delete_object(object_name)

        self._cursor.execute(f"""
                INSERT INTO {self._name}
                (
                    [{envs.E_NAME}],
                    [{envs.E_TYPE}],
                    [{envs.E_PARENT}],
                    [{envs.E_MASS}],
                    [{envs.E_PERIOD}],
                    [{envs.E_INCLINATION}],
                    [{envs.O_SEMI_MAJOR_AXIS}],
                    [{envs.O_INCLINATION}],
                    [{envs.O_ECCENTRICITY}],
                    [{envs.O_ASCENDING_NODE}],
                    [{envs.O_ARG_PERIAPSIS}],
                    [{envs.O_PERIHELION_DAY}],
                    [{envs.O_SEMI_MINOR_AXIS}],
                    [{envs.O_PERIOD}],
                    [{envs.O_CIRCUMFERENCE}],
                    [{envs.O_PERIHELION_D}],
                    [{envs.O_PERIHELION_V}],
                    [{envs.O_APHELION_D}],
                    [{envs.O_APHELION_V}]
                )

                VALUES
                (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """, (object_name,
                      data[envs.E_TYPE],
                      data[envs.E_PARENT],
                      data[envs.E_MASS],
                      data.get(envs.E_PERIOD,0),
                      data.get(envs.E_INCLINATION,0),
                      data.get(envs.O_SEMI_MAJOR_AXIS,0),
                      data.get(envs.O_INCLINATION,0),
                      data.get(envs.O_ECCENTRICITY,0),
                      data.get(envs.O_ASCENDING_NODE,0),
                      data.get(envs.O_ARG_PERIAPSIS,0),
                      str(data.get(envs.O_PERIHELION_DAY,"")),
                      data.get(envs.O_SEMI_MINOR_AXIS,0),
                      data.get(envs.O_PERIOD,0),
                      data.get(envs.O_CIRCUMFERENCE,0),
                      data.get(envs.O_PERIHELION_D,0),
                      data.get(envs.O_PERIHELION_V,0),
                      data.get(envs.O_APHELION_D,0),
                      data.get(envs.O_APHELION_V,0),
                      )
                )

        self._db.commit()

    def read(self):
        self._cursor.execute(f"SELECT * FROM {self._name}")
        return self._cursor.fetchall()
    
    def find_object(self, name:str):
        self._cursor.execute(f"SELECT * FROM {self._name} WHERE [{envs.E_NAME}] = '{name}'")
        return self._cursor.fetchall()
    
    def delete_object(self, name:str):
        sql = f"DELETE FROM {self._name} WHERE [{envs.E_NAME}] = '{name}'"
        self._cursor.execute(sql)
        self._db.commit()

    def close(self) ->None:
        self._db.close()