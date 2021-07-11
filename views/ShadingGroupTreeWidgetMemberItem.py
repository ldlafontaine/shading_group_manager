from PySide2 import QtCore, QtWidgets


class ShadingGroupTreeWidgetMemberItem(QtWidgets.QTreeWidgetItem):

    def __init__(self, *args, **kwargs):
        super(ShadingGroupTreeWidgetMemberItem, self).__init__(*args, **kwargs)