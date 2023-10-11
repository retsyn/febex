'''
skinning.py
Created: Wednesday, 11th October 2023 2:35:54 pm
Matthew Riche
Last Modified: Wednesday, 11th October 2023 2:41:39 pm
Modified By: Matthew Riche
'''

import maya.cmds as cmds

def copy_mesh(mesh: str) -> str:
    """Duplicates the given mesh (with sanitization of input.)

    Args:
        mesh (str): String name of the mesh shape node.

    Raises:
        ValueError: If the node doesn't exist or is not unique.
        TypeError: If the given node isn't of type 'mesh'.

    Returns:
        str: Name of the duplicated mesh.
    """    

    # Sanitizing mesh argument:
    if(cmds.objExists(mesh) == False):
        raise ValueError(f"{mesh} not found in the scene or not unique.")
    if(cmds.objectType(mesh) != 'mesh'):
        raise TypeError(f"{mesh} wasn't of node type 'mesh'.  No use copying this.")

    return cmds.duplicate(mesh, n=f"{mesh}_EXP")[0]


def bind_skin(mesh: str, inf_list: list):
    """Binds an influence list to a mesh.

    Args:
        mesh (str): Mesh shape node name.
        inf_list (list): List of influences, just be joints.

    Raises:
        ValueError: If the mesh node doesn't exist or is not unique.
        TypeError: If the mesh node isn't the right type.
        ValueError: If the influence list is 0.
        TypeError: If the influence list has non-joint objects in it.
    """    
    
    # Guard against the mesh node not being found or being the right type.
    if(cmds.objExists(mesh) != False):
        raise ValueError(f"{mesh} doesn't exist or is not unique.")
    if(cmds.objectType(mesh) != 'mesh'):
        raise TypeError(f"{mesh} isn't a mesh node.  Can't bind a skin to it.")
    
    # Guard against inf list being empty or containing non-joints.
    if(len(list) == 0):
        raise ValueError(f"Influence list doesn't contain anything to bind.")
    for joint in inf_list:
        if(cmds.objectType(joint) != 'joint'):
            raise TypeError(f"{joint} is in the influences list and it's not a joint.")
    
    # Clear the selection and then select the influences.
    cmds.select(cl=True)
    cmds.select(inf_list)
    cmds.bindSkin(mesh, tsb=True, cj=False)


def copy_skinning(old_mesh: str, new_mesh: str):
    pass
