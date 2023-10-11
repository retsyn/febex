"""
skeleton.py
Created: Tuesday, 10th October 2023 8:58:26 pm
Matthew Riche
Last Modified: Tuesday, 10th October 2023 8:58:30 pm
Modified By: Matthew Riche
"""

# Skeleton wrangling.

import maya.cmds as cmds


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

    # Guard against no clusters or not enough clusters being found.
    if len(clusters) == 0:
        raise AttributeError(f"There are no skinclusters attached to {node}")
    elif len(clusters) != 1:
        raise ValueError(f"There are multiple skinclusters connected to {node}")

    return clusters[0]


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

    if(cmds.objExists(cluster) == False):
        raise ValueError(f"No cluster node called {cluster} exists in the scene.")
    elif(cmds.objectType(cluster) != 'skinCluster'):
        raise TypeError(f"{cluster} is not of type 'skinCluster'.")
    
    influences = cmds.skinCluster(cluster, query=True, influence=True)

    if(len(influences == 0)):
        raise ValueError(f"This skinCluster has no connected influences")
    
    return influences


def copy_influence_tree(top_joint: str, inf_list: str) -> list:
  
    for sourceJoint in cmds.listRelatives(top_joint, allDescendents=True, type='joint'):
        # Check if the source joint is in the list of joints to copy
        if sourceJoint in inf_list:
            # Duplicate the joint
            duplicateJoint = cmds.duplicate(sourceJoint, parentOnly=True)[0]
            
            # Get the parent of the source joint
            parentJoint = cmds.listRelatives(sourceJoint, parent=True)
            
            # If there is a parent, find the corresponding parent joint in the destination skeleton
            if parentJoint:
                parentJoint = parentJoint[0].replace(top_joint, destinationSkeleton)
            
            # If the parent joint exists in the destination skeleton, parent the duplicate joint to it
            if cmds.objExists(parentJoint):
                cmds.parent(duplicateJoint, parentJoint)
            else:
                # If the parent joint doesn't exist, parent it to the destination skeleton root joint
                cmds.parent(duplicateJoint, destinationSkeleton)

# 