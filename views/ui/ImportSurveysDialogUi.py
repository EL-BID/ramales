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
        SurveysDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        SurveysDialog.resize(379, 281)
        SurveysDialog.setModal(True)
        self.formLayout = QtWidgets.QFormLayout(SurveysDialog)
        self.formLayout.setObjectName("formLayout")
        self.titleLabel = QtWidgets.QLabel(SurveysDialog)
        self.titleLabel.setObjectName("titleLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.titleLabel)
        self.reloadButton = QtWidgets.QPushButton(SurveysDialog)
        icon = QtGui.QIcon.fromTheme("reload")
        self.reloadButton.setIcon(icon)
        self.reloadButton.setObjectName("reloadButton")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.reloadButton)
        self.buttonBox = QtWidgets.QDialogButtonBox(SurveysDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.buttonBox)
        self.surveysTableWidget = QtWidgets.QTableWidget(SurveysDialog)
        self.surveysTableWidget.setObjectName("surveysTableWidget")
        self.surveysTableWidget.setColumnCount(2)
        self.surveysTableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.surveysTableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.surveysTableWidget.setHorizontalHeaderItem(1, item)
        self.surveysTableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.surveysTableWidget.horizontalHeader().setStretchLastSection(True)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.SpanningRole, self.surveysTableWidget)

        self.retranslateUi(SurveysDialog)
        self.buttonBox.accepted.connect(SurveysDialog.accept)
        self.buttonBox.rejected.connect(SurveysDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SurveysDialog)

    def retranslateUi(self, SurveysDialog):
        _translate = QtCore.QCoreApplication.translate
        SurveysDialog.setWindowTitle(_translate("SurveysDialog", "Importar Encuestas"))
        self.titleLabel.setText(_translate("SurveysDialog", "Seleccione el proyecto que desea importar:"))
        self.reloadButton.setText(_translate("SurveysDialog", "Recargar listado"))
        item = self.surveysTableWidget.horizontalHeaderItem(0)
        item.setText(_translate("SurveysDialog", "Projecto"))
        item = self.surveysTableWidget.horizontalHeaderItem(1)
        item.setText(_translate("SurveysDialog", "Encuesta"))

