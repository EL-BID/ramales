from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGroupBox, QGridLayout, QPushButton, QVBoxLayout, QSpinBox, QDoubleSpinBox, QLabel, \
    QCheckBox, QHBoxLayout, QFormLayout, QWidget

from ...custom_widgets.widgets import ThousandsSeparatorSpinBox
from ...dock_tabs.base.ui_dock_tab_base import DockTab
from ...ui_rep_out_costs import RepOutDataCostsUI


class DockTabCostsBase(DockTab):
    # We must rewrite the tr method, because at runtime, the default self.translate calls within the context of the
    # inherited child class, however, pylupdate reads the python file without executing it, putting the context in
    # translation as the parent class
    # noinspection PyMethodMayBeStatic
    def translate(self, msg, disambiguation=None, n=-1) -> object:
        return QCoreApplication.translate(DockTabCostsBase.__name__, msg, disambiguation, n)

    def __init__(self, dock):
        super().__init__(dock)
        maximum = 9999999
        maxPerc = 100

        self.lb_txt_entrance = QLabel()

        # Dimensionamento
        self.lb_txt_sizing = QLabel()
        self.lb_trench_width = QLabel()
        self.dsb_trench_width = QDoubleSpinBox()
        self.dsb_trench_width.setMaximum(1)
        self.dsb_trench_width.setDecimals(2)
        self.dsb_trench_width.setSuffix(self.translate(' m'))
        self.dsb_trench_width.setSingleStep(0.1)

        self.lb_cradle_height = QLabel()
        self.dsb_cradle_height = QDoubleSpinBox()
        self.dsb_cradle_height.setMaximum(maximum)
        self.dsb_cradle_height.setDecimals(2)
        self.dsb_cradle_height.setSuffix(self.translate(' m'))
        self.dsb_cradle_height.setSingleStep(0.05)

        self.lb_wrap_height = QLabel()
        self.dsb_wrap_height = QDoubleSpinBox()
        self.dsb_wrap_height.setMaximum(maximum)
        self.dsb_wrap_height.setDecimals(2)
        self.dsb_wrap_height.setSuffix(self.translate(' m'))
        self.dsb_wrap_height.setSingleStep(0.05)

        # Tipo de solo
        self.lb_txt_soil = QLabel()
        self.lb_soil = QLabel()
        self.sb_soil = QSpinBox()
        self.sb_soil.setMaximum(maxPerc)
        self.sb_soil.setSuffix(self.translate(' %'))

        self.lb_rock = QLabel()
        self.sb_rock = QSpinBox()
        self.sb_rock.setMaximum(maxPerc)
        self.sb_rock.setSuffix(self.translate(' %'))

        # Tipo de solo, empolamento
        self.lb_soil_bulking = QLabel()
        self.dsb_soil_bulking = QDoubleSpinBox()
        self.dsb_soil_bulking.setMaximum(100)
        self.dsb_soil_bulking.setDecimals(2)
        self.dsb_soil_bulking.setSingleStep(0.1)

        self.lb_rock_swelling = QLabel()
        self.dsb_rock_swelling = QDoubleSpinBox()
        self.dsb_rock_swelling.setMaximum(100)
        self.dsb_rock_swelling.setDecimals(2)
        self.dsb_rock_swelling.setSingleStep(0.1)

        # Tipo de escavação
        self.lb_txt_excavation = QLabel()
        self.lb_manual = QLabel()
        self.sb_manual = QSpinBox()
        self.sb_manual.setMaximum(maxPerc)
        self.sb_manual.setSuffix(self.translate(' %'))

        self.lb_mechanical = QLabel()
        self.sb_mechanical = QSpinBox()
        self.sb_mechanical.setMaximum(maxPerc)
        self.sb_mechanical.setSuffix(self.translate(' %'))

        # Material reaterro
        self.lb_txt_backfill = QLabel()
        self.lb_own = QLabel()
        self.sb_own = QSpinBox()
        self.sb_own.setMaximum(maxPerc)
        self.sb_own.setSuffix(self.translate(' %'))

        self.lb_contribution = QLabel()
        self.sb_contribution = QSpinBox()
        self.sb_contribution.setMaximum(maxPerc)
        self.sb_contribution.setSuffix(self.translate(' %'))

        # Distância descarte
        self.lb_txt_disposal_distance = QLabel()
        self.lb_disposal_distance = QLabel()
        self.dsb_disposal_distance = QDoubleSpinBox()
        self.dsb_disposal_distance.setMaximum(maximum)
        self.dsb_disposal_distance.setDecimals(0)
        self.dsb_disposal_distance.setSuffix(self.translate(' km'))
        self.dsb_disposal_distance.setSingleStep(5)

        self.cb_show_data_costs = QCheckBox()
        self.pb_report_costs = QPushButton()
        self.pb_generate_xls_costs = QPushButton()

        # Costs report
        self.lb_services_costs = QLabel()
        self.lb_materials_costs = QLabel()
        self.lb_total_costs = QLabel()
        self.lb_total_costs_meter = QLabel()


        self.vb_layoutCosts = QVBoxLayout()
        self.gl_layoutCostsPipe = QGridLayout()
        self.gl_layoutCostsTerrain = QGridLayout()
        self.hb_layoutShowCosts = QHBoxLayout()
        self.gl_layoutDataCosts = QGridLayout()
        self.gb_costsPipe = QGroupBox()
        self.gb_costsTerrain = QGroupBox()
        self.gb_DataCosts = QGroupBox()
        self.rep_out_costs = RepOutDataCostsUI()

        self.dialog_contribution_warning = QLabel()
        icon = QWidget().style().standardIcon(QWidget().style().SP_MessageBoxWarning)
        self.dialog_contribution_warning.setPixmap(icon.pixmap(16, 16))
        self.dialog_contribution_warning.hide()
        self.set_logic()

    def tab_start_ui(self):
        self.lb_txt_entrance.setText(self.translate('Para calcular os custos do projeto, preencher os dados abaixo:'))
        self.lb_txt_entrance.setWordWrap(True)
        self.vb_layoutCosts.addWidget(self.lb_txt_entrance)

        self.lb_txt_sizing.setText(self.translate('Dimensionamento:'))
        self.lb_txt_sizing.setFont(self.utils.formatBoldText())
        self.gl_layoutCostsPipe.addWidget(self.lb_txt_sizing, 0, 0, 1, 2)

        self.lb_trench_width.setText(self.translate('Largura da vala'))
        self.gl_layoutCostsPipe.addWidget(self.lb_trench_width, 1, 0)
        self.gl_layoutCostsPipe.addWidget(self.dsb_trench_width, 1, 1)
        self.lb_cradle_height.setText(self.translate('Altura do berço'))
        self.gl_layoutCostsPipe.addWidget(self.lb_cradle_height, 2, 0)
        self.gl_layoutCostsPipe.addWidget(self.dsb_cradle_height, 2, 1)
        self.lb_wrap_height.setText(self.translate('Altura do envoltório'))
        self.gl_layoutCostsPipe.addWidget(self.lb_wrap_height, 3, 0)
        self.gl_layoutCostsPipe.addWidget(self.dsb_wrap_height, 3, 1)

        self.lb_txt_soil.setText(self.translate('Tipo de solo:'))
        self.lb_txt_soil.setFont(self.utils.formatBoldText())
        self.gl_layoutCostsPipe.addWidget(self.lb_txt_soil, 4, 0, 1, 2)
        self.lb_soil.setText(self.translate('Solo'))
        self.lb_soil_bulking.setText(self.translate('Empolamento Solo'))
        self.gl_layoutCostsPipe.addWidget(self.lb_soil, 5, 0)
        self.gl_layoutCostsPipe.addWidget(self.sb_soil, 5, 1)
        self.gl_layoutCostsPipe.addWidget(self.lb_soil_bulking, 5, 2)
        self.gl_layoutCostsPipe.addWidget(self.dsb_soil_bulking, 5, 3)
        self.lb_rock.setText(self.translate('Rocha'))
        self.gl_layoutCostsPipe.addWidget(self.lb_rock, 6, 0)
        self.gl_layoutCostsPipe.addWidget(self.sb_rock, 6, 1)
        self.lb_rock_swelling.setText(self.translate('Empolamento Rocha'))
        self.gl_layoutCostsPipe.addWidget(self.lb_rock_swelling, 6, 2)
        self.gl_layoutCostsPipe.addWidget(self.dsb_rock_swelling, 6, 3)
        self.lb_txt_excavation.setText(self.translate('Tipo de escavação:'))
        self.lb_txt_excavation.setFont(self.utils.formatBoldText())
        self.gl_layoutCostsPipe.addWidget(self.lb_txt_excavation, 7, 0, 1, 2)
        self.lb_manual.setText(self.translate('Manual'))
        self.gl_layoutCostsPipe.addWidget(self.lb_manual, 8, 0)
        self.gl_layoutCostsPipe.addWidget(self.sb_manual, 8, 1)
        self.lb_mechanical.setText(self.translate('Mecânica'))
        self.gl_layoutCostsPipe.addWidget(self.lb_mechanical, 9, 0)
        self.gl_layoutCostsPipe.addWidget(self.sb_mechanical, 9, 1)

        self.lb_txt_backfill.setText(self.translate('Material de reaterro:'))
        self.lb_txt_backfill.setFont(self.utils.formatBoldText())
        self.gl_layoutCostsPipe.addWidget(self.lb_txt_backfill, 10, 0, 1, 2)
        self.lb_own.setText(self.translate('Próprio'))
        self.gl_layoutCostsPipe.addWidget(self.lb_own, 11, 0)
        self.gl_layoutCostsPipe.addWidget(self.sb_own, 11, 1)
        self.lb_contribution.setText(self.translate('Aporte'))
        self.dialog_contribution_warning.setToolTip(self.translate('O aporte deve ser no mínimo equivalente ao percentual de rocha presente.'))
        self.gl_layoutCostsPipe.addWidget(self.lb_contribution, 12, 0)
        self.gl_layoutCostsPipe.addWidget(self.sb_contribution, 12, 1)
        self.gl_layoutCostsPipe.addWidget(self.dialog_contribution_warning, 12, 2)

        self.lb_txt_disposal_distance.setText(self.translate('Distância de descarte:'))
        self.lb_txt_disposal_distance.setFont(self.utils.formatBoldText())
        self.gl_layoutCostsPipe.addWidget(self.lb_txt_disposal_distance, 13, 0, 1, 2)
        self.lb_disposal_distance.setText(self.translate('Distância'))
        self.gl_layoutCostsPipe.addWidget(self.lb_disposal_distance, 14, 0)
        self.gl_layoutCostsPipe.addWidget(self.dsb_disposal_distance, 14, 1)

        self.gb_costsTerrain.setLayout(self.gl_layoutCostsPipe)
        self.vb_layoutCosts.addWidget(self.gb_costsTerrain)
        self.cb_show_data_costs.setText(self.translate('Ver custos'))
        self.pb_report_costs.setText(self.translate('Editar'))
        self.pb_report_costs.setFixedSize(100, 25)
        self.pb_generate_xls_costs.setText(self.translate('Gerar xls custos'))
        self.pb_generate_xls_costs.adjustSize()
        self.hb_layoutShowCosts.addWidget(self.cb_show_data_costs)
        self.hb_layoutShowCosts.addWidget(self.pb_report_costs)

        self.vb_layoutCosts.addLayout(self.hb_layoutShowCosts)
        self.gl_layoutDataCosts.addWidget(QLabel(self.translate('Total serviços')), 0, 0)
        self.gl_layoutDataCosts.addWidget(self.lb_services_costs, 0, 1)
        self.gl_layoutDataCosts.addWidget(QLabel(self.translate('Total materiais')), 1, 0)
        self.gl_layoutDataCosts.addWidget(self.lb_materials_costs, 1, 1)
        self.gl_layoutDataCosts.addWidget(QLabel(self.translate('Total geral')), 2, 0)
        self.gl_layoutDataCosts.addWidget(self.lb_total_costs, 2, 1)
        self.gl_layoutDataCosts.addWidget(QLabel(self.translate('Valor por metro')), 3, 0)
        self.gl_layoutDataCosts.addWidget(self.lb_total_costs_meter, 3, 1)
        self.gl_layoutDataCosts.addWidget(self.pb_generate_xls_costs, 4, 1)
        self.gb_DataCosts.setLayout(self.gl_layoutDataCosts)
        self.vb_layoutCosts.addWidget(self.gb_DataCosts)
        self.gb_DataCosts.hide()

        spinbox_pairs = [
            (self.sb_soil, self.sb_rock),
            (self.sb_manual, self.sb_mechanical),
            (self.sb_own, self.sb_contribution),
        ]

        def update_pair(spinbox, counterpart):
            counterpart.blockSignals(True)
            counterpart.setValue(100 - spinbox.value())
            counterpart.blockSignals(False)

        # Connect signals to a generic handler
        for box1, box2 in spinbox_pairs:
            box1.valueChanged.connect(lambda _, b1=box1, b2=box2: update_pair(b1, b2))
            box2.valueChanged.connect(lambda _, b1=box2, b2=box1: update_pair(b1, b2))

        def dialog_contrib_warning():
            self.dialog_contribution_warning.setVisible(self.sb_rock.value() > self.sb_contribution.value())

        self.vb_layoutCosts.addStretch()
        self.setLayout(self.vb_layoutCosts)
        self.sb_soil.valueChanged.connect(dialog_contrib_warning)
        self.sb_rock.valueChanged.connect(dialog_contrib_warning)
        self.sb_own.valueChanged.connect(dialog_contrib_warning)
        self.sb_contribution.valueChanged.connect(dialog_contrib_warning)






