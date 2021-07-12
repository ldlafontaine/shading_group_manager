import maya.OpenMaya as om
import maya.cmds as cmds


def get_shading_groups():
    """Traverses the scene for shading group dependency nodes."""
    shading_groups = []
    dg_node_fn = om.MFnDependencyNode()
    dg_node_iter = om.MItDependencyNodes(om.MFn.kShadingEngine)
    while not dg_node_iter.isDone():
        shading_groups.append(dg_node_iter.thisNode())
        dg_node_iter.next()
    return shading_groups


def get_node_name(node):
    if type(node) != om.MObject:
        raise TypeError
    dg_node_fn = om.MFnDependencyNode(node)
    return dg_node_fn.name()


def get_shading_group_member_strings(shading_group):
    """Returns a list of strings representing the objects and components assigned to the given shading group."""
    member_strings = []
    if type(shading_group) != om.MObject or not shading_group.hasFn(om.MFn.kShadingEngine):
        raise TypeError
    set_fn = om.MFnSet(shading_group)
    selection_list = om.MSelectionList()
    set_fn.getMembers(selection_list, False)
    selection_list_iter = om.MItSelectionList(selection_list)
    while not selection_list_iter.isDone():
        selection_strings = []
        selection_list_iter.getStrings(selection_strings)
        member_strings.extend(selection_strings)
        selection_list_iter.next()
    return member_strings


def get_selection_list_from_names(names):
    """Returns an MSelectionList produced from the given list of strings.
    This can be used to easily select groups of contiguous components."""
    selection_list = om.MSelectionList()
    for name in names:
        selection_list.add(name)
    return selection_list


def has_components(selection_list):
    if not type(selection_list) == om.MSelectionList:
        raise TypeError
    it = om.MItSelectionList(selection_list)
    while not it.isDone():
        if it.hasComponents():
            return True
        it.next()
    return False


def select(item_list):
    """Sets the current active selection to the supplied list of arguments.
    Accepts a list containing MSelectionLists and MObjects. Other types are discarded."""
    if not type(item_list) == list:
        raise TypeError
    selection_list = om.MSelectionList()
    for item in item_list:
        if type(item) == om.MSelectionList:
            selection_list.merge(item)
        elif type(item) == om.MObject:
            selection_list.add(item, True)
    om.MGlobal_setActiveSelectionList(selection_list)


def update_selection():
    """Allows the current active selection list to be seen in the outliner and viewport."""
    cmds.select(cmds.ls(sl=True), replace=True, noExpand=True)


def assign_to_shading_group(element_name, shading_group_name):
    cmds.sets(element_name, forceElement=shading_group_name, noWarnings=True)


def assign_selection_to_shading_group(shading_group):
    shading_group_name = get_node_name(shading_group)
    current_selection = om.MSelectionList()
    om.MGlobal.getActiveSelectionList(current_selection)
    selection_strings = []
    current_selection.getSelectionStrings(selection_strings)
    for selection_string in selection_strings:
        assign_to_shading_group(selection_string, shading_group_name)


def remove_from_shading_group(selection_list, shading_group):
    # Get subtracted selection list.
    members = om.MSelectionList()
    set_fn = om.MFnSet(shading_group)
    set_fn.getMembers(members, True)

    subtraction_strings = []

    selection_list_strings = []
    selection_list.getSelectionStrings(selection_list_strings)

    members_strings = []
    members.getSelectionStrings(members_strings)

    for members_string in members_strings:
        if members_string not in selection_list_strings:
            subtraction_strings.append(members_string)

    # Clear set members.
    set_fn.clear()

    # Break residual connections.
    #dg_modifier = om.MDGModifier()
    dag_set_members_plug = set_fn.findPlug("dagSetMembers", True)
    array_indices = om.MIntArray()
    dag_set_members_plug.getExistingArrayAttributeIndices(array_indices)
    for element_index in array_indices:
        child_plug = dag_set_members_plug.elementByLogicalIndex(element_index)
        if not child_plug.isConnected():
            continue
        source = child_plug.source()
        cmds.disconnectAttr(source.info(), child_plug.info())
        #dg_modifier.disconnect(source, child_plug)

    # Reconstruct set with new members.
    subtraction = get_selection_list_from_names(subtraction_strings)
    set_fn.addMembers(subtraction)


def merge_selection_lists(selection_list_set):
    if type(selection_list_set) != set:
        raise TypeError
    merged_selection_list = om.MSelectionList()
    for selection_list in selection_list_set:
        if type(selection_list) != om.MSelectionList:
            continue
        merged_selection_list.merge(selection_list)
    return merged_selection_list


def register_set_members_modified_callback(callback_ids, func, node):
    if type(node) == om.MObject and node.hasFn(om.MFn.kShadingEngine):
        set_message = om.MObjectSetMessage()
        callback_id = set_message.addSetMembersModifiedCallback(node, lambda *args: func())
        callback_ids.append(callback_id)


def register_callbacks(callback_ids, func):
    # Register callbacks for all shading groups.
    for shading_group in get_shading_groups():
        register_set_members_modified_callback(callback_ids, func, shading_group)

    # Register a callback that will watch for dependency graph changes in order to add callbacks to new shading groups.
    dg_message = om.MDGMessage()
    add_node_callback_id = dg_message.addNodeAddedCallback(
        lambda node, client_data: register_set_members_modified_callback(callback_ids, func, node))
    callback_ids.append(add_node_callback_id)

    # Register a callback to watch for deleted nodes.
    remove_node_callback_id = dg_message.addNodeRemovedCallback(lambda *args: func())
    callback_ids.append(remove_node_callback_id)


def deregister_callbacks(callback_ids):
    message = om.MMessage()
    for callback_id in callback_ids:
        message.removeCallback(callback_id)
