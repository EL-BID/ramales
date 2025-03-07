from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QGroupBox, QGridLayout, QVBoxLayout, QDoubleSpinBox, QLabel, QSpinBox

from ...dock_tabs.base.ui_dock_tab_base import DockTab


class DockTabFlowsBase(DockTab):

    def translate(self, msg, disambiguation=None, n=-1) -> object:
        return QCoreApplication.translate(DockTabFlowsBase.__name__, msg, disambiguation, n)

    def __init__(self, dock):
        super().__init__(dock)

        self.lb_txt_entrance_flow = QLabel()
        # Dados de entrada
        self.lb_return_coefficient = QLabel()  # coeficiente de retorno
        self.dsb_return_coefficient = QDoubleSpinBox()
        self.dsb_return_coefficient.setDecimals(2)
        self.dsb_return_coefficient.setFixedWidth(120)
        self.lb_per_capita_allocation = QLabel()  # dotacao per capita
        self.dsb_per_capita_allocation = QDoubleSpinBox()
        self.dsb_per_capita_allocation.setDecimals(2)
        self.dsb_per_capita_allocation.setMaximum(9999.99)
        self.dsb_per_capita_allocation.setSuffix(self.translate(' l/hab x dia'))
        self.dsb_per_capita_allocation.setFixedWidth(120)
        self.lb_number_people_economy = QLabel()  # numero de pessoas por economia
        self.dsb_number_people_economy = QDoubleSpinBox()
        self.dsb_number_people_economy.setDecimals(2)
        self.dsb_number_people_economy.setFixedWidth(120)
        self.lb_coefficient_k1 = QLabel()  # coeficiente dia de maior consumo
        self.dsb_coefficient_k1 = QDoubleSpinBox()
        self.dsb_coefficient_k1.setDecimals(2)
        self.dsb_coefficient_k1.setFixedWidth(120)
        self.lb_coefficient_k2 = QLabel()  # coeficiente hora de maior consumo
        self.dsb_coefficient_k2 = QDoubleSpinBox()
        self.dsb_coefficient_k2.setDecimals(2)
        self.dsb_coefficient_k2.setFixedWidth(120)
        self.lb_txt_number_economy_start = QLabel()  # numero de economias de inicio
        self.lb_value_number_economy_start = QLabel()
        self.lb_txt_number_economy_end = QLabel()  # numero de economias de fim
        self.sb_number_economy_end = QSpinBox()
        # dados de saída
        self.lb_flow = QLabel()
        self.lb_txt_start = QLabel()
        self.lb_value_start = QLabel()
        self.lb_txt_end = QLabel()
        self.lb_value_end = QLabel()

        self.vb_layout_flow = QVBoxLayout()
        self.gl_layout_flow_ent = QGridLayout()
        self.gl_layout_flow_data = QGridLayout()
        self.gb_flow_ent = QGroupBox()
        self.gb_flow_data = QGroupBox()
        self.set_logic()

    def tab_start_ui(self):
        self.lb_txt_entrance_flow.setText(self.translate('Para calcular as vazões do projeto, preencher os dados abaixo:'))
        self.lb_txt_entrance_flow.setWordWrap(True)
        self.vb_layout_flow.addWidget(self.lb_txt_entrance_flow)

        self.lb_return_coefficient.setText(self.translate('Coeficiente de retorno (C)'))
        self.gl_layout_flow_ent.addWidget(self.lb_return_coefficient, 0, 0)
        self.gl_layout_flow_ent.addWidget(self.dsb_return_coefficient, 0, 1)
        self.lb_per_capita_allocation.setText(self.translate('Dotação per capita (q)'))
        self.gl_layout_flow_ent.addWidget(self.lb_per_capita_allocation, 1, 0)
        self.gl_layout_flow_ent.addWidget(self.dsb_per_capita_allocation, 1, 1)
        self.lb_number_people_economy.setText(self.translate('Número de pessoas por economia (p)'))
        self.gl_layout_flow_ent.addWidget(self.lb_number_people_economy, 2, 0)
        self.gl_layout_flow_ent.addWidget(self.dsb_number_people_economy, 2, 1)
        self.lb_coefficient_k1.setText(self.translate('Coeficiente dia de maior consumo (K1)'))
        self.gl_layout_flow_ent.addWidget(self.lb_coefficient_k1, 3, 0)
        self.gl_layout_flow_ent.addWidget(self.dsb_coefficient_k1, 3, 1)
        self.lb_coefficient_k2.setText(self.translate('Coeficiente hora de maior consumo (K2)'))
        self.gl_layout_flow_ent.addWidget(self.lb_coefficient_k2, 4, 0)
        self.gl_layout_flow_ent.addWidget(self.dsb_coefficient_k2, 4, 1)
        self.lb_txt_number_economy_start.setText(self.translate('Número de economias inicio de plano (e)'))
        self.lb_value_number_economy_start.setText('')
        self.gl_layout_flow_ent.addWidget(self.lb_txt_number_economy_start, 5, 0)
        self.gl_layout_flow_ent.addWidget(self.lb_value_number_economy_start, 5, 1)
        self.lb_txt_number_economy_end.setText(self.translate('Número de economias fim de plano (e)'))
        self.sb_number_economy_end.setValue(0)
        self.gl_layout_flow_ent.addWidget(self.lb_txt_number_economy_end, 6, 0)
        self.gl_layout_flow_ent.addWidget(self.sb_number_economy_end, 6, 1)
        self.gb_flow_ent.setLayout(self.gl_layout_flow_ent)
        self.vb_layout_flow.addWidget(self.gb_flow_ent)

        self.lb_flow.setText(self.translate('Vazão (l/s)'))
        self.lb_flow.setFont(self.utils.formatBoldText())
        self.gl_layout_flow_data.addWidget(self.lb_flow, 0, 0, 1, 2)
        self.lb_txt_start.setText(self.translate('Inicio'))
        self.lb_value_start.setText('')
        self.gl_layout_flow_data.addWidget(self.lb_txt_start, 1, 0)
        self.gl_layout_flow_data.addWidget(self.lb_value_start, 1, 1)
        self.lb_txt_end.setText(self.translate('Fim'))
        self.lb_value_end.setText('')
        self.gl_layout_flow_data.addWidget(self.lb_txt_end, 2, 0)
        self.gl_layout_flow_data.addWidget(self.lb_value_end, 2, 1)
        self.gb_flow_data.setLayout(self.gl_layout_flow_data)
        self.vb_layout_flow.addWidget(self.gb_flow_data)

        self.vb_layout_flow.addStretch()
        self.setLayout(self.vb_layout_flow)

