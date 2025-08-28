import json

from PyQt5.QtCore import Qt, QLocale, QCoreApplication, QVariant
from qgis._core import QgsProject, QgsVectorLayer
from xlwt import Workbook, easyxf
import os

from ...helpers.utils import Utils
from ...helpers.globals import get_language_file
from ...core.data.data_manager import ProjectDataManager


class ProducesReportOSXls:

    def __init__(self):
        self.data_json = None
        self.segments = None
        self.loc = QLocale()
        self.MAX_COLUMN = 15
        self.utils = Utils()

    def translate(self, msg, disambiguation=None, n=-1) -> object:
        return QCoreApplication.translate(ProducesReportOSXls.__name__, msg, disambiguation, n)

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
        segments = sorted(segments, key=lambda item:
        (item[self.utils.get_idx_attr(self.segments, 'segments', 'branch_id')],
         item[self.utils.get_idx_attr(self.segments, 'segments', 'segment_id')]))
        branchs = []
        for feat in segments:
            branchs.append(feat[self.utils.get_idx_attr_segments('branch_id')])

        branchs = set(branchs)
        workbook = Workbook()
        for branch in branchs:
            q_row = 0
            for feat in segments:
                if feat[self.utils.get_idx_attr_segments('branch_id')] == branch:
                    q_row += 1
            worksheet = workbook.add_sheet('R-' + str(branch), cell_overwrite_ok=True)
            worksheet.set_fit_num_pages(1)
            worksheet.show_grid = False

            is_aerial = False
            h_branch = 0.00
            for feat in segments:
                if feat[self.utils.get_idx_attr_segments('branch_id')] == branch:
                    branch_position = int(feat[self.utils.get_idx_attr_segments("branch_position")])
                    if branch_position == 2:
                        is_aerial = True
                        h_branch = self.utils.get_element_layer_nodes(
                            node=feat[self.utils.get_idx_attr_segments('up_box')], name_attr='h_branch')
                    break

            # CAIXA
            worksheet.col(0).width = 2000
            worksheet.col(1).width = 2100

            # DISTÂNCIA
            worksheet.col(2).width = 1550

            # COTA TERRENO
            worksheet.col(3).width = 1550
            worksheet.col(4).width = 1550

            # COTA RAMAL
            worksheet.col(5).width = 1550
            worksheet.col(6).width = 1550

            # PROFUNDIDADE
            worksheet.col(7).width = 1700
            worksheet.col(8).width = 1700

            # GABARITO
            worksheet.col(9).width = 1550

            # COTA RÉGUA
            worksheet.col(10).width = 1550
            worksheet.col(11).width = 1550

            # PROF. CRÍTICA
            worksheet.col(12).width = 1550

            # CAIM. TRECHO
            worksheet.col(13).width = 1550

            # TUBO DE QUEDA
            worksheet.col(14).width = 2600

            # OBS
            worksheet.col(15).width = 2600

            worksheet.row(7).height_mismatch = True
            worksheet.row(7).height = 130
            worksheet.row(11).height_mismatch = True
            worksheet.row(11).height = 130
            worksheet.row(16).height_mismatch = True
            worksheet.row(16).height = 130
            worksheet.write_merge(0, 2, 0, self.MAX_COLUMN, '', BORDER_1)
            worksheet.write(4, 0, '', BORDER_LEFT)
            worksheet.write(4, self.MAX_COLUMN, '', BORDER_RIGHT)
            worksheet.write_merge(3, 3, 0, self.MAX_COLUMN, self.translate('SISTEMA DE ESGOTAMENTO SANITÁRIO'),
                                  TEXT_BOLD_CENTER_12_BORDER)
            worksheet.write_merge(5, 5, 0, self.MAX_COLUMN, self.translate('ORDEM DE SERVIÇO PARA GABARITO - RAMAL'),
                                  TEXT_BOLD_CENTER_10_RAMAL)
            worksheet.write_merge(6, 6, 0, self.MAX_COLUMN, list_block_values[10], TEXT_BOLD_CENTER_10_OS)

            worksheet.write_merge(8, 8, 0, 1, self.translate('QUADRA:'), TEXT_BOLD_LEFT_12_QUADRA)
            worksheet.write(8, 2, list_block_values[1], TEXT_NORMAL_CENTER_12_QUADRA)
            worksheet.write_merge(8, 8, 3, 10, '', TEXT_NORMAL_LEFT_12_QUADRA)
            worksheet.write_merge(8, 8, 11, 12, self.translate('RAMAL:'), TEXT_BOLD_LEFT_12_RAMAL)
            worksheet.write_merge(8, 8, 13, self.MAX_COLUMN, self.translate('R-') + str(branch),
                                  TEXT_NORMAL_CENTER_12_RAMAL)
            worksheet.write_merge(9, 9, 0, 1, self.translate('BACIA:'), TEXT_BOLD_LEFT_12_BACIA)
            worksheet.write_merge(9, 9, 2, 4, list_block_values[3], TEXT_NORMAL_CENTER_12_BACIA)
            worksheet.write_merge(9, 9, 5, 9, '', TEXT_NORMAL_CENTER_12_BACIA)
            worksheet.write_merge(9, 9, 10, 11, self.translate('DATA:'), TEXT_BOLD_LEFT_12_DATA)
            worksheet.write_merge(9, 9, 12, self.MAX_COLUMN,
                                  str(list_block_values[2].toString(Qt.DefaultLocaleShortDate)).split()[0],
                                  TEXT_NORMAL_CENTER_12_DATA)

            worksheet.write_merge(10, 10, 0, 2, self.translate('PROF.MÍNIMA (m):'), TEXT_NORMAL_RIGHT_PROF)
            worksheet.write(10, 3, '', TEXT_NORMAL_CENTER_PROF)
            worksheet.write_merge(10, 10, 4, 8, list_block_values[4], TEXT_NORMAL_CENTER_PROF)
            worksheet.write(10, 9, '', TEXT_NORMAL_CENTER_PROF)
            worksheet.write_merge(10, 10, 9, 13, self.translate('DECLIVIDADE MÍNIMA (m/m):'), TEXT_NORMAL_RIGHT_DECLIV)
            worksheet.write_merge(10, 10, self.MAX_COLUMN - 1, self.MAX_COLUMN, list_block_values[5],
                                  TEXT_NORMAL_CENTER_DECLIV)

            worksheet.write_merge(12, 12, 0, self.MAX_COLUMN, self.translate('QUANTITATIVOS'),
                                  TEXT_BOLD_CENTER_12_QUANT)
            worksheet.write(13, 0, self.translate('REV.:'), TEXT_NORMAL_LEFT_REV)
            worksheet.write_merge(13, 13, 1, 2, list_block_values[6], TEXT_NORMAL_CENTER_REV)
            worksheet.write_merge(13, 13, 3, 4, self.translate('Data Rev.:'), TEXT_NORMAL_LEFT_DATA_REV)
            worksheet.write_merge(13, 13, 5, 7,
                                  str(list_block_values[7].toString(Qt.DefaultLocaleShortDate)).split()[0],
                                  TEXT_NORMAL_LEFT_DATA_REV)
            worksheet.write_merge(13, 13, 8, self.MAX_COLUMN - 3, '', TEXT_NORMAL_LEFT_DATA_REV)
            worksheet.write_merge(13, 13, self.MAX_COLUMN - 2, self.MAX_COLUMN - 1, self.translate('Extensão total:'),
                                  TEXT_NORMAL_LEFT_DATA_REV)
            worksheet.write(13, self.MAX_COLUMN, list_block_values[8], TEXT_NORMAL_CENTER_EXTEN)
            worksheet.write_merge(14, 14, 0, 7, '', TEXT_NORMAL_LEFT_NULL)
            worksheet.write_merge(14, 14, 8, self.MAX_COLUMN - 3, '', TEXT_NORMAL_CENTER_NULL)
            worksheet.write_merge(14, 14, self.MAX_COLUMN - 2, self.MAX_COLUMN - 1, self.translate('Extensão ramal:'),
                                  TEXT_NORMAL_LEFT_DATA_BRANCH)

            if is_aerial:
                worksheet.write_merge(15, 15, 0, 7, '', TEXT_NORMAL_LEFT_NULL)
                worksheet.write_merge(15, 15, 8, self.MAX_COLUMN - 3, '', TEXT_NORMAL_CENTER_NULL)
                worksheet.write_merge(15, 15, self.MAX_COLUMN - 2, self.MAX_COLUMN - 1, self.translate('H'),
                                      TEXT_NORMAL_LEFT_DATA_BRANCH)
                # Get, from caixa in up_box, the h_branch
                worksheet.write(15, self.MAX_COLUMN,
                                h_branch if type(h_branch) is not QVariant else 0.00,
                                TEXT_NORMAL_CENTER_BRANCH)
            else:
                worksheet.write_merge(15, 15, 0, 3, '', TEXT_NORMAL_LEFT_TUBO)
                worksheet.write(15, 4, '', TEXT_NORMAL_CENTER_TUBO)
                worksheet.write_merge(15, 15, 5, 7, '', TEXT_NORMAL_MERGE_TUBO_L)
                worksheet.write_merge(15, 15, 8, self.MAX_COLUMN, '', TEXT_NORMAL_MERGE_TUBO_R)

            worksheet.write_merge(17, 18, 0, 1, self.translate('CAIXA'), TEXT_NORMAL_CENTER_CAIXA)
            worksheet.write_merge(17, 19, 2, 2, self.translate('DISTÂNCIA (m)'), TEXT_NORMAL_CENTER_HEADER_V)
            worksheet.write_merge(17, 18, 3, 4, self.translate('COTA TERRENO (m)'), TEXT_NORMAL_CENTER_HEADER_H)
            worksheet.write_merge(17, 18, 5, 6, self.translate('COTA RAMAL (m)'), TEXT_NORMAL_CENTER_HEADER_H)
            worksheet.write_merge(17, 18, 7, 8, self.translate('ALTURA / PROFUNDIDADE (m)'),
                                  TEXT_NORMAL_CENTER_HEADER_H)
            worksheet.write_merge(17, 19, 9, 9, self.translate('GABARITO (m)'), TEXT_NORMAL_CENTER_HEADER_V)
            worksheet.write_merge(17, 18, 10, 11, self.translate('COTA RÉGUA (m)'), TEXT_NORMAL_CENTER_HEADER_H)
            worksheet.write_merge(17, 19, 12, 12, self.translate('PROF. CRÍTICA (m)'), TEXT_NORMAL_CENTER_HEADER_V)
            worksheet.write_merge(17, 19, 13, 13, self.translate('CAIM. TRECHO (cm)'), TEXT_NORMAL_CENTER_HEADER_V)
            worksheet.write_merge(17, 19, 14, 14, self.translate('TUBO DE QUEDA (m)'), TEXT_NORMAL_CENTER_HEADER_V)
            worksheet.write_merge(17, 19, 15, 15, self.translate('OBS'), TEXT_NORMAL_CENTER_HEADER_OBS)
            worksheet.write(19, 0, self.translate('MONT.'), TEXT_NORMAL_CENTER_HEADER_BOTTON_L)
            worksheet.write(19, 1, self.translate('JUS.'), TEXT_NORMAL_CENTER_HEADER_BOTTON_R)
            worksheet.write(19, 3, self.translate('MONT.'), TEXT_NORMAL_CENTER_HEADER_BOTTON_R)
            worksheet.write(19, 4, self.translate('JUS.'), TEXT_NORMAL_CENTER_HEADER_BOTTON_R)
            worksheet.write(19, 5, self.translate('MONT.'), TEXT_NORMAL_CENTER_HEADER_BOTTON_R)
            worksheet.write(19, 6, self.translate('JUS.'), TEXT_NORMAL_CENTER_HEADER_BOTTON_R)
            worksheet.write(19, 7, self.translate('MONT.'), TEXT_NORMAL_CENTER_HEADER_BOTTON_R)
            worksheet.write(19, 8, self.translate('JUS.'), TEXT_NORMAL_CENTER_HEADER_BOTTON_R)
            worksheet.write(19, 10, self.translate('MONT.'), TEXT_NORMAL_CENTER_HEADER_BOTTON_R)
            worksheet.write(19, 11, self.translate('JUS.'), TEXT_NORMAL_CENTER_HEADER_BOTTON_R)
            q_row += 20
            row = 20
            branch_length = 0.00
            for i, feat in enumerate(segments):
                if feat[self.utils.get_idx_attr_segments('branch_id')] == branch:
                    worksheet.write(row, 0, str(feat[self.utils.get_idx_attr_segments('up_box')]),
                                    TEXT_NORMAL_CENTER_BODY_L)
                    worksheet.write(row, 1, str(feat[self.utils.get_idx_attr_segments('down_box')]),
                                    NUMBER_NORMAL_CENTER_BODY_C)
                    worksheet.write(row, 2,
                                    self.utils.str_to_float_locale(feat[self.utils.get_idx_attr_segments('length')]),
                                    NUMBER_NORMAL_CENTER_BODY_C)
                    branch_length += self.utils.str_to_float_locale(feat[self.utils.get_idx_attr_segments('length')])
                    branch_pos = (
                        self.utils.get_key_map_of_values(layer=self.segments,
                                                         idx_col=self.utils.get_idx_attr(self.segments, 'segments',
                                                                                         'branch_position'),
                                                         value=segments[i].attributes()[
                                                             self.utils.get_idx_attr(self.segments, 'segments',
                                                                                     'branch_position')]))
                    worksheet.write(row, 3, self.utils.str_to_float_locale(self.utils.get_element_layer_nodes(
                        node=feat[self.utils.get_idx_attr_segments('up_box')], name_attr='q_terrain')),
                                    NUMBER_NORMAL_CENTER_BODY_C_000)
                    worksheet.write(row, 4, self.utils.str_to_float_locale(self.utils.get_element_layer_nodes(
                        node=feat[self.utils.get_idx_attr_segments('down_box')], name_attr='q_terrain')),
                                    NUMBER_NORMAL_CENTER_BODY_C_000)
                    worksheet.write(row, 5,
                                    self.utils.str_to_float_locale(
                                        feat[self.utils.get_idx_attr_segments('up_qproject')]),
                                    NUMBER_NORMAL_CENTER_BODY_C_000)
                    worksheet.write(row, 6,
                                    self.utils.str_to_float_locale(
                                        feat[self.utils.get_idx_attr_segments('dwn_qproject')]),
                                    NUMBER_NORMAL_CENTER_BODY_C_000)
                    if row == 20:
                        if (branch_pos == self.utils.get_json_attr(name_lyr='bool_air', attribute='underground') and
                                self.utils.get_element_layer_nodes(
                                    node=feat[self.utils.get_idx_attr_segments('up_box')], name_attr='depth') <
                                self.utils.get_element_layer_blocks(name_attr='min_depth')):
                            worksheet.write(row, 7,
                                            self.utils.str_to_float_locale(
                                                self.utils.get_element_layer_blocks(name_attr='min_depth')),
                                            NUMBER_NORMAL_CENTER_BODY_C)
                        else:
                            worksheet.write(row, 7, self.utils.str_to_float_locale(self.utils.get_element_layer_nodes(
                                node=feat[self.utils.get_idx_attr_segments('up_box')], name_attr='depth')),
                                            NUMBER_NORMAL_CENTER_BODY_C)
                    else:
                        worksheet.write(row, 7, self.utils.str_to_float_locale(self.utils.get_element_layer_nodes(
                            node=feat[self.utils.get_idx_attr_segments('up_box')], name_attr='q_terrain')) -
                                        float(feat[self.utils.get_idx_attr_segments('up_qproject')]),
                                        NUMBER_NORMAL_CENTER_BODY_C)
                    worksheet.write(row, 8, self.utils.str_to_float_locale(self.utils.get_element_layer_nodes(
                        node=feat[self.utils.get_idx_attr_segments('down_box')], name_attr='depth')),
                                    NUMBER_NORMAL_CENTER_BODY_C)
                    worksheet.write(row, 9, self.utils.str_to_float_locale(self.utils.get_element_layer_nodes(
                        node=feat[self.utils.get_idx_attr_segments('up_box')], name_attr='template')),
                                    NUMBER_NORMAL_CENTER_BODY_C)
                    worksheet.write(row, 10, self.utils.str_to_float_locale(self.utils.get_element_layer_nodes(
                        node=feat[self.utils.get_idx_attr_segments('up_box')], name_attr='q_rule')),
                                    NUMBER_NORMAL_CENTER_BODY_C_000)
                    worksheet.write(row, 11, self.utils.str_to_float_locale(self.utils.get_element_layer_nodes(
                        node=feat[self.utils.get_idx_attr_segments('down_box')], name_attr='q_rule')),
                                    NUMBER_NORMAL_CENTER_BODY_C_000)
                    worksheet.write(row, 12, self.utils.str_to_float_locale(self.utils.get_element_layer_nodes(
                        node=feat[self.utils.get_idx_attr_segments('up_box')], name_attr='critical_depth')),
                                    NUMBER_NORMAL_CENTER_BODY_C)
                    worksheet.write(row, 13, self.utils.str_to_float_locale(
                        feat[self.utils.get_idx_attr_segments('unevenness_segment')]),
                                    NUMBER_NORMAL_CENTER_BODY_C_0)
                    worksheet.write(row, 14,
                                    self.utils.str_to_float_locale(feat[self.utils.get_idx_attr_segments('h_tq')]),
                                    NUMBER_NORMAL_CENTER_BODY_C)
                    worksheet.write(row, 15, str(feat[self.utils.get_idx_attr_segments('comments')])
                                    .replace('NULL', '').replace('0.0', ''),
                                    TEXT_NORMAL_CENTER_BODY_R)
                    row += 1
            worksheet.write(14, self.MAX_COLUMN, branch_length, TEXT_NORMAL_CENTER_BRANCH)
            worksheet.write_merge(q_row, q_row, 0, self.MAX_COLUMN, self.translate('NOTAS'), TEXT_BOLD_CENTER_OBS_0)
            q_row += 1
            worksheet.write_merge(q_row, q_row + 11, 0, self.MAX_COLUMN, '', TEXT_NOTES_SPACE)
            q_row += 12
            worksheet.write_merge(q_row, q_row, 0, 5, self.translate('Emissão:'), TEXT_NORMAL_LEFT_EMIS)
            worksheet.write_merge(q_row, q_row, 6, 9,
                                  self.translate('Liberação:') + '         /         /             ',
                                  TEXT_NORMAL_CENTER_LIB)
            worksheet.write_merge(q_row, q_row, 10, self.MAX_COLUMN,
                                  self.translate(
                                      'Recebido:') + '         /         /                                     ',
                                  TEXT_NORMAL_CENTER_REC)
            q_row += 1
            worksheet.write_merge(q_row, q_row, 0, 1, self.translate('Por:'), TEXT_NORMAL_CENTER_EMIS_POR)
            worksheet.write_merge(q_row, q_row, 2, 5, '__________________________', TEXT_NORMAL_CENTER_EMIS_ROW)
            worksheet.write(q_row, 6, self.translate('Por:'), TEXT_NORMAL_CENTER_LIB_POR)
            worksheet.write_merge(q_row, q_row, 7, 9, '____________________', TEXT_NORMAL_CENTER_EMIS_ROW)
            worksheet.write(q_row, 10, self.translate('Por:'), TEXT_NORMAL_CENTER_REC_POR)
            worksheet.write_merge(q_row, q_row, 11, self.MAX_COLUMN, '_____________________________',
                                  TEXT_NORMAL_CENTER_REC_ROW)
            q_row += 1
            worksheet.write_merge(q_row, q_row, 0, 5,
                                  '                                      ' + self.translate('Projeto'),
                                  TEXT_NORMAL_CENTER_EMIS_PROJ)
            worksheet.write_merge(q_row, q_row, 6, 9, '               ' + self.translate('Fiscalização'),
                                  TEXT_NORMAL_CENTER_LIB_FIS)
            worksheet.write_merge(q_row, q_row, 10, self.MAX_COLUMN, '               ' + self.translate('Construtora'),
                                  TEXT_NORMAL_CENTER_REC_CONS)
        workbook.save(local_file)


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
                                  'borders: left 1, right 0, top 1, bottom 2;')
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
TEXT_NOTES_SPACE = easyxf('font: name Arial, height 240, bold True; '
                          'align: vert center, horiz center; '
                          'borders: left 2, right 2, top 2, bottom 2;')
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
