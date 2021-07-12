from PySide2 import QtCore, QtWidgets, QtGui

from views.ShadingGroupTreeWidgetSetItem import ShadingGroupTreeWidgetSetItem
from views.ShadingGroupTreeWidgetMemberItem import ShadingGroupTreeWidgetMemberItem
from models import scene


class ShadingGroupTreeWidget(QtWidgets.QTreeWidget):

    def __init__(self, parent=None):
        super(ShadingGroupTreeWidget, self).__init__(parent)

        # Set styles.
        self.setHeaderHidden(True)
        self.invisibleRootItem()

        # Set behaviours.
        self.setSelectionMode(self.ExtendedSelection)
        self.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.header().setStretchLastSection(False)

        # Create connections.
        self.itemSelectionChanged.connect(self.on_item_selection_changed)

        # Create properties.
        self.expanded_items = []
        self.selection_is_being_propagated = False
        self.callback_ids = []

        self.populate()

        scene.register_callbacks(self.callback_ids, self.refresh)

    def resize(self):
        self.header().setMinimumSectionSize(self.maximumViewportSize().width())

    def populate(self):
        shading_groups = scene.get_shading_groups()

        for shading_group in shading_groups:
            shading_group_name = scene.get_node_name(shading_group)
            shading_group_item = ShadingGroupTreeWidgetSetItem([shading_group_name])
            shading_group_item.setData(0, QtCore.Qt.UserRole, shading_group)
            self.addTopLevelItem(shading_group_item)

            if shading_group in self.expanded_items:
                shading_group_item.setExpanded(True)

            shading_group_member_strings = scene.get_shading_group_member_strings(shading_group)
            for member_name in shading_group_member_strings:
                member_selection_list = scene.get_selection_list_from_names([member_name])
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

    def remove_selection(self):
        # Get all shading groups and their members from selection.
        assignments = {}
        for item in self.selectedItems():
            if type(item) != ShadingGroupTreeWidgetMemberItem:
                continue
            parent_item = item.parent()
            shading_group = parent_item.data(0, QtCore.Qt.UserRole)

            if shading_group not in assignments:
                assignments[shading_group] = set()

            members = item.data(0, QtCore.Qt.UserRole)
            assignments[shading_group].add(members)

        # Remove selected members from shading groups.
        for key in assignments.keys():
            members = scene.merge_selection_lists(assignments[key])
            scene.remove_from_shading_group(members, key)

        self.refresh()

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
                    if scene.has_components(selection_list):
                        child_item.setSelected(True)
                        item_list.append(selection_list)
        scene.select(item_list)
        scene.update_selection()

    def expand_all(self):
        for item_index in range(self.topLevelItemCount()):
            item = self.topLevelItem(item_index)
            item.setExpanded(True)

    def collapse_all(self):
        for item_index in range(self.topLevelItemCount()):
            item = self.topLevelItem(item_index)
            item.setExpanded(False)

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
        scene.select(item_list)
        scene.update_selection()
