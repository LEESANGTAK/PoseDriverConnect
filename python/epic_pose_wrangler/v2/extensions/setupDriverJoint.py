# Copyright Epic Games, Inc. All Rights Reserved.

# External
from maya import cmds

# Internal
from epic_pose_wrangler.log import LOG
from epic_pose_wrangler.v2.model import base_extension


class SetupDriverJoint(base_extension.PoseWranglerExtension):
    __category__ = "Core Extensions"

    @property
    def view(self):
        if self._view is not None:
            return self._view
        from PySide2 import QtWidgets

        self._view = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        self._view.setLayout(layout)

        button_layout = QtWidgets.QHBoxLayout()
        layout.addLayout(button_layout)

        self._driverOffsetChkbox = QtWidgets.QCheckBox('Offset')
        button_layout.addWidget(self._driverOffsetChkbox)

        setupDriverJntBtn = QtWidgets.QPushButton("Setup Driver Joint")
        button_layout.addWidget(setupDriverJntBtn)

        setupDriverJntBtn.clicked.connect(self.setupDriverJoint)

        return self._view

    def setupDriverJoint(self):
        selJnts = cmds.ls(sl=True, type='joint')
        if not selJnts:
            cmds.error('Please select a skin joint.')
            return

        cmds.undoInfo(openChunk=True, undoName='Setup driver joint')

        skinJoint = selJnts[0]
        driverJnt = cmds.duplicate(skinJoint, n='{skelJoint}_drv'.format(skelJoint=skinJoint))[0]
        if self._driverOffsetChkbox.isChecked():
            splitNames = skinJoint.rsplit('_', 1)
            driverOffsetJnt = cmds.duplicate(skinJoint, n='{prefix}Off_{suffix}_drv'.format(prefix=splitNames[0], suffix=splitNames[-1]))[0]
            cmds.parent(driverJnt, driverOffsetJnt)
        cmds.parentConstraint(driverJnt, skinJoint, mo=False)
        cmds.scaleConstraint(driverJnt, skinJoint, mo=False)

        cmds.undoInfo(closeChunk=True)
