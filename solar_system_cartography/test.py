import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem



app = QApplication(sys.argv)
window = QMainWindow()
treeWidget = QTreeWidget()
window.setCentralWidget(treeWidget)

# Ajoutez quelques éléments à votre QTreeWidget pour l'exemple
root = QTreeWidgetItem(treeWidget, ["Root"])
item1 = QTreeWidgetItem(root, ["Item 1"])
item2 = QTreeWidgetItem(root, ["Item 2"])
subitem1 = QTreeWidgetItem(item2, ["Subitem 1"])
subitem2 = QTreeWidgetItem(item2, ["Subitem 2"])

# Appelez la fonction pour lister les éléments
lister_elements(root)

window.show()
sys.exit(app.exec_())
