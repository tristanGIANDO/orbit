import os, sys
from functools import partial
from solar_system_cartography.Qt import QtWidgets, QtGui, QtCore
from solar_system_cartography.api import ObjectInOrbit
from solar_system_cartography.envs import PRESETS
from solar_system_cartography.database import Database

try:
    from solar_system_cartography.rig import Rig
    from maya import OpenMayaUI as omui
    from shiboken2 import wrapInstance
    STANDALONE = False
except:
    STANDALONE = True

TYPES = ["Planet", "Star", "Comet", "Natural Satellite", "Artificial Satellite", "Asteroid", "Random"]

COLORS = {
    TYPES[0] : [255,255,255],
    TYPES[1] : [0,0,0],
    TYPES[2] : [0,0,255],
    TYPES[3] : [255,0,0],
    TYPES[4] : [0,255,0],
    TYPES[5] : [80,20,255],
    TYPES[6] : [50,50,50],
}

class CustomTreeItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, data:dict):
        super(CustomTreeItem, self).__init__()
        if not data:
            return
        self._data = data
        for i in range(17):
            self.setText(i, str(data[i+1]))

class MainUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainUI, self).__init__(parent)

        self._title = "ORBIT"
        self._version = "dev"
        self._db = None
        self.setWindowTitle(f"{self._title} v-{self._version}")
        self.setGeometry(100, 100, 600, 400)
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        self._layout = QtWidgets.QVBoxLayout()
        central_widget.setLayout(self._layout)
        self._project_path = ""

        self.create_menubar()

        title_label = QtWidgets.QLabel(self._title)
        title_label.setFont(QtGui.QFont("Arial", 18, QtGui.QFont.Bold))
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        central_widget.layout().addWidget(title_label)
        # root
        root_layout = QtWidgets.QHBoxLayout()
        self.root_project_line_edit = QtWidgets.QLineEdit()
        self.root_project_line_edit.addAction(ICONS.get("folder"), QtWidgets.QLineEdit.LeadingPosition)
        self.root_project_line_edit.setPlaceholderText("Project Directory")
        self.set_project_button = QtWidgets.QPushButton("Set Project")
        root_layout.addWidget(self.root_project_line_edit)
        root_layout.addWidget(self.set_project_button)
        central_widget.layout().addLayout(root_layout)

        self.tab_widget = QtWidgets.QTabWidget()
        self.objects_creation_tab()
        self.objects_vis_tab()
        self.objects_settings_tab()

        self.tab_widget.addTab(self.creation_tab, ICONS.get("create"), "CREATE")
        self.tab_widget.addTab(self.select_tab, ICONS.get("select"), "SELECT")
        self.tab_widget.addTab(self.settings_tab, ICONS.get("settings"), "SETTINGS")
        self._layout.addWidget(self.tab_widget)

        self.create_connections()

    def objects_creation_tab(self) ->None:
        self.creation_tab = QtWidgets.QWidget()
        self.creation_tab.setLayout(QtWidgets.QVBoxLayout())
        # parent box
        self.parent_box = QtWidgets.QComboBox()
        self.creation_tab.layout().addWidget(self.parent_box)
        # type box
        self.type_box = QtWidgets.QComboBox()
        self.type_box.addItems(TYPES)
        self.creation_tab.layout().addWidget(self.type_box)
        
        # global grid
        glob_group_box = QtWidgets.QGroupBox("GLOBAL")
        object_grid_layout = QtWidgets.QGridLayout()
        self.glob_data = {}
        self.glob_data["name"] = QtWidgets.QLineEdit()
        self.glob_data["name"].setPlaceholderText("Object name")
        self.glob_data["type"] = self.type_box
        self.glob_data["parent"] = self.parent_box
        i = 1      
        for lbl,box in self.glob_data.items():
            object_grid_layout.addWidget(QtWidgets.QLabel(lbl), i, 0)
            object_grid_layout.addWidget(box, i, 1)
            i += 1
        glob_group_box.setLayout(object_grid_layout)
        self.creation_tab.layout().addWidget(glob_group_box)

        # object grid
        object_group_box = QtWidgets.QGroupBox("PHYSICAL CHARACTERISTICS")
        object_grid_layout = QtWidgets.QGridLayout()
        self.obj_data = {}
        self.obj_data["mass"] = QtWidgets.QLineEdit()
        self.obj_data["mass"].setPlaceholderText("Object mass (kg)")
        self.obj_data["day"] = QtWidgets.QLineEdit()
        self.obj_data["day"].setPlaceholderText("Number of earth days to complete a full circle on its axis")
        self.obj_data["axis_inclination"] = QtWidgets.QLineEdit()
        self.obj_data["axis_inclination"].setPlaceholderText("Inclination of the object on its axis (°)")
        i = 1      
        for lbl,box in self.obj_data.items():
            object_grid_layout.addWidget(QtWidgets.QLabel(lbl), i, 0)
            object_grid_layout.addWidget(box, i, 1)
            i += 1
        object_group_box.setLayout(object_grid_layout)
        self.creation_tab.layout().addWidget(object_group_box)

        # orbital grid
        orbital_group_box = QtWidgets.QGroupBox("ORBITAL CHARACTERISTICS")
        orbital_grid_layout = QtWidgets.QGridLayout()
        self.orb_data = {}
        self.orb_data["semi_major_axis"] = QtWidgets.QLineEdit()
        self.orb_data["semi_major_axis"].setPlaceholderText("Semi major axis of the orbit (AU)")
        self.orb_data["inclination"] = QtWidgets.QLineEdit()
        self.orb_data["inclination"].setPlaceholderText("Inclination of the orbit (°)")
        self.orb_data["eccentricity"] = QtWidgets.QLineEdit()
        self.orb_data["eccentricity"].setPlaceholderText("Eccentricity of the orbit")
        self.orb_data["arg_periapsis"] = QtWidgets.QLineEdit()
        self.orb_data["arg_periapsis"].setPlaceholderText("Periapsis argument (°)")
        self.orb_data["ascending_node"] = QtWidgets.QLineEdit()
        self.orb_data["ascending_node"].setPlaceholderText("Ascending node (°)")
        self.orb_data["random_perihelion_day"] = QtWidgets.QDateEdit()
        self.orb_data["random_perihelion_day"].setDisplayFormat("yyyy, MM, dd")
        i = 1      
        for lbl,box in self.orb_data.items():
            orbital_grid_layout.addWidget(QtWidgets.QLabel(lbl), i, 0)
            orbital_grid_layout.addWidget(box, i, 1)
            i += 1
        orbital_group_box.setLayout(orbital_grid_layout)
        self.creation_tab.layout().addWidget(orbital_group_box)

        # create button
        self.create_button = QtWidgets.QPushButton("CREATE")
        self.creation_tab.layout().addWidget(self.create_button)
        self.creation_tab.layout().addStretch(1)

    def objects_vis_tab(self) ->None:
        self.select_tab = QtWidgets.QWidget()
        self.tree = QtWidgets.QTreeWidget()
        self.tree.setColumnCount(17)
        self.tree.setHeaderLabels(["Name",
                                   "Type",
                                   "Mass",
                                   "Rotation Period",
                                   "Axis Inclination",
                                   "Semi Major Axis",
                                   "Semi Minor Axis",
                                   "Inclination",
                                   "Eccentricity",
                                   "Period",
                                   "Ascending Node",
                                   "Periapsis Argument",
                                   "Circumference",
                                   "Perihelion Distance",
                                   "Perihelion Speed",
                                   "Aphelion Distance",
                                   "Aphelion Speed",
                                   "Perihelion Date"
                                   ])
        
        select_tab_layout = QtWidgets.QVBoxLayout()
        select_tab_layout.addWidget(self.tree)
        self.select_tab.setLayout(select_tab_layout)

    def objects_settings_tab(self) ->None:
        self.settings_tab = QtWidgets.QWidget()
        self.settings_tab.setLayout(QtWidgets.QVBoxLayout())
        
        # visualisation grid
        visu_group_box = QtWidgets.QGroupBox("COLORS")
        visu_grid_layout = QtWidgets.QGridLayout()
        self.visu_data = {}
        for typ in TYPES:
            self.visu_data[typ] = QtWidgets.QLineEdit()
            self.visu_data[typ].setText(str(COLORS[typ]))
        i = 1      
        for lbl,box in self.visu_data.items():
            visu_grid_layout.addWidget(QtWidgets.QLabel(lbl), i, 0)
            visu_grid_layout.addWidget(box, i, 1)
            i += 1
        visu_group_box.setLayout(visu_grid_layout)
        self.settings_tab.layout().addWidget(visu_group_box)
        
        self.settings_tab.layout().addStretch(1)

    def reload_tree(self) ->None:
        self.tree.clear()
        objects = self._db.read()
        if not objects:
            return
  
        for data in objects or []:
            item = CustomTreeItem(data)
            self.tree.addTopLevelItem(item)

    def create_menubar(self):
        self.menu_bar = self.menuBar()

        self.presets_menu = self.menu_bar.addMenu("Presets")
        self.action = {}
        for obj in ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto", "1P/Halley"]:
            self.action[obj] = QtWidgets.QAction(obj, self)
            self.presets_menu.addAction(self.action[obj])
            self.action[obj].triggered.connect(partial(self.on_preset_triggered, obj))

    def create_connections(self) ->None:
        self.set_project_button.clicked.connect(self.show_project_dialog)
        self.create_button.clicked.connect(self.on_create_button_clicked)

    def read(self) ->dict:
        date = self.orb_data.get("random_perihelion_day").date().toString("yyyy.MM.dd").split(".")
        date = [int(d) for d in date]
        
        data = {
            "name" : self.glob_data["name"].text(),
            "type" : self.glob_data["type"].currentText(),
            "mass" : float(self.obj_data.get("mass").text()),
            "day" : float(self.obj_data.get("day").text()),
            "axis_inclination" : float(self.obj_data.get("axis_inclination").text()),
            "semi_major_axis" : float(self.orb_data.get("semi_major_axis").text()),
            "inclination" : float(self.orb_data.get("inclination").text()),
            "eccentricity" : float(self.orb_data.get("eccentricity").text()),
            "arg_periapsis" : float(self.orb_data.get("arg_periapsis").text()),
            "ascending_node" : float(self.orb_data.get("ascending_node").text()),
            "random_perihelion_day" : date
        }
        return data
    
    def on_preset_triggered(self, name) ->None:
        d = PRESETS.get(name)
        self.glob_data["name"].setText(name)
        self.obj_data["mass"].setText(str(d["mass"]))
        self.obj_data["day"].setText(str(d["day"]))
        self.obj_data["axis_inclination"].setText(str(d["axis_inclination"]))
        self.orb_data["semi_major_axis"].setText(str(d["semi_major_axis"]))
        self.orb_data["inclination"].setText(str(d["inclination"]))
        self.orb_data["eccentricity"].setText(str(d["eccentricity"]))
        self.orb_data["arg_periapsis"].setText(str(d["arg_periapsis"]))
        self.orb_data["ascending_node"].setText(str(d["ascending_node"]))
        q_date = QtCore.QDate(d["random_perihelion_day"][0],
                              d["random_perihelion_day"][1],
                              d["random_perihelion_day"][2])
        self.orb_data["random_perihelion_day"].setDate(q_date) 

    def show_color_dialog(self, typ:str):
        color = QtWidgets.QColorDialog.getColor()

        if color.isValid():
            self.visu_data[typ].setStyleSheet(f"background-color: {color.name()};")
            # add to general dict
            COLORS[typ] = [color.red()/255,color.green()/255,color.blue()/255]

    def show_project_dialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.ShowDirsOnly

        project_path = QtWidgets.QFileDialog.getExistingDirectory(self,
                                                                 "Set Project Directory",
                                                                 "",
                                                                 options=options)

        if project_path:
            self._project_path = project_path
            self.root_project_line_edit.setText(project_path)
            self._db = Database(project_path)
            self.reload_tree()
            self.build_from_tree()

    def build_from_tree(self) ->None:
        items = []
        def get_items(tree_item):
            try:
                items.append(tree_item._data)
            except:
                "is invisibleRootItem"
            for i in range(tree_item.childCount()):
                get_items(tree_item.child(i))

        get_items(self.tree.invisibleRootItem())
        
        for item in items:
            data = {
                "name" : item[1],
                "type" : item[2],
                "mass" : item[3],
                "day" : item[4],
                "axis_inclination" : item[5],
                "semi_major_axis" : item[6],
                "inclination" : item[7],
                "eccentricity" : item[9],
                "arg_periapsis" : item[12],
                "ascending_node" : item[11],
                "random_perihelion_day" : eval(item[18])
            }
            self.build_rig(data)

    def on_create_button_clicked(self) ->None:
        self.build_rig(self.read())
    
    def build_rig(self, d:dict) ->None:
        obj = ObjectInOrbit(project_path=self._project_path,
                            object_name=d["name"],
                            object_type=d["type"],
                            object_mass=d["mass"],
                            semi_major_axis=d["semi_major_axis"],
                            inclination=d["inclination"],
                            eccentricity=d["eccentricity"],
                            rotation_period=d["day"],
                            arg_periapsis=d["arg_periapsis"],
                            ascending_node=d["ascending_node"],
                            axis_inclination=d["axis_inclination"],
                            random_perihelion_day=d["random_perihelion_day"]
                            )
        
        self.reload_tree()
        
        if not STANDALONE:
            rig = Rig(obj, COLORS[d["type"]])

class Icons():
    def __init__(self):
        self._root = os.path.join(os.path.dirname(__file__), "icons")
        self._cache = {}
        self._icons = {
            "logo" : "logo.png",
            "create" : "create.png",
            "folder" : "folder.png",
            "global" : "global.png",
            "orbital" : "orbital.png",
            "physical" : "physical.png",
            "select" : "select.jpg",
            "settings" : "settings.png"
        }

    def get(self, key):
        if key in self._cache:
            return self._cache[key]
        
        path = os.path.join(self._root, self._icons.get(key))
        icon = QtGui.QIcon(path)
        self._cache[path] = icon
        return icon

ICONS = Icons()

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

def run_ui():
    try:
        parent = maya_main_window()
        global my_window
        my_window = MainUI(parent)
        my_window.show()
    except:
        try:
            app = QtWidgets.QApplication(sys.argv)
        except:
            try:
                ui.close()
            except:
                pass

        ui = MainUI()
        ui.show()

        try:
            sys.exit(app.exec_())
        except:
            pass
    
if __name__ == '__main__':
    run_ui()