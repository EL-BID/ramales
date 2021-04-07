from PyQt5.QtWidgets import QDialog
from .ui.PublishDialogUi import Ui_PublishDialog

class PublishDialog(QDialog, Ui_PublishDialog):

    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)