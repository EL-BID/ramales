from PyQt5.QtWidgets import QDialog
from .ui.ImportSurveysDialogUi import Ui_SurveysDialog

class ImportSurveysDialog(QDialog, Ui_SurveysDialog):

    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)