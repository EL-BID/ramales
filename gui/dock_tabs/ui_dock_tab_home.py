import json
import os

from PyQt5.QtCore import pyqtSignal, QCoreApplication
from PyQt5.QtWidgets import QDialog
from qgis.PyQt.QtWidgets import QMessageBox
from qgis._core import QgsDefaultValue, QgsFeature
from qgis.core import QgsMapLayerType, QgsVectorLayer
from qgis.core import QgsProject, edit

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
        self.proj.blockDialog.accepted.connect(lambda: self.dock.reload())
        # self.pb_set_layers.clicked.connect(self.__show_set_vector_layers)

    def __create_project(self):
        # gets if it accepted or not, if yes, it will create the project
        if self.create_project_dialog.exec_() == QDialog.Accepted:
            set_language_file(self.create_project_dialog.cb_local.currentText()[-6:-1])
            ProjectDataManager.save_language_project(
                language=Language(LANGUAGE=self.create_project_dialog.cb_local.currentText()[-6:-1]))
            self.__init_resume_frame()
            #self.__set_file_layout()
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
        response = self.utils.show_dialog_question(title=self.title,
                                                   message=(self.tr('Confirma a seleção da camada ') +
                                                            self.cb_raster.currentText() + ':'))
        if response:
            nodes = self.proj.getNodesLayer()
            default_value = QgsDefaultValue(expression='', applyOnUpdate=False)
            q_terrain_ex = nodes.defaultValueDefinition(self.__get_idx_attr(nodes, 'nodes', 'q_terrain')).expression()
            if ProjectDataManager.get_layer_raster().LAYER_RASTER == '':
                q_terrain_ex = q_terrain_ex.replace(self.__get_raster_express(), self.cb_raster.currentText())
            else:
                q_terrain_ex = q_terrain_ex.replace(ProjectDataManager.get_layer_raster().LAYER_RASTER,
                                                    self.cb_raster.currentText())
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

    @staticmethod
    def __get_list_vector_layers():
        layers = [l for l in QgsProject().instance().mapLayers().values() if isinstance(l, QgsVectorLayer)]
        layerList = [layer.name() for layer in layers]
        layerList.insert(0, '')
        return layerList

    def __init_resume_frame(self):
        resume_frame = QgsProject.instance().mapLayer(ProjectDataManager.get_layers_id().RESUME_FRAME_LAYER_ID)
        feat_exist = None

        with edit(resume_frame):
            feature = QgsFeature(resume_frame.fields())
            resume_frame.addFeature(feature)
            for feat in resume_frame.getFeatures():
                feat_exist = feat.id()
                break
            attributes = {
                self.utils.get_json_attr('resume_frame', 'length_segments_DN100(m)'): 0,
                self.utils.get_json_attr('resume_frame', 'length_TQ_DN100'): 0,
                self.utils.get_json_attr('resume_frame', 'length_total_DN100(m)'): 0,
                self.utils.get_json_attr('resume_frame', "length_segments_DN150(m)"): 0,
                self.utils.get_json_attr('resume_frame', "length_TQ_DN150(m)"): 0,
                self.utils.get_json_attr('resume_frame', "length_total_DN150(m)"): 0,
                self.utils.get_json_attr('resume_frame', "length_total(m)"): 0,
                self.utils.get_json_attr('resume_frame', "box_Ø40"): 0,
                self.utils.get_json_attr('resume_frame', "box_Ø60"): 0,
                self.utils.get_json_attr('resume_frame', "box_rect_brick"): 0,
                self.utils.get_json_attr('resume_frame', "cx_ret_concret"): 0,
                self.utils.get_json_attr('resume_frame', "TIL"): 0,
                self.utils.get_json_attr('resume_frame', "total_inspection"): 0,
                self.utils.get_json_attr('resume_frame', "saddle"): 0,
                self.utils.get_json_attr('resume_frame', "C90º"): 0,
                self.utils.get_json_attr('resume_frame', "TE"): 0,
                self.utils.get_json_attr('resume_frame', "buildings"): 0,
                self.utils.get_json_attr('resume_frame', "economies"): 0,
                self.utils.get_json_attr('resume_frame', "service_lane"): 0,
                self.utils.get_json_attr('resume_frame', "economies_final"): 0,
                self.utils.get_json_attr('resume_frame', "flow_initial"): 0,
                self.utils.get_json_attr('resume_frame', "flow_final"): 0,
            }
            for field, value in attributes.items():
                if feat_exist is not None:
                    resume_frame.changeAttributeValue(feat_exist,
                                                      self.utils.get_idx_attr(resume_frame, 'resume_frame', field),
                                                      value)
                else:
                    feature.setAttribute(field, value)
                    resume_frame.addFeature(feature)
