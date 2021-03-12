# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'import_surveys_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SurveysDialog(object):
    def setupUi(self, SurveysDialog):
        SurveysDialog.setObjectName("SurveysDialog")
        SurveysDialog.resize(320, 307)
        self.formLayout = QtWidgets.QFormLayout(SurveysDialog)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(SurveysDialog)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.label)
        self.listWidget = QtWidgets.QListWidget(SurveysDialog)
        self.listWidget.setObjectName("listWidget")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.SpanningRole, self.listWidget)
        self.pushButton = QtWidgets.QPushButton(SurveysDialog)
        self.pushButton.setObjectName("pushButton")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.pushButton)
        self.buttonBox = QtWidgets.QDialogButtonBox(SurveysDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.buttonBox)

        self.retranslateUi(SurveysDialog)
        self.buttonBox.accepted.connect(SurveysDialog.accept)
        self.buttonBox.rejected.connect(SurveysDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SurveysDialog)

    def retranslateUi(self, SurveysDialog):
        _translate = QtCore.QCoreApplication.translate
        SurveysDialog.setWindowTitle(_translate("SurveysDialog", "Importar Encuestas"))
        self.label.setText(_translate("SurveysDialog", "Seleccione el proyecto que desea importar:"))
        self.pushButton.setText(_translate("SurveysDialog", "Recargar listado"))

