import sys
from functools import partial
from solar_system_cartography.Qt import QtWidgets
from solar_system_cartography.api import ObjectInOrbit
from solar_system_cartography.envs import PRESETS

try:
    from solar_system_cartography import rig
    from maya import OpenMayaUI as omui
    from shiboken2 import wrapInstance
except:
    print("Standalone mode")

class MainUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainUI, self).__init__(parent)

        self.setWindowTitle("Cartographer v-dev")
        self.setGeometry(100, 100, 600, 400)
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        self._layout = QtWidgets.QVBoxLayout()
        central_widget.setLayout(self._layout)

        self.create_menubar()

        self.tab_widget = QtWidgets.QTabWidget()
        self.create_first_tab()
        self.create_second_tab()

        self.tab_widget.addTab(self.first_tab, "CREATE")
        self.tab_widget.addTab(self.select_tab, "SELECT")
        self._layout.addWidget(self.tab_widget)

        self.create_connections()

    def create_first_tab(self) ->None:
        self.first_tab = QtWidgets.QWidget()
        self.first_tab.setLayout(QtWidgets.QVBoxLayout())
        
        name_layout = QtWidgets.QHBoxLayout()
        name_lbl = QtWidgets.QLabel("Name")
        self.name_line_edit = QtWidgets.QLineEdit()
        name_layout.addWidget(name_lbl)
        name_layout.addWidget(self.name_line_edit)
        self.first_tab.layout().addLayout(name_layout)
        
        # object grid
        object_group_box = QtWidgets.QGroupBox("PHYSICAL CHARACTERISTICS")
        object_grid_layout = QtWidgets.QGridLayout()
        self.obj_data = {}
        self.obj_data["mass"] = QtWidgets.QLineEdit()
        self.obj_data["day"] = QtWidgets.QLineEdit()
        self.obj_data["axis_inclination"] = QtWidgets.QLineEdit()
        self.obj_data["radius"] = QtWidgets.QLineEdit()
        i = 1      
        for lbl,box in self.obj_data.items():
            object_grid_layout.addWidget(QtWidgets.QLabel(lbl), i, 0)
            object_grid_layout.addWidget(box, i, 1)
            i += 1
        object_group_box.setLayout(object_grid_layout)
        self.first_tab.layout().addWidget(object_group_box)

        # orbital grid
        orbital_group_box = QtWidgets.QGroupBox("ORBITAL CHARACTERISTICS")
        orbital_grid_layout = QtWidgets.QGridLayout()
        self.orb_data = {}
        self.orb_data["semi_major_axis"] = QtWidgets.QLineEdit()
        self.orb_data["inclination"] = QtWidgets.QLineEdit()
        self.orb_data["eccentricity"] = QtWidgets.QLineEdit()
        i = 1      
        for lbl,box in self.orb_data.items():
            orbital_grid_layout.addWidget(QtWidgets.QLabel(lbl), i, 0)
            orbital_grid_layout.addWidget(box, i, 1)
            i += 1
        orbital_group_box.setLayout(orbital_grid_layout)
        self.first_tab.layout().addWidget(orbital_group_box)

        # create button
        self.create_button = QtWidgets.QPushButton("CREATE")
        self.first_tab.layout().addWidget(self.create_button)
        self.first_tab.layout().addStretch(1)

    def create_second_tab(self) ->None:
        self.select_tab = QtWidgets.QWidget()
        tree_widget = QtWidgets.QTreeWidget()
        tree_widget.setColumnCount(5)
        tree_widget.setHeaderLabels(["Header 1", "Header 2", "Header 3", "Header 4", "Header 5"])
        
        select_tab_layout = QtWidgets.QVBoxLayout()
        select_tab_layout.addWidget(tree_widget)
        self.select_tab.setLayout(select_tab_layout)

    def create_menubar(self):
        self.menu_bar = self.menuBar()
        self.presets_menu = self.menu_bar.addMenu("Presets")
        self.mercury_action = QtWidgets.QAction("Mercury", self)
        self.venus_action = QtWidgets.QAction("Venus", self)
        self.earth_action = QtWidgets.QAction("Earth", self)
        self.mars_action = QtWidgets.QAction("Mars", self)
        self.jupiter_action = QtWidgets.QAction("Jupiter", self)
        self.presets_menu.addAction(self.mercury_action)
        self.presets_menu.addAction(self.venus_action)
        self.presets_menu.addAction(self.earth_action)
        self.presets_menu.addAction(self.mars_action)
        self.presets_menu.addAction(self.jupiter_action)

    def create_connections(self) ->None:
        self.create_button.clicked.connect(self.on_create_button_clicked)
        self.mercury_action.triggered.connect(partial(self.on_preset_triggered, "Mercury"))
        self.venus_action.triggered.connect(partial(self.on_preset_triggered, "Venus"))
        self.earth_action.triggered.connect(partial(self.on_preset_triggered, "Earth"))
        self.mars_action.triggered.connect(partial(self.on_preset_triggered, "Mars"))
        self.jupiter_action.triggered.connect(partial(self.on_preset_triggered, "Jupiter"))

    def read(self) ->dict:
        data = {
            "mass" : float(self.obj_data.get("mass").text()),
            "day" : float(self.obj_data.get("day").text()),
            "radius" : float(self.obj_data.get("radius").text()),
            "axis_inclination" : float(self.obj_data.get("axis_inclination").text()),
            "semi_major_axis" : float(self.orb_data.get("semi_major_axis").text()),
            "inclination" : float(self.orb_data.get("inclination").text()),
            "eccentricity" : float(self.orb_data.get("eccentricity").text()),
        }
        return data
    
    def on_preset_triggered(self, name) ->None:
        d = PRESETS.get(name)
        self.name_line_edit.setText(name)
        self.obj_data["mass"].setText(str(d["mass"]))
        self.obj_data["day"].setText(str(d["day"]))
        self.obj_data["radius"].setText(str(d["radius"]))
        self.obj_data["axis_inclination"].setText(str(d["axis_inclination"]))
        self.orb_data["semi_major_axis"].setText(str(d["semi_major_axis"]))
        self.orb_data["inclination"].setText(str(d["inclination"]))
        self.orb_data["eccentricity"].setText(str(d["eccentricity"]))

    def on_create_button_clicked(self) ->None:
        d = self.read()
        obj = ObjectInOrbit(object_name=self.name_line_edit.text(),
                            object_mass=d["mass"],
                            semi_major_axis=d["semi_major_axis"],
                            inclination=d["inclination"],
                            eccentricity=d["eccentricity"],
                            rotation_period=d["day"],
                            axis_inclination=d["axis_inclination"],
                            object_radius=d["radius"])
        print(obj)
        try:
            rig.build(obj)
        except:
            print("Visualisation available in Maya only")

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