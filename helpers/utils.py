def setComboItem(combo, value):
    fndIndex = combo.findText(value)
    if not fndIndex:
        combo.setCurrentIndex(0)
    else:
        combo.setCurrentIndex(fndIndex)


from qgis.PyQt.QtCore import QCoreApplication, QLocale
from qgis.PyQt.QtGui import QFont
from qgis.PyQt.QtWidgets import QMessageBox
import os.path


class Utils:
    loc = QLocale()
    file = __file__

    def tr(self, message):
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('SanihubRamales', message)

    def formatNum3Dec(self, valor):
        if isinstance(valor, int):
            valor = float(valor)
        return self.loc.toString(valor, 'f', 3)

    def formatNum2Dec(self, valor):
        if isinstance(valor, int):
            valor = float(valor)
        return self.loc.toString(valor, 'f', 2)

    def formatNum1Dec(self, valor):
        if isinstance(valor, int):
            valor = float(valor)
        return self.loc.toString(valor, 'f', 1)

    @staticmethod
    def formatInteger(valor):
        return str(round(valor))

    def formatBoldText(self):
        myFont = QFont()
        myFont.setBold(True)
        return myFont

    def formatItalicText(self):
        myFont = QFont()
        myFont.setItalic(True)
        return myFont

    def formatBoldItalicText(self):
        myFont = QFont()
        myFont.setBold(True)
        myFont.setItalic(True)
        return myFont

    def show_dialog(self, title, message, information):
        msgBox = QMessageBox()
        msgBox.setIcon(information)  # Question, Warning, Critical QMessageBox.Information
        msgBox.setText(message)
        msgBox.setWindowTitle(title)
        msgBox.buttonClicked.connect(self.on_click)
        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            msgBox.close()

    def on_click(self):
        pass

    def get_metadata_value(self, key):
        filename = os.path.dirname(os.path.realpath(self.file)).replace('helpers', '') + '/metadata.txt'
        with open(filename, "r", encoding='utf-8') as f:
            for line in f:
                if line.startswith(key):
                    return line.split("=")[1].strip()
        return None

    def show_dialog_question(self, title, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText(message)
        msg_box.setWindowTitle(title)
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        btY = msg_box.button(QMessageBox.Yes)
        btY.setText(self.tr('Sim'))
        btN = msg_box.button(QMessageBox.No)
        btN.setText(self.tr('Não'))
        msg_box.buttonClicked.connect(self.on_click)
        returnValue = msg_box.exec()
        if returnValue == QMessageBox.Yes:
            msg_box.close()
            return True
        elif returnValue == QMessageBox.No:
            msg_box.close()
            return False

    def get_plugin_dir(self):
        return os.path.dirname(os.path.realpath(__file__)).replace('helpers', '')
