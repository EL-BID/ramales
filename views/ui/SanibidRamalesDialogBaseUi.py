# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sanibid_ramales_dialog_base.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SanibidRamalesDialogBase(object):
    def setupUi(self, SanibidRamalesDialogBase):
        SanibidRamalesDialogBase.setObjectName("SanibidRamalesDialogBase")
        SanibidRamalesDialogBase.resize(400, 300)
        self.button_box = QtWidgets.QDialogButtonBox(SanibidRamalesDialogBase)
        self.button_box.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.button_box.setObjectName("button_box")

        self.retranslateUi(SanibidRamalesDialogBase)
        self.button_box.accepted.connect(SanibidRamalesDialogBase.accept)
        self.button_box.rejected.connect(SanibidRamalesDialogBase.reject)
        QtCore.QMetaObject.connectSlotsByName(SanibidRamalesDialogBase)

    def retranslateUi(self, SanibidRamalesDialogBase):
        _translate = QtCore.QCoreApplication.translate
        SanibidRamalesDialogBase.setWindowTitle(_translate("SanibidRamalesDialogBase", "SanibidRamales"))

