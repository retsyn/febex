

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
    def __init__(self, parent = maya_main_window()):
        super(Febex_Ui, self).__init__(parent)

        self.setWindowTitle("FeBeX v{}".format(globals.RIGID_VERSION))

        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self._init_ui()
        self._populate_and_edit_widgets()
        self._create_connections()

        # init the load path.
        mod_path = os.path.abspath(__file__)
        parent_path = os.path.dirname(mod_path)
        self.ctrls_path = ("{}/control_shapes/".format(parent_path))