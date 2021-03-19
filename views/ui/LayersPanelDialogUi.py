# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'layers_panel_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_LayersPanelDialog(object):
    def setupUi(self, LayersPanelDialog):
        LayersPanelDialog.setObjectName("LayersPanelDialog")
        LayersPanelDialog.resize(429, 451)
        self.buttonBox = QtWidgets.QDialogButtonBox(LayersPanelDialog)
        self.buttonBox.setGeometry(QtCore.QRect(100, 380, 301, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.frame = QtWidgets.QFrame(LayersPanelDialog)
        self.frame.setGeometry(QtCore.QRect(20, 20, 381, 41))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.existingLayerRadioButton = QtWidgets.QRadioButton(self.frame)
        self.existingLayerRadioButton.setGeometry(QtCore.QRect(10, 10, 201, 23))
        self.existingLayerRadioButton.setChecked(True)
        self.existingLayerRadioButton.setObjectName("existingLayerRadioButton")
        self.newLayerRadioButton = QtWidgets.QRadioButton(self.frame)
        self.newLayerRadioButton.setGeometry(QtCore.QRect(230, 10, 141, 23))
        self.newLayerRadioButton.setObjectName("newLayerRadioButton")
        self.scrollArea = QtWidgets.QScrollArea(LayersPanelDialog)
        self.scrollArea.setGeometry(QtCore.QRect(20, 80, 381, 261))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 377, 257))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.selectLayersGroupBox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.selectLayersGroupBox.setGeometry(QtCore.QRect(9, 20, 351, 201))
        self.selectLayersGroupBox.setObjectName("selectLayersGroupBox")
        self.selectNodesLayerComboBox = QtWidgets.QComboBox(self.selectLayersGroupBox)
        self.selectNodesLayerComboBox.setGeometry(QtCore.QRect(140, 90, 201, 33))
        self.selectNodesLayerComboBox.setObjectName("selectNodesLayerComboBox")
        self.blocksLayerLabel = QtWidgets.QLabel(self.selectLayersGroupBox)
        self.blocksLayerLabel.setGeometry(QtCore.QRect(20, 50, 131, 17))
        self.blocksLayerLabel.setObjectName("blocksLayerLabel")
        self.selectBlocksLayerComboBox = QtWidgets.QComboBox(self.selectLayersGroupBox)
        self.selectBlocksLayerComboBox.setGeometry(QtCore.QRect(141, 40, 201, 33))
        self.selectBlocksLayerComboBox.setObjectName("selectBlocksLayerComboBox")
        self.nodesLayerLabel = QtWidgets.QLabel(self.selectLayersGroupBox)
        self.nodesLayerLabel.setGeometry(QtCore.QRect(20, 100, 111, 17))
        self.nodesLayerLabel.setObjectName("nodesLayerLabel")
        self.createLayersGroupBox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.createLayersGroupBox.setEnabled(True)
        self.createLayersGroupBox.setGeometry(QtCore.QRect(9, 20, 351, 131))
        self.createLayersGroupBox.setObjectName("createLayersGroupBox")
        self.blocksLayerNameEdit = QtWidgets.QLineEdit(self.createLayersGroupBox)
        self.blocksLayerNameEdit.setGeometry(QtCore.QRect(150, 42, 171, 31))
        self.blocksLayerNameEdit.setObjectName("blocksLayerNameEdit")
        self.nodesLayerNameEdit = QtWidgets.QLineEdit(self.createLayersGroupBox)
        self.nodesLayerNameEdit.setGeometry(QtCore.QRect(150, 92, 171, 31))
        self.nodesLayerNameEdit.setObjectName("nodesLayerNameEdit")
        self.blocksEditLabel = QtWidgets.QLabel(self.createLayersGroupBox)
        self.blocksEditLabel.setGeometry(QtCore.QRect(20, 50, 131, 20))
        self.blocksEditLabel.setObjectName("blocksEditLabel")
        self.nodesEditLabel = QtWidgets.QLabel(self.createLayersGroupBox)
        self.nodesEditLabel.setGeometry(QtCore.QRect(20, 100, 131, 20))
        self.nodesEditLabel.setObjectName("nodesEditLabel")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.retranslateUi(LayersPanelDialog)
        self.buttonBox.accepted.connect(LayersPanelDialog.accept)
        self.buttonBox.rejected.connect(LayersPanelDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(LayersPanelDialog)

    def retranslateUi(self, LayersPanelDialog):
        _translate = QtCore.QCoreApplication.translate
        LayersPanelDialog.setWindowTitle(_translate("LayersPanelDialog", "Ajustes"))
        self.existingLayerRadioButton.setText(_translate("LayersPanelDialog", "Seleccionar capa existente"))
        self.newLayerRadioButton.setText(_translate("LayersPanelDialog", "Crear nueva capa"))
        self.selectLayersGroupBox.setTitle(_translate("LayersPanelDialog", "Seleccionar"))
        self.blocksLayerLabel.setText(_translate("LayersPanelDialog", "Capa de Manzana"))
        self.nodesLayerLabel.setText(_translate("LayersPanelDialog", "Capa de Encuesta"))
        self.createLayersGroupBox.setTitle(_translate("LayersPanelDialog", "Crear Capa"))
        self.blocksEditLabel.setText(_translate("LayersPanelDialog", "Capa de Manzana"))
        self.nodesEditLabel.setText(_translate("LayersPanelDialog", "Capa de Encuesta"))

