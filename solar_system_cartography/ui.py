import sys
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

class CustomTreeItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, data:dict):
        super(CustomTreeItem, self).__init__()
        if not data:
            return
        self._obj = data
        for i in range(17):
            self.setText(i, str(data[i+1]))

class MainUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainUI, self).__init__(parent)

        self._db = None

        self.setWindowTitle("Cartographer v-dev")
        self.setGeometry(100, 100, 600, 400)
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        self._layout = QtWidgets.QVBoxLayout()
        central_widget.setLayout(self._layout)

        self.create_menubar()

        # root
        root_layout = QtWidgets.QHBoxLayout()
        self.root_project_line_edit = QtWidgets.QLineEdit()
        self.root_project_line_edit.setPlaceholderText("Project Directory")
        self.set_project_button = QtWidgets.QPushButton("Set Project")
        root_layout.addWidget(self.root_project_line_edit)
        root_layout.addWidget(self.set_project_button)
        central_widget.layout().addLayout(root_layout)

        self.tab_widget = QtWidgets.QTabWidget()
        self.objects_creation_tab()
        self.objects_vis_tab()

        self.tab_widget.addTab(self.creation_tab, "CREATE")
        self.tab_widget.addTab(self.select_tab, "SELECT")
        self._layout.addWidget(self.tab_widget)

        self.create_connections()

        self.selected_color = QtGui.QColor(1, 1, 1)
        self._maya_data = {} # to use for specific settings (color, textures...)

    def objects_creation_tab(self) ->None:
        self.creation_tab = QtWidgets.QWidget()
        self.creation_tab.setLayout(QtWidgets.QVBoxLayout())
        # parent box
        self.parent_box = QtWidgets.QComboBox()
        self.creation_tab.layout().addWidget(self.parent_box)
        # type box
        self.type_box = QtWidgets.QComboBox()
        self.type_box.addItems(["Object", "Star"])
        self.creation_tab.layout().addWidget(self.type_box)
        
        # global grid
        glob_group_box = QtWidgets.QGroupBox("GLOBAL")
        object_grid_layout = QtWidgets.QGridLayout()
        self.glob_data = {}
        self.glob_data["name"] = QtWidgets.QLineEdit()
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
        self.obj_data["day"] = QtWidgets.QLineEdit()
        self.obj_data["axis_inclination"] = QtWidgets.QLineEdit()
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
        self.orb_data["inclination"] = QtWidgets.QLineEdit()
        self.orb_data["eccentricity"] = QtWidgets.QLineEdit()
        self.orb_data["arg_periapsis"] = QtWidgets.QLineEdit()
        self.orb_data["ascending_node"] = QtWidgets.QLineEdit()
        self.orb_data["random_perihelion_day"] = QtWidgets.QDateEdit()
        self.orb_data["random_perihelion_day"].setDisplayFormat("yyyy, MM, dd")
        i = 1      
        for lbl,box in self.orb_data.items():
            orbital_grid_layout.addWidget(QtWidgets.QLabel(lbl), i, 0)
            orbital_grid_layout.addWidget(box, i, 1)
            i += 1
        orbital_group_box.setLayout(orbital_grid_layout)
        self.creation_tab.layout().addWidget(orbital_group_box)

        # visualisation grid
        visu_group_box = QtWidgets.QGroupBox("VISUALISATION SETTINGS")
        visu_grid_layout = QtWidgets.QGridLayout()
        self.visu_data = {}
        self.visu_data["orbit color"] = QtWidgets.QPushButton()
        # self.visu_data["object texture"] = QtWidgets.QLineEdit()
        i = 1      
        for lbl,box in self.visu_data.items():
            visu_grid_layout.addWidget(QtWidgets.QLabel(lbl), i, 0)
            visu_grid_layout.addWidget(box, i, 1)
            i += 1
        visu_group_box.setLayout(visu_grid_layout)
        self.creation_tab.layout().addWidget(visu_group_box)

        # create button
        self.create_button = QtWidgets.QPushButton("CREATE")
        self.creation_tab.layout().addWidget(self.create_button)
        self.creation_tab.layout().addStretch(1)

    def objects_vis_tab(self) ->None:
        self.select_tab = QtWidgets.QWidget()
        self.tree = QtWidgets.QTreeWidget()
        self.tree.setColumnCount(17)
        self.tree.setHeaderLabels(["Name",
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

    def reload_tree(self) ->None:
        self.tree.clear()
        objects = self._db.read()
        if not objects:
            return
  
        for obj in objects or []:
            item = CustomTreeItem(obj)
            self.tree.addTopLevelItem(item)

    def create_menubar(self):
        self.menu_bar = self.menuBar()
        
        self.file_menu = self.menu_bar.addMenu("File")
        self.new_file_action = QtWidgets.QAction("New file", self)
        self.open_file_action = QtWidgets.QAction("Open file", self)
        self.file_menu.addAction(self.new_file_action)
        self.file_menu.addAction(self.open_file_action)

        self.presets_menu = self.menu_bar.addMenu("Presets")
        self.action = {}
        for obj in ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto", "1P/Halley"]:
            self.action[obj] = QtWidgets.QAction(obj, self)
            self.presets_menu.addAction(self.action[obj])
            self.action[obj].triggered.connect(partial(self.on_preset_triggered, obj))

    def create_connections(self) ->None:
        self.set_project_button.clicked.connect(self.show_project_dialog)
        self.create_button.clicked.connect(self.on_create_button_clicked)
        self.visu_data["orbit color"].clicked.connect(self.show_color_dialog)

    def read(self) ->dict:
        date = self.orb_data.get("random_perihelion_day").date().toString("yyyy.MM.dd").split(".")
        date = [int(d) for d in date]
        
        data = {
            "name" : self.glob_data["name"].text(),
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

    def show_color_dialog(self):
        color = QtWidgets.QColorDialog.getColor(initial=self.selected_color)

        if color.isValid():
            self.selected_color = color
            self.visu_data["orbit color"].setStyleSheet(f"background-color: {color.name()};")
            # add to general dict
            self._maya_data["orbit_color"] = [color.red()/255,color.green()/255,color.blue()/255]

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
                items.append(tree_item._obj)
            except:
                "is invisibleRootItem"
            for i in range(tree_item.childCount()):
                get_items(tree_item.child(i))

        get_items(self.tree.invisibleRootItem())
        
        for item in items:
            data = {
                "name" : item[1],
                "mass" : item[2],
                "day" : item[3],
                "axis_inclination" : item[4],
                "semi_major_axis" : item[5],
                "inclination" : item[7],
                "eccentricity" : item[8],
                "arg_periapsis" : item[11],
                "ascending_node" : item[10],
                "random_perihelion_day" : eval(item[17])
            }
            self.build_rig(data, insert_in_database=False)

    def on_create_button_clicked(self) ->None:
        self.build_rig(self.read())
    
    def build_rig(self, d:dict, insert_in_database:bool=True) ->None:
        obj = ObjectInOrbit(project_path=self._project_path,
                            object_name=d["name"],
                            object_mass=d["mass"],
                            semi_major_axis=d["semi_major_axis"],
                            inclination=d["inclination"],
                            eccentricity=d["eccentricity"],
                            rotation_period=d["day"],
                            arg_periapsis=d["arg_periapsis"],
                            ascending_node=d["ascending_node"],
                            axis_inclination=d["axis_inclination"],
                            random_perihelion_day=d["random_perihelion_day"],
                            insert_in_database=insert_in_database)
        
        self.reload_tree()
        
        if not STANDALONE:
            rig = Rig(obj, self._maya_data)

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