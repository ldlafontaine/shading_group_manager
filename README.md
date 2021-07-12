# shading_group_manager

Autodesk Maya is notoriously troublesome with its management of shader assignments. Certain operations will result in component assignments that can be overlooked. Maya has difficulties breaking these connections or replacing them with more appropriate ones. It can often require a very deliberate approach to avoid these problems. This utility provides a fast and easy mechanism to view and manipulate all shader assignments on a per shading group basis.

<div align=center>
<img src="url" alt="Tool Demo">
</div>

## Features

<img src="url" align="right" alt="Tool User Interface">

 - The main dialog contains an outline of all shading groups in your current scene and their members. Selecting an item in the outline will select the corresponding object or component in your scene.

- Using the various dialog options can allow the user to purge their scene of all unintended component assignments and replace them with object assignments in a couple clicks.
 
 - Events are listened for from Maya via message callbacks to always keep the contents of the outline in sync with your scene.

 - **Reassign Selection:** The current selection in the outline will be reassigned to the desired shading group, which can be picked from the modal dialog that appears when this button is pressed.
 
 - **Remove Selection:** The current selection in the outline will be disconnected from its shading group, leaving it assigned to no shader.

 - **Remove Components:** Clears the selected objects of all component assignments and applies whichever shader is assigned to the most components across the entire object.

 - **Select All Empty:** Replaces the current selection to only contain shading groups that have no objects or components assigned to them.

 - **Select All Components:** Finds all component assignments and replaces the current selection with them.