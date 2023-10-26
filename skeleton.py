"""
skeleton.py
Created: Tuesday, 10th October 2023 8:58:26 pm
Matthew Riche
Last Modified: Tuesday, 10th October 2023 8:58:30 pm
Modified By: Matthew Riche
"""

# Skeleton wrangling.

import maya.cmds as cmds



def find_influence_list(cluster: str) -> list:
    """Finds all the influences connected to a cluster.

    Args:
        cluster (str): Name of a skinCluster node.

    Raises:
        ValueError: If the cluster node name can't be found in the scene.
        TypeError: If the given node isn't a skinCluster.
        ValueError: If the skinCluster has no influences at all.

    Returns:
        list: List of connected influences.
    """

    if cmds.objExists(cluster) == False:
        raise ValueError(f"No cluster node called {cluster} exists in the scene.")
    elif cmds.objectType(cluster) != "skinCluster":
        raise TypeError(f"{cluster} is not of type 'skinCluster'.")

    influences = cmds.skinCluster(cluster, query=True, influence=True)

    if len(influences) == 0:
        raise ValueError(f"This skinCluster has no connected influences")

    return influences


def copy_influence_tree(top_joint: str, inf_list: str) -> list:
    """Given a list of influences to a skin, rebuilds them as best as possible.  Will try to retain
    parent structure, provided all influences in use are part of the parent structure.  If any
    influences are not used in the skin cluster, they are bypassed-- probably at no cost to the
    animation accuracy.

    Args:
        top_joint (str): Highest joint of the skeleton to copy.
        inf_list (str): List of joints that actually matter to the cluster.

    Returns:
        list: List of all duplicated influences.  They will be parented in scene, but an unordered
        list returned.
    """

    # Copy the topmost joint.
    dup_top_joint = cmds.duplicate(
        top_joint, un=False, ic=False, po=True, n=f"{top_joint}_INF"
    )[0]
    influence_tree = [dup_top_joint]

    export_group = cmds.createNode('transform', n="export_group")


    # Duplicate all influence joints.
    for source_joint in cmds.listRelatives(top_joint, ad=True, type="joint"):
        # Check if the source joint is in the list of joints to copy
        if source_joint in inf_list:
            # Duplicate the joint
            dup_joint = cmds.duplicate(
                source_joint, po=True, n=f"{source_joint}_INF", un=False, ic=False
            )[0]
            influence_tree.append(dup_joint)

            cmds.parent(dup_joint, dup_top_joint)

    # Once they are all created, we can parent them based on how they were parented before.
    for source_joint in cmds.listRelatives(top_joint, ad=True, type="joint"):
        if source_joint in inf_list:
            parent = cmds.listRelatives(source_joint, parent=True)[0]
            # Make sure a parent is actually found, and it's not already the top_joint duplicate.
            if parent is not None and parent:
                if (
                    cmds.listRelatives(f"{source_joint}_INF", parent=True)[0]
                    != f"{parent}_INF"
                ):
                    cmds.parent(f"{source_joint}_INF", f"{parent}_INF")

    cmds.parent(dup_top_joint, export_group)

    return influence_tree


def bind_exported_skeleton(old_infs: list):
    """Binds 1:1 the original influences to the new influences with parent constraints set to
    'no-flip'.

    Args:
        old_infs (list): The list of old influences.
    """    

    print("Binding new export skeleton to old skeleton...")
    for jnt in old_infs:
        pconstraint = cmds.parentConstraint(jnt, f"{jnt}_INF", mo=False)[0]
        # Make this a 'no flip' constraint.
        cmds.setAttr(f"{pconstraint}.interpType", 0)