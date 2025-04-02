from typing import Optional

from PyQt5.QtCore import QTimer

from ..generate_costs_ui import GenerateCostsUI
from ...core.calculate.CostsCalculation import QuantitiesCalculations
from .base.ui_dock_tab_costs_base import DockTabCostsBase
from ...core.data.data_manager import ProjectDataManager
from ...core.data.models import Costs


class DockTabCosts(DockTabCostsBase):
    def __init__(self, dock):
        super().__init__(dock)
        self.quantities_calculator: Optional[QuantitiesCalculations] = None
        self.loaded_from_db = False
        self.costs: Optional[Costs] = None
        self.generate_costs = GenerateCostsUI()

        self.save_timer = QTimer()
        self.save_timer.setSingleShot(True)
        self.save_timer.timeout.connect(self.save_values)

    def set_logic(self):
        self.sb_soil.valueChanged.connect(self.on_data_changed)
        self.sb_rock.valueChanged.connect(self.on_data_changed)
        self.sb_manual.valueChanged.connect(self.on_data_changed)
        self.sb_mechanical.valueChanged.connect(self.on_data_changed)
        self.sb_own.valueChanged.connect(self.on_data_changed)
        self.sb_contribution.valueChanged.connect(self.on_data_changed)
        self.dsb_wrap_height.valueChanged.connect(self.on_data_changed)
        self.dsb_cradle_height.valueChanged.connect(self.on_data_changed)
        self.dsb_trench_width.valueChanged.connect(self.on_data_changed)
        self.dsb_disposal_distance.valueChanged.connect(self.on_data_changed)
        self.dsb_soil_bulking.valueChanged.connect(self.on_data_changed)
        self.dsb_rock_swelling.valueChanged.connect(self.on_data_changed)

        self.cb_show_data_costs.toggled.connect(self.on_cb_costs_toggle)
        self.pb_report_costs.clicked.connect(self.__show_report_costs)
        self.pb_generate_xls_costs.clicked.connect(self.__generete_xls_costs)
        self.rep_out_costs.pb_saveEditCosts.clicked.connect(self.on_services_cost_update)
        self.cb_show_data_costs.toggled.connect(
            lambda: ProjectDataManager.set_show_costs(self.cb_show_data_costs.isChecked()))

    def load_data(self):
        if ProjectDataManager.is_costs_loaded():
            self.costs = ProjectDataManager.get_costs()
        self.load_costs_calculations()
        self.load_costs_values()
        self.load_user_input()
        self.loaded_from_db = True

    def load_user_input(self):
        if self.costs is not None:
            self.sb_soil.setValue(self.costs.SOIL_PERCENT)
            self.sb_rock.setValue(self.costs.ROCK_PERCENT)
            self.sb_manual.setValue(self.costs.MANUAL_PERCENT)
            self.sb_mechanical.setValue(self.costs.MECHANICAL_PERCENT)
            self.sb_own.setValue(self.costs.OWN_PERCENT)
            self.sb_contribution.setValue(self.costs.CONTRIBUTION_PERCENT)
            self.dsb_wrap_height.setValue(self.costs.WRAP_HEIGHT)
            self.dsb_cradle_height.setValue(self.costs.CRADLE_HEIGHT)
            self.dsb_trench_width.setValue(self.costs.TRENCH_WIDTH)
            self.dsb_disposal_distance.setValue(self.costs.DISPOSAL_DISTANCE)
            self.dsb_rock_swelling.setValue(self.costs.ROCK_SWELLING)
            self.dsb_soil_bulking.setValue(self.costs.SOIL_BULKING)
        else:
            self.sb_soil.setValue(100)
            self.sb_rock.setValue(0)
            self.sb_manual.setValue(100)
            self.sb_mechanical.setValue(0)
            self.sb_own.setValue(100)
            self.sb_contribution.setValue(0)
            self.dsb_wrap_height.setValue(0)
            self.dsb_cradle_height.setValue(0)
            self.dsb_trench_width.setValue(0)
            self.dsb_disposal_distance.setValue(0)
            self.dsb_rock_swelling.setValue(1)
            self.dsb_soil_bulking.setValue(1)
        self.cb_show_data_costs.setChecked(ProjectDataManager.should_show_costs())

    def load_costs_values(self):
        if self.costs is not None:
            # Serviços de custos sao de 1 a 33
            costs_services = self.costs.SERVICES[:33]
            costs_materials = self.costs.SERVICES[33:]

            methods_quantities = [method for method in dir(self.quantities_calculator)
                                  if callable(getattr(self.quantities_calculator, method)) and method.startswith("get_")]
            methods_quantities.sort()
            values_quantities = [getattr(self.quantities_calculator, method)() for method in methods_quantities]

            total_costs_services = 0
            total_costs_materials = 0
            for i in range(33):
                total_costs_services += costs_services[i] * values_quantities[i]

            for i in range(33, 40):
                total_costs_materials += costs_materials[i-33] * values_quantities[i]

            total_costs = total_costs_services + total_costs_materials
            total_costs_meter = total_costs / self.quantities_calculator.costs_calculation.get_total_extension()

            self.lb_materials_costs.setText(f"{self.translate('Custo dos materiais (USD):')} $ {self.utils.formatNum2Dec(total_costs_materials)}")
            self.lb_services_costs.setText(f"{self.translate('Custo dos serviços (USD):')} $ {self.utils.formatNum2Dec(total_costs_services)}")
            self.lb_total_costs.setText(f"{self.translate('Custo total (USD):')} $ {self.utils.formatNum2Dec(total_costs)}")
            self.lb_total_costs_meter.setText(f"{self.translate('Custo total por metro (USD):')} $ {self.utils.formatNum2Dec(total_costs_meter)}")
        else:
            self.lb_materials_costs.setText(f"{self.translate('Custo dos materiais (USD):')} $ {self.utils.formatNum2Dec(0)}")
            self.lb_services_costs.setText(f"{self.translate('Custo dos serviços (USD):')} $ {self.utils.formatNum2Dec(0)}")
            self.lb_total_costs.setText(f"{self.translate('Custo total (USD):')} $ {self.utils.formatNum2Dec(0)}")
            self.lb_total_costs_meter.setText(f"{self.translate('Custo total por metro (USD):')} $ {self.utils.formatNum2Dec(0)}")


    def load_costs_calculations(self):
        self.costs = ProjectDataManager.get_costs()
        self.quantities_calculator = QuantitiesCalculations(
            costs=self.costs,
            ramals=ProjectDataManager.get_all_segments(),
        )

    def reload(self):
        self.loaded_from_db = False
        self.load_data()

    def on_cb_costs_toggle(self, checked: bool):
        self.load_costs_calculations()
        if self.cb_show_data_costs.isChecked():
            self.gb_DataCosts.show()
        else:
            self.gb_DataCosts.hide()

    def on_data_changed(self):
        self.save_timer.start(500)

    def save_values(self):
        if not self.loaded_from_db:
            return
        tmp_costs = Costs(
            SOIL_PERCENT=self.sb_soil.value(),
            ROCK_PERCENT=self.sb_rock.value(),
            MANUAL_PERCENT=self.sb_manual.value(),
            MECHANICAL_PERCENT=self.sb_mechanical.value(),
            OWN_PERCENT=self.sb_own.value(),
            CONTRIBUTION_PERCENT=self.sb_contribution.value(),
            WRAP_HEIGHT=self.dsb_wrap_height.value(),
            CRADLE_HEIGHT=self.dsb_cradle_height.value(),
            TRENCH_WIDTH=self.dsb_trench_width.value(),
            DISPOSAL_DISTANCE=self.dsb_disposal_distance.value(),
            SOIL_BULKING=self.dsb_soil_bulking.value(),
            ROCK_SWELLING=self.dsb_rock_swelling.value(),
            SERVICES=self.costs.SERVICES
        )
        # if self.costs is None:
        #     tmp_costs.services = Costs().services

        if tmp_costs != self.costs:
            self.costs = tmp_costs
            ProjectDataManager.save_costs(self.costs)
            self.dock.reload()

        # if self.check_data_costs():
        #     self.rb_show_data_costs.setChecked(False)

    def on_services_cost_update(self):
        print("on_services_cost_update called")
        self.rep_out_costs.saveChanges()
        services = [dsb.value() for dsb in self.rep_out_costs.dsb_list_entrance]

        if self.costs is not None:
            self.costs.SERVICES = services
        print("self.costs.SERVICES", self.costs.SERVICES)
        ProjectDataManager.save_costs(self.costs)
        self.dock_reload()
        self.load_costs_values()

    def __show_report_costs(self):
        self.rep_out_costs.loadReportCosts(self.quantities_calculator)
        self.rep_out_costs.showReportCosts()

    def __generete_xls_costs(self):
        self.generate_costs.show_generate_costs(self.quantities_calculator)

