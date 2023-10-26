import os, sqlite3

class Database():
    def __init__(self, project_path:str) -> None:
        self._path = project_path
        self._name = os.path.basename(self._path)

        self._db = sqlite3.connect(os.path.join(self._path, f"{self._name}.db"))
        self._cursor = self._db.cursor()

        self.create()

    def _row_exists(self, row_id:str) ->bool:
        for file in self.select_rows():
            if file[0] == row_id:
                return True
            
    def create(self) ->None:
        self._cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {self._name}
                (
                    [id] INT AUTO_INCREMENT PRIMARY KEY,
                    [name] TEXT,
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
                (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """, (object_name,
                      data["mass"],
                      data["rotation_period"],
                      data["axis_inclination"],
                      data["semi_major_axis"],
                      data["semi_minor_axis"],
                      data["inclination"],
                      data["eccentricity"],
                      data["period"],
                      data["ascending_node"],
                      data["arg_periapsis"],
                      data["circumference"],
                      data["distance_at_perihelion"],
                      data["velocity_at_perihelion"],
                      data["distance_at_aphelion"],
                      data["velocity_at_aphelion"],
                      str(data["perihelion_day"]),
                      )
                )

        self._db.commit()
        self._db.close()

    def read(self):
        self._cursor.execute(f"SELECT * FROM {self._name}")
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