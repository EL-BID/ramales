from PyQt5.QtWidgets import QDialog
from .ui.BlockDialogUi import Ui_BlockDialog

class BlockView(QDialog, Ui_BlockDialog):

    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)