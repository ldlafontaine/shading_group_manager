import sys
import maya.cmds as cmds

if not cmds.commandPort(':4434', query=True):
    cmds.commandPort(name=':4434')
    
package_path = 'D:\\Productivity\\Programming\\Python\\shading_group_manager'
if package_path not in sys.path:
    sys.path.append(package_path)
