import sqlite3

class Database():
    def __init__(self, path:str=None, name:str="solar_system") -> None:
        self._name = name
        self._table_name = "objects"

        self._db = sqlite3.connect(self._name)
        self._cursor = self._db.cursor()

        self.create()

    def create(self) ->None:
        self._cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {self._table_name}
                (
                    [id] INT AUTO_INCREMENT PRIMARY KEY,
                    [name] TEXT,
                    [mass] REAL,
                    [rotation_period] REAL,
                    [axis_inclination] REAL,
                    [semi_major_axis] REAL,
                    [inclination] REAL,
                    [eccentricity] REAL
                )
                """)

    def insert(self, data:dict) ->None:
        self._cursor.execute(f"""
                INSERT INTO {self._table_name}
                (
                    name,
                    mass,
                    rotation_period,
                    axis_inclination,
                    semi_major_axis,
                    inclination,
                    eccentricity
                )

                VALUES
                (?,?,?,?,?,?,?)
                """, (data["name"],
                      data["mass"],
                      data["rotation_period"],
                      data["axis_inclination"],
                      data["semi_major_axis"],
                      data["inclination"],
                      data["eccentricity"]
                      )
                )

        self._db.commit()
        self._db.close()

    def read(self):
        self._cursor.execute(f"SELECT * FROM {self._table_name}")
        return self._cursor.fetchall()
    
    def update(self, column:str, id:str, new_value:str):
        try:
            sql = f"UPDATE {self._table_name} SET {column} = '{new_value}' WHERE (id = '{str(id)}')"
            self._cursor.execute(sql)
            self._db.commit()
        except:
            pass