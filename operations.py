"""
operations.py
Created: Wednesday, 11th October 2023 8:12:47 pm
Matthew Riche
Last Modified: Wednesday, 11th October 2023 8:12:52 pm
Modified By: Matthew Riche
"""

import maya.cmds as cmds
from . import skeleton
from . import skinning
from . mesh import MeshData

def build_export_content(target_geo: MeshData, top_joint: str, new_mesh=True):
    mesh = MeshData(target_geo)
    print(f"Mesh shape node is {mesh.mesh_node}.")

    old_cluster = skinning.find_cluster_node(mesh.mesh_node)
    print(f"Identified original skinCluster: \"{old_cluster}\"...")
    old_influences = skeleton.find_influence_list(old_cluster)
    new_influences = skeleton.copy_influence_tree(top_joint, old_influences)
    print(f"Copied new skeleton based on valid influences:\n{new_influences}")

    new_mesh = MeshData(cmds.duplicate(mesh.trans_node, n=f"{mesh.trans_node}_EXP")[0])
    cmds.parent(new_mesh.trans_node, 'export_group')
    print(f"Created new mesh: \"{new_mesh.mesh_node}\"...")
    new_cluster = skinning.bind_skin(new_mesh.mesh_node, new_influences)

    # Now copy skin weights with closest point on surface, closest-bone, closest joint, then name.
    cmds.copySkinWeights(
            ss=old_cluster, 
            ds=new_cluster, 
            sa='closestPoint', 
            ia=['closestBone', 'closestJoint', 'name']
        )
    
    skeleton.bind_exported_skeleton(old_influences)


def bake_animated_skeleton(old_influences, new_influences):

    skeleton.bind_exported_skeleton(old_influences)

    # TODO bake it!
    pass
