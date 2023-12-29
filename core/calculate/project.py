import os
from qgis.PyQt.QtCore import QCoreApplication, QVariant
import json
from qgis.core import *

from ..data.data_manager import ProjectDataManager
from ..calculate.BlockView import BlockViewDialog

BLOCKS_LAYER_NAME = 'BLOCKS_LAYER'
NODES_LAYER_NAME = 'NODES_LAYER'
SEGMENTS_LAYER_NAME = 'SEGMENTS_LAYER'
LINEAR_OBSTACLES_LAYER_NAME = 'LINEAR_OBSTACLES_LAYER'
POINT_OBSTACLES_LAYER_NAME = 'POINT_OBSTACLES_LAYER'
PLUGIN_ID = 'ramales'

resources_folder = os.path.join(os.path.dirname(__file__), '../..', 'resources')

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
                ("id", QVariant.String),
                ("branch_id", QVariant.Int),
                ("branch", QVariant.String),
                ("comments", QVariant.String),
                ("down_box", QVariant.String),
                ("x", QVariant.Double),
                ("y", QVariant.Double),
                ("model", QVariant.Double),
                ("critDepth", QVariant.Double)
            ),
            SEGMENTS_LAYER_NAME:(
                ("name", QVariant.String),
                ("branch", QVariant.String),
                ("length", QVariant.Double),
                ("up_box", QVariant.String),
                ("up_gl", QVariant.Double),
                ("down_gl", QVariant.Double),
                ("pvc_diam", QVariant.Int),
                ("upBrLevel", QVariant.Double),
                ("dwnBrLevel", QVariant.Double),
                ("upDepth", QVariant.Double),
                ("dwnDepth", QVariant.Double),
                ("slopeSec", QVariant.Double),
                ("pavement", QVariant.String),
                ("obstacles", QVariant.String)
            ),
            BLOCKS_LAYER_NAME:(
                ("date", QVariant.Date),
                ("block", QVariant.String),
                ("username", QVariant.String),
                ("blockName", QVariant.String),
                ("watershed", QVariant.String),
                ("minDepth", QVariant.Double),
                ("minSlope", QVariant.Double),
                ("revision", QVariant.String),
                ("revDate", QVariant.Double),
                ("length", QVariant.Double),
                ("comments", QVariant.String)
            ),
            LINEAR_OBSTACLES_LAYER_NAME: (
                ("type", QVariant.String),
                ("comments", QVariant.String)
            ),
            POINT_OBSTACLES_LAYER_NAME: (
                ("type", QVariant.String),
                ("comments", QVariant.String)
            )}

    def getLayerFields(self, layerName):
        """ returns layer QgsFields """
        fields = QgsFields()
        attributes = (QgsField(name, type)
                      for name, type in self.layerAttributes()[layerName])
        for attribute in attributes:
            fields.append(attribute)
        return fields

    def tr(self, message, default=None):
        """Get the translation for a string using Qt translation API."""
        tranlated = QCoreApplication.translate('SanihubRamales', message)
        if default:
            if tranlated == message:
                return default

        return tranlated

    def showMessage(self, msg):
        msgTxt = self.tr(msg)
        self.iface.messageBar().pushMessage("saniHUB Ramales:", msgTxt, duration=3)

    def showError(self, msg):
        msgTxt = self.tr(msg)
        self.iface.messageBar().pushMessage("saniHUB Ramales:",
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
        # layerName = self.getValue(name)
        # if layerName:
        #     lst = self.proj.mapLayersByName(layerName)
        #     if lst:
        #         return lst[0]
        lyr = QgsProject.instance().mapLayer(name)
        if lyr:
            return lyr
        return None

    def getSegmentsLayer(self):
        """ Returns current SEGEMENTS layer """
        return self.getLayer(ProjectDataManager.get_layers_id().SEGMENTS_LAYER_ID)

    def getNodesLayer(self):
        """ Returns current NODES layer """
        return self.getLayer(ProjectDataManager.get_layers_id().NODES_LAYER_ID)

    def getBlocksLayer(self):
        """ Returns current BLOCKS layer """
        return self.getLayer(ProjectDataManager.get_layers_id().BLOCKS_LAYER_ID)

    def getLinearObstaclesLayer(self):
        """ Returns current OBSTACLES layer """
        return self.getLayer(ProjectDataManager.get_layers_id().LINEAR_OBSTACLES_LAYER_ID)

    def getPointObstaclesLayer(self):
        """ Returns current OBSTACLES layer """
        return self.getLayer(ProjectDataManager.get_layers_id().POINT_OBSTACLES_LAYER_ID)

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
        self.disconnectSignals(NODES_LAYER_NAME)
        self.setValue(NODES_LAYER_NAME, layerName)
        self.connectNodesSignals()

    def setSegmentsLayer(self, layerName):
        """ sets SEGMENTS layer """
        self.setValue(SEGMENTS_LAYER_NAME, layerName)

    def setLinearObstaclesLayer(self, layerName):
        """ sets OBSTACLES layer """
        self.setValue(LINEAR_OBSTACLES_LAYER_NAME, layerName)

    def setPointObstaclesLayer(self, layerName):
        """ sets OBSTACLES layer """
        self.setValue(POINT_OBSTACLES_LAYER_NAME, layerName)

    def layersToJson(self):
        try:
            crs = QgsProject.instance().crs()
            WGS84 = QgsCoordinateReferenceSystem(4326)
            transform = QgsCoordinateTransform(crs, WGS84, QgsProject.instance())

            #blocks
            featureList = []
            blocks = self.getBlocksLayer()
            for f in blocks.getFeatures():
                g = f.geometry()
                g.transform(transform)
                f.setGeometry(g)
                featureList.append(f)
            
            exporter = QgsJsonExporter(blocks)
            blocks_geojson = exporter.exportFeatures(blocks.getFeatures())

            #nodes
            featureList = []
            nodes = self.getNodesLayer()
            for f in nodes.getFeatures():
                g = f.geometry()
                g.transform(transform)
                f.setGeometry(g)
                featureList.append(f)  

            exporter = QgsJsonExporter(nodes) 
            nodes_geojson = exporter.exportFeatures(nodes.getFeatures())
            
            #obstacles
            featureList = []
            liner_obstacles = self.getLinearObstaclesLayer()
            for f in liner_obstacles.getFeatures():
                g = f.geometry()
                g.transform(transform)
                f.setGeometry(g)
                featureList.append(f)
            exporter_l = QgsJsonExporter(liner_obstacles)
            linear_obstacles_geojson = exporter_l.exportFeatures(liner_obstacles.getFeatures())

            points_obstacles = self.getPointObstaclesLayer()
            for f in points_obstacles.getFeatures():
                g = f.geometry()
                g.transform(transform)
                f.setGeometry(g)
                featureList.append(f)
            exporter_p = QgsJsonExporter(points_obstacles)
            points_obstacles_geojson = exporter_p.exportFeatures(points_obstacles.getFeatures())

            return {
                'blocks': json.loads(blocks_geojson),
                'nodes': json.loads(nodes_geojson),
                'linear_obstacles': json.loads(linear_obstacles_geojson),
                'points_obstacles': json.loads(points_obstacles_geojson),
            }
          

        except Exception as e:
            return False

    def connectBlockSignals(self):
        layer = self.getBlocksLayer()
        if layer:
            form_config = layer.editFormConfig() 
            form_config.setSuppress(QgsEditFormConfig.SuppressOn) 
            layer.setEditFormConfig(form_config)
            layer.featureAdded.connect(self.handleBlocksFeatureAdded)
            layer.selectionChanged.connect(self.handleBlocksSelectionChanged)


    def connectNodesSignals(self):
        """ Adds signas callbacks to layers """
        layer = self.getNodesLayer()
        if layer:            
            layer.geometryChanged.connect(self.resetSegmentsLayer)
            layer.attributeValueChanged.connect(self.resetSegmentsLayer)


    def disconnectSignals(self, layerName):
        """ Disconnect layer signals """
        layer = self.getLayer(layerName)
        errors = []
        if (layer):
            if layer.name() == self.getValue(NODES_LAYER_NAME):
                try:
                    layer.featureAdded.disconnect(self.resetSegmentsLayer)
                except:
                    errors.append("unable to disconnect nodes featureAdded signal")

                try:
                    layer.attributeValueChanged.disconnect(self.resetSegmentsLayer)
                except:
                    errors.append("unable to disconnect nodes afterCommitChanges signal")

                try:
                    layer.geometryChanged(self.resetSegmentsLayer)
                except:
                    errors.append("unable to disconnect nodes geometryChanged signal")

            if layer.name() == self.getValue(BLOCKS_LAYER_NAME):
                try:
                    form_config = layer.editFormConfig()
                    form_config.setSuppress(QgsEditFormConfig.SuppressOff)
                    layer.setEditFormConfig(form_config)
                except TypeError:
                    errors.append("unable to SuppressOff editFormConfig")
                
                try:
                    layer.featureAdded.disconnect(self.handleBlocksFeatureAdded)
                except TypeError:
                    errors.append("unable to disconnect blocks featureAdded signal")
                    
                try:
                    layer.selectionChanged.disconnect(self.handleBlocksSelectionChanged)
                except TypeError:
                    errors.append("unable to disconnect selectionChanged signal")
        if(len(errors) > 0):
            #TODO: handle this
            #print(errors)
            pass


    def hasNodesLayer(self):
        """ Returns True/False if NODES layer is setted """
        return not self.getLayer(NODES_LAYER_NAME) is None
    
    def hasBlocksLayer(self):
        """ Returns True/False if BLOCKS layer is setted """
        return not self.getLayer(BLOCKS_LAYER_NAME) is None

    def hasSegmentsLayer(self):
        """ Returns True/False if SEGMENTS layer is setted """
        return not self.getLayer(SEGMENTS_LAYER_NAME) is None

    def hasLinearObstaclesLayer(self):
        """ Returns True/False if OBSTACLES layer is setted """
        return not self.getLayer(LINEAR_OBSTACLES_LAYER_NAME) is None

    def hasPointObstaclesLayer(self):
        """ Returns True/False if OBSTACLES layer is setted """
        return not self.getLayer(POINT_OBSTACLES_LAYER_NAME) is None

    # def createLayer(self, name, fields, type, crs, destName=None):
    #     """ Creates shapefile layer """
    #     try:
    #         path_absolute = self.proj.readPath("./")+"/layers"
    #         if not os.path.exists(path_absolute):
    #             os.makedirs(path_absolute)
    #         if destName != None:
    #             name_to_save = path_absolute + "/" + destName + ".shp"
    #         else:
    #             name_to_save = path_absolute + "/" + name + ".shp"
    #
    #         writter = QgsVectorFileWriter(name_to_save, "UTF-8", fields, type, crs, "ESRI Shapefile")
    #         del writter
    #         layer = QgsVectorLayer(name_to_save, name, "ogr")
    #         dp = layer.dataProvider()
    #         layer.commitChanges()
    #         self.proj.addMapLayer(layer)
    #
    #         return layer
    #     except:
    #         self.showError("not able to create layer")
    #         return False
    #
    #
    # def createBlocksLayer(self, name):
    #     """ Creates layer to store neighborhood areas """
    #     crs = self.iface.mapCanvas().mapSettings().destinationCrs()
    #     fields = self.getLayerFields(BLOCKS_LAYER_NAME)
    #     layer = self.createLayer(name, fields, QgsWkbTypes.Polygon, crs)
    #     return layer
    #
    # def createNodesLayer(self, name):
    #     """ Creates layer to store surveys points """
    #     crs = self.iface.mapCanvas().mapSettings().destinationCrs()
    #     fields = self.getLayerFields(NODES_LAYER_NAME)
    #     layer = self.createLayer(name, fields, QgsWkbTypes.Point, crs)
    #     return layer
    #
    # def createSegmentsLayer(self, name):
    #     """ Creates layer to store surveys points """
    #     crs = self.iface.mapCanvas().mapSettings().destinationCrs()
    #     fields = self.getLayerFields(SEGMENTS_LAYER_NAME)
    #     layer = self.createLayer(name, fields, QgsWkbTypes.LineString, crs)
    #     qmlFile = os.path.join(os.path.dirname(__file__),'..', 'resources', 'styles', 'segment.qml')
    #     layer.loadNamedStyle(qmlFile)
    #     return layer
    #
    # def createObstaclesLayer(self, name):
    #     """ Creates layer to store obstacles points from surveys """
    #     crs = self.iface.mapCanvas().mapSettings().destinationCrs()
    #     fields = self.getLayerFields(OBSTACLES_LAYER_NAME)
    #     layer = self.createLayer(name, fields, QgsWkbTypes.Point, crs)
    #     qmlFile = os.path.join(os.path.dirname(__file__),'..', 'resources', 'styles', 'obstacle.qml')
    #     layer.loadNamedStyle(qmlFile)
    #     return layer
    
    def populateNodesLayer(self, data):
        """ Truncates and insert points into NODES layer """

        layer = self.getLayer(NODES_LAYER_NAME)
        sourceCrs = QgsCoordinateReferenceSystem(4326)
        destCrs = self.iface.mapCanvas().mapSettings().destinationCrs()
        tr = QgsCoordinateTransform(sourceCrs, destCrs, QgsProject.instance())

        with edit(layer):
            #clear features
            for feature in layer.getFeatures():
                layer.deleteFeature(feature.id())
            
            feature = QgsFeature(layer.fields())
            idx = 0
            for block in data:
                for branch in block['data']:
                    for node in branch['nodes']:
                        idx = idx + 1
                        features = []
                        obstacles = []
                        if type(node.get('geo')) in [list] and len(node.get('geo')) == 2:
                            
                            #feature geometry
                            _x = node.get('geo')[1]
                            _y = node.get('geo')[0]
                            point = QgsPointXY(float(_x), float(_y))
                            projected_point = tr.transform(point)
                            geom = QgsGeometry.fromPointXY(projected_point)
                            feature.setGeometry(geom)
                            
                            #feature Attributes
                            feature.setAttribute('id', idx)
                            feature.setAttribute("block", block.get('name', ''))
                            feature.setAttribute("branch_id", branch.get('id', ''))
                            feature.setAttribute("branch", branch.get('branch_name', ''))
                            feature.setAttribute("length", node.get('length', ''))
                            feature.setAttribute("username", branch.get('username', ''))
                            feature.setAttribute("comments", node.get('observation', ''))
                            feature.setAttribute("up_box", node.get('upstream_box', ''))
                            feature.setAttribute("up_gl", node.get('upstream_gl', ''))
                            feature.setAttribute("down_gl", node.get('downstream_gl', ''))
                            feature.setAttribute("critDepth", node.get('critical_depth', 0))
                            feature.setAttribute("x", _x)
                            feature.setAttribute("y", _y)
                            for o in node.get('obstacles', []):
                                types = o.get('type', [])
                                obstacles.append(", ".join(types))
                            feature.setAttribute("obstacles", ", ".join(obstacles))
                            feature.setAttribute("down_box", node.get('downstream_box', ''))
                            feature.setAttribute("pavement", ", ".join(node.get("pavement_type", '')))
                            feature.setAttribute("metadata", 'status:{} deviceid:{} version:{}'.format(
                                branch.get('status', 'null'), 
                                branch.get('deviceid', 'null'), 
                                branch.get('version', 'null'))
                            )  

                            #in case of splice node
                            if (node['point_type'] == "end" and node.get('splice_downstream') is not None):
                                idx = idx + 1
                                splice_name = node['splice_downstream']
                                feature.setAttribute("down_box", splice_name)
                                features.append(feature) 

                                #new feature
                                splice_feature = QgsFeature(layer.fields())
                                _x = node.get('splice_geo')[1]
                                _y = node.get('splice_geo')[0]
                                splice_feature.setAttribute("id", idx)
                                splice_feature.setAttribute("splice", True)
                                splice_feature.setAttribute("block", block.get('name', ''))
                                splice_feature.setAttribute("branch_id", branch.get('id', ''))
                                splice_feature.setAttribute("branch", branch.get('branch_name', ''))
                                splice_feature.setAttribute("length", node.get('splice_extension', ''))
                                splice_feature.setAttribute("username", branch.get('username', ''))
                                splice_feature.setAttribute("up_box", splice_name)
                                splice_feature.setAttribute("x", _x)
                                splice_feature.setAttribute("y", _y)
                                
                                #geometry
                                point = QgsPointXY(float(_x), float(_y))
                                projected_point = tr.transform(point)
                                geom = QgsGeometry.fromPointXY(projected_point)
                                splice_feature.setGeometry(geom)
                                features.append(splice_feature)
                            else:
                                feature.setAttribute("down_box", node.get('downstream_box', ''))
                                features.append(feature)

                            (res, outFeats) = layer.dataProvider().addFeatures(features)
                        else:
                            print("Error: Node without geometry")
    
    def getDownstreamNode(self, down_box, nodes, block, branch):
        """ Returns node, is_valid and error_message if there is """

        results = list(filter(lambda node: (node['up_box'] == down_box and node['block'] == block and node['branch'] == branch), nodes))
        if len(results) > 0:
            node = results[0]
            return (node, (len(results) == 1), '' if len(results) == 1 else 'multiple results')
        else:
            #end of line or input error
            return (None, False, 'downstream box not found')

    def resetSegmentsLayer(self):
        """ Delete all and insert node points into SEGMENTS layer """

        layer = self.getLayer(SEGMENTS_LAYER_NAME)
        sourceCrs = QgsCoordinateReferenceSystem(4326)
        destCrs = self.iface.mapCanvas().mapSettings().destinationCrs()
        tr = QgsCoordinateTransform(sourceCrs, destCrs, QgsProject.instance())
        
        with edit(layer):
            #clear features
            for feat in layer.getFeatures():
                layer.deleteFeature(feat.id())
            new_features = []
            nodes = [i for i in self.getNodesLayer().getFeatures()]
            
            for node in nodes:
                feat = QgsFeature(layer.fields())
                start_point = node.geometry()
                branch = node['branch']
                block = node['block']
                up_box = node['up_box']
                down_box = node['down_box']
                (down_node, is_valid, error_msg) = self.getDownstreamNode(down_box, nodes, block, branch)
                if is_valid:
                    _name = "{}-{}".format(up_box, down_box)
                    end_point = down_node.geometry()
                    feat.setAttribute('name', _name)
                    feat.setAttribute('branch', branch),
                    feat.setAttribute("length", node['length'])
                    geom = QgsGeometry.fromPolylineXY([start_point.asPoint(), end_point.asPoint()])
                    feat.setGeometry(geom)
                    new_features.append(feat)
                else:
                    print("WARNING: branch {} {}-{} -> {}".format(branch, up_box, down_box, error_msg))
            (res, outFeats) = layer.dataProvider().addFeatures(new_features)

    def populateLinearObstaclesLayer(self, data):
        """ Truncate and insert points into OBSTACLES layer """

        layer = self.getLayer(LINEAR_OBSTACLES_LAYER_NAME)
        sourceCrs = QgsCoordinateReferenceSystem(4326)
        destCrs = self.iface.mapCanvas().mapSettings().destinationCrs()
        tr = QgsCoordinateTransform(sourceCrs, destCrs, QgsProject.instance())
        with edit(layer):
            # clear features
            for feat in layer.getFeatures():
                layer.deleteFeature(feat.id())

            feat = QgsFeature(layer.fields())
            for block in data:
                for branch in block['data']:
                    for node in branch['nodes']:
                        if type(node.get('geo')) in [list] and len(node.get('geo')) == 2:
                            _obs = node.get('obstacles', [])
                            for o in _obs:
                                if type(o.get('geo')) in [list] and len(o.get('geo')) == 2:
                                    _x = o.get('geo')[1]
                                    _y = o.get('geo')[0]
                                    feat.setAttribute("name", '')
                                    feat.setAttribute("type", ", ".join(o.get('type', '')))
                                    feat.setAttribute("comments", o.get('observation', ''))

                                    # geometry
                                    point = QgsPointXY(float(_x), float(_y))
                                    point = tr.transform(point)
                                    geom = QgsGeometry.fromPointXY(point)
                                    feat.setGeometry(geom)

                                    (res, outFeats) = layer.dataProvider().addFeatures([feat])
                        else:
                            print("Error: Invalid NODE, ignoring LINEAR OBSTACLES")

    def populatePointsObstaclesLayer(self, data):
        """ Truncate and insert points into OBSTACLES layer """

        layer = self.getLayer(POINT_OBSTACLES_LAYER_NAME)
        sourceCrs = QgsCoordinateReferenceSystem(4326)
        destCrs = self.iface.mapCanvas().mapSettings().destinationCrs()
        tr = QgsCoordinateTransform(sourceCrs, destCrs, QgsProject.instance())
        with edit(layer):
            # clear features
            for feat in layer.getFeatures():
                layer.deleteFeature(feat.id())

            feat = QgsFeature(layer.fields())
            for block in data:
                for branch in block['data']:
                    for node in branch['nodes']:
                        if type(node.get('geo')) in [list] and len(node.get('geo')) == 2:
                            _obs = node.get('obstacles', [])
                            for o in _obs:
                                if type(o.get('geo')) in [list] and len(o.get('geo')) == 2:
                                    _x = o.get('geo')[1]
                                    _y = o.get('geo')[0]
                                    feat.setAttribute("name", '')
                                    feat.setAttribute("type", ", ".join(o.get('type', '')))
                                    feat.setAttribute("comments", o.get('observation', ''))

                                    # geometry
                                    point = QgsPointXY(float(_x), float(_y))
                                    point = tr.transform(point)
                                    geom = QgsGeometry.fromPointXY(point)
                                    feat.setGeometry(geom)

                                    (res, outFeats) = layer.dataProvider().addFeatures([feat])
                        else:
                            print("Error: Invalid NODE, ignoring POINTS OBSTACLES")

    def handleBlocksFeatureAdded(self, fid):
        """ BLOCKS layer FeatureAdded callback """
        self.showEditForm(fid, True)
        pass
    

    def handleBlocksSelectionChanged(self, selected, deselected, clearAndSelect):
        """ BLOCKS layer SelectionChanged callback """
        fid = selected[0] if len(selected) > 0 else -1
        if fid != -1:
            self.showEditForm(fid)
        pass

    
    def showEditForm(self, fid, is_new=False):
        """ Shows Blocks Dialog for selected layer feature """
        nodes = []
        blocks = self.getBlocksLayer()
        allNodes = self.getNodesLayer().getFeatures()
        block = blocks.getFeature(fid)
        for node in allNodes:
            if block.geometry().intersects(node.geometry()):
                nodes.append(node)
        self.blockDialog.setData(is_new)
        