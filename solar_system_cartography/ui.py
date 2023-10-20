import sys
from PyQt5 import QtWidgets

class MainUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

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

        self.tab_widget.addTab(self.create_tab, "CREATE")
        self.tab_widget.addTab(self.select_tab, "SELECT")
        self._layout.addWidget(self.tab_widget)

    def create_first_tab(self) ->None:
        self.create_tab = QtWidgets.QWidget()
        create_layout = QtWidgets.QGridLayout()
        create_button = QtWidgets.QPushButton("CREATE")
        
        # data
        object_title = QtWidgets.QLabel(f"PHYSICAL CHARACTERISTICS")
        data = {}
        data["Name"] = QtWidgets.QLineEdit()
        data["Mass"] = QtWidgets.QDoubleSpinBox()
        data["Rotation period"] = QtWidgets.QDoubleSpinBox()
        data["Axis inclination"] = QtWidgets.QDoubleSpinBox()

        i = 0      
        for lbl,box in data.items():
            create_layout.addWidget(QtWidgets.QLabel(lbl), i, 0)
            create_layout.addWidget(box, i, 1)
            i += 1

        create_layout.addWidget(create_button, 5, 0, 1, 2)
        self.create_tab.setLayout(create_layout)

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

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainUI()
    window.show()
    sys.exit(app.exec_())
