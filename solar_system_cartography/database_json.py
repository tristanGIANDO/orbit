import os, json

class Database():
    def __init__(self, project_path:str) -> None:
        self._path = project_path
        self._name = os.path.basename(self._path)
        self._json_path = os.path.join(self._path, f"{self._name}.json")

        self._data = self.read()
        # init project
        self._data["project_path"] = self._path
        self.write()

    def insert_object(self, data:dict) ->None:
        self._data[data.get("name","")] = data
        self.write()

    def write(self) ->None:
        """Writes data to a .json file.

        :param data: The data 
        :type data: dict
        :param path: path of the json file
        :type path: str
        """
        with open(self._json_path, 'w') as f:
            json.dump(self._data, f, indent=4)

    def read(self) ->list:
        """Reads json file

        :param path: the path of the json file
        :type path: str
        :return: the data
        :rtype: dict
        """
        if not os.path.isfile(self._json_path):
            return {}
        with open(self._json_path, 'r') as openfile:
            data = json.load(openfile)

        return data