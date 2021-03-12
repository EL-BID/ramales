
import os
from qgis.PyQt import uic
from qgis.PyQt import QtWidgets
from .ui.LayersPanelDialogUi import Ui_LayersPanelDialog


class LayersPanelDialog(QtWidgets.QDialog, Ui_LayersPanelDialog):
    def __init__(self, parent=None):
        """Constructor."""
        super(LayersPanelDialog, self).__init__(parent)        
        self.setupUi(self)
        self.createLayersGroupBox.setVisible(False)
        self.existingLayerRadioButton.toggled.connect(self.toogleVisibleGroup)
        self.newLayerRadioButton.toggled.connect(self.toogleVisibleGroup)
    
    def toogleVisibleGroup(self, _b):
        if self.existingLayerRadioButton.isChecked():
            self.selectLayersGroupBox.setVisible(True)
            self.createLayersGroupBox.setVisible(False)
        if self.newLayerRadioButton.isChecked():
            self.createLayersGroupBox.setVisible(True)
            self.selectLayersGroupBox.setVisible(False)