from PyQt5.QtWidgets import QDialog
from .ui.BlockDialogUi import Ui_BlockDialog

class BlockViewDialog(QDialog, Ui_BlockDialog):

    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)

    def setData(self, block, nodes):
        print("aca habria que hacer el mapeo de los campos al dialogo")
        self.show()