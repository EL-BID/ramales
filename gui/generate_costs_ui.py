from typing import Optional

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QLineEdit, QMessageBox, QHBoxLayout, QFormLayout, QFileDialog

from ..core.calculate.CostsCalculation import QuantitiesCalculations
from ..core.xls.produces_costs_xls import ProducesReportCostsXls
from ..helpers.utils import Utils


class GenerateCostsUI:

    # def tr(self, message):
    #     # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
    #     return QCoreApplication.translate('SanihubRamales', message)

    def translate(self, msg, disambiguation=None, n=-1) -> object:
        return QCoreApplication.translate(GenerateCostsUI.__name__, msg, disambiguation, n)

    def __init__(self):
        self.windows = QDialog()
        self.utils = Utils()
        self.produces_costs = ProducesReportCostsXls()
        self.windows.setWindowTitle(self.translate('Geração de planilha de custos'))
        self.windows.setGeometry(350, 140, 350, 140)
        self.fl_layout = QFormLayout()
        self.hl_layout = QHBoxLayout()
        self.lb_select_folder = QLabel(self.translate('Selecione pasta para salvar planilha de custos:'))
        self.le_select_folder = QLineEdit()
        self.pb_select_folder = QPushButton('...')
        self.pb_gerenate = QPushButton(self.translate('Gerar planilha'))
        self.pb_gerenate.adjustSize()
        self.quantities_calculator: Optional[QuantitiesCalculations] = None
        self.__load_components()
        self.pb_select_folder.clicked.connect(self.__select_folder_save_os)
        self.pb_gerenate.clicked.connect(self.__generate_costs)

    def __load_components(self):
        self.le_select_folder.setFixedSize(400, 25)
        self.pb_select_folder.setFixedSize(100, 25)
        self.pb_gerenate.adjustSize()
        self.fl_layout.addRow(self.lb_select_folder)
        self.fl_layout.addRow(self.le_select_folder, self.pb_select_folder)
        self.fl_layout.addRow('', self.pb_gerenate)
        self.windows.setLayout(self.fl_layout)

    def __select_folder_save_os(self):
        name_file = QFileDialog.getSaveFileName(self.windows, self.translate("Salvar planilha de custos"), '', '*.xls', '')[0]
        if name_file[-4:] != '.xls':
            name_file += '.xls'
        self.le_select_folder.setText(name_file)

    def show_generate_costs(self, quantities_calculator):
        self.quantities_calculator = quantities_calculator
        self.windows.exec_()

    def __generate_costs(self):
        self.produces_costs.generate_report_costs(local_file=self.le_select_folder.text(),
                                                  quantities_calculator=self.quantities_calculator)
        self.utils.show_dialog(title='SaniHub Ramales', message=self.translate('Arquivo gerado com sucesso'),
                               information=QMessageBox.Information)
        self.le_select_folder.clear()
        self.windows.close()
