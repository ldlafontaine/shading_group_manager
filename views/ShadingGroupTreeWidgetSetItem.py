from PySide2 import QtCore, QtWidgets, QtGui


class ShadingGroupTreeWidgetSetItem(QtWidgets.QTreeWidgetItem):

    def __init__(self, *args, **kwargs):
        super(ShadingGroupTreeWidgetSetItem, self).__init__(*args, **kwargs)

        font = QtGui.QFont()
        font.setBold(True)
        self.setFont(0, font)
        self.setSizeHint(0, QtCore.QSize(18, 18))
