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


def get_shading_group_name(shading_group):
    if type(shading_group) != om.MObject:
        raise TypeError
    dg_node_fn = om.MFnDependencyNode(shading_group)
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


def get_selection_list_from_name(name):
    """Returns an MSelectionList produced from the given string.
    This can be used to easily select groups of contiguous components."""
    selection_list = om.MSelectionList()
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
