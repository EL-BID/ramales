import os
from qgis.PyQt.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, Qt, QVariant
import shutil
import errno
from qgis.core import *
from qgis.PyQt.QtGui import QColor
from qgis.gui import QgsMessageBar
from ..views.BlockView import BlockViewDialog

BLOCKS_LAYER_NAME = 'BLOCKS_LAYER'
NODES_LAYER_NAME = 'NODES_LAYER'
PLUGIN_ID = 'ramales'

resources_folder = os.path.join(os.path.dirname(__file__),'..','resources')

class Project:

    def __init__(self, iface):
        self.iface = iface
        self.plugin_id = PLUGIN_ID
        self.proj = QgsProject.instance()
        self.blockDialog = BlockViewDialog(self)

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
                ("up_box", QVariant.Int),
                ("down_box", QVariant.Int),
                ("up_gl", QVariant.Double),
                ("down_gl", QVariant.Double),
                ("x", QVariant.Double),
                ("y", QVariant.Double),
                ("pvc_diam", QVariant.Int),
                ("upBrLevel", QVariant.Double),
                ("dwnBrLevel", QVariant.Double),
                ("upDepth", QVariant.Double),
                ("dwnDepth", QVariant.Double),
                ("model", QVariant.Double),
                ("upRuleLvl", QVariant.Double),
                ("dwnRuleLvl", QVariant.Double),
                ("critDepth", QVariant.Double),
                ("slopeSec", QVariant.Double),
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

    def getLayer(self, name):
        """ Get Layer by name """
        layerName = self.getValue(name)
        if layerName:
            lst = self.proj.mapLayersByName(layerName)
            if lst:
                return lst[0]
        return None


    def getNodesLayer(self):
        """ Returns current NODES layer """
        return self.getLayer(NODES_LAYER_NAME)


    def getBlocksLayer(self):
        """ Returns current BLOCKS layer """
        return self.getLayer(BLOCKS_LAYER_NAME)


    def setValue(self, key, value):
        """ Set project key->value variable """
        self.proj.writeEntry(self.plugin_id, key, value)
    

    def setBlocksLayer(self, layerName):
        """ Sets BLOCKS layer """
        self.disconnectSignals(BLOCKS_LAYER_NAME)
        self.setValue(BLOCKS_LAYER_NAME, layerName)        
        self.connectBlockSignals()


    def setNodesLayer(self, layerName):
        """ Sets NODES layer """
        #self.disconnectSignals(NODES_LAYER_NAME)
        self.setValue(NODES_LAYER_NAME, layerName)        
        #self.connectNodesSignals()


    def connectBlockSignals(self):        
        layer = self.getBlocksLayer()
        if layer:
            print("connecting BLOCKS signals to layer: {}".format(layer.name()))
            form_config = layer.editFormConfig() 
            form_config.setSuppress(QgsEditFormConfig.SuppressOn) 
            layer.setEditFormConfig(form_config)
            layer.featureAdded.connect(self.handleBlocksFeatureAdded)            
            layer.selectionChanged.connect(self.handleBlocksSelectionChanged)


    def connectNodesSignals(self):
        """ Adds signas callbacks to layers """       
        layer = self.getNodesLayer()
        if layer:
            print("connecting NODES signals to layer: {}".format(layer.name()))
            form_config = layer.editFormConfig() 
            form_config.setSuppress(QgsEditFormConfig.SuppressOn) 
            layer.setEditFormConfig(form_config)
            layer.featureAdded.connect(self.handleNodesFeatureAdded)            
            layer.selectionChanged.connect(self.handleNodesSelectionChanged)


    def disconnectSignals(self, layerName):
        """ Disconnect layer signals """       
        layer = self.getLayer(layerName)
        if (layer):
            print("removing signals from layer: {}".format(layer.name()))
            try:
                form_config = layer.editFormConfig()
                form_config.setSuppress(QgsEditFormConfig.SuppressOff)
                layer.setEditFormConfig(form_config)
            except TypeError:
                print("unable to SuppressOff")
            
            try:                 
                layer.featureAdded.disconnect(self.handleBlocksFeatureAdded)
            except TypeError:
                print("unable to disconnect blocks featureAdded")
                
            try:
                layer.selectionChanged.disconnect(self.handleBlocksSelectionChanged)
            except TypeError:
                print("unable to disconnect selectionChanged")


    def hasNodesLayer(self):
        """ Returns True/False if NODES layer is setted """
        return not self.getLayer(NODES_LAYER_NAME) is None
    

    def hasBlocksLayer(self):
        """ Returns True/False if BLOCKS layer is setted """
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
        return layer

    def createNodesLayer(self, name):
        """ Creates layer to store surveys points """

        fields = QgsFields()
        attributes = (QgsField(name, type)
                      for name, type in self.layerAttributes()[NODES_LAYER_NAME])

        for attribute in attributes:
            fields.append(attribute)

        layer = self.createLayer(name, fields, QgsWkbTypes.Point,
                                 self.iface.mapCanvas().mapSettings().destinationCrs())
        return layer


    def populateNodesLayer(self, data):
        """ Truncates and insert points into NODES layer """

        layer = self.getLayer(NODES_LAYER_NAME)
        with edit(layer):
            #clear features
            for feat in layer.getFeatures():
                layer.deleteFeature(feat.id())
            
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
   

    def handleBlocksFeatureAdded(self, fid):
        """ BLOCKS layer FeatureAdded callback """
        self.showEditForm(fid)
        pass
    
    
    def handleBlocksSelectionChanged(self, selected, deselected, clearAndSelect):
         """ BLOCKS layer SelectionChanged callback """
        fid = selected[0] if len(selected) > 0 else -1
        if fid != -1:
            self.showEditForm(fid)
        pass                          

    
    def showEditForm(self, fid):
        """ Shows Blocks Dialog for selected layer feature """
        nodes = []
        blocks = self.getBlocksLayer()
        allNodes = self.getNodesLayer().getFeatures()
        block = blocks.getFeature(fid)
        for node in allNodes:
            if block.geometry().intersects(node.geometry()):
                nodes.append(node)        
        self.blockDialog.setData(block, nodes)