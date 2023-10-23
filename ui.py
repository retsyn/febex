"""
ui.py
Created: Saturday, 21st October 2023 9:35:44 am
Matthew Riche
Last Modified: Saturday, 21st October 2023 9:51:33 am
Modified By: Matthew Riche
"""


import maya.OpenMayaUI as omui
import maya.cmds as cmds
import sys
import os
from PySide2 import QtCore, QtWidgets as qtw, QtGui, QtUiTools
from shiboken2 import wrapInstance


def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), qtw.QWidget)


class Febex_Ui(qtw.QDialog):
    def __init__(self, parent=maya_main_window()):
        """Initialize and show a UI window.

        Args:
            parent (fn, optional): Defaults to maya_main_window().
        """
        super(Febex_Ui, self).__init__(parent)

        self.setWindowTitle(f"FeBeX v{1.0}")

        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self._init_ui()
        # self._populate_and_edit_widgets()
        # self._create_connections()

        # init the load path.
        mod_path = os.path.abspath(__file__)
        parent_path = os.path.dirname(mod_path)

    def _init_ui(self):
        """Finds the path and wraps the loader."""
        mod_path = os.path.abspath(__file__)
        parent_path = os.path.dirname(mod_path)
        print('Febex path is "{}"'.format(parent_path))

        ui_file = QtCore.QFile("{}/uis/febex_main.ui".format(parent_path))
        ui_file.open(QtCore.QFile.ReadOnly)

        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(ui_file, parentWidget=self)

        self.ExportAnim_QLabel_QLabel = self.findChild(qtw.QLabel, "ExportAnim_QLabel")
        self.SelectedJoint_QLineEdit_QLineEdit = self.findChild(
            qtw.QLineEdit, "SelectedJoint_QLineEdit"
        )
        self.PopulateJoint_QPushButton_QPushButton = self.findChild(
            qtw.QPushButton, "PopulateJoint_QPushButton"
        )
        self.BakeAnim_QPushButton_QPushButton = self.findChild(
            qtw.QPushButton, "BakeAnim_QPushButton"
        )
        self.verticalLayoutWidget_QWidget = self.findChild(
            qtw.QWidget, "verticalLayoutWidget"
        )
        self.Version_QLabel_QLabel = self.findChild(qtw.QLabel, "Version_QLabel")
        self.Authorship_QLabel_QLabel = self.findChild(qtw.QLabel, "Authorship_QLabel")

        self.show()


class UiState:
    def __init__(self):
        """Hold onto the UI recent state."""
        self._selected_mesh = None
        self._selected_joint = None
        self._last_rig_path = None
        self._last_anim_path = None

    @property
    def selected_mesh(self):
        return self._selected_mesh

    @selected_mesh.setter
    def selected_mesh(self, value):
        # No error handling happens here, as these values will get sanitized elsewhere.
        self._selected_mesh = value

    @property
    def selected_joint(self):
        return self._selected_joint

    @selected_joint.setter
    def selected_joint(self, value):
        self._selected_joint = value

    @property
    def rig_path(self):
        return self._last_rig_path

    @rig_path.setter
    def rig_path(self, value):
        self._last_rig_path = value

    @property
    def anim_path(self):
        return self._last_anim_path

    @anim_path.setter
    def anim_path(self, value):
        self._last_anim_path
