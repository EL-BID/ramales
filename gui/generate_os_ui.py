from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QLineEdit, QMessageBox, QHBoxLayout, QFormLayout, QFileDialog

from ..core.xls.produces_os_xls import ProducesReportOSXls
from ..helpers.utils import Utils


class GenerateOsUI:

    def tr(self, message):
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('SanihubRamales', message)

    def __init__(self):
        self.windows = QDialog()
        self.utils = Utils()
        self.produces_os = ProducesReportOSXls()
        self.windows.setWindowTitle(self.tr('Geração de OS - xls'))
        self.windows.setGeometry(350, 140, 350, 140)
        self.fl_layout = QFormLayout()
        self.hl_layout = QHBoxLayout()
        self.lb_select_folder = QLabel(self.tr('Selecione pasta para salvar o arquivo da OS:'))
        self.le_select_folder = QLineEdit()
        self.pb_select_folder = QPushButton('...')
        self.pb_gerenate = QPushButton(self.tr('Gerar OS'))
        self.__load_components()
        self.pb_select_folder.clicked.connect(self.select_folder_save_os)
        self.pb_gerenate.clicked.connect(self.generate_os)

    def __load_components(self):
        self.le_select_folder.setFixedSize(400, 25)
        self.pb_select_folder.setFixedSize(100, 25)
        self.pb_gerenate.setFixedSize(100, 25)
        self.fl_layout.addRow(self.lb_select_folder)
        self.fl_layout.addRow(self.le_select_folder, self.pb_select_folder)
        self.fl_layout.addRow('', self.pb_gerenate)
        self.windows.setLayout(self.fl_layout)

    def select_folder_save_os(self):
        name_file = QFileDialog.getSaveFileName(self.windows, self.tr("Salvar planilha OS"), '', '*.xls', '')[0]
        if name_file[-4:] != '.xls':
            name_file += '.xls'
        self.le_select_folder.setText(name_file)

    def show_generate_os(self):
        self.windows.exec_()

    def generate_os(self):
        self.produces_os.generate_report_os(local_file=self.le_select_folder.text())
        self.utils.show_dialog(title='SaniHub Ramales', message=self.tr('Arquivo gerado com sucesso'),
                               information=QMessageBox.Information)
        self.windows.close()
