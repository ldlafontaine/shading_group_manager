from PySide2 import QtCore, QtWidgets


class ShadingGroupTreeWidgetSetItem(QtWidgets.QTreeWidgetItem):

    def __init__(self, *args, **kwargs):
        super(ShadingGroupTreeWidgetSetItem, self).__init__(*args, **kwargs)

        self.setFlags(self.flags() | QtCore.Qt.ItemIsEditable)
        self.setSizeHint(0, QtCore.QSize(20, 20))
