import decimal

from PyQt5.QtCore import QLocale, QVariant
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QDoubleSpinBox
from qgis.PyQt.QtCore import QCoreApplication
from qgis._core import QgsProject, QgsApplication, QgsVectorLayer, QgsDefaultValue, QgsFeature
from qgis.core import edit

from ...core.data.data_manager import ProjectDataManager
from ...gui.BlockDialogUi import Ui_BlockDialog
from ...helpers.utils import Utils

translate = QCoreApplication.translate


class BlockViewDialog(QDialog, Ui_BlockDialog):


    def translate(self, msg, disambiguation=None, n=-1) -> object:
        return QCoreApplication.translate(BlockViewDialog.__name__, msg, disambiguation, n)

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
            self.translate("branch"), self.translate("up_box"), self.translate("down_box"),
            self.translate("length"), self.translate("up_gl"), self.translate("down_gl"),
            self.translate("upBrLevel"), self.translate("dwnBrLevel"), self.translate("upDepth"),
            self.translate("dwnDepth"), self.translate("model"), self.translate("upRuleLvl"),
            self.translate("dwnRuleLvl"), self.translate("critDepth"), self.translate("slopeSection"),
            self.translate("pvc_diameter"), self.translate("pavement"), self.translate("Posição ramal"),
            self.translate("H Ramal"), self.translate("Tubo de Queda"), self.translate("H Tubo Queda"),
            self.translate("obs")
        ]
        self.tableWidget.setColumnCount(len(self.headers))
        self.tableWidget.setHorizontalHeaderLabels(self.headers)

        # Signals
        self.accepted.connect(self.save)
        self.tableWidget.itemChanged.connect(self.onItemChanged)
        self.minDepth.valueChanged.connect(self.depthMinChanged)
        self.minSlope.valueChanged.connect(self.slopeMinChanged)

    # def tr(self, message):
    #     # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
    #     return translate('BlockViewDialog', message)

    def setData(self, is_new=False):
        block = QgsProject.instance().mapLayer(ProjectDataManager.get_layers_id().BLOCKS_LAYER_ID)
        block_fields = [field.name() for field in block.fields()]
        block_values = [f.attributes() for f in block.getFeatures()]
        block_dict = dict(zip(block_fields, block_values[0]))
        # resume = QgsProject.instance().mapLayer(ProjectDataManager.get_layers_id().RESUME_FRAME_LAYER_ID)
        # resume_fields = [field.name() for field in resume.fields()]
        # resume_values = [f.attributes() for f in resume.getFeatures()]
        # resume_dict = dict(zip(resume_fields, resume_values))
        # list_block_values = list(block_dict.values())
        self.block_id = block_dict[self.utils.get_json_attr('blocks', 'id')]
        # v = resume_dict[self.utils.get_json_attr('resume_frame', 'id')]
        # print(v)
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
        segments = sorted(segments, key=lambda item:
        (item[self.utils.get_idx_attr(segments_lyr, 'segments', 'branch_id')],
         item[self.utils.get_idx_attr(segments_lyr, 'segments', 'segment_id')]))
        self.minDepth.blockSignals(True)
        self.minSlope.blockSignals(True)
        self.tableWidget.blockSignals(True)
        self.revision.setText(
            self.check(block_dict[self.utils.get_json_attr('blocks', 'revision')]))  # block_dict['revisao']))
        self.blockName.setText(
            self.check(block_dict[self.utils.get_json_attr('blocks', 'name')]))  # block_dict['user_name']))
        if block_dict[self.utils.get_json_attr('blocks', 'date')]:  # block_dict['data']:
            self.date.setDate(block_dict[self.utils.get_json_attr('blocks', 'date')].date())  # block_dict['data'])
        if block_dict[self.utils.get_json_attr('blocks', 'rev_date')]:  # block_dict['rev_data']:
            self.revisionDate.setDate(block_dict[self.utils.get_json_attr('blocks', 'rev_date')].date())
        self.watershed.setText(
            self.check(block_dict[self.utils.get_json_attr('blocks', 'watershed')]))  # block_dict['bacia']))
        if block_dict[self.utils.get_json_attr('blocks', 'total_length')]:  # block_dict['extensao_total']:
            self.totalLength.setValue(float(block_dict[self.utils.get_json_attr('blocks', 'total_length')]))
        if block_dict[self.utils.get_json_attr('blocks', 'min_depth')]:  # block_dict['prof_min']:
            self.minDepth.setValue(block_dict[self.utils.get_json_attr('blocks', 'min_depth')])
        if block_dict[self.utils.get_json_attr('blocks', 'min_slope')]:  # block_dict['decl_min']:
            self.minSlope.setValue(block_dict[self.utils.get_json_attr('blocks', 'min_slope')])
        self.observations.setPlainText(
            self.check(block_dict[self.utils.get_json_attr('blocks', 'comments')]))  # block_dict['comments']))
        self.os_name_le.setText(self.check(block_dict[self.utils.get_json_attr('blocks', 'os_name')]))
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
                totalLength = totalLength + self.utils.str_to_float_locale(
                    segments[i].attributes()[self.utils.get_idx_attr(segments_lyr, 'segments', 'length')])
            self.tableWidget.setItem(i, 0, QTableWidgetItem(self.check(
                segments[i].attributes()[self.utils.get_idx_attr(segments_lyr, 'segments', 'branch_id')])))  # ramal_id
            self.tableWidget.setItem(i, 1, QTableWidgetItem(self.check(
                segments[i].attributes()[
                    self.utils.get_idx_attr(segments_lyr, 'segments', 'up_box')])))  # node('up_box'))))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(self.check(
                segments[i].attributes()[
                    self.utils.get_idx_attr(segments_lyr, 'segments', 'down_box')])))  # node('cx_jusante'))))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(
                self.__float_to_str_locale(
                    segments[i].attributes()[self.utils.get_idx_attr(segments_lyr, 'segments', 'length')],
                    2)))  # node('length'))))
            self.tableWidget.setItem(i, 4, QTableWidgetItem(
                self.__float_to_str_locale(
                    self.utils.get_element_layer_nodes(
                        node=segments[i].attributes()[self.utils.get_idx_attr(segments_lyr, 'segments', 'up_box')],
                        name_attr=self.utils.get_json_attr('nodes',
                                                       'q_terrain')))))  # node('up_gl')))) #cota de terreno montate
            self.tableWidget.setItem(i, 5, QTableWidgetItem(
                self.__float_to_str_locale(self.utils.get_element_layer_nodes(
                    node=segments[i].attributes()[self.utils.get_idx_attr(segments_lyr, 'segments', 'down_box')],
                    name_attr=self.utils.get_json_attr('nodes',
                                                   'q_terrain')))))  # node('down_gl')))) # cota terreno jusanta
            self.tableWidget.setItem(i, 6, QTableWidgetItem(
                self.check(segments[i].attributes()[
                               self.utils.get_idx_attr(segments_lyr, 'segments', 'up_qproject')])))  # node('upBrLevel'))))
            self.tableWidget.setItem(i, 7, QTableWidgetItem(
                self.check(segments[i].attributes()[self.utils.get_idx_attr(segments_lyr, 'segments',
                                                                        'dwn_qproject')])))  # node('dwnBrLevel'))))
            self.tableWidget.setItem(i, 8, QTableWidgetItem(
                self.check(self.utils.formatNum2Dec(self.utils.str_to_float_locale(
                    self.utils.get_element_layer_nodes(
                        node=segments[i].attributes()[self.utils.get_idx_attr(segments_lyr, 'segments', 'up_box')],
                        name_attr=self.utils.get_json_attr('nodes', 'depth')))))))  # node('upDepth'))))
            self.tableWidget.setItem(i, 9, QTableWidgetItem(
                self.check(self.utils.formatNum2Dec(self.utils.str_to_float_locale(
                    self.utils.get_element_layer_nodes(
                        node=segments[i].attributes()[self.utils.get_idx_attr(segments_lyr, 'segments', 'down_box')],
                        name_attr=self.utils.get_json_attr('nodes', 'depth')))))))  # node('dwnDepth'))))
            self.tableWidget.setItem(i, 10, QTableWidgetItem(
                self.__float_to_str_locale(value=2.00, decimals=2)))  # node('gabarito'))))
            self.tableWidget.setItem(i, 11, QTableWidgetItem(
                self.check(self.utils.get_element_layer_nodes(
                    node=segments[i].attributes()[self.utils.get_idx_attr(segments_lyr, 'segments', 'up_box')],
                    name_attr=self.utils.get_json_attr('nodes', 'q_rule')))))  # node('upRuleLvl'))))
            self.tableWidget.setItem(i, 12, QTableWidgetItem(
                self.check(self.utils.get_element_layer_nodes(
                    node=segments[i].attributes()[self.utils.get_idx_attr(segments_lyr, 'segments', 'down_box')],
                    name_attr=self.utils.get_json_attr('nodes', 'q_rule')))))  # node('dwnRuleLvl'))))
            self.tableWidget.setItem(i, 13, QTableWidgetItem(
                self.__float_to_str_locale(self.utils.get_element_layer_nodes(
                    node=segments[i].attributes()[self.utils.get_idx_attr(segments_lyr, 'segments', 'up_box')],
                    name_attr=self.utils.get_json_attr('nodes', 'critical_depth')), decimals=2)))  # node('prof_critica'))))
            self.tableWidget.setItem(i, 14, QTableWidgetItem(
                self.__float_to_str_locale(
                    segments[i].attributes()[self.utils.get_idx_attr(segments_lyr, 'segments', 'unevenness_segment')],
                    decimals=1)))  # node('slopeSec'))))
            dsb_pcv = QDoubleSpinBox()
            dsb_pcv.setDecimals(0)
            dsb_pcv.setSingleStep(10.00)
            dsb_pcv.setRange(100.00, 160.00)
            dsb_pcv.setValue(150.0)
            dsb_pcv.setValue(segments[i].attributes()[
                                 self.utils.get_idx_attr(segments_lyr, 'segments', 'pvc_diameter')])
            self.tableWidget.setCellWidget(i, 15, dsb_pcv)  # 'pvc_diam'))))
            self.tableWidget.setItem(i, 16, QTableWidgetItem(
                self.concat1(
                    self.__get_key_map_of_values(layer=segments_lyr,
                                                 idx_col=self.utils.get_idx_attr(segments_lyr, 'segments', 'paviment_1'),
                                                 value=segments[i].attributes()[
                                                     self.utils.get_idx_attr(segments_lyr, 'segments', 'paviment_1')]),
                    self.__get_key_map_of_values(layer=segments_lyr,
                                                 idx_col=self.utils.get_idx_attr(segments_lyr, 'segments', 'paviment_2'),
                                                 value=segments[i].attributes()[
                                                     self.utils.get_idx_attr(segments_lyr, 'segments',
                                                                         'paviment_2')]))))  # paviment
            # TODO: REMOVER
            # self.tableWidget.setItem(i, 17, QTableWidgetItem(  # tubo queda
            #     self.check(segments[i].attributes()[self.utils.get_idx_attr(segments_lyr, 'segments', 'fall_tube')])))
            # self.tableWidget.setItem(i, 17, QTableWidgetItem(self.check(segments[i].attributes()[
            #                    self.utils.get_idx_attr(segments_lyr, 'segments', 'h_tq')])))
            # self.tableWidget.setItem(i, 18, QTableWidgetItem(
            #     self.concat2(
            #         self.__get_key_map_of_values(layer=segments_lyr,
            #                                      idx_col=self.utils.get_idx_attr(segments_lyr, 'segments', 'obstacle1'),
            #                                      value=segments[i].attributes()[
            #                                          self.utils.get_idx_attr(segments_lyr, 'segments', 'obstacle1')]),
            #         self.__get_key_map_of_values(layer=segments_lyr,
            #                                      idx_col=self.utils.get_idx_attr(segments_lyr, 'segments', 'obstacle2'),
            #                                      value=segments[i].attributes()[
            #                                          self.utils.get_idx_attr(segments_lyr, 'segments', 'obstacle2')]),
            #         self.__get_key_map_of_values(layer=segments_lyr,
            #                                      idx_col=self.utils.get_idx_attr(segments_lyr, 'segments', 'obstacle3'),
            #                                      value=segments[i].attributes()[
            #                                          self.utils.get_idx_attr(segments_lyr, 'segments',
            #                                                              'obstacle3')]))))  # 'obstacles'))))
            self.tableWidget.setItem(i, 17, QTableWidgetItem(
                self.__get_key_map_of_values(layer=nodes_lyr,
                                             idx_col=self.utils.get_idx_attr(nodes_lyr, 'nodes', 'branch_position'),
                                             value=segments[i].attributes()[self.utils.get_idx_attr(segments_lyr, 'nodes',
                                                                                                'branch_position')])))  # node('posicao_ramal'))))
            self.tableWidget.setItem(i, 18, QTableWidgetItem(
                self.__float_to_str_locale(self.utils.get_element_layer_nodes(
                    node=segments[i].attributes()[self.utils.get_idx_attr(segments_lyr, 'segments', 'up_box')],
                    name_attr=self.utils.get_json_attr('nodes', 'h_branch')), decimals=2)))  # node('h_ramal'))))
            self.tableWidget.setItem(i, 19, QTableWidgetItem(
                self.check(segments[i].attributes()[self.utils.get_idx_attr(segments_lyr, 'segments', 'tq')]).replace(
                    'NULL', '')))
            self.tableWidget.setItem(i, 20, QTableWidgetItem(
                self.check(self.__float_to_str_locale(
                    segments[i].attributes()[self.utils.get_idx_attr(segments_lyr, 'segments', 'h_TQ')],
                    decimals=2).replace(
                    'NULL', ''))))
            self.tableWidget.setItem(i, 21, QTableWidgetItem(
                self.check(segments[i].attributes()[self.utils.get_idx_attr(segments_lyr, 'segments', 'comments')]).replace(
                    'NULL', '')))  # node('comments'))))
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

    # def get_element_layer_nodes(self, node: str, name_attr: str):
    #     nodes_lyr = QgsProject.instance().mapLayer(ProjectDataManager.get_layers_id().NODES_LAYER_ID)
    #     all_nodes = nodes_lyr.getFeatures()
    #     for n in all_nodes:
    #         if n.attributes()[self.utils.get_idx_attr(nodes_lyr, 'nodes', 'name')] == node:
    #             return n.attributes()[self.utils.get_idx_attr(nodes_lyr, 'nodes', name_attr)]
    #     return

    def save(self):
        self.tableWidget.blockSignals(True)
        blocks = self.proj.getBlocksLayer()
        if not blocks.isEditable():
            blocks.startEditing()
        blocks.changeAttributeValue(
            self.block_id,
            blocks.fields().lookupField(self.utils.get_json_attr('blocks', 'name')),
            self.blockName.text())
        blocks.changeAttributeValue(
            self.block_id,
            blocks.fields().lookupField(self.utils.get_json_attr('blocks', 'date')),
            self.date.dateTime())
        blocks.changeAttributeValue(
            self.block_id,
            blocks.fields().lookupField(self.utils.get_json_attr('blocks', 'rev_date')),
            self.revisionDate.dateTime())
        blocks.changeAttributeValue(
            self.block_id,
            blocks.fields().lookupField(self.utils.get_json_attr('blocks', 'watershed')),
            self.watershed.text())
        blocks.changeAttributeValue(
            self.block_id,
            blocks.fields().lookupField(self.utils.get_json_attr('blocks', 'total_length')),
            self.totalLength.value())
        blocks.changeAttributeValue(
            self.block_id,
            blocks.fields().lookupField(self.utils.get_json_attr('blocks', 'min_depth')),
            self.minDepth.value())
        blocks.changeAttributeValue(
            self.block_id,
            blocks.fields().lookupField(self.utils.get_json_attr('blocks', 'min_slope')),
            self.minSlope.value())
        blocks.changeAttributeValue(
            self.block_id,
            blocks.fields().lookupField(self.utils.get_json_attr('blocks', 'revision')),
            self.revision.text())
        blocks.changeAttributeValue(
            self.block_id,
            blocks.fields().lookupField(self.utils.get_json_attr('blocks', 'comments')),
            self.observations.toPlainText())
        blocks.changeAttributeValue(
            self.block_id,
            blocks.fields().lookupField(self.utils.get_json_attr('blocks', 'os_name')),
            self.os_name_le.text())
        blocks.commitChanges()
        nodes = self.proj.getNodesLayer()
        if not nodes.isEditable():
            nodes.startEditing()
        default_value = QgsDefaultValue(expression='', applyOnUpdate=False)

        name_ex = nodes.defaultValueDefinition(self.utils.get_idx_attr(nodes, 'nodes', 'name')).expression()
        q_terrain_ex = nodes.defaultValueDefinition(self.utils.get_idx_attr(nodes, 'nodes', 'q_terrain')).expression()
        raster = ProjectDataManager.get_layer_raster().LAYER_RASTER
        if ProjectDataManager.get_layer_raster().LAYER_RASTER == '':
            q_terrain_ex = q_terrain_ex.replace(self.__get_raster_express(), raster)
        else:
            q_terrain_ex = q_terrain_ex.replace(ProjectDataManager.get_layer_raster().LAYER_RASTER,
                                                raster)
        nodes.setDefaultValueDefinition(self.utils.get_idx_attr(nodes, 'nodes', 'name'), default_value)
        nodes.setDefaultValueDefinition(self.utils.get_idx_attr(nodes, 'nodes', 'q_terrain'), default_value)
        box_list = []
        for node in self.current_nodes:
            row = 0
            while row < self.tableWidget.rowCount():
                if (node[self.utils.get_idx_attr(nodes, 'nodes', 'name')] ==
                        self.getTableValue(row, 'up_box') and
                        node[self.utils.get_idx_attr(nodes, 'nodes', 'name')] not in box_list):
                    nodes.changeAttributeValue(node.id(), self.utils.get_idx_attr(nodes, 'nodes', 'q_terrain'),
                                               self.utils.str_to_float_locale(self.getTableValue(row, 'up_gl')), 2)
                    nodes.changeAttributeValue(node.id(), self.utils.get_idx_attr(nodes, 'nodes', 'depth'),
                                               self.utils.str_to_float_locale(self.getTableValue(row, 'upDepth')), 2)
                    nodes.changeAttributeValue(node.id(), self.utils.get_idx_attr(nodes, 'nodes', 'q_rule'),
                                               self.utils.str_to_float_locale(self.getTableValue(row, 'upRuleLvl')), 3)
                    # nodes.changeAttributeValue(node.id(), self.utils.get_idx_attr(nodes, 'nodes', 'critical_depth'),
                    #                            self.utils.str_to_float_locale(self.getTableValue(row, 'critDepth')), 2)
                    nodes.changeAttributeValue(node.id(), self.utils.get_idx_attr(nodes, 'nodes', 'template'),
                                               self.utils.str_to_float_locale(self.getTableValue(row, 'model')), 2)
                    box_list.append(node[self.utils.get_idx_attr(nodes, 'nodes', 'name')])
                if (node[self.utils.get_idx_attr(nodes, 'nodes', 'name')] ==
                        self.getTableValue(row, 'down_box') and
                        node[self.utils.get_idx_attr(nodes, 'nodes', 'name')] not in box_list):
                    nodes.changeAttributeValue(node.id(), self.utils.get_idx_attr(nodes, 'nodes', 'q_terrain'),
                                               self.utils.str_to_float_locale(self.getTableValue(row, 'down_gl')), 2)
                    nodes.changeAttributeValue(node.id(), self.utils.get_idx_attr(nodes, 'nodes', 'depth'),
                                               self.utils.str_to_float_locale(self.getTableValue(row, 'dwnDepth')), 2)
                    nodes.changeAttributeValue(node.id(), self.utils.get_idx_attr(nodes, 'nodes', 'q_rule'),
                                               self.utils.str_to_float_locale(self.getTableValue(row, 'dwnRuleLvl')), 3)
                    # nodes.changeAttributeValue(node.id(), self.utils.get_idx_attr(nodes, 'nodes', 'critical_depth'),
                    #                            self.utils.str_to_float_locale(self.getTableValue(row, 'critDepth')), 2)
                    nodes.changeAttributeValue(node.id(), self.utils.get_idx_attr(nodes, 'nodes', 'template'),
                                               self.utils.str_to_float_locale(self.getTableValue(row, 'model')), 2)
                    box_list.append(node[self.utils.get_idx_attr(nodes, 'nodes', 'name')])
                row += 1
        nodes.commitChanges()

        default_value.setExpression(name_ex)
        default_value.setApplyOnUpdate(True)
        nodes.setDefaultValueDefinition(self.utils.get_idx_attr(nodes, 'nodes', 'name'), default_value)
        default_value.setExpression(q_terrain_ex)
        default_value.setApplyOnUpdate(True)
        nodes.setDefaultValueDefinition(self.utils.get_idx_attr(nodes, 'nodes', 'q_terrain'), default_value)
        segments = self.proj.getSegmentsLayer()
        if not segments.isEditable():
            segments.startEditing()
        row = 0
        for segment in self.current_segments:
            segments.changeAttributeValue(segment.id(), self.utils.get_idx_attr(segments, 'segments', 'up_qproject'),
                                          self.utils.str_to_float_locale(self.getTableValue(row, 'upBrLevel')))
            segments.changeAttributeValue(segment.id(), self.utils.get_idx_attr(segments, 'segments', 'dwn_qproject'),
                                          self.utils.str_to_float_locale(self.getTableValue(row, 'dwnBrLevel')))
            segments.changeAttributeValue(segment.id(), self.utils.get_idx_attr(segments, 'segments', 'unevenness_segment'),
                                          self.utils.str_to_float_locale(self.getTableValue(row, 'slopeSection')))
            segments.changeAttributeValue(segment.id(), self.utils.get_idx_attr(segments, 'segments', 'pvc_diameter'),
                                          self.utils.str_to_float_locale(
                                              self.getTableValuePvcDiameter(row, 'pvc_diameter')))
            row += 1
        segments.commitChanges()
        self.tableWidget.blockSignals(False)
        self.proj.showMessage('saved successfully')
        self.hide()
        ProjectDataManager.save_status_calculation(status=True)
        self.save_resume_frame()

    def save_resume_frame(self):
        self.tableWidget.blockSignals(True)
        resume_frame = self.proj.getResumeFrameLayer()

        with edit(resume_frame):
            feature = QgsFeature(resume_frame.fields())
            feat_exist = None
            for feat in resume_frame.getFeatures():
                feat_exist = feat.id()
                break
            ext_trechos_DN100 = self.__get_len_DN(100)
            ext_TQ_DN100 = self.__get_len_tq_DN(100)
            ext_trechos_DN150 = self.__get_len_DN(150)
            ext_TQ_DN150 = self.__get_len_tq_DN(150)
            cx_040 = self.__get_cx('DN40')
            cx_060 = self.__get_cx('DN60')
            cx_ret_brick = self.__get_cx('Retangular Tijolinho')
            cx_ret_concrete = self.__get_cx('Retangular Concreto')
            til = self.__get_cx('TIL_Terminal Inspeção-Limpeza')
            attributes = {
                self.utils.get_json_attr('resume_frame', 'ext_trechos_DN100(m)'): ext_trechos_DN100,
                self.utils.get_json_attr('resume_frame', 'ext_TQ_DN100'): ext_TQ_DN100,
                self.utils.get_json_attr('resume_frame', 'ext_total_DN100(m)'):
                    (ext_trechos_DN100 + ext_TQ_DN100),
                self.utils.get_json_attr('resume_frame', "ext_trechos_DN150(m)"): ext_trechos_DN150,
                self.utils.get_json_attr('resume_frame', "ext_TQ_DN150(m)"): ext_TQ_DN150,
                self.utils.get_json_attr('resume_frame', "ext_total_DN150(m)"):
                    (ext_trechos_DN150 + ext_TQ_DN150),
                self.utils.get_json_attr('resume_frame', "ext_total(m)"):
                    (ext_trechos_DN100 + ext_TQ_DN100 + ext_trechos_DN150 + ext_TQ_DN150),
                self.utils.get_json_attr('resume_frame', "cx_Ø40"): cx_040,
                self.utils.get_json_attr('resume_frame', "cx_Ø60"): cx_060,
                self.utils.get_json_attr('resume_frame', "cx_ret_tijolinho"): cx_ret_brick,
                self.utils.get_json_attr('resume_frame', "cx_ret_concreto"): cx_ret_concrete,
                self.utils.get_json_attr('resume_frame', "TIL"): til,
                self.utils.get_json_attr('resume_frame', "total_inspeção"):
                    (cx_040 + cx_060 + cx_ret_brick + cx_ret_concrete + til),
                self.utils.get_json_attr('resume_frame', "selim"): self.__get_cx('Selim_Rede'),
                self.utils.get_json_attr('resume_frame', "C90º"): self.__get_connections('C90°'),
                self.utils.get_json_attr('resume_frame', "TE"): self.__get_connections('TE'),
                self.utils.get_json_attr('resume_frame', "imoveis"): self.__get_count_buildings(),
                self.utils.get_json_attr('resume_frame', "economias"): self.__get_count_economy(),
                self.utils.get_json_attr('resume_frame', "faixa_servidão"): self.__get_length_service_lane(),
            }
            for field, value in attributes.items():
                if feat_exist is not None:
                    resume_frame.changeAttributeValue(feat_exist,
                                                      self.utils.get_idx_attr(resume_frame, 'resume_frame', field),
                                                      value)
                else:
                    feature.setAttribute(field, value)
                    resume_frame.addFeature(feature)

    def __get_len_DN(self, dn):
        total = 0.00
        self.tableWidget.blockSignals(True)
        grouped = {
            k: [i for i in range(self.tableWidget.rowCount()) if self.getTableValue(i, "branch") == k]
            for k in [self.getTableValue(i, "branch") for i in range(self.tableWidget.rowCount())]
        }
        for key in grouped:
            for i in range(self.tableWidget.rowCount()):
                if self.getTableValue(i, "branch") == key:
                    if int(self.getTableValuePvcDiameter(i, 'pvc_diameter')) - int(dn) <= 10:
                        total += self.utils.str_to_float_locale(
                            self.tableWidget.item(i, self.getColumnIndex('length')).text())
                        # print(self.tableWidget.item(i, self.getColumnIndex('length')).text())
        return round(total, 2)

    def __get_len_tq_DN(self, dn):
        total = 0.00
        self.tableWidget.blockSignals(True)
        grouped = {
            k: [i for i in range(self.tableWidget.rowCount()) if self.getTableValue(i, "branch") == k]
            for k in [self.getTableValue(i, "branch") for i in range(self.tableWidget.rowCount())]
        }
        for key in grouped:
            for i in range(self.tableWidget.rowCount()):
                if self.getTableValue(i, "branch") == key:
                    if (int(self.getTableValuePvcDiameter(i, 'pvc_diameter')) - int(dn) <= 10 and
                            self.getTableValue(i, "Tubo de Queda") == 'True'):
                        total += self.utils.str_to_float_locale(
                            self.tableWidget.item(i, self.getColumnIndex('length')).text())
        return round(total, 2)

    def __get_cx(self, cx):
        nodes_lyr = QgsProject.instance().mapLayer(ProjectDataManager.get_layers_id().NODES_LAYER_ID)
        all_nodes = nodes_lyr.getFeatures()
        nodes = []
        for s in all_nodes:
            nodes.append(s)
        if not nodes_lyr.isValid():
            raise ValueError(self.translate('Camada inválida!'))
        count = 0
        for i, feat in enumerate(nodes_lyr.getFeatures()):
            item = (self.__get_key_map_of_values(layer=nodes_lyr,
                                                 idx_col=self.utils.get_idx_attr(nodes_lyr, 'nodes', 'node_type'),
                                                 value=nodes[i].attributes()[
                                                     self.utils.get_idx_attr(nodes_lyr, 'nodes', 'node_type')]))
            if item == cx:
                count += 1
        return count

    def __get_connections(self, connector):
        segments_lyr = QgsProject.instance().mapLayer(ProjectDataManager.get_layers_id().SEGMENTS_LAYER_ID)
        all_segs = segments_lyr.getFeatures()
        segments = []
        for s in all_segs:
            segments.append(s)
        if not segments_lyr.isValid():
            raise ValueError(self.translate('Camada inválida!'))
        count = 0
        for i, feat in enumerate(segments_lyr.getFeatures()):
            if feat[self.utils.get_json_attr('segments', 'tq')]:
                conn_1 = (self.__get_key_map_of_values(layer=segments_lyr,
                                                       idx_col=self.utils.get_idx_attr(segments_lyr, 'segments', 'tq_link1'),
                                                       value=segments[i].attributes()[
                                                           self.utils.get_idx_attr(segments_lyr, 'segments', 'tq_link1')]))
                conn_2 = (self.__get_key_map_of_values(layer=segments_lyr,
                                                       idx_col=self.utils.get_idx_attr(segments_lyr, 'segments', 'tq_link2'),
                                                       value=segments[i].attributes()[
                                                           self.utils.get_idx_attr(segments_lyr, 'segments', 'tq_link2')]))
                if conn_1 == connector:
                    count += 1
                if conn_2 == connector:
                    count += 1
        return count

    def __get_count_buildings(self):
        buildings_lyr = QgsProject.instance().mapLayer(ProjectDataManager.get_layers_id().BUILDINGS_LAYER_ID)
        if not buildings_lyr.isValid():
            raise ValueError(self.translate('Camada inválida!'))
        return buildings_lyr.featureCount()

    def __get_count_economy(self):
        buildings_lyr = QgsProject.instance().mapLayer(ProjectDataManager.get_layers_id().BUILDINGS_LAYER_ID)
        if not buildings_lyr.isValid():
            raise ValueError(self.translate('Camada inválida!'))
        count = 0
        for feat in buildings_lyr.getFeatures():
            count += feat[self.utils.get_json_attr('buildings', 'n_econ')]
        return count

    def __get_length_service_lane(self):
        service_lane_lyr = QgsProject.instance().mapLayer(ProjectDataManager.get_layers_id().SERVICE_LANE_LAYER_ID)
        if not service_lane_lyr.isValid():
            raise ValueError(self.translate('Camada inválida!'))
        length_service_lane = 0
        for feat in service_lane_lyr.getFeatures():
            length_service_lane = feat[self.utils.get_json_attr('service_lane', 'extensao')]
            break
        return length_service_lane


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

    def getTableValuePvcDiameter(self, row, columnName):
        """ Returns value from single cell from table """
        index = self.getColumnIndex(columnName)
        item = self.tableWidget.cellWidget(row, index)
        return item.value() if item else None

    def getColumnIndex(self, columnName):
        return self.headers.index(self.translate(columnName))

    # def to_float(self, str, default=0):
    #     return float(str.replace(',', '.')) if str != '' else default

    # def __str_to_float_locale(self, value: str) -> float:
    #     # if QgsApplication.instance().locale() == 'pt_BR':
    #     if type(value) is str and len(value) > 0:
    #         if value[-1].isnumeric():
    #             return self.loc.toFloat(value)[0]
    #         return 0.00
    #     elif type(value) is float:
    #         return value
    #     else:
    #         return 0.00

    def __float_to_str_locale(self, value: float, decimals=3):
        if type(value) is float:  # != '' and value != 'NULL':
            return self.loc.toString(value, 'd', decimals)
        return str(value)

    # def __set_data_json(self):
    #     plg_dir = os.path.dirname(__file__)
    #     plg_dir = plg_dir.replace('core' + os.sep + 'calculate', 'resources' + os.sep + 'localizations' + os.sep)
    #     set_language_file('pt_BR') #TODO: remover set antes com o novo gpkg
    #     lang = ProjectDataManager.get_language_project().LANGUAGE
    #     lang = lang if lang != '' else get_language_file()
    #     file_json = open(os.path.join(plg_dir, lang + '.json'), 'r')
    #     self.data_json = json.load(file_json)
    #     file_json.close()
    #
    # def __get_json_attr(self, name_lyr: str, attribute: str):
    #     if self.data_json is None:
    #         self.__set_data_json()
    #     lyr = self.data_json[name_lyr][1]
    #
    #     def get_key(val):
    #         for k, v in lyr.items():
    #             if v == val:
    #                 return k
    #         return
    #
    #     try:
    #         return lyr[attribute]
    #     except KeyError:
    #         att = get_key(attribute)
    #         if att is not None:
    #             return lyr[att]
    #         return
    #
    # def __get_idx_attr(self, layer: QgsVectorLayer, name_lyr: str, name_attr: str):
    #     attrs = layer.fields().names()
    #     return attrs.index(self.utils.get_json_attr(name_lyr, name_attr))

    def __get_raster_express(self):
        # if self.data_json is None:
        #     self.__set_data_json()
        #     self.utils.data_json
        return self.utils.data_json['raster']

    def __calculate_underground(self, i, initial, minDepth, minSlope):
        length = self.utils.str_to_float_locale(self.getTableValue(i, "length"))
        up_gl = self.utils.str_to_float_locale(self.getTableValue(i, "up_gl"))
        down_box = self.getTableValue(i, "down_box")
        down_gl = self.utils.str_to_float_locale(self.getTableValue(i, "down_gl"))
        # model = self.to_float(self.getTableValue(i, "model"))
        critDepth = self.utils.str_to_float_locale(self.getTableValue(i, "critDepth"))
        dwnDepthPrev = 0.00 if i == initial else self.utils.str_to_float_locale(
            self.getTableValue((i - 1), "dwnDepth"))
        dwnBrLevelPrev = 0.00 if i == initial else self.utils.str_to_float_locale(
            self.getTableValue((i - 1), "dwnBrLevel"))
        if i == initial:
            upDepth = (
                minDepth if minDepth > critDepth else critDepth) if down_box != '' else ''  # H21 i==0
            upBrLevel = (up_gl - upDepth) if down_box != '' else ''  # tocheck ''  #F21 i==0
        else:
            upBrLevel = '' if down_box == '' else (
                0.00 if decimal.Decimal(length) == decimal.Decimal(0.00) else (
                    dwnBrLevelPrev if (dwnDepthPrev > critDepth) else (up_gl - critDepth)))
            upDepth = (up_gl - upBrLevel) if down_box != '' else 0.00
        dwnBrLevel = '' if down_box == '' else (
            0.00 if decimal.Decimal(length) == decimal.Decimal(0.00) else (
                (down_gl - minDepth) if (upBrLevel - (down_gl - minDepth)) / length >= minSlope else (
                        upBrLevel - length * minSlope - 0.0005)))  # G21
        dwnDepth = (down_gl - dwnBrLevel) if down_box != '' else ''  # I21
        model = 2.00  # J21 = 2 ->
        upRuleLvl = '' if down_box == '' else (
            '' if decimal.Decimal(length) == decimal.Decimal(0.00) else (model + upBrLevel))  # K21
        dwnRuleLvl = '' if down_box == '' else (
            '' if decimal.Decimal(length) == decimal.Decimal(0.00) else (model + dwnBrLevel))  # L21
        slopeSection = '' if down_box == '' else round((upBrLevel - dwnBrLevel) * 100.00,
                                                       1)  # N21 slopeSection
        return upBrLevel, dwnBrLevel, upDepth, dwnDepth, model, upRuleLvl, slopeSection, critDepth, dwnRuleLvl

    def __calculate_overhead(self, i, initial, minDepth, minSlope):
        length = self.utils.str_to_float_locale(self.getTableValue(i, "length"))
        up_gl = self.utils.str_to_float_locale(self.getTableValue(i, "up_gl"))
        down_box = self.getTableValue(i, "down_box")
        down_gl = self.utils.str_to_float_locale(self.getTableValue(i, "down_gl"))
        # model = self.to_float(self.getTableValue(i, "model"))
        critDepth = self.utils.str_to_float_locale(self.getTableValue(i, "critDepth"))
        h_branch = - self.utils.str_to_float_locale(self.getTableValue(initial, "H Ramal"))
        dwnDepthPrev = 0.00 if i == initial else self.utils.str_to_float_locale(
            self.getTableValue((i - 1), "dwnDepth"))
        dwnBrLevelPrev = 0.00 if i == initial else self.utils.str_to_float_locale(
            self.getTableValue((i - 1), "dwnBrLevel"))
        if i == initial:
            upBrLevel = (up_gl - h_branch) if down_box != '' else ''  # tocheck ''  #F21 i==0
            upDepth = h_branch if down_box != '' else 0.00
        else:
            upBrLevel = '' if down_box == '' else dwnBrLevelPrev
            upDepth = (up_gl - upBrLevel) if down_box != '' else 0.00
        dwnBrLevel = '' if down_box == '' else (
            0.00 if decimal.Decimal(length) == decimal.Decimal(0.00) else (
                (down_gl - h_branch) if (up_gl - (down_gl)) / length >= minSlope else (
                        upBrLevel - length * minSlope - 0.0005)))  # G21
        dwnDepth = (down_gl - dwnBrLevel) if down_box != '' else ''  # I21
        model = 2.00  # J21 = 2 ->
        upRuleLvl = '' if down_box == '' else (
            '' if decimal.Decimal(length) == decimal.Decimal(0.00) else (model + upBrLevel))  # K21
        dwnRuleLvl = '' if down_box == '' else (
            '' if decimal.Decimal(length) == decimal.Decimal(0.00) else (model + dwnBrLevel))  # L21
        slopeSection = '' if down_box == '' else round((upBrLevel - dwnBrLevel) * 100.00,
                                                       1)  # N21 slopeSection
        return upBrLevel, dwnBrLevel, upDepth, dwnDepth, model, upRuleLvl, slopeSection, critDepth, dwnRuleLvl

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
                    if (self.getTableValue(i, "Posição ramal") ==
                            self.utils.get_json_attr(name_lyr='bool_air', attribute='underground')):  # tubo enterrado
                        upBrLevel, dwnBrLevel, upDepth, dwnDepth, model, upRuleLvl, slopeSection, critDepth, dwnRuleLvl = (
                            self.__calculate_underground(i, initial, minDepth, minSlope))
                    else:
                        upBrLevel, dwnBrLevel, upDepth, dwnDepth, model, upRuleLvl, slopeSection, critDepth, dwnRuleLvl = (
                            self.__calculate_overhead(i, initial, minDepth, minSlope))
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
