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
except:
    print("Standalone mode")

class CustomTreeItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, data:list):
        super(CustomTreeItem, self).__init__()
        
        self.setText(0, data[1])
        self.setText(1, str(data[2]))
        self.setText(2, str(data[3]))
        self.setText(3, str(data[4]))
        self.setText(4, str(data[5]))
        self.setText(5, str(data[6]))
        self.setText(6, str(data[7]))

class MainUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainUI, self).__init__(parent)

        # self._db = Database(path=r"C:\Users\giand\OneDrive\Documents\packages\solar_system_cartography\dev\solar_system_cartography",
        #                        name="solar_system.db")

        self.setWindowTitle("Cartographer v-dev")
        self.setGeometry(100, 100, 600, 400)
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        self._layout = QtWidgets.QVBoxLayout()
        central_widget.setLayout(self._layout)

        self.create_menubar()

        self.tab_widget = QtWidgets.QTabWidget()
        self.objects_creation_tab()
        self.objects_vis_tab()

        self.tab_widget.addTab(self.creation_tab, "CREATE")
        self.tab_widget.addTab(self.select_tab, "SELECT")
        self._layout.addWidget(self.tab_widget)

        self.create_connections()

        self.selected_color = QtGui.QColor(1, 1, 1)

    def objects_creation_tab(self) ->None:
        self.creation_tab = QtWidgets.QWidget()
        self.creation_tab.setLayout(QtWidgets.QVBoxLayout())

        # root
        root_layout = QtWidgets.QHBoxLayout()
        root_label = QtWidgets.QLabel("Project Directory")
        self.root_line_edit = QtWidgets.QLineEdit()
        self.set_project_button = QtWidgets.QPushButton("Set Project")
        root_layout.addWidget(root_label)
        root_layout.addWidget(self.root_line_edit)
        root_layout.addWidget(self.set_project_button)
        self.creation_tab.layout().addLayout(root_layout)

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
        tree_widget = QtWidgets.QTreeWidget()
        tree_widget.setColumnCount(7)
        tree_widget.setHeaderLabels(["Name", "Mass", "Rotation period", "Axis inclination", "Semi Major Axis", "Inclination", "Eccentricity"])
        
        select_tab_layout = QtWidgets.QVBoxLayout()
        select_tab_layout.addWidget(tree_widget)
        self.select_tab.setLayout(select_tab_layout)

        # for obj in self._db.read() or []:
        #     item = CustomTreeItem(obj)
        #     tree_widget.addTopLevelItem(item)

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
        self.create_button.clicked.connect(self.on_create_button_clicked)
        self.visu_data["orbit color"].clicked.connect(self.showColorDialog)

    def read(self) ->dict:
        date = self.orb_data.get("random_perihelion_day").date().toString("yyyy.MM.dd").split(".")
        date = [int(d) for d in date]
        
        data = {
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

    def showColorDialog(self):
        color = QtWidgets.QColorDialog.getColor(initial=self.selected_color)

        if color.isValid():
            print(f"{color.red()}, {color.green()}, {color.blue()}")
            self.selected_color = color
            self.visu_data["orbit color"].setStyleSheet(f"background-color: {color.name()};")

    def on_create_button_clicked(self) ->None:
        d = self.read()
        obj = ObjectInOrbit(object_name=self.glob_data["name"].text(),
                            object_mass=d["mass"],
                            semi_major_axis=d["semi_major_axis"],
                            inclination=d["inclination"],
                            eccentricity=d["eccentricity"],
                            rotation_period=d["day"],
                            arg_periapsis=d["arg_periapsis"],
                            ascending_node=d["ascending_node"],
                            axis_inclination=d["axis_inclination"],
                            random_perihelion_day=d["random_perihelion_day"])
        print(obj)
        # try:
        rig = Rig(obj)
        # except:
        #     print("Visualisation available in Maya only")

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