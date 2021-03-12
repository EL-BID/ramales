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
        """ Get project variable value by key """       
        entry = self.proj.readEntry(self.plugin_id, key)[0]
        if entry:
            value = entry
        else:
            value = defaultValue
        print(key, value)
        return value

    def setValue(self, key, value):
        """ Set project key->value variable """
        self.proj.writeEntry(self.plugin_id, key, value)

    def getLayer(self, name):
        """ Get Layer by name """

        layerName = self.getValue(name)
        if layerName:
            lst = self.proj.mapLayersByName(layerName)
            if lst:
                return lst[0]

        return None

    def createLayer(self, name, fields, type, crs, destName=None):
        """ Creates shapefile layer """
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
        """ Creates layer to store neighborhood areas """

        fields = QgsFields()
        fields = QgsFields()        
        attributes = (
            QgsField("date", QVariant.Date),
            QgsField("name", QVariant.String),
            QgsField("watershed", QVariant.String),
            QgsField("min_depth", QVariant.Double),
            QgsField("min_slope", QVariant.Double),
            QgsField("revision", QVariant.String),
            QgsField("rev_date", QVariant.Double),
            QgsField("length_all", QVariant.Double),
            QgsField("pvc_pipe", QVariant.Double),            
            QgsField("comments", QVariant.String)
        )

        for attribute in attributes:
            fields.append(attribute)

        layer = self.createLayer(name, fields, QgsWkbTypes.Polygon,
                                 self.iface.mapCanvas().mapSettings().destinationCrs())
        if layer:
            self.setValue(BLOCKS_LAYER_NAME, name)

    def createNodesLayer(self, name):
        """ Creates layer to store surveys points """

        fields = QgsFields()        
        attributes = (
            QgsField("id", QVariant.Int),
            QgsField("length", QVariant.Double),
            QgsField("username", QVariant.String),
            QgsField("geo_loc", QVariant.String),        
            QgsField("comments", QVariant.String),
            QgsField("up_box", QVariant.Double),
            QgsField("down_box", QVariant.Double),
            QgsField("up_gl", QVariant.Double),
            QgsField("down_gl", QVariant.Double),
            QgsField("x", QVariant.Double),
            QgsField("y", QVariant.Double),
            QgsField("metadata", QVariant.String)
        )

        for attribute in attributes:
            fields.append(attribute)
        
        layer = self.createLayer(name, fields, QgsWkbTypes.Point,
                                 self.iface.mapCanvas().mapSettings().destinationCrs())
        if layer:
            self.setValue(NODES_LAYER_NAME, name)
