from PySide2 import QtCore, QtWidgets, QtGui

from views.ShadingGroupTreeWidgetSetItem import ShadingGroupTreeWidgetSetItem
from views.ShadingGroupTreeWidgetMemberItem import ShadingGroupTreeWidgetMemberItem
import models.sg_funcs


class ShadingGroupTreeWidget(QtWidgets.QTreeWidget):

    def __init__(self, parent=None):
        super(ShadingGroupTreeWidget, self).__init__(parent)

        self.setHeaderHidden(True)
        self.setSelectionMode(self.ExtendedSelection)
        self.invisibleRootItem()

        self.itemSelectionChanged.connect(self.on_item_selection_changed)

        self.expanded_items = []
        self.selection_is_being_propagated = False

        self.populate()

    def populate(self):
        shading_groups = models.sg_funcs.get_shading_groups()

        for shading_group in shading_groups:
            shading_group_name = models.sg_funcs.get_shading_group_name(shading_group)
            shading_group_item = ShadingGroupTreeWidgetSetItem([shading_group_name])
            shading_group_item.setData(0, QtCore.Qt.UserRole, shading_group)
            self.addTopLevelItem(shading_group_item)

            if shading_group in self.expanded_items:
                shading_group_item.setExpanded(True)

            shading_group_member_strings = models.sg_funcs.get_shading_group_member_strings(shading_group)
            for member_name in shading_group_member_strings:
                member_selection_list = models.sg_funcs.get_selection_list_from_name(member_name)
                member_item = ShadingGroupTreeWidgetMemberItem([member_name])
                member_item.setData(0, QtCore.Qt.UserRole, member_selection_list)

                shading_group_item.addChild(member_item)

    def refresh(self):
        # Store which top level items are expanded in order to preserve the current layout.
        self.expanded_items = []
        for item_index in range(self.topLevelItemCount()):
            item = self.topLevelItem(item_index)
            if item.isExpanded():
                item_data = item.data(0, QtCore.Qt.UserRole)
                self.expanded_items.append(item_data)

        # Refresh view.
        self.clear()
        self.populate()

    def select_empty(self):
        self.clearSelection()
        for item_index in range(self.topLevelItemCount()):
            item = self.topLevelItem(item_index)
            if not item.childCount() > 0:
                item.setSelected(True)

    def select_components(self):
        self.clearSelection()
        item_list = []
        for item_index in range(self.topLevelItemCount()):
            item = self.topLevelItem(item_index)
            if item.childCount() > 0:
                for child_index in range(item.childCount()):
                    child_item = item.child(child_index)
                    selection_list = child_item.data(0, QtCore.Qt.UserRole)
                    if models.sg_funcs.has_components(selection_list):
                        child_item.setSelected(True)
                        item_list.append(selection_list)
        models.sg_funcs.select(item_list)
        models.sg_funcs.update_selection()

    def propagate_selection_to_children(self, item):
        self.selection_is_being_propagated = True
        selection_state = item.isSelected()
        for child_index in range(item.childCount()):
            child_item = item.child(child_index)
            child_item.setSelected(selection_state)
            if child_item.childCount() > 0:
                self.propagate_selection_to_children(child_item)
        self.selection_is_being_propagated = False

    def on_item_selection_changed(self):
        if self.selection_is_being_propagated:
            return
        selected_items = self.selectedItems()
        # Propagate selection to children.
        for item in selected_items:
            self.propagate_selection_to_children(item)
        # Select associated objects and components in Maya.
        propagated_selection = self.selectedItems()
        item_list = []
        for item in propagated_selection:
            item_list.append(item.data(0, QtCore.Qt.UserRole))
        models.sg_funcs.select(item_list)
        models.sg_funcs.update_selection()
