import json

from PyQt5.QtCore import Qt, QLocale
from qgis._core import QgsProject, QgsVectorLayer
from xlwt import Workbook, easyxf
import os

from ...helpers.globals import get_language_file
from ...core.data.data_manager import ProjectDataManager


class ProducesReportOSXls:

    def __init__(self):
        self.data_json = None
        self.segments = None
        self.loc = QLocale()

    def generate_report_os(self, local_file):
        local_file = os.path.normpath(local_file)
        block = QgsProject.instance().mapLayer(ProjectDataManager.get_layers_id().BLOCKS_LAYER_ID)
        block_fields = [field.name() for field in block.fields()]
        block_values = [f.attributes() for f in block.getFeatures()]
        block_dict = dict(zip(block_fields, block_values[0]))
        list_block_values = list(block_dict.values())
        nodes = []
        nodes_lyr = QgsProject.instance().mapLayer(ProjectDataManager.get_layers_id().NODES_LAYER_ID)
        all_nodes = nodes_lyr.getFeatures()
        for n in all_nodes:
            nodes.append(n)
        self.segments = QgsProject.instance().mapLayer(ProjectDataManager.get_layers_id().SEGMENTS_LAYER_ID)
        all_segs = self.segments.getFeatures()
        segments = []
        for s in all_segs:
            segments.append(s)
        branchs = []
        for feat in segments:
            branchs.append(feat[self.__get_idx_attr_segments('branch_id')])
        branchs = set(branchs)
        workbook = Workbook()
        for branch in branchs:
            q_row = 0
            for feat in segments:
                if feat[self.__get_idx_attr_segments('branch_id')] == branch:
                    q_row += 1
            worksheet = workbook.add_sheet('R-' + str(branch), cell_overwrite_ok=True)
            worksheet.set_fit_num_pages(1)
            worksheet.show_grid = False
            worksheet.col(0).width = 2000
            worksheet.col(1).width = 2100
            worksheet.col(2).width = 1550
            worksheet.col(3).width = 1550
            worksheet.col(4).width = 1550
            worksheet.col(5).width = 1550
            worksheet.col(6).width = 1550
            worksheet.col(7).width = 1550
            worksheet.col(8).width = 1550
            worksheet.col(9).width = 1550
            worksheet.col(10).width = 1550
            worksheet.col(11).width = 1550
            worksheet.col(12).width = 1550
            worksheet.col(13).width = 1550
            worksheet.col(14).width = 2600
            worksheet.row(7).height_mismatch = True
            worksheet.row(7).height = 130
            worksheet.row(11).height_mismatch = True
            worksheet.row(11).height = 130
            worksheet.row(16).height_mismatch = True
            worksheet.row(16).height = 130
            worksheet.write_merge(0, 2, 0, 14, '', BORDER_1)
            worksheet.write(4, 0, '', BORDER_LEFT)
            worksheet.write(4, 14, '', BORDER_RIGHT)
            worksheet.write_merge(3, 3, 0, 14, 'SISTEMA DE ESGOTAMENTO SANITÁRIO', TEXT_BOLD_CENTER_12_BORDER)
            worksheet.write_merge(5, 5, 0, 14, 'ORDEM DE SERVIÇO PARA GABARITO - RAMAL', TEXT_BOLD_CENTER_10_RAMAL)
            worksheet.write_merge(6, 6, 0, 14, list_block_values[10], TEXT_BOLD_CENTER_10_OS)

            worksheet.write_merge(8, 8, 0, 1, 'QUADRA:', TEXT_BOLD_LEFT_12_QUADRA)
            worksheet.write(8, 2, list_block_values[1], TEXT_NORMAL_CENTER_12_QUADRA)
            worksheet.write_merge(8, 8, 3, 10, '', TEXT_NORMAL_LEFT_12_QUADRA)
            worksheet.write_merge(8, 8, 11, 12, 'RAMAL:', TEXT_BOLD_LEFT_12_RAMAL)
            worksheet.write_merge(8, 8, 13, 14, 'R-' + str(branch), TEXT_NORMAL_CENTER_12_RAMAL)
            worksheet.write_merge(9, 9, 0, 1, 'BACIA:', TEXT_BOLD_LEFT_12_BACIA)
            worksheet.write_merge(9, 9, 2, 4, list_block_values[3], TEXT_NORMAL_CENTER_12_BACIA)
            worksheet.write_merge(9, 9, 5, 9, '', TEXT_NORMAL_CENTER_12_BACIA)
            worksheet.write_merge(9, 9, 10, 11, 'DATA:', TEXT_BOLD_LEFT_12_DATA)
            worksheet.write_merge(9, 9, 12, 14,
                                  str(list_block_values[2].toString(Qt.DefaultLocaleShortDate)).split()[0],
                                  TEXT_NORMAL_CENTER_12_DATA)
            worksheet.write_merge(10, 10, 0, 1, 'PROF.MÍNIMA (m):', TEXT_NORMAL_RIGHT_PROF)
            worksheet.write(10, 2, '', TEXT_NORMAL_CENTER_PROF)
            worksheet.write_merge(10, 10, 3, 9, list_block_values[4], TEXT_NORMAL_CENTER_PROF)
            worksheet.write_merge(10, 10, 9, 13, 'DECLIVIDADE MÍNIMA (m/m):', TEXT_NORMAL_RIGHT_DECLIV)
            worksheet.write(10, 14, list_block_values[5], TEXT_NORMAL_CENTER_DECLIV)

            worksheet.write_merge(12, 12, 0, 14, 'QUANTITATIVOS', TEXT_BOLD_CENTER_12_QUANT)
            worksheet.write(13, 0, 'REV.:', TEXT_NORMAL_LEFT_REV)
            worksheet.write_merge(13, 13, 1, 2, list_block_values[6], TEXT_NORMAL_CENTER_REV)
            worksheet.write_merge(13, 13, 3, 4, 'Data Rev.:', TEXT_NORMAL_LEFT_DATA_REV)
            worksheet.write_merge(13, 13, 5, 7,
                                  str(list_block_values[7].toString(Qt.DefaultLocaleShortDate)).split()[0],
                                  TEXT_NORMAL_LEFT_DATA_REV)
            worksheet.write_merge(13, 13, 8, 11, '', TEXT_NORMAL_LEFT_DATA_REV)
            worksheet.write_merge(13, 13, 12, 13, 'Extensão total:', TEXT_NORMAL_LEFT_DATA_REV)
            worksheet.write(13, 14, list_block_values[8], TEXT_NORMAL_CENTER_EXTEN)
            worksheet.write_merge(14, 14, 0, 7, '', TEXT_NORMAL_LEFT_NULL)
            worksheet.write_merge(14, 14, 8, 11, '', TEXT_NORMAL_CENTER_NULL)
            worksheet.write_merge(14, 14, 12, 13, 'Extensão ramal:', TEXT_NORMAL_LEFT_DATA_BRANCH)

            worksheet.write_merge(15, 15, 0, 3, '', TEXT_NORMAL_LEFT_TUBO)
            worksheet.write(15, 4, '', TEXT_NORMAL_CENTER_TUBO)
            worksheet.write_merge(15, 15, 5, 7, '', TEXT_NORMAL_MERGE_TUBO_L)
            worksheet.write_merge(15, 15, 8, 14, '', TEXT_NORMAL_MERGE_TUBO_R)

            worksheet.write_merge(17, 18, 0, 1, 'CAIXA', TEXT_NORMAL_CENTER_CAIXA)
            worksheet.write_merge(17, 19, 2, 2, 'DISTÂNCIA (m)', TEXT_NORMAL_CENTER_HEADER_V)
            worksheet.write_merge(17, 18, 3, 4, 'COTA TERRENO (m)', TEXT_NORMAL_CENTER_HEADER_H)
            worksheet.write_merge(17, 18, 5, 6, 'COTA RAMAL (m)', TEXT_NORMAL_CENTER_HEADER_H)
            worksheet.write_merge(17, 18, 7, 8, 'PROFUNDIDADE (m)', TEXT_NORMAL_CENTER_HEADER_H)
            worksheet.write_merge(17, 19, 9, 9, 'GABARITO (m)', TEXT_NORMAL_CENTER_HEADER_V)
            worksheet.write_merge(17, 18, 10, 11, 'COTA RÉGUA (m)', TEXT_NORMAL_CENTER_HEADER_H)
            worksheet.write_merge(17, 19, 12, 12, 'PROF. CRÍTICA (m)', TEXT_NORMAL_CENTER_HEADER_V)
            worksheet.write_merge(17, 19, 13, 13, 'CAIM. TRECHO (cm)', TEXT_NORMAL_CENTER_HEADER_V)
            worksheet.write_merge(17, 19, 14, 14, 'OBS', TEXT_NORMAL_CENTER_HEADER_OBS)
            worksheet.write(19, 0, 'MONT.', TEXT_NORMAL_CENTER_HEADER_BOTTON_L)
            worksheet.write(19, 1, 'JUS.', TEXT_NORMAL_CENTER_HEADER_BOTTON_R)
            worksheet.write(19, 3, 'MONT.', TEXT_NORMAL_CENTER_HEADER_BOTTON_R)
            worksheet.write(19, 4, 'JUS.', TEXT_NORMAL_CENTER_HEADER_BOTTON_R)
            worksheet.write(19, 5, 'MONT.', TEXT_NORMAL_CENTER_HEADER_BOTTON_R)
            worksheet.write(19, 6, 'JUS.', TEXT_NORMAL_CENTER_HEADER_BOTTON_R)
            worksheet.write(19, 7, 'MONT.', TEXT_NORMAL_CENTER_HEADER_BOTTON_R)
            worksheet.write(19, 8, 'JUS.', TEXT_NORMAL_CENTER_HEADER_BOTTON_R)
            worksheet.write(19, 10, 'MONT.', TEXT_NORMAL_CENTER_HEADER_BOTTON_R)
            worksheet.write(19, 11, 'JUS.', TEXT_NORMAL_CENTER_HEADER_BOTTON_R)
            q_row += 20
            row = 20
            branch_length = 0.00
            for feat in segments:
                if feat[self.__get_idx_attr_segments('branch_id')] == branch:
                    worksheet.write(row, 0, str(feat[self.__get_idx_attr_segments('up_box')]),
                                    TEXT_NORMAL_CENTER_BODY_L)
                    worksheet.write(row, 1, str(feat[self.__get_idx_attr_segments('down_box')]),
                                    NUMBER_NORMAL_CENTER_BODY_C)
                    worksheet.write(row, 2, self.__str_to_float_locale(feat[self.__get_idx_attr_segments('length')]),
                                    NUMBER_NORMAL_CENTER_BODY_C)
                    branch_length += self.__str_to_float_locale(feat[self.__get_idx_attr_segments('length')])
                    worksheet.write(row, 3, self.__str_to_float_locale(self.get_element_layer_nodes(
                        node=feat[self.__get_idx_attr_segments('up_box')], name_attr='q_terrain')),
                                    NUMBER_NORMAL_CENTER_BODY_C_000)
                    worksheet.write(row, 4, self.__str_to_float_locale(self.get_element_layer_nodes(
                        node=feat[self.__get_idx_attr_segments('down_box')], name_attr='q_terrain')),
                                    NUMBER_NORMAL_CENTER_BODY_C_000)
                    worksheet.write(row, 5, self.__str_to_float_locale(feat[self.__get_idx_attr_segments('up_qproject')]),
                                    NUMBER_NORMAL_CENTER_BODY_C_000)
                    worksheet.write(row, 6, self.__str_to_float_locale(feat[self.__get_idx_attr_segments('dwn_qproject')]),
                                    NUMBER_NORMAL_CENTER_BODY_C_000)
                    if row == 20:
                        worksheet.write(row, 7, self.__str_to_float_locale(self.get_element_layer_nodes(
                            node=feat[self.__get_idx_attr_segments('up_box')], name_attr='depth')),
                                        NUMBER_NORMAL_CENTER_BODY_C)
                    else:
                        worksheet.write(row, 7, self.__str_to_float_locale(self.get_element_layer_nodes(
                            node=feat[self.__get_idx_attr_segments('up_box')], name_attr='q_terrain')) -
                                        float(feat[self.__get_idx_attr_segments('up_qproject')]),
                                        NUMBER_NORMAL_CENTER_BODY_C)
                    worksheet.write(row, 8, self.__str_to_float_locale(self.get_element_layer_nodes(
                        node=feat[self.__get_idx_attr_segments('down_box')], name_attr='depth')),
                                    NUMBER_NORMAL_CENTER_BODY_C)
                    worksheet.write(row, 9, self.__str_to_float_locale(self.get_element_layer_nodes(
                        node=feat[self.__get_idx_attr_segments('up_box')], name_attr='template')),
                                    NUMBER_NORMAL_CENTER_BODY_C)
                    worksheet.write(row, 10, self.__str_to_float_locale(self.get_element_layer_nodes(
                        node=feat[self.__get_idx_attr_segments('up_box')], name_attr='q_rule')),
                                    NUMBER_NORMAL_CENTER_BODY_C_000)
                    worksheet.write(row, 11, self.__str_to_float_locale(self.get_element_layer_nodes(
                        node=feat[self.__get_idx_attr_segments('down_box')], name_attr='q_rule')),
                                    NUMBER_NORMAL_CENTER_BODY_C_000)
                    worksheet.write(row, 12, self.__str_to_float_locale(self.get_element_layer_nodes(
                        node=feat[self.__get_idx_attr_segments('up_box')], name_attr='critical_depth')),
                                    NUMBER_NORMAL_CENTER_BODY_C)
                    worksheet.write(row, 13, self.__str_to_float_locale(feat[self.__get_idx_attr_segments('unevenness_segment')]),
                                    NUMBER_NORMAL_CENTER_BODY_C_0)
                    worksheet.write(row, 14, str(self.get_element_layer_nodes(
                        node=feat[self.__get_idx_attr_segments('up_box')], name_attr='comments'))
                                    .replace('NULL', '').replace('0.0', ''),
                                    TEXT_NORMAL_CENTER_BODY_R)
                    row += 1
            worksheet.write(14, 14, branch_length, TEXT_NORMAL_CENTER_BRANCH)
            worksheet.write_merge(q_row, q_row, 0, 14, 'OBSERVAÇÕES', TEXT_BOLD_CENTER_OBS_0)
            q_row += 1
            worksheet.write(q_row, 0, 'Obs 1:', TEXT_NORMAL_CENTER_OBS_1)
            worksheet.write_merge(q_row, q_row, 1, 14, '', TEXT_NORMAL_CENTER_OBS_2)
            q_row += 1
            worksheet.write_merge(q_row, q_row, 0, 14, '', TEXT_NORMAL_CENTER_OBS_3)
            q_row += 1
            worksheet.write(q_row, 0, 'Obs 2:', TEXT_NORMAL_CENTER_OBS_1)
            worksheet.write_merge(q_row, q_row, 1, 14, '', TEXT_NORMAL_CENTER_OBS_2)
            q_row += 1
            worksheet.write_merge(q_row, q_row, 0, 14, '', TEXT_NORMAL_CENTER_OBS_3)
            q_row += 1
            worksheet.write(q_row, 0, 'Obs 3:', TEXT_NORMAL_CENTER_OBS_1)
            worksheet.write_merge(q_row, q_row, 1, 14, '', TEXT_NORMAL_CENTER_OBS_2)
            q_row += 1
            worksheet.write_merge(q_row, q_row, 0, 14, '', TEXT_NORMAL_CENTER_OBS_3)
            q_row += 1
            worksheet.write(q_row, 0, 'Obs 4:', TEXT_NORMAL_CENTER_OBS_1)
            worksheet.write_merge(q_row, q_row, 1, 14, '', TEXT_NORMAL_CENTER_OBS_2)
            q_row += 1
            worksheet.write_merge(q_row, q_row, 0, 14, '', TEXT_NORMAL_CENTER_OBS_3)
            q_row += 1
            worksheet.write(q_row, 0, 'Obs 5:', TEXT_NORMAL_CENTER_OBS_1)
            worksheet.write_merge(q_row, q_row, 1, 14, '', TEXT_NORMAL_CENTER_OBS_2)
            q_row += 1
            worksheet.write_merge(q_row, q_row, 0, 14, '', TEXT_NORMAL_CENTER_OBS_3)
            q_row += 1
            worksheet.write_merge(q_row, q_row, 0, 14, '', TEXT_NORMAL_CENTER_OBS_3)
            q_row += 1
            worksheet.write_merge(q_row, q_row, 0, 14, '', TEXT_NORMAL_CENTER_OBS_3)
            q_row += 1
            worksheet.write_merge(q_row, q_row, 0, 5, 'Emissão:', TEXT_NORMAL_LEFT_EMIS)
            worksheet.write_merge(q_row, q_row, 6, 9, 'Liberação:         /         /             ',
                                  TEXT_NORMAL_CENTER_LIB)
            worksheet.write_merge(q_row, q_row, 10, 14,
                                  'Recebido:         /         /                                     ',
                                  TEXT_NORMAL_CENTER_REC)
            q_row += 1
            worksheet.write_merge(q_row, q_row, 0, 1, 'Por:', TEXT_NORMAL_CENTER_EMIS_POR)
            worksheet.write_merge(q_row, q_row, 2, 5, '__________________________', TEXT_NORMAL_CENTER_EMIS_ROW)
            worksheet.write(q_row, 6, 'Por:', TEXT_NORMAL_CENTER_LIB_POR)
            worksheet.write_merge(q_row, q_row, 7, 9, '____________________', TEXT_NORMAL_CENTER_EMIS_ROW)
            worksheet.write(q_row, 10, 'Por:', TEXT_NORMAL_CENTER_REC_POR)
            worksheet.write_merge(q_row, q_row, 11, 14, '_____________________________',
                                  TEXT_NORMAL_CENTER_REC_ROW)
            q_row += 1
            worksheet.write_merge(q_row, q_row, 0, 5, '                                      Projeto',
                                  TEXT_NORMAL_CENTER_EMIS_PROJ)
            worksheet.write_merge(q_row, q_row, 6, 9, '               Fiscalização', TEXT_NORMAL_CENTER_LIB_FIS)
            worksheet.write_merge(q_row, q_row, 10, 14, '               Construtora', TEXT_NORMAL_CENTER_REC_CONS)
        workbook.save(local_file)

    def get_element_layer_nodes(self, node: str, name_attr: str):
        nodes_lyr = QgsProject.instance().mapLayer(ProjectDataManager.get_layers_id().NODES_LAYER_ID)
        all_nodes = nodes_lyr.getFeatures()
        for n in all_nodes:
            if n.attributes()[self.__get_idx_attr(nodes_lyr, 'nodes', 'name')] == node:
                return n.attributes()[self.__get_idx_attr(nodes_lyr, 'nodes', name_attr)]
        return

    def __get_idx_attr(self, layer: QgsVectorLayer, name_lyr: str, name_attr: str):
        attrs = layer.fields().names()
        return attrs.index(self.__get_json_attr(name_lyr, name_attr))

    def __get_idx_attr_segments(self, name_attr: str):
        attrs = self.segments.fields().names()
        return attrs.index(self.__get_json_attr('segments', name_attr))

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

    def __set_data_json(self):
        plg_dir = os.path.dirname(__file__)
        plg_dir = plg_dir.replace('core' + os.sep + 'xls', 'resources' + os.sep + 'localizations' + os.sep)
        lang = ProjectDataManager.get_language_project().LANGUAGE
        lang = lang if lang != '' else get_language_file()
        file_json = open(os.path.join(plg_dir, lang + '.json'), 'r')
        self.data_json = json.load(file_json)
        file_json.close()

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


TEXT_BOLD_CENTER_12_BORDER = easyxf('font: name Arial, height 240, bold True; '
                                    'align: vert center, horiz center;'
                                    'borders: left 2, right 2, top 2, bottom 0;')
TEXT_BOLD_LEFT_12 = easyxf('font: name Arial, height 240, bold True; '
                           'align: vert center, horiz left; borders: left 2, right 0, top 2, bottom 1;')
TEXT_BOLD_LEFT_12_QUADRA = easyxf('font: name Arial, height 240, bold True; '
                                  'align: vert center, horiz left; '
                                  'borders: left 2, right 0, top 2, bottom 1;')
TEXT_NORMAL_CENTER_12_QUADRA = easyxf('font: name Arial, height 240; '
                                      'align: vert center, horiz center; '
                                      'borders: left 0, right 1, top 2, bottom 1;')
TEXT_NORMAL_LEFT_12_QUADRA = easyxf('font: name Arial, height 240; '
                                    'align: vert center, horiz left; '
                                    'borders: left 1, right 0, top 2, bottom 1;')
TEXT_BOLD_LEFT_12_RAMAL = easyxf('font: name Arial, height 240, bold True; '
                                 'align: vert center, horiz left; '
                                 'borders: left 0, right 0, top 2, bottom 1;')
TEXT_NORMAL_CENTER_12_RAMAL = easyxf('font: name Arial, height 240; '
                                     'align: vert center, horiz center; '
                                     'borders: left 0, right 2, top 2, bottom 1;')
TEXT_BOLD_CENTER_10_RAMAL = easyxf('font: name Arial, height 200, bold True; '
                                   'align: vert center, horiz center; '
                                   'borders: left 2, right 2, top 0, bottom 0;')
TEXT_BOLD_CENTER_10_OS = easyxf('font: name Arial, height 200, bold True; '
                                'align: vert center, horiz center;'
                                'borders: left 2, right 2, top 0, bottom 2;')
TEXT_BOLD_LEFT_12_BACIA = easyxf('font: name Arial, height 240, bold True; '
                                 'align: vert center, horiz left; '
                                 'borders: left 2, right 0, top 1, bottom 1;')
TEXT_NORMAL_CENTER_12_BACIA = easyxf('font: name Arial, height 240; '
                                     'align: vert center, horiz center; '
                                     'borders: left 0, right 0, top 1, bottom 1;')
TEXT_BOLD_LEFT_12_DATA = easyxf('font: name Arial, height 240, bold True; '
                                'align: vert center, horiz left; '
                                'borders: left 0, right 0, top 1, bottom 1;')
TEXT_NORMAL_CENTER_12_DATA = easyxf('font: name Arial, height 240; '
                                    'align: vert center, horiz center; '
                                    'borders: left 0, right 2, top 1, bottom 1;',
                                    num_format_str='DD/MM/YYYY')
TEXT_NORMAL_RIGHT_PROF = easyxf('font: name Arial, height 160; align: vert center, horiz right; '
                                'borders: left 2, right 0, top 1, bottom 2;')
TEXT_NORMAL_CENTER_PROF = easyxf('font: name Arial, height 160; align: vert center, horiz center; '
                                 'borders: left 0, right 0, top 1, bottom 2;')
TEXT_NORMAL_RIGHT_DECLIV = easyxf('font: name Arial, height 160; align: vert center, horiz right; '
                                  'borders: left 0, right 0, top 1, bottom 2;')
TEXT_NORMAL_CENTER_DECLIV = easyxf('font: name Arial, height 160; align: vert center, horiz center; '
                                   'borders: left 0, right 2, top 1, bottom 2;')
TEXT_BOLD_CENTER_12_QUANT = easyxf('font: name Arial, height 240, bold True; '
                                   'align: vert center, horiz center; '
                                   'borders: left 0, right 0, top 0, bottom 2;')
TEXT_NORMAL_LEFT_REV = easyxf('font: name Arial, height 160; align: vert center, horiz left; '
                              'borders: left 2, right 0, top 2, bottom 1;')
TEXT_NORMAL_CENTER_REV = easyxf('font: name Arial, height 160; align: vert center, horiz center; '
                                'borders: left 0, right 1, top 2, bottom 1;')
TEXT_NORMAL_LEFT_DATA_REV = easyxf('font: name Arial, height 160; align: vert center, horiz left; '
                                   'borders: left 1, right 1, top 2, bottom 1;')
TEXT_NORMAL_LEFT_DATA_BRANCH = easyxf('font: name Arial, height 160; align: vert center, horiz left; '
                                      'borders: left 1, right 1, top 1, bottom 1;')
TEXT_NORMAL_CENTER_EXTEN = easyxf('font: name Arial, height 160; align: vert center, horiz center; '
                                  'borders: left 1, right 2, top 2, bottom 1;')
TEXT_NORMAL_CENTER_BRANCH = easyxf('font: name Arial, height 160; align: vert center, horiz center; '
                                   'borders: left 1, right 2, top 1, bottom 1;', num_format_str='#,##0.00')
TEXT_NORMAL_LEFT_NULL = easyxf('font: name Arial, height 160; align: vert center, horiz center; '
                               'borders: left 2, right 1, top 1, bottom 1;')
TEXT_NORMAL_RIGHT_NULL = easyxf('font: name Arial, height 160; align: vert center, horiz center; '
                                'borders: left 1, right 2, top 1, bottom 1;')
TEXT_NORMAL_CENTER_NULL = easyxf('font: name Arial, height 160; align: vert center, horiz center; '
                                 'borders: left 1, right 1, top 1, bottom 1;')
TEXT_NORMAL_LEFT_TUBO = easyxf('font: name Arial, height 160; align: vert center, horiz left; '
                               'borders: left 2, right 0, top 1, bottom 2;')
TEXT_NORMAL_CENTER_TUBO = easyxf('font: name Arial, height 160; align: vert center, horiz center; '
                                 'borders: left 0, right 0, top 1, bottom 2;')
TEXT_NORMAL_MERGE_TUBO_L = easyxf('font: name Arial, height 160; align: vert center, horiz left; '
                                  'borders: left 0, right 1, top 1, bottom 2;')
TEXT_NORMAL_MERGE_TUBO_R = easyxf('font: name Arial, height 160; align: vert center, horiz left; '
                                  'borders: left 1, right 2, top 1, bottom 2;')
TEXT_NORMAL_CENTER_CAIXA = easyxf('font: name Arial, height 160; '
                                  'align: wrap on, vert center, horiz center; '
                                  'borders: left 2, right 1, top 2, bottom 1;')
TEXT_NORMAL_CENTER_HEADER_V = easyxf('font: name Arial, height 160; '
                                     'align: wrap on, vert center, horiz center; '
                                     'borders: left 1, right 1, top 2, bottom 2;')
TEXT_NORMAL_CENTER_HEADER_H = easyxf('font: name Arial, height 160; '
                                     'align: wrap on, vert center, horiz center; '
                                     'borders: left 1, right 1, top 2, bottom 1;')
TEXT_NORMAL_CENTER_HEADER_OBS = easyxf('font: name Arial, height 160; align: vert center, horiz center; '
                                       'borders: left 1, right 2, top 2, bottom 2;')
TEXT_NORMAL_CENTER_HEADER_BOTTON_L = easyxf('font: name Arial, height 160; '
                                            'align: vert center, horiz center; '
                                            'borders: left 2, right 1, top 1, bottom 2;')
TEXT_NORMAL_CENTER_HEADER_BOTTON_R = easyxf('font: name Arial, height 160; '
                                            'align: vert center, horiz center; '
                                            'borders: left 1, right 1, top 1, bottom 2;')
TEXT_NORMAL_CENTER_BODY_L = easyxf('font: name Arial, height 160; align: vert center, horiz center; '
                                   'borders: left 2, right 1, bottom 1;')
NUMBER_NORMAL_CENTER_BODY_C = easyxf('font: name Arial, height 160; align: vert center, horiz center; '
                                     'borders: left 1, right 1, bottom 1;', num_format_str='#,##0.00')
NUMBER_NORMAL_CENTER_BODY_C_000 = easyxf('font: name Arial, height 160; align: vert center, horiz center; '
                                         'borders: left 1, right 1, bottom 1;', num_format_str='#,##0.000')
NUMBER_NORMAL_CENTER_BODY_C_0 = easyxf('font: name Arial, height 160; align: vert center, horiz center; '
                                       'borders: left 1, right 1, bottom 1;', num_format_str='#,##0.0')
TEXT_NORMAL_CENTER_BODY_R = easyxf('font: name Arial, height 160; align: vert center, horiz center; '
                                   'borders: left 1, right 2, bottom 1;', num_format_str='#,##0.00')
TEXT_BOLD_CENTER_OBS_0 = easyxf('font: name Arial, height 240, bold True; '
                                'align: vert center, horiz center; '
                                'borders: left 2, right 2, top 2, bottom 0;')
TEXT_NORMAL_CENTER_OBS_1 = easyxf('font: name Arial, height 200; align: vert center, horiz left; '
                                  'borders: left 2, right 0, top 0, bottom 0;')
TEXT_NORMAL_CENTER_OBS_2 = easyxf('font: name Arial, height 200; align: vert center, horiz center; '
                                  'borders: left 0, right 2, top 0, bottom 0;')
TEXT_NORMAL_CENTER_OBS_3 = easyxf('font: name Arial, height 200; align: vert center, horiz center; '
                                  'borders: left 2, right 2, top 0, bottom 0;')
TEXT_NORMAL_LEFT_EMIS = easyxf('font: name Arial, height 160; align: vert center, horiz left; '
                               'borders: left 2, right 1, top 2, bottom 0;')
TEXT_NORMAL_CENTER_EMIS_POR = easyxf('font: name Arial, height 160; align: vert center, horiz center; '
                                     'borders: left 2, right 0, top 0, bottom 0;')
TEXT_NORMAL_CENTER_EMIS_ROW = easyxf('font: name Arial, height 160; align: vert center, horiz center; '
                                     'borders: left 0, right 1, top 0, bottom 0;')
TEXT_NORMAL_CENTER_EMIS_PROJ = easyxf('font: name Arial, height 160; align: vert center, horiz center; '
                                      'borders: left 2, right 1, top 0, bottom 2;')
TEXT_NORMAL_CENTER_LIB = easyxf('font: name Arial, height 160; align: vert center, horiz center; '
                                'borders: left 1, right 1, top 2, bottom 0;')
TEXT_NORMAL_CENTER_LIB_POR = easyxf('font: name Arial, height 160; align: vert center, horiz center; '
                                    'borders: left 1, right 0, top 0, bottom 0;')
TEXT_NORMAL_CENTER_LIB_ROW = easyxf('font: name Arial, height 160; align: vert center, horiz center; '
                                    'borders: left 0, right 1, top 0, bottom 0;')
TEXT_NORMAL_CENTER_LIB_FIS = easyxf('font: name Arial, height 160; align: vert center, horiz center; '
                                    'borders: left 1, right 1, top 0, bottom 2;')
TEXT_NORMAL_CENTER_REC = easyxf('font: name Arial, height 160; align: vert center, horiz center; '
                                'borders: left 1, right 2, top 2, bottom 0;')
TEXT_NORMAL_CENTER_REC_POR = easyxf('font: name Arial, height 160; align: vert center, horiz center; '
                                    'borders: left 1, right 0, top 0, bottom 0;')
TEXT_NORMAL_CENTER_REC_ROW = easyxf('font: name Arial, height 160; align: vert center, horiz center; '
                                    'borders: left 0, right 2, top 0, bottom 0;')
TEXT_NORMAL_CENTER_REC_CONS = easyxf('font: name Arial, height 160; align: vert center, horiz center; '
                                     'borders: left 1, right 2, top 0, bottom 2;')
TEXT_BOLD_LEFT = easyxf('font: name Arial, height 160, bold True; align: vert center, horiz left;')
TEXT_NORMAL_CENTER = easyxf('font: name Arial, height 160; align: wrap on, vert center, horiz center;')
TEXT_NORMAL_LEFT = easyxf('font: name Arial, height 160; align: vert center, horiz left;')
TEXT_NORMAL_RIGHT = easyxf('font: name Arial, height 160; align: vert center, horiz right;')
NUMBER_STYLE = easyxf(num_format_str='#,##0.00')
DATE_STYLE = easyxf(num_format_str='D-MMM-YY')
BORDER_1 = easyxf('borders: left 2, right 2, top 2, bottom 2;')
BORDER_2 = easyxf('borders: left 2, right 2, top 2, bottom 0;')
BORDER_LEFT = easyxf('borders: left 2, right 0, top 0, bottom 0;')
BORDER_RIGHT = easyxf('borders: left 0, right 2, top 0, bottom 0;')
