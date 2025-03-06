import os

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QPushButton, QLabel, QComboBox, QGroupBox, QVBoxLayout, QBoxLayout, QHBoxLayout)
from qgis.PyQt.QtCore import Qt

from ..base.ui_dock_tab_base import DockTab
from ....helpers.utils import Utils


class DockTabHomeBase(DockTab):


    # def tr(self, message):
    #     # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
    #     return QCoreApplication.translate('SanihubRamales', message)

    def translate(self, msg, disambiguation=None, n=-1) -> object:
        return QCoreApplication.translate(DockTabHomeBase.__name__, msg, disambiguation, n)

    def set_logic(self):
        """Insere a lógica de controle da aba. A ser implementada pelos controladores que
            herdam essa classe."""

    def __init__(self, dock, iface, title):
        super().__init__(dock)
        self.iface = iface
        self.title = title
        self.vb_layout = QVBoxLayout()
        self.gb_project = QGroupBox()
        self.vb_layout_project = QVBoxLayout()
        self.lb_create_project = QLabel(self.translate('Criar projeto Qgis:'))
        self.pb_create_project = QPushButton(self.translate('Criar'))
        self.lb_raster_select = QLabel(self.translate('Selecionar camada raster:'))
        self.cb_raster = QComboBox()
        self.pb_update_list_layers = QPushButton(self.translate('Atualizar camadas'))
        self.pb_set_raster = QPushButton(self.translate('Definir Raster'))
        self.gb_field_data = QGroupBox()
        self.vb_layout_field_data = QVBoxLayout()
        # self.lb_status_layers = QLabel()
        # self.pb_set_layers = QPushButton(self.translate('Definir camadas'))
        self.lb_calculate = QLabel(self.translate('Calcular ramais:'))
        self.pb_calculate = QPushButton(self.translate('Calcular'))
        self.lb_generate_os = QLabel(self.translate('Gerar Os xls:'))
        self.pb_generate_os = QPushButton(self.translate('Gerar'))
        self.logo_label = QLabel()
        self.img_label = QLabel()

        self.utils = Utils()
        self.set_logic()

    def tab_start_ui(self):
        # Add Plugin Logo at the top of the tab
        path = os.path.join(self.utils.get_plugin_dir(), 'icons/saniramales_02.png')
        logo = QPixmap(path)
        self.logo_label.setPixmap(logo.scaled(int(logo.width()/3), int(logo.height()/3), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.vb_layout.addWidget(self.logo_label)

        self.__start_project()
        self.__start_field_data()
        path_img = os.path.join(self.utils.get_plugin_dir(), 'icons/img_quadra.png')
        img = QPixmap(path_img)
        self.img_label.setPixmap(img.scaled(int(img.width()/2), int(img.height()/2), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.vb_layout.addWidget(self.img_label)
        # self.vb_layout.setStretch(0, 0)
        self.vb_layout.setDirection(QBoxLayout.TopToBottom)
        self.vb_layout.addStretch()
        self.setLayout(self.vb_layout)
        #self.setMaximumHeight(350)

    def __start_project(self):
        self.gb_project.setTitle(self.translate('Projeto Ramal'))
        self.lb_create_project.setWordWrap(True)
        self.lb_create_project.setAlignment(Qt.AlignLeft)
        self.vb_layout_project.addWidget(self.lb_create_project)
        self.pb_create_project.setToolTip(self.translate('Criar projeto Qgis para ramal.'))
        self.pb_create_project.setFixedSize(100, 25)
        self.vb_layout_project.addWidget(self.pb_create_project)
        self.lb_raster_select.setWordWrap(True)
        self.vb_layout_project.addWidget(self.lb_raster_select)
        self.vb_layout_project.addWidget(self.cb_raster)
        h_raster = QHBoxLayout()
        self.pb_update_list_layers.setFixedSize(100, 25)
        self.pb_update_list_layers.setToolTip(self.translate('Atualizar a lista de camadas'))
        self.pb_set_raster.setFixedSize(100, 25)
        self.pb_set_raster.setToolTip(self.translate('Definir camada raster do projeto'))
        h_raster.addWidget(self.pb_update_list_layers)
        h_raster.addWidget(self.pb_set_raster)
        self.vb_layout_project.addLayout(h_raster)
        self.gb_project.setMaximumHeight(200)
        self.gb_project.setLayout(self.vb_layout_project)
        self.vb_layout.addWidget(self.gb_project)

    def __start_field_data(self):
        self.gb_field_data.setTitle(self.translate('Dados de campo'))
        # hb_set_layer = QHBoxLayout()
        # hb_set_layer.addWidget(self.lb_status_layers)
        # self.pb_set_layers.setFixedSize(100, 25)
        # hb_set_layer.addWidget(self.pb_set_layers)
        # self.vb_layout_field_data.addLayout(hb_set_layer)
        self.lb_calculate.setWordWrap(True)
        self.vb_layout_field_data.addWidget(self.lb_calculate)
        self.pb_calculate.setToolTip(self.translate('Calcular/atualizar cálculos.'))
        self.pb_calculate.setFixedSize(100, 25)
        self.vb_layout_field_data.addWidget(self.pb_calculate)
        self.lb_generate_os.setWordWrap(True)
        self.vb_layout_field_data.addWidget(self.lb_generate_os)
        self.pb_generate_os.setToolTip(self.translate('Gerar OS'))
        self.pb_generate_os.setFixedSize(100, 25)
        self.vb_layout_field_data.addWidget(self.pb_generate_os)
        self.gb_field_data.setMaximumHeight(150)
        self.gb_field_data.setLayout(self.vb_layout_field_data)
        self.vb_layout.addWidget(self.gb_field_data)




