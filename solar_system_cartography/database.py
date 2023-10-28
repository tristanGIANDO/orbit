import os, sqlite3

class Database():
    def __init__(self, project_path:str) -> None:
        self._path = project_path
        self._name = os.path.basename(self._path)

        self._db = self.connect()
        self._cursor = self._db.cursor()

        self.create()

    def connect(self):
        return sqlite3.connect(os.path.join(self._path, f"{self._name}.db"))

    def _row_exists(self, name:str) ->bool:
        for file in self.read():
            if file[1] == name:
                return True
            
    def create(self) ->None:
        self._cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {self._name}
                (
                    [id] INT AUTO_INCREMENT PRIMARY KEY,
                    [name] TEXT,
                    [type] TEXT,
                    [parent] TEXT,
                    [mass] REAL,
                    [rotation_period] REAL,
                    [axis_inclination] REAL,
                    [semi_major_axis] REAL,
                    [semi_minor_axis] REAL,
                    [inclination] REAL,
                    [eccentricity] REAL,
                    [period] REAL,
                    [ascending_node] REAL,
                    [arg_periapsis] REAL,
                    [circumference] REAL,
                    [distance_at_perihelion] REAL,
                    [velocity_at_perihelion] REAL,
                    [distance_at_aphelion] REAL,
                    [velocity_at_aphelion] REAL,
                    [perihelion_day] TEXT
                )
                """)

    def insert_object(self, data:dict) ->None:
        object_name = data["name"]
        if self._row_exists(object_name):
            self.delete_object(object_name)

        self._cursor.execute(f"""
                INSERT INTO {self._name}
                (
                    name,
                    type,
                    parent,
                    mass,
                    rotation_period,
                    axis_inclination,
                    semi_major_axis,
                    semi_minor_axis,
                    inclination,
                    eccentricity,
                    period,
                    ascending_node,
                    arg_periapsis,
                    circumference,
                    distance_at_perihelion,
                    velocity_at_perihelion,
                    distance_at_aphelion,
                    velocity_at_aphelion,
                    perihelion_day
                )

                VALUES
                (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """, (object_name,
                      data["type"],
                      data["parent"],
                      data["mass"],
                      data.get("rotation_period",0),
                      data.get("axis_inclination",0),
                      data.get("semi_major_axis",0),
                      data.get("semi_minor_axis",0),
                      data.get("inclination",0),
                      data.get("eccentricity",0),
                      data.get("period",0),
                      data.get("ascending_node",0),
                      data.get("arg_periapsis",0),
                      data.get("circumference",0),
                      data.get("distance_at_perihelion",0),
                      data.get("velocity_at_perihelion",0),
                      data.get("distance_at_aphelion",0),
                      data.get("velocity_at_aphelion",0),
                      str(data.get("perihelion_day","")),
                      )
                )

        self._db.commit()

    def read(self):
        self._cursor.execute(f"SELECT * FROM {self._name}")
        return self._cursor.fetchall()
    
    def find_object(self, name:str):
        self._cursor.execute(f"SELECT * FROM {self._name} WHERE name = '{name}'")
        return self._cursor.fetchall()
    
    def delete_object(self, name:str):
        sql = f"DELETE FROM {self._name} WHERE name = '{name}'"
        self._cursor.execute(sql)
        self._db.commit()

    def update(self, column:str, id:str, new_value:str):
        try:
            sql = f"UPDATE {self._name} SET {column} = '{new_value}' WHERE (id = '{str(id)}')"
            self._cursor.execute(sql)
            self._db.commit()
        except:
            pass

    def close(self) ->None:
        self._db.close()