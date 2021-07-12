from PySide2 import QtCore, QtWidgets, QtGui

import models.sg_funcs


class ShadingGroupSelectionDialog(QtWidgets.QDialog):

    selection_accepted = QtCore.Signal(object)

    def __init__(self, parent, receiver):
        super(ShadingGroupSelectionDialog, self).__init__(parent)

        self.setWindowTitle('Select Shading Group')

        # Create widgets.
        self.tree_widget = QtWidgets.QTreeWidget(self)
        self.btn_select = QtWidgets.QPushButton('Select')
        self.btn_close = QtWidgets.QPushButton('Close')

        # Set styles.
        self.tree_widget.setMinimumWidth(250)
        self.tree_widget.setMinimumHeight(350)
        self.tree_widget.setHeaderHidden(True)
        self.tree_widget.invisibleRootItem()
        self.tree_widget.setRootIsDecorated(False)
        self.tree_widget.setStyleSheet("QTreeView::item { padding: 2px }")

        # Set behaviours.
        self.tree_widget.setSelectionMode(self.tree_widget.SingleSelection)
        self.tree_widget.header().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.tree_widget.header().setStretchLastSection(False)

        # Create layouts.
        self.main_layout = QtWidgets.QVBoxLayout()
        self.bottom_layout = QtWidgets.QHBoxLayout()

        self.main_layout.addWidget(self.tree_widget)
        self.main_layout.addLayout(self.bottom_layout)

        self.bottom_layout.addWidget(self.btn_select)
        self.bottom_layout.addWidget(self.btn_close)

        self.setLayout(self.main_layout)

        self.tree_widget.header().setMinimumSectionSize(self.tree_widget.width() + 2)

        # Create connections.
        self.btn_select.clicked.connect(self.on_select_clicked)
        self.btn_close.clicked.connect(self.on_close_clicked)
        self.selection_accepted.connect(receiver)

        self.populate()

    def populate(self):
        shading_groups = models.sg_funcs.get_shading_groups()

        for shading_group in shading_groups:
            shading_group_name = models.sg_funcs.get_node_name(shading_group)
            shading_group_item = QtWidgets.QTreeWidgetItem([shading_group_name])
            shading_group_item.setData(0, QtCore.Qt.UserRole, shading_group)
            self.tree_widget.addTopLevelItem(shading_group_item)

    def on_select_clicked(self):
        for item in self.tree_widget.selectedItems():
            data = item.data(0, QtCore.Qt.UserRole)
            self.selection_accepted.emit(data)
            break
        self.close()

    def on_close_clicked(self):
        self.close()
