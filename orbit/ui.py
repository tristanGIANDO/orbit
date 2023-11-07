import os, sys, webbrowser
from functools import partial
from orbit.Qt import QtWidgets, QtGui, QtCore
from orbit import envs
from orbit.presets import PRESETS
from orbit.api import Api

try:
    from maya import OpenMayaUI as omui
    from shiboken2 import wrapInstance
    STANDALONE = False
except:
    STANDALONE = True

HEADERS = [envs.E_NAME,
           envs.E_TYPE,
           envs.E_PARENT,
           envs.E_MASS,
           envs.E_PERIOD,
           envs.E_INCLINATION,
           envs.O_SEMI_MAJOR_AXIS,
           envs.O_INCLINATION,
           envs.O_ECCENTRICITY,
           envs.O_ASCENDING_NODE,
           envs.O_ARG_PERIAPSIS,
           envs.O_PERIHELION_DAY,
           envs.O_SEMI_MINOR_AXIS,  
           envs.O_PERIOD,
           envs.O_CIRCUMFERENCE,
           envs.O_PERIHELION_D,
           envs.O_PERIHELION_V,
           envs.O_APHELION_D,
           envs.O_APHELION_V]

class CustomTreeItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, data:dict):
        super(CustomTreeItem, self).__init__()
        if not data:
            return
        self._data = data
        if data:
            self._name = data[0]
            for i in range(len(HEADERS)):
                self.setText(i, str(data[i]))
                # self.setTextAlignment(i, QtCore.Qt.AlignCenter)
                if i % 2 == 0:
                    if STANDALONE:
                        self.setBackground(i, QtGui.QColor(240,240,240))
                    else:
                        self.setBackground(i, QtGui.QColor(50,50,50))

            # color type
            self.setIcon(1, QtGui.QIcon(self.type_color(data[1])))

        self.setSizeHint(2,QtCore.QSize(20,20))

    def type_color(self, typ:str) ->QtGui.QPixmap:
        ct = envs.COLORS[typ]
        color = QtGui.QPixmap(20,20)
        color.fill(QtGui.QColor(*ct))

        return color

class MainUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainUI, self).__init__(parent)

        self._title = "ORBIT"
        self._version = "1.0"
        self._builder = None
        self.setWindowTitle(f"{self._title} v-{self._version}")
        self.setWindowIcon(ICONS.get("logo"))
        self.setGeometry(100, 100, 600, 400)
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        self._layout = QtWidgets.QVBoxLayout()
        central_widget.setLayout(self._layout)
        self._project_path = ""

        self.create_menubar()
        # title
        title_label = QtWidgets.QLabel(self)
        pixmap = QtGui.QPixmap(ICONS.get_title())
        pixmap = pixmap.scaledToWidth(200, QtCore.Qt.SmoothTransformation)
        title_label.setPixmap(pixmap)
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        central_widget.layout().addWidget(title_label)
        # root
        root_layout = QtWidgets.QHBoxLayout()
        self.root_project_line_edit = QtWidgets.QLineEdit()
        self.root_project_line_edit.addAction(ICONS.get("folder"), QtWidgets.QLineEdit.LeadingPosition)
        self.root_project_line_edit.setPlaceholderText("Project Directory")
        self.root_project_line_edit.setReadOnly(True)
        self.set_project_button = QtWidgets.QPushButton("Set Project")
        root_layout.addWidget(self.root_project_line_edit)
        root_layout.addWidget(self.set_project_button)
        central_widget.layout().addLayout(root_layout)

        self.tab_widget = QtWidgets.QTabWidget()
        self.objects_creation_tab()
        self.database_tab()
        # self.objects_settings_tab()

        self.tab_create_idx = self.tab_widget.addTab(self.creation_tab, ICONS.get("create"), "CREATE")
        self.tab_db_idx = self.tab_widget.addTab(self.db_tab, ICONS.get("physical"), "DATABASE")
        # self.tab_settings_idx = self.tab_widget.addTab(self.settings_tab, ICONS.get("settings"), "SETTINGS")
        self._layout.addWidget(self.tab_widget)

        self._layout.addWidget(QtWidgets.QLabel("By Tristan Giandoriggio"))

        self.create_connections()

    def closeEvent(self, event):
        if self._builder:
            self._builder.close()
        event.accept()

    def objects_creation_tab(self) ->None:
        self.creation_tab = QtWidgets.QWidget()
        self.creation_tab.setLayout(QtWidgets.QVBoxLayout())
 
        # global grid
        glob_group_box = QtWidgets.QGroupBox("GLOBAL")
        object_grid_layout = QtWidgets.QGridLayout()
        self.glob_data = {}
        self.glob_data[envs.E_NAME] = QtWidgets.QLineEdit()
        self.glob_data[envs.E_NAME].addAction(ICONS.get("name"), QtWidgets.QLineEdit.LeadingPosition)
        self.glob_data[envs.E_NAME].setPlaceholderText("Object name ( No special character )")
        self.glob_data[envs.E_TYPE] = QtWidgets.QComboBox()
        self.glob_data[envs.E_TYPE].addItems(envs.TYPES)
        self.glob_data[envs.E_PARENT] = QtWidgets.QComboBox()
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
        self.obj_data[envs.E_MASS] = QtWidgets.QLineEdit()
        self.obj_data[envs.E_MASS].addAction(ICONS.get("mass"), QtWidgets.QLineEdit.LeadingPosition)
        self.obj_data[envs.E_MASS].setPlaceholderText("Object mass")
        self.obj_data[envs.E_PERIOD] = QtWidgets.QLineEdit()
        self.obj_data[envs.E_PERIOD].addAction(ICONS.get("period"), QtWidgets.QLineEdit.LeadingPosition)
        self.obj_data[envs.E_PERIOD].setPlaceholderText("Number of earth days to complete a full circle on its axis")
        self.obj_data[envs.E_INCLINATION] = QtWidgets.QLineEdit()
        self.obj_data[envs.E_INCLINATION].addAction(ICONS.get("axis"), QtWidgets.QLineEdit.LeadingPosition)
        self.obj_data[envs.E_INCLINATION].setPlaceholderText("Inclination of the object on its axis")
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
        self.orb_data[envs.O_SEMI_MAJOR_AXIS] = QtWidgets.QLineEdit()
        self.orb_data[envs.O_SEMI_MAJOR_AXIS].setPlaceholderText("Semi major axis of the orbit")
        self.orb_data[envs.O_SEMI_MAJOR_AXIS].addAction(ICONS.get("major_axis"), QtWidgets.QLineEdit.LeadingPosition)
        self.orb_data[envs.O_INCLINATION] = QtWidgets.QLineEdit()
        self.orb_data[envs.O_INCLINATION].setPlaceholderText("Inclination of the orbit")
        self.orb_data[envs.O_INCLINATION].addAction(ICONS.get("inclination"), QtWidgets.QLineEdit.LeadingPosition)
        self.orb_data[envs.O_ECCENTRICITY] = QtWidgets.QLineEdit()
        self.orb_data[envs.O_ECCENTRICITY].setPlaceholderText("Eccentricity of the orbit")
        self.orb_data[envs.O_ECCENTRICITY].addAction(ICONS.get("eccentricity"), QtWidgets.QLineEdit.LeadingPosition)
        self.orb_data[envs.O_ARG_PERIAPSIS] = QtWidgets.QLineEdit()
        self.orb_data[envs.O_ARG_PERIAPSIS].setPlaceholderText("Periapsis argument")
        self.orb_data[envs.O_ARG_PERIAPSIS].addAction(ICONS.get("arg"), QtWidgets.QLineEdit.LeadingPosition)
        self.orb_data[envs.O_ASCENDING_NODE] = QtWidgets.QLineEdit()
        self.orb_data[envs.O_ASCENDING_NODE].setPlaceholderText("Ascending node")
        self.orb_data[envs.O_ASCENDING_NODE].addAction(ICONS.get("node"), QtWidgets.QLineEdit.LeadingPosition)
        self.orb_data[envs.O_PERIHELION_DAY] = QtWidgets.QDateEdit()
        self.orb_data[envs.O_PERIHELION_DAY].setDisplayFormat("yyyy, MM, dd")
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

    def database_tab(self) ->None:
        self.db_tab = QtWidgets.QWidget()
        # tree
        self.tree = QtWidgets.QTreeWidget() 
        self.tree.setColumnCount(len(HEADERS))
        self.tree.setHeaderLabels(HEADERS)
        for i in range(len(HEADERS)):
            self.tree.header().setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
        self.tree.setRootIsDecorated(False)
        self.tree.setSortingEnabled(True)
        self.tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self._show_context_menu)
        self.tree.header().sectionsMovable()
        
        select_tab_layout = QtWidgets.QVBoxLayout()
        select_tab_layout.addWidget(self.tree)

        self.db_tab.setLayout(select_tab_layout)

    def objects_settings_tab(self) ->None:
        self.settings_tab = QtWidgets.QWidget()
        self.settings_tab.setLayout(QtWidgets.QVBoxLayout())
        
        # visualisation grid
        visu_group_box = QtWidgets.QGroupBox("COLORS")
        visu_grid_layout = QtWidgets.QGridLayout()
        self.visu_data = {}
        for typ in envs.TYPES:
            self.visu_data[typ] = QtWidgets.QLineEdit()
            self.visu_data[typ].setText(str(envs.COLORS[typ]))
        i = 1      
        for lbl,box in self.visu_data.items():
            visu_grid_layout.addWidget(QtWidgets.QLabel(lbl), i, 0)
            visu_grid_layout.addWidget(box, i, 1)
            i += 1
        visu_group_box.setLayout(visu_grid_layout)
        self.settings_tab.layout().addWidget(visu_group_box)
        
        self.settings_tab.layout().addStretch(1)

    def reload(self) ->None:
        self.reload_parents()
        self.reload_tree()

    def reload_parents(self) ->None:
        parents = [envs.ORIGIN] + [p[0] for p in self._builder.read()]
        self.glob_data[envs.E_PARENT].clear()
        self.glob_data[envs.E_PARENT].addItems(parents)

    def reload_tree(self) ->None:
        self.tree.clear()
        objects = self._builder.read()
        if not objects:
            return
  
        for data in objects or []:
            item = CustomTreeItem(data)
            self.tree.addTopLevelItem(item)

    def create_menubar(self):
        self.menu_bar = self.menuBar()

        self.presets_menu = self.menu_bar.addMenu("Presets")
        self.action = {}
        for obj in PRESETS:
            name = obj[0]
            self.action[name] = QtWidgets.QAction(name, self)
            self.presets_menu.addAction(self.action[name])
            self.action[name].triggered.connect(partial(self.on_preset_triggered, name))

        self.about_menu = self.menu_bar.addMenu("About")
        self.action["help"] = QtWidgets.QAction("Help (?)", self)
        self.action["help"].triggered.connect(self.on_help_triggered)
        self.about_menu.addAction(self.action["help"])
        self.action["about"] = QtWidgets.QAction("About me", self)
        self.action["about"].triggered.connect(self.on_about_triggered)
        self.about_menu.addAction(self.action["about"])

    def on_help_triggered(self) ->None:
        message_box = QtWidgets.QMessageBox.question(
                    self,
                    "Need help ?", 
                    f"""
        Some important conventions:\n
    * The object name should not contain any special characters apart from '/' and spaces should be replaced by '_'.
    * Decimal numbers are written as 'xxx.x', no ',' is required.
    * Powers are written as 'xxex'.
    * The parent 'Origin' means that the object rotates around the barycentre of the system represented.

        Approximations :\n
    * It is difficult to find all the data, especially that concerning physical characteristics.
    However, always enter a value in all the boxes, even if it is 0.

    * To change the colours of the types, go to the 'envs.py' file.

    Have fun ! :)
                    """,
                    QtWidgets.QMessageBox.Ok)

    def on_about_triggered(self) ->None:
        webbrowser.open(envs.ME)

    def create_connections(self) ->None:
        self.set_project_button.clicked.connect(self.on_set_project_clicked)
        self.create_button.clicked.connect(self.on_create_button_clicked)
        self.glob_data[envs.E_TYPE].currentTextChanged.connect(self.on_type_changed)

    def _show_context_menu(self, position):
        delete_action = QtWidgets.QAction("Delete")
        delete_action.triggered.connect(self.on_delete_triggered)
        modify_action = QtWidgets.QAction("Modify")
        modify_action.triggered.connect(self.on_modified_triggered)
        menu = QtWidgets.QMenu(self)
        menu.addAction(delete_action)
        menu.addAction(modify_action)
        menu.exec_(self.mapToGlobal(position))

    def on_delete_triggered(self) ->None:
        name = self.tree.currentItem()._name
        self._builder.delete_element(name)
        self.reload()

    def on_modified_triggered(self) ->None:
        data = self.tree.currentItem()._data
        # set to creation tab
        self.tab_widget.setCurrentIndex(self.tab_create_idx)

        # fill fields
        self.glob_data[envs.E_NAME].setText(data[0])
        self.glob_data[envs.E_TYPE].setItemText(0, data[1])
        self.glob_data[envs.E_PARENT].setItemText(0, data[2])
        self.obj_data[envs.E_MASS].setText(str(data[3]))
        self.obj_data[envs.E_PERIOD].setText(str(data[4]))
        self.obj_data[envs.E_INCLINATION].setText(str(data[5]))
        self.orb_data[envs.O_SEMI_MAJOR_AXIS].setText(str(data[6]))
        self.orb_data[envs.O_INCLINATION].setText(str(data[7]))
        self.orb_data[envs.O_ECCENTRICITY].setText(str(data[8]))
        self.orb_data[envs.O_ASCENDING_NODE].setText(str(data[9]))
        self.orb_data[envs.O_ARG_PERIAPSIS].setText(str(data[10]))
        date = eval(data[11])
        q_date = QtCore.QDate(int(date[0]),
                                int(date[1]),
                                int(date[2]))
        self.orb_data[envs.O_PERIHELION_DAY].setDate(q_date)

    def on_type_changed(self) ->None:
        if self.glob_data[envs.E_TYPE].currentText() == envs.T_STAR:
            for wdg in list(self.orb_data.values()):
                wdg.setEnabled(False)
                self.obj_data[envs.E_PERIOD].setEnabled(False)
                self.obj_data[envs.E_INCLINATION].setEnabled(False)
        else:
            for wdg in list(self.orb_data.values()):
                wdg.setEnabled(True)
                self.obj_data[envs.E_PERIOD].setEnabled(True)
                self.obj_data[envs.E_INCLINATION].setEnabled(True)

    def read(self) ->dict:
        date = self.orb_data.get(envs.O_PERIHELION_DAY).date().toString("yyyy.MM.dd").split(".")
        date = [int(d) for d in date]
        typ = self.glob_data[envs.E_TYPE].currentText()
        if typ == envs.T_STAR:
            return [
                self.glob_data[envs.E_NAME].text(),
                typ,
                self.glob_data[envs.E_PARENT].currentText(),
                float(self.obj_data.get(envs.E_MASS).text())
            ]
        
        return [
            self.glob_data[envs.E_NAME].text(),
            typ,
            self.glob_data[envs.E_PARENT].currentText(),
            float(self.obj_data.get(envs.E_MASS).text()),
            float(self.obj_data.get(envs.E_PERIOD).text()),
            float(self.obj_data.get(envs.E_INCLINATION).text()),
            float(self.orb_data.get(envs.O_SEMI_MAJOR_AXIS).text()),
            float(self.orb_data.get(envs.O_INCLINATION).text()),
            float(self.orb_data.get(envs.O_ECCENTRICITY).text()),
            float(self.orb_data.get(envs.O_ASCENDING_NODE).text()),
            float(self.orb_data.get(envs.O_ARG_PERIAPSIS).text()),
            date
        ]
    
    def on_preset_triggered(self, name) ->None:
        for preset in PRESETS:
            if preset[0] == name:
                self.glob_data[envs.E_NAME].setText(name)
                self.glob_data[envs.E_TYPE].setItemText(0, preset[1])
                self.glob_data[envs.E_PARENT].setItemText(0, preset[2])
                self.obj_data[envs.E_MASS].setText(str(preset[3]))
                self.obj_data[envs.E_PERIOD].setText(str(preset[4]))
                self.obj_data[envs.E_INCLINATION].setText(str(preset[5]))
                self.orb_data[envs.O_SEMI_MAJOR_AXIS].setText(str(preset[6]))
                self.orb_data[envs.O_INCLINATION].setText(str(preset[7]))
                self.orb_data[envs.O_ECCENTRICITY].setText(str(preset[8]))
                self.orb_data[envs.O_ASCENDING_NODE].setText(str(preset[9]))
                self.orb_data[envs.O_ARG_PERIAPSIS].setText(str(preset[10]))
                q_date = QtCore.QDate(preset[11][0],
                                      preset[11][1],
                                      preset[11][2])
                self.orb_data[envs.O_PERIHELION_DAY].setDate(q_date)
                break

    def show_color_dialog(self, typ:str):
        color = QtWidgets.QColorDialog.getColor()

        if color.isValid():
            self.visu_data[typ].setStyleSheet(f"background-color: {color.name()};")
            # add to general dict
            envs.COLORS[typ] = [color.red()/255,color.green()/255,color.blue()/255]

    def show_file_dialog(self, project_path:str):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.ReadOnly

        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self,
                                                            'Open existing file',
                                                            project_path,
                                                            "Fichiers Maya (*.ma *.mb)",
                                                            options=options)

        if file_path:
            return file_path

    def show_project_dialog(self) ->None:
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.ShowDirsOnly

        project_path = QtWidgets.QFileDialog.getExistingDirectory(self,
                                                                 "Set Project Directory",
                                                                 "",
                                                                 options=options)

        if project_path:
            return project_path
        
    def init_project(self):
            self._project_path = self.show_project_dialog()
            self.root_project_line_edit.setText(self._project_path)

            # init database
            self._builder = Api(self._project_path)
            self.reload()
            
            # message box
            if not STANDALONE:
                message_box = QtWidgets.QMessageBox.question(
                    self,
                    "Open existing file ?", 
                    f"Open existing file ?",
                    QtWidgets.QMessageBox.Yes | 
                    QtWidgets.QMessageBox.No)
                if message_box == QtWidgets.QMessageBox.No:
                    # build all in new scene
                    self._builder.build_all()
                else:
                    # only open existing scene
                    file = self.show_file_dialog(self._project_path)
                    self._builder.open_file(file)
                    self._builder.build_all(rebuild=False)

    def on_set_project_clicked(self) ->None:
        self.init_project()
        self.tab_widget.setCurrentIndex(self.tab_db_idx)

    def on_create_button_clicked(self) ->None:
        self._builder.add_element(self.read())
        message_box = QtWidgets.QMessageBox.information(
                    self,
                    "Success", 
                    f"Object created with success !",
                    QtWidgets.QMessageBox.Ok)
        self.reload()

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
            "database" : "database.svg",
            "settings" : "settings.png",
            "title_light" : "title_light.png",
            "title_dark" : "title_dark.png",
            "inclination" : "inclination.png",
            "node" : "ascending_node.png",
            "arg" : "periapsis_arg.png",
            "major_axis" : "major_axis.png",
            "eccentricity" : "eccentricity.png",
            "axis" : "axis.png",
            "date" : "date.png",
            "mass" : "mass.png",
            "name" : "name.png",
            "period" : "period.png"
        }

    def get_title(self) ->str:
        if STANDALONE:
            title = self._icons.get("title_dark")
        else:
            title = self._icons.get("title_dark")

        return os.path.join(self._root, title)
    
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