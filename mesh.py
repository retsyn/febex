"""
mesh.py
Created: Saturday, 14th October 2023 9:49:06 am
Matthew Riche
Last Modified: Saturday, 14th October 2023 9:49:10 am
Modified By: Matthew Riche
"""


import maya.cmds as cmds


class MeshData:
    def __init__(self, mesh: str):
        """Class for sanitizing and collecting needed data for meshes.

        Args:
            mesh (str): The name of the mesh in the scene, can be either the transform node or the
            shape node.

        Raises:
            ValueError: Given string doesn't match any node in the scene.
            TypeError: The shape node is found to be something other than mesh.
            ValueError: The transform node has no shape node.
            TypeError: The node isn't a transform or mesh.
        """
        self.mesh_node = None
        self.trans_node = None

        if cmds.objExists(mesh) == False:
            raise ValueError(f"{mesh} can't be found in scene.")

        if cmds.objectType(mesh) == "transform":
            self.trans_node = mesh
            relatives = cmds.listRelatives(mesh, s=True)
            if(relatives is None):
                raise TypeError(f"{mesh} doesn't have a shape node.")
            else:
                self.mesh_node = relatives[0]
        elif cmds.objectType(mesh) == "mesh":
            self.mesh_node = mesh
            self.trans_node = cmds.listRelatives(mesh, p=True)[0]
        else:
            raise TypeError(f"{mesh} is of type {cmds.objectType(mesh)}, not 'mesh'")


    @property
    def shape(self):
        return self.mesh_node

    @property
    def trans(self):
        return self.trans_node
