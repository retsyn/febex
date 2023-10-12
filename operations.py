"""
operations.py
Created: Wednesday, 11th October 2023 8:12:47 pm
Matthew Riche
Last Modified: Wednesday, 11th October 2023 8:12:52 pm
Modified By: Matthew Riche
"""

import maya.cmds as cmds


def build_export_content(target_geo, new_mesh=True):
    mesh = sanitize_mesh(target_geo)


def sanitize_mesh(mesh_node: str) -> str:
    """Sanitizes mesh node input.

    Args:
        mesh_node (str): Node for the geo desired.

    Raises:
        ValueError: If the node doesn't exist in the scene.
        TypeError: Node is a transform but doesn't have any shape beneath it.
        TypeError: Node has a shape node that is not a mesh.

    Returns:
        str: A usable shape node, perhaps the same one that went in.
    """    
    if cmds.objExists(mesh_node) == False:
        raise ValueError(f"{mesh_node} does not exist in the scene.")

    # If the incoming target isn't a mesh, assume it's a transform and get the shape mesh_node.
    if cmds.objectType(mesh_node) == "transform":
        mesh_node = cmds.listRelatives(mesh_node, s=True)[0]
        if mesh_node is None:
            raise TypeError(f"Given transform node {mesh_node} doesn't have a shape.")
    elif cmds.objectType(mesh_node) != "mesh":
        raise TypeError(
            f"{mesh_node} must be of type 'mesh', not {cmds.objectType(mesh_node)}"
        )

    return mesh_node
