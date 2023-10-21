import sys
from solar_system_cartography.Qt import QtWidgets
try:
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
        data = {}
        data["Mass (kg)"] = QtWidgets.QLineEdit()
        data["Rotation period (d)"] = QtWidgets.QLineEdit()
        data["Axis inclination (°)"] = QtWidgets.QLineEdit()
        i = 1      
        for lbl,box in data.items():
            object_grid_layout.addWidget(QtWidgets.QLabel(lbl), i, 0)
            object_grid_layout.addWidget(box, i, 1)
            i += 1
        object_group_box.setLayout(object_grid_layout)
        self.first_tab.layout().addWidget(object_group_box)

        # orbital grid
        orbital_group_box = QtWidgets.QGroupBox("ORBITAL CHARACTERISTICS")
        orbital_grid_layout = QtWidgets.QGridLayout()
        data = {}
        data["Semi Major Axis (AU)"] = QtWidgets.QLineEdit()
        data["Inclination (°)"] = QtWidgets.QLineEdit()
        data["Eccentricity"] = QtWidgets.QLineEdit()
        i = 1      
        for lbl,box in data.items():
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
        self.presets_menu.addAction(self.mercury_action)
        self.presets_menu.addAction(self.venus_action)

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
