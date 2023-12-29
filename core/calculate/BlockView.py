import json
import os

from PyQt5.QtCore import QLocale, QVariant
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from qgis.PyQt.QtCore import QCoreApplication
from qgis._core import QgsProject, QgsApplication, QgsVectorLayer, QgsDefaultValue

from ...core.data.data_manager import ProjectDataManager
from ...gui.BlockDialogUi import Ui_BlockDialog
from ...helpers.globals import get_language_file
from ...helpers.utils import Utils

translate = QCoreApplication.translate


class BlockViewDialog(QDialog, Ui_BlockDialog):

    def __init__(self, project):
        QDialog.__init__(self)
        self.setupUi(self)
        self.proj = project
        self.current_block = None
        self.current_nodes = None
        self.current_segments = None
        self.block_id = None
        self.utils = Utils()
        self.loc = QLocale()
        self.data_json = None

        # Table headers        
        self.headers = [
            self.tr("branch"), self.tr("up_box"), self.tr("down_box"),
            self.tr("length"), self.tr("up_gl"), self.tr("down_gl"),
            self.tr("upBrLevel"), self.tr("dwnBrLevel"), self.tr("upDepth"),
            self.tr("dwnDepth"), self.tr("model"), self.tr("upRuleLvl"),
            self.tr("dwnRuleLvl"), self.tr("critDepth"), self.tr("slopeSection"),
            self.tr("pvc_diameter"), self.tr("pavement"), self.tr("obs"), self.tr("obstacles")
        ]
        self.tableWidget.setColumnCount(len(self.headers))
        self.tableWidget.setHorizontalHeaderLabels(self.headers)

        # Signals
        self.accepted.connect(self.save)
        self.tableWidget.itemChanged.connect(self.onItemChanged)
        self.minDepth.valueChanged.connect(self.depthMinChanged)
        self.minSlope.valueChanged.connect(self.slopeMinChanged)

    def tr(self, message):
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return translate('BlockViewDialog', message)

    def setData(self, is_new=False):
        block = QgsProject.instance().mapLayer(ProjectDataManager.get_layers_id().BLOCKS_LAYER_ID)
        block_fields = [field.name() for field in block.fields()]
        block_values = [f.attributes() for f in block.getFeatures()]
        block_dict = dict(zip(block_fields, block_values[0]))
        # list_block_values = list(block_dict.values())
        self.block_id = block_dict[self.__get_json_attr('blocks', 'id')]
        nodes = []
        nodes_lyr = QgsProject.instance().mapLayer(ProjectDataManager.get_layers_id().NODES_LAYER_ID)
        all_nodes = nodes_lyr.getFeatures()
        for n in all_nodes:
            nodes.append(n)
        segments_lyr = QgsProject.instance().mapLayer(ProjectDataManager.get_layers_id().SEGMENTS_LAYER_ID)
        all_segs = segments_lyr.getFeatures()
        segments = []
        for s in all_segs:
            segments.append(s)
        self.minDepth.blockSignals(True)
        self.minSlope.blockSignals(True)
        self.tableWidget.blockSignals(True)
        self.revision.setText(
            self.check(block_dict[self.__get_json_attr('blocks', 'revision')]))  # block_dict['revisao']))
        self.blockName.setText(
            self.check(block_dict[self.__get_json_attr('blocks', 'user_name')]))  # block_dict['user_name']))
        if block_dict[self.__get_json_attr('blocks', 'date')]:  # block_dict['data']:
            self.date.setDate(block_dict[self.__get_json_attr('blocks', 'date')].date())  # block_dict['data'])
        if block_dict[self.__get_json_attr('blocks', 'rev_date')]:  # block_dict['rev_data']:
            self.revisionDate.setDate(block_dict[self.__get_json_attr('blocks', 'rev_date')].date())
        self.watershed.setText(
            self.check(block_dict[self.__get_json_attr('blocks', 'watershed')]))  # block_dict['bacia']))
        if block_dict[self.__get_json_attr('blocks', 'total_length')]:  # block_dict['extensao_total']:
            self.totalLength.setValue(float(block_dict[self.__get_json_attr('blocks', 'total_length')]))
        if block_dict[self.__get_json_attr('blocks', 'min_depth')]:  # block_dict['prof_min']:
            self.minDepth.setValue(block_dict[self.__get_json_attr('blocks', 'min_depth')])
        if block_dict[self.__get_json_attr('blocks', 'min_slope')]:  # block_dict['decl_min']:
            self.minSlope.setValue(block_dict[self.__get_json_attr('blocks', 'min_slope')])
        self.observations.setPlainText(
            self.check(block_dict[self.__get_json_attr('blocks', 'comments')]))  # block_dict['comments']))
        self.os_name_le.setText(self.check(block_dict[self.__get_json_attr('blocks', 'os_name')]))
        # Add block name if is new record
        if is_new:
            _name = nodes[0]['blocks'] if len(nodes) > 0 else 'Undefined'
            self.blockName.setText(_name)

        self.current_block = block
        self.current_nodes = nodes
        self.current_segments = segments

        segsCount = len(segments)
        self.tableWidget.setRowCount(segsCount)

        # Set the table values
        totalLength = 0
        for i in range(segsCount):
            if self.check(segments[i].attributes()[1]) != '':
                totalLength = totalLength + self.__str_to_float_locale(
                    segments[i].attributes()[self.__get_idx_attr(segments_lyr, 'segments', 'length')])
            self.tableWidget.setItem(i, 0, QTableWidgetItem(self.check(
                segments[i].attributes()[self.__get_idx_attr(segments_lyr, 'segments', 'branch_id')])))  # ramal_id
            self.tableWidget.setItem(i, 1, QTableWidgetItem(self.check(
                segments[i].attributes()[
                    self.__get_idx_attr(segments_lyr, 'segments', 'up_box')])))  # node('up_box'))))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(self.check(
                segments[i].attributes()[
                    self.__get_idx_attr(segments_lyr, 'segments', 'down_box')])))  # node('cx_jusante'))))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(
                self.__float_to_str_locale(
                    segments[i].attributes()[self.__get_idx_attr(segments_lyr, 'segments', 'length')],
                    2)))  # node('length'))))
            self.tableWidget.setItem(i, 4, QTableWidgetItem(
                self.__float_to_str_locale(
                    self.get_element_layer_nodes(
                        node=segments[i].attributes()[self.__get_idx_attr(segments_lyr, 'segments', 'up_box')],
                        name_attr=self.__get_json_attr('nodes',
                                                       'q_terrain')))))  # node('up_gl')))) #cota de terreno montate
            self.tableWidget.setItem(i, 5, QTableWidgetItem(
                self.__float_to_str_locale(self.get_element_layer_nodes(
                    node=segments[i].attributes()[self.__get_idx_attr(segments_lyr, 'segments', 'down_box')],
                    name_attr=self.__get_json_attr('nodes',
                                                   'q_terrain')))))  # node('down_gl')))) # cota terreno jusanta
            self.tableWidget.setItem(i, 6, QTableWidgetItem(
                self.check(segments[i].attributes()[
                               self.__get_idx_attr(segments_lyr, 'segments', 'up_qproject')])))  # node('upBrLevel'))))
            self.tableWidget.setItem(i, 7, QTableWidgetItem(
                self.check(segments[i].attributes()[self.__get_idx_attr(segments_lyr, 'segments',
                                                                        'dwn_qproject')])))  # node('dwnBrLevel'))))
            self.tableWidget.setItem(i, 8, QTableWidgetItem(
                self.check(self.utils.formatNum2Dec(self.__str_to_float_locale(
                    self.get_element_layer_nodes(
                        node=segments[i].attributes()[self.__get_idx_attr(segments_lyr, 'segments', 'up_box')],
                        name_attr=self.__get_json_attr('nodes', 'depth')))))))  # node('upDepth'))))
            self.tableWidget.setItem(i, 9, QTableWidgetItem(
                self.check(self.utils.formatNum2Dec(self.__str_to_float_locale(
                    self.get_element_layer_nodes(
                        node=segments[i].attributes()[self.__get_idx_attr(segments_lyr, 'segments', 'down_box')],
                        name_attr=self.__get_json_attr('nodes', 'depth')))))))  # node('dwnDepth'))))
            self.tableWidget.setItem(i, 10, QTableWidgetItem(
                self.__float_to_str_locale(value=2.00, decimals=2)))  # node('gabarito'))))
            self.tableWidget.setItem(i, 11, QTableWidgetItem(
                self.check(self.get_element_layer_nodes(
                    node=segments[i].attributes()[self.__get_idx_attr(segments_lyr, 'segments', 'up_box')],
                    name_attr=self.__get_json_attr('nodes', 'q_rule')))))  # node('upRuleLvl'))))
            self.tableWidget.setItem(i, 12, QTableWidgetItem(
                self.check(self.get_element_layer_nodes(
                    node=segments[i].attributes()[self.__get_idx_attr(segments_lyr, 'segments', 'down_box')],
                    name_attr=self.__get_json_attr('nodes', 'q_rule')))))  # node('dwnRuleLvl'))))
            self.tableWidget.setItem(i, 13, QTableWidgetItem(
                self.__float_to_str_locale(self.get_element_layer_nodes(
                    node=segments[i].attributes()[self.__get_idx_attr(segments_lyr, 'segments', 'up_box')],
                    name_attr=self.__get_json_attr('nodes', 'critical_depth')), decimals=2)))  # node('prof_critica'))))
            self.tableWidget.setItem(i, 14, QTableWidgetItem(
                self.__float_to_str_locale(
                    segments[i].attributes()[self.__get_idx_attr(segments_lyr, 'segments', 'unevenness_segment')],
                    decimals=1)))  # node('slopeSec'))))
            self.tableWidget.setItem(i, 15, QTableWidgetItem(
                self.check(segments[i].attributes()[
                               self.__get_idx_attr(segments_lyr, 'segments', 'pvc_diameter')])))  # 'pvc_diam'))))
            self.tableWidget.setItem(i, 16, QTableWidgetItem(
                self.concat1(
                    self.__get_key_map_of_values(layer=segments_lyr,
                                                 idx_col=self.__get_idx_attr(segments_lyr, 'segments', 'paviment_1'),
                                                 value=segments[i].attributes()[
                                                     self.__get_idx_attr(segments_lyr, 'segments', 'paviment_1')]),
                    self.__get_key_map_of_values(layer=segments_lyr,
                                                 idx_col=self.__get_idx_attr(segments_lyr, 'segments', 'paviment_2'),
                                                 value=segments[i].attributes()[
                                                     self.__get_idx_attr(segments_lyr, 'segments',
                                                                         'paviment_2')]))))  # paviment
            self.tableWidget.setItem(i, 17, QTableWidgetItem(
                self.check(segments[i].attributes()[self.__get_idx_attr(segments_lyr, 'segments', 'comments')]).replace(
                    'NULL', '')))  # node('comments'))))
            self.tableWidget.setItem(i, 18, QTableWidgetItem(
                self.concat2(
                    self.__get_key_map_of_values(layer=segments_lyr,
                                                 idx_col=self.__get_idx_attr(segments_lyr, 'segments', 'obstacle1'),
                                                 value=segments[i].attributes()[
                                                     self.__get_idx_attr(segments_lyr, 'segments', 'obstacle1')]),
                    self.__get_key_map_of_values(layer=segments_lyr,
                                                 idx_col=self.__get_idx_attr(segments_lyr, 'segments', 'obstacle2'),
                                                 value=segments[i].attributes()[
                                                     self.__get_idx_attr(segments_lyr, 'segments', 'obstacle2')]),
                    self.__get_key_map_of_values(layer=segments_lyr,
                                                 idx_col=self.__get_idx_attr(segments_lyr, 'segments', 'obstacle3'),
                                                 value=segments[i].attributes()[
                                                     self.__get_idx_attr(segments_lyr, 'segments',
                                                                         'obstacle3')]))))  # 'obstacles'))))
        self.totalLength.setValue(round(totalLength, 2))
        # Resize of the rows and columns based on the content
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()
        # Display the table
        if self.minDepth.value() >= 0.00 and self.minSlope.value() >= 0.00:
            self.calculate()
        self.tableWidget.show()
        self.tableWidget.blockSignals(False)
        self.minDepth.blockSignals(False)
        self.minSlope.blockSignals(False)
        self.show()

    @staticmethod
    def __get_key_map_of_values(layer: QgsVectorLayer, idx_col: int, value: str) -> str:
        for dicts in layer.editorWidgetSetup(idx_col).config().values():
            for item in dicts:
                k = [k for k in item.keys()]
                v = [v for v in item.values()]
                if v[0] == value:
                    return k[0]
        return 'NULL'

    @staticmethod
    def concat1(str1, str2) -> str:
        if str(str1) != 'NULL' and str(str2) != 'NULL':
            return str(str1) + ' - ' + str(str2)
        return str(str1).replace('NULL', '')

    @staticmethod
    def concat2(str1, str2, str3) -> str:
        if str(str1) != 'NULL' and str(str2) != 'NULL' and str(str3) != 'NULL':
            return str(str1) + ' - ' + str(str2) + ' - ' + str(str3)
        elif str(str1) != 'NULL' and str(str2) != 'NULL':
            return str(str1) + ' - ' + str(str2)
        return str(str1).replace('NULL', '')

    def get_element_layer_nodes(self, node: str, name_attr: str):
        nodes_lyr = QgsProject.instance().mapLayer(ProjectDataManager.get_layers_id().NODES_LAYER_ID)
        all_nodes = nodes_lyr.getFeatures()
        for n in all_nodes:
            if n.attributes()[self.__get_idx_attr(nodes_lyr, 'nodes', 'name')] == node:
                return n.attributes()[self.__get_idx_attr(nodes_lyr, 'nodes', name_attr)]
        return

    def save(self):
        self.tableWidget.blockSignals(True)
        blocks = self.proj.getBlocksLayer()
        if not blocks.isEditable():
            blocks.startEditing()
        blocks.changeAttributeValue(
            self.block_id,
            blocks.fields().lookupField(self.__get_json_attr('blocks', 'name')),
            self.blockName.text())
        blocks.changeAttributeValue(
            self.block_id,
            blocks.fields().lookupField(self.__get_json_attr('blocks', 'date')),
            self.date.dateTime())
        blocks.changeAttributeValue(
            self.block_id,
            blocks.fields().lookupField(self.__get_json_attr('blocks', 'rev_date')),
            self.revisionDate.dateTime())
        blocks.changeAttributeValue(
            self.block_id,
            blocks.fields().lookupField(self.__get_json_attr('blocks', 'watershed')),
            self.watershed.text())
        blocks.changeAttributeValue(
            self.block_id,
            blocks.fields().lookupField(self.__get_json_attr('blocks', 'total_length')),
            self.totalLength.value())
        blocks.changeAttributeValue(
            self.block_id,
            blocks.fields().lookupField(self.__get_json_attr('blocks', 'min_depth')),
            self.minDepth.value())
        blocks.changeAttributeValue(
            self.block_id,
            blocks.fields().lookupField(self.__get_json_attr('blocks', 'min_slope')),
            self.minSlope.value())
        blocks.changeAttributeValue(
            self.block_id,
            blocks.fields().lookupField(self.__get_json_attr('blocks', 'revision')),
            self.revision.text())
        blocks.changeAttributeValue(
            self.block_id,
            blocks.fields().lookupField(self.__get_json_attr('blocks', 'comments')),
            self.observations.toPlainText())
        blocks.changeAttributeValue(
            self.block_id,
            blocks.fields().lookupField(self.__get_json_attr('blocks', 'os_name')),
            self.os_name_le.text())
        blocks.commitChanges()
        nodes = self.proj.getNodesLayer()
        if not nodes.isEditable():
            nodes.startEditing()
        default_value = QgsDefaultValue(expression='', applyOnUpdate=False)

        name_ex = nodes.defaultValueDefinition(self.__get_idx_attr(nodes, 'nodes', 'name')).expression()
        q_terrain_ex = nodes.defaultValueDefinition(self.__get_idx_attr(nodes, 'nodes', 'q_terrain')).expression()
        raster = ProjectDataManager.get_layer_raster().LAYER_RASTER
        if ProjectDataManager.get_layer_raster().LAYER_RASTER == '':
            q_terrain_ex = q_terrain_ex.replace(self.__get_raster_express(), raster)
        else:
            q_terrain_ex = q_terrain_ex.replace(ProjectDataManager.get_layer_raster().LAYER_RASTER,
                                                raster)
        nodes.setDefaultValueDefinition(self.__get_idx_attr(nodes, 'nodes', 'name'), default_value)
        nodes.setDefaultValueDefinition(self.__get_idx_attr(nodes, 'nodes', 'q_terrain'), default_value)
        box_list = []
        for node in self.current_nodes:
            row = 0
            while row < self.tableWidget.rowCount():
                if (node[self.__get_idx_attr(nodes, 'nodes', 'name')] ==
                        self.getTableValue(row, 'up_box') and
                        node[self.__get_idx_attr(nodes, 'nodes', 'name')] not in box_list):
                    nodes.changeAttributeValue(node.id(), self.__get_idx_attr(nodes, 'nodes', 'q_terrain'),
                                               self.__str_to_float_locale(self.getTableValue(row, 'up_gl')), 2)
                    nodes.changeAttributeValue(node.id(), self.__get_idx_attr(nodes, 'nodes', 'depth'),
                                               self.__str_to_float_locale(self.getTableValue(row, 'upDepth')), 2)
                    nodes.changeAttributeValue(node.id(), self.__get_idx_attr(nodes, 'nodes', 'q_rule'),
                                               self.__str_to_float_locale(self.getTableValue(row, 'upRuleLvl')), 3)
                    # nodes.changeAttributeValue(node.id(), self.__get_idx_attr(nodes, 'nodes', 'critical_depth'),
                    #                            self.__str_to_float_locale(self.getTableValue(row, 'critDepth')), 2)
                    nodes.changeAttributeValue(node.id(), self.__get_idx_attr(nodes, 'nodes', 'template'),
                                               self.__str_to_float_locale(self.getTableValue(row, 'model')), 2)
                    box_list.append(node[self.__get_idx_attr(nodes, 'nodes', 'name')])
                if (node[self.__get_idx_attr(nodes, 'nodes', 'name')] ==
                        self.getTableValue(row, 'down_box') and
                        node[self.__get_idx_attr(nodes, 'nodes', 'name')] not in box_list):
                    nodes.changeAttributeValue(node.id(), self.__get_idx_attr(nodes, 'nodes', 'q_terrain'),
                                               self.__str_to_float_locale(self.getTableValue(row, 'down_gl')), 2)
                    nodes.changeAttributeValue(node.id(), self.__get_idx_attr(nodes, 'nodes', 'depth'),
                                               self.__str_to_float_locale(self.getTableValue(row, 'dwnDepth')), 2)
                    nodes.changeAttributeValue(node.id(), self.__get_idx_attr(nodes, 'nodes', 'q_rule'),
                                               self.__str_to_float_locale(self.getTableValue(row, 'dwnRuleLvl')), 3)
                    # nodes.changeAttributeValue(node.id(), self.__get_idx_attr(nodes, 'nodes', 'critical_depth'),
                    #                            self.__str_to_float_locale(self.getTableValue(row, 'critDepth')), 2)
                    nodes.changeAttributeValue(node.id(), self.__get_idx_attr(nodes, 'nodes', 'template'),
                                               self.__str_to_float_locale(self.getTableValue(row, 'model')), 2)
                    box_list.append(node[self.__get_idx_attr(nodes, 'nodes', 'name')])
                row += 1
        nodes.commitChanges()

        default_value.setExpression(name_ex)
        default_value.setApplyOnUpdate(True)
        nodes.setDefaultValueDefinition(self.__get_idx_attr(nodes, 'nodes', 'name'), default_value)
        default_value.setExpression(q_terrain_ex)
        default_value.setApplyOnUpdate(True)
        nodes.setDefaultValueDefinition(self.__get_idx_attr(nodes, 'nodes', 'q_terrain'), default_value)
        segments = self.proj.getSegmentsLayer()
        if not segments.isEditable():
            segments.startEditing()
        row = 0
        for segment in self.current_segments:
            segments.changeAttributeValue(segment.id(), self.__get_idx_attr(segments, 'segments', 'up_qproject'),
                                          self.__str_to_float_locale(self.getTableValue(row, 'upBrLevel')))
            segments.changeAttributeValue(segment.id(), self.__get_idx_attr(segments, 'segments', 'dwn_qproject'),
                                          self.__str_to_float_locale(self.getTableValue(row, 'dwnBrLevel')))
            segments.changeAttributeValue(segment.id(), self.__get_idx_attr(segments, 'segments', 'unevenness_segment'),
                                          self.__str_to_float_locale(self.getTableValue(row, 'slopeSection')))
            row += 1
        segments.commitChanges()
        self.tableWidget.blockSignals(False)
        self.proj.showMessage('saved successfully')
        self.hide()
        ProjectDataManager.save_status_calculation(status=True)

    def check(self, var):
        if QgsApplication.instance().locale() == 'pt_BR':
            if var is None or type(var) == QVariant:
                return ''
            else:
                if str(var).find('.') != -1:
                    return str(var).replace(',', '_').replace('.', ',').replace('_', '.')
                else:
                    return str(var)
        return '' if var is None or type(var) == QVariant else str(var)

    def depthMinChanged(self, val):
        self.calculate()

    def slopeMinChanged(self, val):
        self.calculate()

    def onItemChanged(self, index):
        val = self.tableWidget.item(index.row(), index.column()).text()
        val = val if val != '' else None
        # current_branch = self.getTableValue(index.row(), 'branch')
        self.tableWidget.blockSignals(True)
        self.tableWidget.setItem(index.row(), self.getColumnIndex('upDepth'), QTableWidgetItem(val))
        self.tableWidget.blockSignals(False)
        self.calculate()

    def getTableValue(self, row, columnName):
        """ Returns value from single cell from table """
        index = self.getColumnIndex(columnName)
        item = self.tableWidget.item(row, index)
        return item.text() if item else None

    def getColumnIndex(self, columnName):
        return self.headers.index(self.tr(columnName))

    # def to_float(self, str, default=0):
    #     return float(str.replace(',', '.')) if str != '' else default

    def __str_to_float_locale(self, value: str) -> float:
        # if QgsApplication.instance().locale() == 'pt_BR':
        if type(value) is str and len(value) > 0:
            if value[-1].isnumeric():
                return self.loc.toFloat(value)[0]
            return 0.00
        elif type(value) is float:
            return value
        else:
            return 0.00

    def __float_to_str_locale(self, value: float, decimals=3):
        if type(value) is float:  # != '' and value != 'NULL':
            return self.loc.toString(value, 'd', decimals)
        return str(value)

    def __set_data_json(self):
        plg_dir = os.path.dirname(__file__)
        plg_dir = plg_dir.replace('core' + os.sep + 'calculate', 'resources' + os.sep + 'localizations' + os.sep)
        lang = ProjectDataManager.get_language_project().LANGUAGE
        lang = lang if lang != '' else get_language_file()
        file_json = open(os.path.join(plg_dir, lang + '.json'), 'r')
        self.data_json = json.load(file_json)
        file_json.close()

    def __get_json_attr(self, name_lyr: str, attribute: str):
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

    def __get_idx_attr(self, layer: QgsVectorLayer, name_lyr: str, name_attr: str):
        attrs = layer.fields().names()
        return attrs.index(self.__get_json_attr(name_lyr, name_attr))

    def __get_raster_express(self):
        if self.data_json is None:
            self.__set_data_json()
        return self.data_json['raster']

    def calculate(self, branchName=None):
        self.tableWidget.blockSignals(True)
        minDepth = self.minDepth.value()
        minSlope = self.minSlope.value()
        grouped = {
            k: [i for i in range(self.tableWidget.rowCount()) if self.getTableValue(i, "branch") == k]
            for k in [self.getTableValue(i, "branch") for i in range(self.tableWidget.rowCount())]
        }
        down_box_list = []
        for key in grouped:
            initial = grouped[key][0]
            for i in range(self.tableWidget.rowCount()):
                if self.getTableValue(i, "branch") == key:
                    length = self.__str_to_float_locale(self.getTableValue(i, "length"))
                    up_gl = self.__str_to_float_locale(self.getTableValue(i, "up_gl"))
                    down_box = self.getTableValue(i, "down_box")
                    down_gl = self.__str_to_float_locale(self.getTableValue(i, "down_gl"))
                    # model = self.to_float(self.getTableValue(i, "model"))
                    critDepth = self.__str_to_float_locale(self.getTableValue(i, "critDepth"))
                    dwnDepthPrev = 0.00 if i == initial else self.__str_to_float_locale(
                        self.getTableValue((i - 1), "dwnDepth"))
                    dwnBrLevelPrev = 0.00 if i == initial else self.__str_to_float_locale(
                        self.getTableValue((i - 1), "dwnBrLevel"))
                    if i == initial:
                        upDepth = (minDepth if minDepth > critDepth else critDepth) if down_box != '' else ''  # H21 i==0
                        upBrLevel = (up_gl - upDepth) if down_box != '' else ''  # tocheck ''  #F21 i==0
                    else:
                        upBrLevel = '' if down_box == '' else (0.00 if length == 0.00 else (
                            dwnBrLevelPrev if (dwnDepthPrev > critDepth) else (up_gl - critDepth)))
                        upDepth = (up_gl - upBrLevel) if down_box != '' else 0.00
                    dwnBrLevel = '' if down_box == '' else (0.00 if length == 0.00 else (
                        (down_gl - minDepth) if (upBrLevel - (down_gl - minDepth)) / length >= minSlope else (
                                upBrLevel - length * minSlope - 0.0005)))  # G21
                    dwnDepth = (down_gl - dwnBrLevel) if down_box != '' else ''  # I21
                    model = 2.00  # J21 = 2 ->
                    upRuleLvl = '' if down_box == '' else ('' if length == 0.00 else (model + upBrLevel))  # K21
                    dwnRuleLvl = '' if down_box == '' else ('' if length == 0.00 else (model + dwnBrLevel))  # L21
                    slopeSection = '' if down_box == '' else round((upBrLevel - dwnBrLevel) * 100.00,
                                                                   1)  # N21 slopeSection

                    self.tableWidget.setItem(i, self.getColumnIndex('upBrLevel'),
                                             QTableWidgetItem(self.__float_to_str_locale(upBrLevel)))
                    self.tableWidget.setItem(i, self.getColumnIndex('dwnBrLevel'),
                                             QTableWidgetItem(self.__float_to_str_locale(dwnBrLevel)))
                    self.tableWidget.setItem(i, self.getColumnIndex('upDepth'),
                                             QTableWidgetItem(self.__float_to_str_locale(upDepth, decimals=2)))
                    self.tableWidget.setItem(i, self.getColumnIndex('dwnDepth'),
                                             QTableWidgetItem(self.__float_to_str_locale(dwnDepth, decimals=2)))
                    self.tableWidget.setItem(i, self.getColumnIndex('model'),
                                             QTableWidgetItem(self.__float_to_str_locale(model, 2)))  # tocheck
                    self.tableWidget.setItem(i, self.getColumnIndex('upRuleLvl'),
                                             QTableWidgetItem(self.__float_to_str_locale(upRuleLvl)))
                    self.tableWidget.setItem(i, self.getColumnIndex('dwnRuleLvl'),
                                             QTableWidgetItem(self.__float_to_str_locale(dwnRuleLvl)))
                    self.tableWidget.setItem(i, self.getColumnIndex('critDepth'),
                                             QTableWidgetItem(self.__float_to_str_locale(critDepth, decimals=2)))
                    self.tableWidget.setItem(i, self.getColumnIndex('slopeSection'),
                                             QTableWidgetItem(self.__float_to_str_locale(slopeSection, decimals=1)))
                    down_box_list.append([self.tableWidget.item(i, self.getColumnIndex('down_box')).text(), dwnDepth])
        for idx, item in enumerate(down_box_list):
            count = 0
            value_depth = 0.00
            for box in down_box_list:
                if item[0] == box[0] and count == 0:
                    count += 1
                    value_depth = box[1]
                elif item[0] == box[0] and count == 1:
                    if value_depth > item[1]:
                        self.tableWidget.setItem(idx, self.getColumnIndex('dwnDepth'), QTableWidgetItem(
                            self.__float_to_str_locale(value_depth, decimals=2)))
                        for i in range(0, self.tableWidget.rowCount()):
                            if self.tableWidget.item(i, self.getColumnIndex('up_box')).text() == box[0]:
                                self.tableWidget.setItem(i, self.getColumnIndex('upDepth'), QTableWidgetItem(
                                    self.__float_to_str_locale(value_depth, decimals=2)))
                            if self.tableWidget.item(i, self.getColumnIndex('down_box')).text() == box[0]:
                                self.tableWidget.setItem(i, self.getColumnIndex('dwnDepth'), QTableWidgetItem(
                                    self.__float_to_str_locale(value_depth, decimals=2)))
                    elif value_depth < item[1]:
                        self.tableWidget.setItem(idx, self.getColumnIndex('dwnDepth'), QTableWidgetItem(
                            self.__float_to_str_locale(item[1], decimals=2)))
                        for i in range(0, self.tableWidget.rowCount()):
                            if self.tableWidget.item(i, self.getColumnIndex('up_box')).text() == box[0]:
                                self.tableWidget.setItem(i, self.getColumnIndex('upDepth'), QTableWidgetItem(
                                    self.__float_to_str_locale(item[1], decimals=2)))
                            if self.tableWidget.item(i, self.getColumnIndex('down_box')).text() == box[0]:
                                self.tableWidget.setItem(i, self.getColumnIndex('dwnDepth'), QTableWidgetItem(
                                    self.__float_to_str_locale(item[1], decimals=2)))
        self.tableWidget.blockSignals(False)
