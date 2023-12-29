import errno
import json
import os
import sqlite3

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QDialog, QFormLayout, QComboBox, QLabel, QLineEdit, QTableWidget, QTableWidgetItem,
                             QAbstractItemView, QDialogButtonBox, QPushButton, QHBoxLayout, QFileDialog, QMessageBox,
                             QProgressBar)
from qgis._core import QgsProject
from qgis.core import QgsApplication

from ....core.data.data_manager import ProjectDataManager
from ....core.data.models import LayersData
from ....core.project_creation.project_creation import generate_project
from ....helpers.utils import Utils


class CreateProjectDialog(QDialog):
    """
        Dialog to create a new project.
    """

    def __init__(self, iface):
        super().__init__()
        self.setWindowTitle(self.tr('Criar projeto QGIS'))
        self.setGeometry(300, 100, 600, 500)
        self.setModal(True)
        self.utils = Utils()

        # Make it so you can resize it but, starts at 800x800
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        # self.resize(800, 800)

        self.cb_local = QComboBox()
        self.le_name = QLineEdit()
        self.le_path = QLineEdit()
        self.le_srid_filter = QLineEdit()
        self.tb_filter = QTableWidget()
        self.pb_path = QPushButton()
        self.hl_path = QHBoxLayout()
        self.pbar = QProgressBar()

        self.le_srid_filter.textChanged[str].connect(self.__filter_srids)

        self.bb = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Close)
        bt_ok = self.bb.button(QDialogButtonBox.Ok)
        bt_ok.setText(self.tr('Confirmar'))
        bt_close = self.bb.button(QDialogButtonBox.Close)
        bt_close.setText(self.tr('Cancelar'))
        self.bb.accepted.connect(self.__accept)
        self.bb.rejected.connect(self.reject)

        self.set_ui()
        self.set_logic()
        self.iface = iface
        self.dict_layers = {}

    def __accept(self):
        if not self.check_if_is_valid():
            self.utils.show_dialog(title=self.tr('Erro'), message=self.tr('Preencha todos os campos!'),
                                   information=QMessageBox.Warning)
            return

        ret = self.utils.show_dialog_question(title='Criar novo projeto?',
                                              message=self.tr("Tem certeza que quer criar um novo projeto? Suas " +
                                                              "alterações não salvas do projeto atual serão perdidas," +
                                                              " e você será movido automaticamente para o novo projeto."))

        if ret is not True:
            return

        def get_id_layer(lang) -> str:
            layers = self.__get_layers(lang)
            # for lyr in layers:
            for k, v in layers.items():
                layer = QgsProject.instance().mapLayersByName(v)
                if len(layer) == 1:
                    self.dict_layers[k] = layer[0].id()

        try:
            generate_project(
                local=self.__parse_name_language(self.cb_local.currentText()),
                srid=self.tb_filter.selectedItems()[1].text(),
                srid_type=self.tb_filter.selectedItems()[0].text(),
                project_name=self.le_name.text(),
                project_path=self.le_path.text(),
                iface=self.iface
            )
            get_id_layer(self.__parse_name_language(self.cb_local.currentText()))
            ProjectDataManager.save_layers_id(layers_data=LayersData(
                BLOCKS_LAYER_ID=self.dict_layers['blocks'],
                NODES_LAYER_ID=self.dict_layers['nodes'],
                SEGMENTS_LAYER_ID=self.dict_layers['segments'],
                LINEAR_OBSTACLES_LAYER_ID=self.dict_layers['linear_obstacles'],
                POINT_OBSTACLES_LAYER_ID=self.dict_layers['point_obstacles'],
                ACCESSORIES_LAYER_ID=self.dict_layers['accessories']))
            self.utils.show_dialog(title=self.tr('Criação sucedida'),
                                   message=self.tr('Projeto criado com sucesso!'),
                                   information=QMessageBox.Information)
        except (FileNotFoundError, NotADirectoryError) as e:
            self.utils.show_dialog(title=self.tr('Erro na criação do projeto'),
                                   message=self.tr(f'O diretório "{self.le_path.text()}" selecionado não é válido!'),
                                   information=QMessageBox.Warning)
        except OSError as e:
            if e.errno == errno.EACCES:
                self.utils.show_dialog(title=self.tr('Erro de permissão'),
                                       message=self.tr('Você não tem permissão para criar o projeto nesse diretório!'),
                                       information=QMessageBox.Warning)
            elif e.errno == errno.ENOSPC:
                self.utils.show_dialog(title=self.tr('Falta de espaço'),
                                       message=self.tr('Não há espaço suficiente no disco para criar o projeto!'),
                                       information=QMessageBox.Warning)
            else:
                self.utils.show_dialog(title=self.tr('Erro de sistema operacional'),
                                       message=self.tr('Erro desconhecido: ') + str(e),
                                       information=QMessageBox.Warning)
        except Exception as e:
            self.utils.show_dialog(title=self.tr('Erro na criação do projeto'),
                                   message=self.tr('Erro desconhecido: ') + str(e),
                                   information=QMessageBox.Warning)
        else:
            self.accept()

    def set_logic(self):
        self.pb_path.clicked.connect(self.__select_path)

    def __select_path(self):
        """Selects the path to create the project."""
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.Directory)
        file_dialog.setOption(QFileDialog.ShowDirsOnly, True)
        if file_dialog.exec_():
            self.le_path.setText(file_dialog.selectedFiles()[0])

    def set_ui(self):
        layout = QFormLayout()
        languages = self.__get_lacales()
        self.cb_local.addItems(languages)

        # Show first all SRIDS on the table
        # Columns are: Type, SRID, Description
        self.tb_filter.setColumnCount(3)
        self.tb_filter.setHorizontalHeaderLabels([self.tr('Tipo'), self.tr('SRID'), self.tr('Descrição')])

        # Make the folder line edit and button in same horizontal layout
        self.pb_path.setText(self.tr('Buscar...'))
        self.pb_path.setToolTip(self.tr('Selecione a pasta para a criação do projeto QGIS'))
        self.hl_path.addWidget(self.le_path, stretch=1)
        self.hl_path.addWidget(self.pb_path)

        # Getting all crs
        con = sqlite3.connect(QgsApplication.srsDatabaseFilePath())
        cur = con.cursor()
        cur.execute('select * from vw_srs')
        rows = cur.fetchall()
        con.close()
        for i, crs in enumerate(rows):
            description = crs[0]
            srid = crs[-2]
            srid_type = crs[-3]
            self.tb_filter.insertRow(i)
            self.tb_filter.setItem(i, 0, QTableWidgetItem(srid_type))
            self.tb_filter.setItem(i, 1, QTableWidgetItem(str(srid)))
            self.tb_filter.setItem(i, 2, QTableWidgetItem(description))

        # Make it non editable
        self.tb_filter.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # Fill the entire space
        self.tb_filter.horizontalHeader().setStretchLastSection(True)

        # Make it so the table is selectable, one item at time only
        self.tb_filter.setSelectionBehavior(QTableWidget.SelectRows)
        self.tb_filter.setSelectionMode(QTableWidget.SingleSelection)

        layout.addRow(self.tr('Local:'), self.cb_local)
        layout.addRow(self.tr('Nome:'), self.le_name)
        layout.addRow(self.tr('Pasta de instalação'), self.hl_path)
        layout.addRow(self.tr('Filtro (SRID):'), self.le_srid_filter)
        layout.addWidget(QLabel(self.tr('Selecione um SRID:')))
        layout.addWidget(self.tb_filter)
        layout.addWidget(self.bb)
        self.setLayout(layout)

    def __filter_srids(self, txt):
        """Filters the SRIDS table."""
        for i in range(self.tb_filter.rowCount()):
            self.tb_filter.setRowHidden(i, True)
            for j in range(self.tb_filter.columnCount()):
                if txt.lower() in self.tb_filter.item(i, j).text().lower():
                    self.tb_filter.setRowHidden(i, False)
                    break

    def check_if_is_valid(self):
        """Checks if the input data is valid."""
        # Count the number of selected rows
        selected_rows = len(self.tb_filter.selectionModel().selectedRows())

        return self.le_name.text() and self.le_path.text() and self.cb_local.currentText() and self.le_path.text() and \
            selected_rows == 1

    @staticmethod
    def __get_lacales():
        langs = []
        plg_dir = os.path.dirname(__file__)
        plg_dir = plg_dir.replace('gui' + os.sep + 'dock_tabs' + os.sep + 'views',
                                  'resources' + os.sep + 'localizations' + os.sep)
        files = os.listdir(plg_dir)
        for file in files:
            file_json = open(os.path.join(plg_dir, file), 'r')
            data_json = json.load(file_json)
            file_json.close()
            langs.append(data_json['locale_name'])
        return langs

    @staticmethod
    def __parse_name_language(lang):
        lang = lang[-6:-1]
        return lang

    @staticmethod
    def __get_layers(lang):
        plg_dir = os.path.dirname(__file__)
        plg_dir = plg_dir.replace('gui' + os.sep + 'dock_tabs' + os.sep + 'views',
                                  'resources' + os.sep + 'localizations' + os.sep)
        file_json = open(os.path.join(plg_dir, lang + '.json'), 'r')
        data_json = json.load(file_json)
        file_json.close()
        return data_json['layers']
