import os
from qgis.PyQt.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, Qt, QVariant
import shutil
import errno
from qgis.core import *
from qgis.PyQt.QtGui import QColor
from qgis.gui import QgsMessageBar

BLOCKS_LAYER_NAME = 'BLOCKS_LAYER'
NODES_LAYER_NAME = 'NODES_LAYER'
PLUGIN_ID = 'ramales'


class Project:

    def __init__(self, iface):
        self.iface = iface
        self.plugin_id = PLUGIN_ID
        self.proj = QgsProject.instance()

    def tr(self, message, default=None):
        """Get the translation for a string using Qt translation API."""
        tranlated = QCoreApplication.translate('SanibidRamales', message)
        if default:
            if tranlated == message:
                return default

        return tranlated

    def showMessage(self, msg):
        msgTxt = self.tr(msg)
        self.iface.messageBar().pushMessage("saniBID Ramales:", msgTxt, duration=3)

    def showError(self, msg):
        msgTxt = self.tr(msg)
        self.iface.messageBar().pushMessage("saniBID Ramales:",
                                            msgTxt, level=Qgis.Critical, duration=5)

    def getValue(self, key, defaultValue=None):
        entry = self.proj.readEntry(self.plugin_id, key)[0]
        if entry:
            value = entry
        else:
            value = defaultValue
        print(key, value)
        return value

    def setValue(self, key, value):
        self.proj.writeEntry(self.plugin_id, key, value)

    def getLayer(self, name):
        layerName = self.getValue(name)

        if layerName:
            lst = self.proj.mapLayersByName(layerName)
            if lst:
                return lst[0]

        return None

    def createLayer(self, name, fields, type, crs, destName=None):
        try:
            path_absolute = self.proj.readPath("./")+"/layers"
            if not os.path.exists(path_absolute):
                os.makedirs(path_absolute)
            if destName != None:
                name_to_save = path_absolute + "/" + destName + ".shp"
            else:
                name_to_save = path_absolute + "/" + name + ".shp"

            writter = QgsVectorFileWriter(
                name_to_save, "UTF-8", fields, type, crs, "ESRI Shapefile")
            layer = QgsVectorLayer(name_to_save, name, "ogr")
            dp = layer.dataProvider()
            layer.startEditing()
            dp.addAttributes(fields)
            layer.commitChanges()
            self.proj.addMapLayer(layer)
            del writter
            return layer
        except:
            self.showError("not able to create layer")
            return False

    def createBlocksLayer(self, name):
        fields = QgsFields()
        fields.append(QgsField('ID', QVariant.Int))
        fields.append(QgsField('Value', QVariant.Double))
        fields.append(QgsField('Name', QVariant.String))
        layer = self.createLayer(name, fields, QgsWkbTypes.Polygon,
                                 self.iface.mapCanvas().mapSettings().destinationCrs())
        if layer:
            self.setValue(BLOCKS_LAYER_NAME, name)

    def createNodesLayer(self, name):
        fields = QgsFields()
        fields.append(QgsField('ID', QVariant.Int))
        fields.append(QgsField('Value', QVariant.Double))
        fields.append(QgsField('Name', QVariant.String))
        layer = self.createLayer(name, fields, QgsWkbTypes.Point,
                                 self.iface.mapCanvas().mapSettings().destinationCrs())
        if layer:
            self.setValue(NODES_LAYER_NAME, name)
