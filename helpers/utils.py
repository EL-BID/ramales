import json

from ..core.data.data_manager import ProjectDataManager
from .globals import get_language_file


def setComboItem(combo, value):
    fndIndex = combo.findText(value)
    if not fndIndex:
        combo.setCurrentIndex(0)
    else:
        combo.setCurrentIndex(fndIndex)


from qgis.PyQt.QtCore import QCoreApplication, QLocale
from qgis._core import QgsProject, QgsVectorLayer
from qgis.PyQt.QtGui import QFont
from qgis.PyQt.QtWidgets import QMessageBox
import os.path


class Utils:
    loc = QLocale()
    file = __file__

    @property
    def segments(self):
        return QgsProject.instance().mapLayer(ProjectDataManager.get_layers_id().SEGMENTS_LAYER_ID)

    def __init__(self):
        self.data_json = None
        # self.segments = QgsProject.instance().mapLayer(ProjectDataManager.get_layers_id().SEGMENTS_LAYER_ID)

    def translate(self, msg, disambiguation=None, n=-1) -> str:
        return QCoreApplication.translate(Utils.__name__, msg, disambiguation, n)

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
        btY.setText(self.translate('Sim'))
        btN = msg_box.button(QMessageBox.No)
        btN.setText(self.translate('Não'))
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

    def get_element_layer_nodes(self, node: str, name_attr: str):
        nodes_lyr = QgsProject.instance().mapLayer(ProjectDataManager.get_layers_id().NODES_LAYER_ID)
        all_nodes = nodes_lyr.getFeatures()
        for n in all_nodes:
            if n.attributes()[self.get_idx_attr(nodes_lyr, 'nodes', 'name')] == node:
                return n.attributes()[self.get_idx_attr(nodes_lyr, 'nodes', name_attr)]
        return

    def get_idx_attr(self, layer: QgsVectorLayer, name_lyr: str, name_attr: str):
        attrs = layer.fields().names()
        return attrs.index(self.get_json_attr(name_lyr, name_attr))

    def get_idx_attr_segments(self, name_attr: str):
        attrs = self.segments.fields().names()
        return attrs.index(self.get_json_attr('segments', name_attr))

    def get_json_attr(self, name_lyr: str, attribute: str):
        if self.data_json is None:
            self.__set_data_json()
        lyr = self.data_json[name_lyr][1]

        def get_key(val):
            for k, v in lyr.items():
                if v == val:
                    return k
            return

        try:
            return lyr[attribute]
        except KeyError:
            att = get_key(attribute)
            if att is not None:
                return lyr[att]
            return

    def __set_data_json(self):
        plg_dir = os.path.dirname(__file__)
        plg_dir = plg_dir.replace('helpers', 'resources' + os.sep + 'localizations' + os.sep)

        lang = ProjectDataManager.get_language_project().LANGUAGE
        lang = lang if lang != '' else get_language_file()
        file_json = open(os.path.join(plg_dir, lang + '.json'), 'r')
        self.data_json = json.load(file_json)
        file_json.close()

    def str_to_float_locale(self, value: str) -> float:
        # if QgsApplication.instance().locale() == 'pt_BR':
        if type(value) is str and len(value) > 0:
            if value[-1].isnumeric():
                return self.loc.toFloat(value)[0]
            return 0.00
        elif type(value) is float:
            return value
        elif type(value) is int:
            return float(value)
        else:
            return 0.00
