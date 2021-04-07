# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'publish_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_PublishDialog(object):
    def setupUi(self, PublishDialog):
        PublishDialog.setObjectName("PublishDialog")
        PublishDialog.resize(423, 197)
        self.buttonBox = QtWidgets.QDialogButtonBox(PublishDialog)
        self.buttonBox.setGeometry(QtCore.QRect(90, 150, 301, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.usernameText = QtWidgets.QLineEdit(PublishDialog)
        self.usernameText.setGeometry(QtCore.QRect(110, 30, 281, 33))
        self.usernameText.setObjectName("usernameText")
        self.passwordText = QtWidgets.QLineEdit(PublishDialog)
        self.passwordText.setGeometry(QtCore.QRect(110, 80, 281, 33))
        self.passwordText.setObjectName("passwordText")
        self.usernameLabel = QtWidgets.QLabel(PublishDialog)
        self.usernameLabel.setGeometry(QtCore.QRect(20, 40, 60, 17))
        self.usernameLabel.setObjectName("usernameLabel")
        self.passwordLabel = QtWidgets.QLabel(PublishDialog)
        self.passwordLabel.setGeometry(QtCore.QRect(20, 90, 60, 17))
        self.passwordLabel.setObjectName("passwordLabel")

        self.retranslateUi(PublishDialog)
        self.buttonBox.accepted.connect(PublishDialog.accept)
        self.buttonBox.rejected.connect(PublishDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(PublishDialog)

    def retranslateUi(self, PublishDialog):
        _translate = QtCore.QCoreApplication.translate
        PublishDialog.setWindowTitle(_translate("PublishDialog", "Publish"))
        self.usernameLabel.setText(_translate("PublishDialog", "username"))
        self.passwordLabel.setText(_translate("PublishDialog", "password"))

