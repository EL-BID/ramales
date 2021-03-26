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

resources_folder = os.path.join(os.path.dirname(__file__),'..','resources')

class Project:

    def __init__(self, iface):
        self.iface = iface
        self.plugin_id = PLUGIN_ID
        self.proj = QgsProject.instance()

    def instance(self):
        return self.proj

    def layerAttributes(self):
        return {
            NODES_LAYER_NAME:( 
                ("id", QVariant.Int),
                ("length", QVariant.Double),
                ("username", QVariant.String),
                ("geo_loc", QVariant.String),
                ("comments", QVariant.String),
                ("up_box", QVariant.Double),
                ("down_box", QVariant.Double),
                ("up_gl", QVariant.Double),
                ("down_gl", QVariant.Double),
                ("x", QVariant.Double),
                ("y", QVariant.Double),
                ("pvc_diameter", QVariant.Double),
                ("metadata", QVariant.String)
            ),
            BLOCKS_LAYER_NAME:(
                ("date", QVariant.Date),
                ("blockName", QVariant.String),
                ("watershed", QVariant.String),
                ("minDepth", QVariant.Double),
                ("minSlope", QVariant.Double),
                ("revision", QVariant.String),
                ("revDate", QVariant.Double),
                ("length", QVariant.Double),
                ("comments", QVariant.String)
            )}

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

    def getNodesLayer(self):
        return self.getLayer(NODES_LAYER_NAME)

    def getBlocksLayer(self):
        return self.getLayer(BLOCKS_LAYER_NAME)

    def hasNodesLayer(self):
        return not self.getLayer(NODES_LAYER_NAME) is None
    
    def hasBlocksLayer(self):
        return not self.getLayer(BLOCKS_LAYER_NAME) is None

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

            writter = QgsVectorFileWriter(name_to_save, "UTF-8", fields, type, crs, "ESRI Shapefile")
            del writter
            layer = QgsVectorLayer(name_to_save, name, "ogr")
            dp = layer.dataProvider()
            dp.addAttributes(fields)
            layer.commitChanges()
            self.proj.addMapLayer(layer)
            
            return layer
        except:
            self.showError("not able to create layer")
            return False

    def createBlocksLayer(self, name):
        """ Creates layer to store neighborhood areas """

        fields = QgsFields()
        attributes = (QgsField(name, type)
                      for name, type in self.layerAttributes()[BLOCKS_LAYER_NAME])
        for attribute in attributes:
            fields.append(attribute)

        layer = self.createLayer(name, fields, QgsWkbTypes.Polygon,
                                 self.iface.mapCanvas().mapSettings().destinationCrs())
        if layer:
            self.setValue(BLOCKS_LAYER_NAME, name)

    def createNodesLayer(self, name):
        """ Creates layer to store surveys points """

        fields = QgsFields()
        attributes = (QgsField(name, type)
                      for name, type in self.layerAttributes()[NODES_LAYER_NAME])

        for attribute in attributes:
            fields.append(attribute)

        layer = self.createLayer(name, fields, QgsWkbTypes.Point,
                                 self.iface.mapCanvas().mapSettings().destinationCrs())
        if layer:
            self.setValue(NODES_LAYER_NAME, name)

    def populateNodesLayer(self, data):
        layer = self.getLayer(NODES_LAYER_NAME)
        if layer:
            feat = QgsFeature(layer.fields())
            for item in data:
                feat.setAttribute('id', item['_id'])
                feat.setAttribute("length", item['length'])
                feat.setAttribute("username", item['username'])
                feat.setAttribute("geo_loc", item['geolocation'])
                feat.setAttribute("comments", item['observations'])
                feat.setAttribute("up_box", item['upstream_box'])
                feat.setAttribute("down_box", item['downstream_box'])
                feat.setAttribute("up_gl", item['upstream_gl'])
                feat.setAttribute("down_gl", item['downstream_gl'])
                feat.setAttribute("x", item['_geolocation'][1])
                feat.setAttribute("y", item['_geolocation'][0])
                feat.setAttribute("metadata", 'status:{} deviceid:{} version:{}'.format(
                    item['_status'], item['deviceid'], item['__version__']))
                # geometry
                sourceCrs = QgsCoordinateReferenceSystem(4326)
                destCrs = self.iface.mapCanvas().mapSettings().destinationCrs()
                tr = QgsCoordinateTransform(
                    sourceCrs, destCrs, QgsProject.instance())
                point = QgsPointXY(
                    float(item['_geolocation'][1]), float(item['_geolocation'][0]))
                point = tr.transform(point)
                geom = QgsGeometry.fromPointXY(point)
                feat.setGeometry(geom)

                (res, outFeats) = layer.dataProvider().addFeatures([feat])
            layer.updateExtents()
            layer.commitChanges()
