from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui

from views.ShadingGroupTreeWidget import ShadingGroupTreeWidget
from views.ShadingGroupSelectionDialog import ShadingGroupSelectionDialog
from models import scene


def get_maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class ShadingGroupManagerMainDialog(QtWidgets.QDialog):

    def __init__(self, parent=get_maya_main_window()):
        super(ShadingGroupManagerMainDialog, self).__init__(parent)

        self.setWindowTitle('Shading Group Manager')

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        self.tree_view = ShadingGroupTreeWidget(self)
        self.tree_view.setMinimumWidth(300)
        self.tree_view.setMinimumHeight(350)

        self.btn_reassign = QtWidgets.QPushButton('Reassign Selection')
        self.btn_remove = QtWidgets.QPushButton('Remove Selection')
        self.btn_remove_components = QtWidgets.QPushButton('Remove Components')
        self.btn_select_all = QtWidgets.QPushButton('Select All')
        self.btn_select_none = QtWidgets.QPushButton('Select None')
        self.btn_select_empty = QtWidgets.QPushButton('Select All Empty')
        self.btn_select_components = QtWidgets.QPushButton('Select All Components')
        self.btn_expand_all = QtWidgets.QPushButton('Expand All')
        self.btn_collapse_all = QtWidgets.QPushButton('Collapse All')

        self.btn_reassign.setMinimumWidth(150)  # All buttons stretch to fit this width

        self.btn_refresh = QtWidgets.QPushButton('Refresh')
        self.btn_close = QtWidgets.QPushButton('Close')

    def create_layouts(self):
        self.main_layout = QtWidgets.QVBoxLayout()
        self.columns_layout = QtWidgets.QHBoxLayout()
        self.right_layout = QtWidgets.QVBoxLayout()
        self.bottom_layout = QtWidgets.QHBoxLayout()

        self.main_layout.addLayout(self.columns_layout)
        self.main_layout.addLayout(self.bottom_layout)

        self.columns_layout.addWidget(self.tree_view)
        self.columns_layout.addLayout(self.right_layout)

        self.right_layout.setSpacing(0)
        self.right_layout.addWidget(self.btn_reassign)
        self.right_layout.addWidget(self.btn_remove)
        self.right_layout.addSpacing(20)
        self.right_layout.addWidget(self.btn_remove_components)
        self.right_layout.addSpacing(20)
        self.right_layout.addWidget(self.btn_select_all)
        self.right_layout.addWidget(self.btn_select_none)
        self.right_layout.addWidget(self.btn_select_empty)
        self.right_layout.addWidget(self.btn_select_components)
        self.right_layout.addSpacing(20)
        self.right_layout.addWidget(self.btn_expand_all)
        self.right_layout.addWidget(self.btn_collapse_all)
        self.right_layout.addStretch()

        self.bottom_layout.addWidget(self.btn_refresh)
        self.bottom_layout.addWidget(self.btn_close)

        self.setLayout(self.main_layout)

        self.tree_view.resize()

    def create_connections(self):
        self.btn_reassign.clicked.connect(self.on_reassign_clicked)
        self.btn_remove.clicked.connect(self.on_remove_clicked)
        self.btn_select_all.clicked.connect(self.on_select_all_clicked)
        self.btn_select_none.clicked.connect(self.on_select_none_clicked)
        self.btn_select_empty.clicked.connect(self.on_select_empty_clicked)
        self.btn_select_components.clicked.connect(self.on_select_components_clicked)
        self.btn_refresh.clicked.connect(self.on_refresh_clicked)
        self.btn_close.clicked.connect(self.on_close_clicked)
        self.btn_expand_all.clicked.connect(self.on_expand_all_clicked)
        self.btn_collapse_all.clicked.connect(self.on_collapse_all_clicked)
        self.finished.connect(self.on_finished)

    def on_reassign_clicked(self):
        selection_dialog = ShadingGroupSelectionDialog(self, self.on_reassign_selection_accepted)
        selection_dialog.exec_()

    def on_reassign_selection_accepted(self, shading_group):
        scene.assign_selection_to_shading_group(shading_group)

    def on_remove_clicked(self):
        self.tree_view.remove_selection()

    def on_select_all_clicked(self):
        self.tree_view.selectAll()

    def on_select_none_clicked(self):
        self.tree_view.clearSelection()

    def on_select_empty_clicked(self):
        self.tree_view.select_empty()

    def on_select_components_clicked(self):
        self.tree_view.select_components()

    def on_expand_all_clicked(self):
        self.tree_view.expand_all()

    def on_collapse_all_clicked(self):
        self.tree_view.collapse_all()

    def on_refresh_clicked(self):
        self.tree_view.refresh()

    def on_close_clicked(self):
        self.close()

    def on_finished(self, result):
        scene.deregister_callbacks(self.tree_view.callback_ids)
