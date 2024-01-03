import json
import os

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog
from qgis.PyQt.QtWidgets import QMessageBox
from qgis._core import QgsDefaultValue
from qgis.core import QgsMapLayerType, QgsVectorLayer
from qgis.core import QgsProject

from .views.ui_dock_tab_home_base import DockTabHomeBase
from .views.ui_dock_tab_home_create_project import CreateProjectDialog
from ...core.calculate.project import Project
from ...core.data.data_manager import ProjectDataManager
from ...core.data.models import Language, LayerRaster
from ...gui.generate_os_ui import GenerateOsUI
from ...helpers.globals import *
from ...helpers.utils import Utils


class DockTabHome(DockTabHomeBase):
    update_ready = pyqtSignal(dict)

    def __init__(self, dock, iface, title):
        super().__init__(dock, iface, title)
        self.iface = iface
        self.utils = Utils()
        self.create_project_dialog = CreateProjectDialog(self.iface)
        self.proj = Project(self.iface)
        self.generate_os = GenerateOsUI()
        # self.set_layers = SetLayersUI()
        self.data_json = None
        # self.set_layers.pb_start.clicked.connect(self.__set_id_layers)
        # self.set_layers.pb_cancel.clicked.connect(self.__close_set_id_layers)

    def on_layer_selected(self, features_ids):
        pass

    def set_logic(self):
        self.pb_create_project.clicked.connect(self.__create_project)
        QgsProject.instance().layersAdded.connect(self.__layer_add)
        self.pb_update_list_layers.clicked.connect(self.__layer_add)
        self.pb_set_raster.clicked.connect(self.__set_raster_layer)
        self.pb_calculate.clicked.connect(self.__update_calculate)
        self.pb_generate_os.clicked.connect(self.__produces_xls_os)
        # self.pb_set_layers.clicked.connect(self.__show_set_vector_layers)

    def __create_project(self):
        # gets if it accepted or not, if yes, it will create the project
        if self.create_project_dialog.exec_() == QDialog.Accepted:
            set_language_file(self.create_project_dialog.cb_local.currentText()[-6:-1])
            ProjectDataManager.save_language_project(
                language=Language(LANGUAGE=self.create_project_dialog.cb_local.currentText()[-6:-1]))
            self.dock.reload()

    def __layer_add(self):
        list_layers = QgsProject.instance().mapLayers().values()
        raster_layers = []
        self.cb_raster.clear()
        for i in list_layers:
            if i.type() != QgsMapLayerType.VectorLayer:
                raster_layers.append(i.name())
        self.cb_raster.addItems(raster_layers)
        # self.__recognize_vector_layers()

    def __set_raster_layer(self):
        response = self.utils.show_dialog_question(title=self.title, message=(self.tr('Confirma a seleção da camada ') +
                                                                              self.cb_raster.currentText() + ':'))
        if response:
            nodes = self.proj.getNodesLayer()
            default_value = QgsDefaultValue(expression='', applyOnUpdate=False)
            q_terrain_ex = nodes.defaultValueDefinition(self.__get_idx_attr(nodes, 'nodes', 'q_terrain')).expression()
            if ProjectDataManager.get_layer_raster().LAYER_RASTER == '':
                q_terrain_ex = q_terrain_ex.replace(self.__get_raster_express(), self.cb_raster.currentText())
            else:
                q_terrain_ex = q_terrain_ex.replace(ProjectDataManager.get_layer_raster().LAYER_RASTER, self.cb_raster.currentText())
            default_value.setExpression(q_terrain_ex)
            default_value.setApplyOnUpdate(True)
            nodes.setDefaultValueDefinition(self.__get_idx_attr(nodes, 'nodes', 'q_terrain'), default_value)
            set_layer_raster(self.cb_raster.currentText())
            ProjectDataManager.save_layer_raster(layer_raster=LayerRaster(LAYER_RASTER=self.cb_raster.currentText()))
            self.utils.show_dialog(title=self.title, message=self.tr('Camadar raster definida com sucesso!'),
                                   information=QMessageBox.Information)
        else:
            self.utils.show_dialog(title=self.title, message=self.tr('Uma camada raster deve ser definida!'),
                                   information=QMessageBox.Warning)

    def __get_idx_attr(self, layer: QgsVectorLayer, name_lyr: str, name_attr: str):
        attrs = layer.fields().names()
        return attrs.index(self.__get_json_attr(name_lyr, name_attr))

    def __set_data_json(self):
        plg_dir = os.path.dirname(__file__)
        plg_dir = plg_dir.replace('gui' + os.sep + 'dock_tabs', 'resources' + os.sep + 'localizations' + os.sep)
        lang = ProjectDataManager.get_language_project().LANGUAGE
        lang = lang if lang != '' else get_language_file()
        file_json = open(os.path.join(plg_dir, lang + '.json'), 'r')
        self.data_json = json.load(file_json)
        file_json.close()

    def __get_raster_express(self):
        if self.data_json is None:
            self.__set_data_json()
        return self.data_json['raster']

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

    # def load_data(self):
        # self.set_layers.load_set_layers(self.__get_list_vector_layers())
        # self.__recognize_vector_layers()

    def reload(self):
        # self.load_data()
        pass

    def __update_calculate(self):
        # if ProjectDataManager.is_data_layers_names_loaded():
        self.proj.blockDialog.setData(is_new=False)
        # else:
        #     self.utils.show_dialog(title=self.title,
        #                            message=self.tr('Primeiro selecione as camadas do projeto em Iniciar.'),
        #                            information=QMessageBox.Critical)

    def __produces_xls_os(self):
        if ProjectDataManager.get_status_calculation():
            self.generate_os.show_generate_os()
        else:
            self.utils.show_dialog(title=self.tr('SaniHub Ramal'),
                                   message=self.tr('Antes de gerar a OS, clique em Atualizar Cálculos. '),
                                   information=QMessageBox.Critical)

    # def __show_set_vector_layers(self):
    #     self.set_layers.show_set_layers(self.__get_list_vector_layers())

    # def __set_id_layers(self):
    #     def get_id_layer(name_layer) -> str:
    #         layer = QgsProject.instance().mapLayersByName(name_layer)
    #         if len(layer) == 1:
    #             return layer[0].id()
    #         return
    #
    #     if self.set_layers.check_selection_layers():
    #         set_language_file(self.set_layers.cb_language.currentText()[-6:-1])
    #         ProjectDataManager.save_language_project(
    #             language=Language(LANGUAGE=self.set_layers.cb_language.currentText()[-6:-1]))
    #         ProjectDataManager.save_layers_id(layers_data=LayersData(
    #             BLOCKS_LAYER_ID=get_id_layer(self.set_layers.cb_blocks.currentText()),
    #             NODES_LAYER_ID=get_id_layer(self.set_layers.cb_nodes.currentText()),
    #             SEGMENTS_LAYER_ID=get_id_layer(self.set_layers.cb_segments.currentText()),
    #             LINEAR_OBSTACLES_LAYER_ID=get_id_layer(self.set_layers.cb_linear_obstacles.currentText()),
    #             POINT_OBSTACLES_LAYER_ID=get_id_layer(self.set_layers.cb_points_obstacles.currentText()),
    #             ACCESSORIES_LAYER_ID=get_id_layer(self.set_layers.cb_accessories.currentText())
    #         ))
    #         # self.proj.blockDialog.setData(is_new=False)
    #         self.utils.show_dialog(title=self.title, message=self.tr('Camadas definidas com sucesso!'),
    #                                information=QMessageBox.Information)
    #         self.set_layers.close()
    #     else:
    #         self.utils.show_dialog(title=self.title, message=self.tr('Todas as camadas devem ser identificadas!'),
    #                                information=QMessageBox.Critical)
    #
    # def __close_set_id_layers(self):
    #     self.set_layers.close()

    @staticmethod
    def __get_list_vector_layers():
        layers = [l for l in QgsProject().instance().mapLayers().values() if isinstance(l, QgsVectorLayer)]
        layerList = [layer.name() for layer in layers]
        layerList.insert(0, '')
        return layerList

    # def __recognize_vector_layers(self):
    #     if ProjectDataManager.is_data_layers_id_loaded():
    #         self.lb_status_layers.setText(self.tr('Camadas reconhecidas!'))
    #         self.lb_status_layers.setStyleSheet(
    #             'background-color: lightgreen; border: 1px solid green; border-style: outset; border-radius: 10px;')
    #         self.lb_status_layers.setAlignment(Qt.AlignCenter)
    #         # self.pb_set_layers.setEnabled(False)
    #     else:
    #         self.lb_status_layers.setText(self.tr('Definir camadas!'))
    #         self.lb_status_layers.setStyleSheet(
    #             'background-color: rgb(235,142,141); border: 1px solid red; border-style: outset; border-radius: 10px;')
    #         self.lb_status_layers.setAlignment(Qt.AlignCenter)
    #         self.pb_set_layers.setEnabled(True)
