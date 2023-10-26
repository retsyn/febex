"""
skinning.py
Created: Wednesday, 11th October 2023 2:35:54 pm
Matthew Riche
Last Modified: Wednesday, 11th October 2023 2:41:39 pm
Modified By: Matthew Riche
"""

import maya.cmds as cmds

from . import skeleton
from .mesh import MeshData


def find_cluster_node(node: str) -> str:
    """Finds the skin cluster node affecting a given mesh node.

    Args:
        node (str): Name of a node of type 'mesh' in the scene.

    Raises:
        ValueError: The given node name can't find a node.
        TypeError: The given node name isn't a mesh.
        AttributeError: The given mesh doesn't have a skin cluster attached.
        ValueError: There are more than one incoming skin cluster node attached to this mesh.

    Returns:
        str: Name of the skinCluster node.
    """

    # Guard against the wrong node name or type.
    if cmds.objExists(node) == False:
        raise ValueError(f"{node} is not in the scene or is not unique.")
    elif cmds.objectType(node) != "mesh":
        raise TypeError(f"{node} was not a mesh.")

    # Find the connections of the skinCluster type.
    clusters = cmds.listConnections(
        node, source=True, destination=False, type="skinCluster"
    )

    print(f"Clusters found are: {clusters}")
    # Guard against no clusters or not enough clusters being found.
    if clusters is None:
        # The cluster might not exist, or there are nodes between it and out mesh.  Falling back to
        # the slower type of check:
        # List all nodes in the history of the mesh
        history_nodes = cmds.listHistory(node)

        # Initialize a variable to store the skin cluster node name
        skin_cluster_node = None

        # Loop through the history nodes and find the skin cluster
        for node in history_nodes:
            node_type = cmds.nodeType(node)
            if node_type == "skinCluster":
                skin_cluster_node = node
                break
        if skin_cluster_node is None:
            raise AttributeError(f"There are no skinclusters attached to {node}")
        else:
            clusters = [skin_cluster_node]
    elif len(clusters) != 1:
        raise ValueError(f"There are multiple skinclusters connected to {node}")

    return clusters[0]


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
    if cmds.objExists(mesh) == False:
        raise ValueError(f"{mesh} doesn't exist or is not unique.")
    if cmds.listRelatives(mesh, s=True) is None:
        mesh_shape = mesh
    if cmds.objectType(mesh_shape) != "mesh":
        raise TypeError(f"{mesh_shape} isn't a mesh node.  Can't bind a skin to it.")

    # Guard against inf list being empty or containing non-joints.
    if len(inf_list) == 0:
        raise ValueError(f"Influence list doesn't contain anything to bind.")
    for joint in inf_list:
        if cmds.objectType(joint) != "joint":
            raise TypeError(f"{joint} is in the influences list and it's not a joint.")

    # Clear the selection and then select the influences.
    cmds.select(cl=True)

    return cmds.skinCluster(mesh_shape, inf_list, bm=0)[0]


def copy_skinning(old_mesh: str, new_mesh: str):
    print(f"Copying {old_mesh} skin influence to {new_mesh} skin influence.")

    old_cluster = find_cluster_node(old_mesh)
    new_cluster = find_cluster_node(new_mesh)

    verts = cmds.ls(f"{old_mesh}.vtx[*]", flatten=True)
    print(
        f"Copying skin weights from {old_mesh} to {new_mesh}, this may take some time..."
    )
    inf_data = cmds.skinCluster(old_cluster, q=True, inf=True)
    total_verts = len(verts)
    current_vert = 0
    for vert in verts:
        print(f"{current_vert / total_verts}% complete.")
        dest_vert = vert.replace(".vtx", "_EXP.vtx")

        vertex_data = cmds.skinPercent(old_cluster, vert, q=True, value=True)

        for joint, weight in zip(inf_data, vertex_data):
            dest_joint = joint + "_INF"
            cmds.skinPercent(
                new_cluster, dest_vert, transformValue=(dest_joint, weight)
            )
        current_vert += 1
