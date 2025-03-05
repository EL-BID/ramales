from typing import Optional

from qgis._core import QgsProject
from ...core.data.data_manager import ProjectDataManager
from ...core.data.models import EconomyMetrics
from .base.ui_dock_tab_flows_base import DockTabFlowsBase

class DockTabflows(DockTabFlowsBase):

    DAY = 86400

    def __init__(self, dock):
        super().__init__(dock)
        self.economy_metrics = EconomyMetrics()
        self.loaded_from_db = False

    def set_logic(self):
        self.dsb_return_coefficient.valueChanged.connect(self.on_data_changed)
        self.dsb_per_capita_allocation.valueChanged.connect(self.on_data_changed)
        self.dsb_number_people_economy.valueChanged.connect(self.on_data_changed)
        self.dsb_coefficient_k1.valueChanged.connect(self.on_data_changed)
        self.dsb_coefficient_k2.valueChanged.connect(self.on_data_changed)

    def load_data(self):
        resume_lyr = QgsProject.instance().mapLayer(ProjectDataManager.get_layers_id().RESUME_FRAME_LAYER_ID)
        if not resume_lyr:
            return
        resume_fields = [field.name() for field in resume_lyr.fields()]
        resume_values = [f.attributes() for f in resume_lyr.getFeatures()]
        resume_dict = dict(zip(resume_fields, resume_values[0]))
        economy_star = str(resume_dict[self.translate('economias')])
        self.lb_value_number_economy_start.setText(economy_star)
        self.lb_value_number_economy_end.setText(economy_star)
        self.load_user_input()
        self.loaded_from_db = True

    def load_user_input(self):
        if ProjectDataManager.is_save_economy_metrics_loaded():
            self.economy_metrics = ProjectDataManager.get_economy_metrics()

        self.dsb_return_coefficient.setValue(self.economy_metrics.return_coefficient)
        self.dsb_number_people_economy.setValue(self.economy_metrics.number_of_people_per_economy)
        self.dsb_coefficient_k1.setValue(self.economy_metrics.peak_day_coefficient)
        self.dsb_coefficient_k2.setValue(self.economy_metrics.peak_hour_coefficient)
        self.dsb_per_capita_allocation.setValue(self.economy_metrics.per_capita_endowment)

    def reload(self):
        self.load_data()

    def on_data_changed(self):
        if not self.loaded_from_db:
            return
        tmp_economy_metrics = EconomyMetrics(
            return_coefficient=self.dsb_return_coefficient.value(),
            number_of_people_per_economy=self.dsb_number_people_economy.value(),
            peak_day_coefficient=self.dsb_coefficient_k1.value(),
            peak_hour_coefficient=self.dsb_coefficient_k2.value(),
            per_capita_endowment=self.dsb_per_capita_allocation.value(),
        )

        if tmp_economy_metrics != self.economy_metrics:
            self.economy_metrics = tmp_economy_metrics
            ProjectDataManager.save_economy_metrics(self.economy_metrics)
            #self.dock.reload()


        calc = (self.dsb_return_coefficient.value() * self.dsb_per_capita_allocation.value()
                  * self.dsb_number_people_economy.value() * self.dsb_coefficient_k1.value()
                  * self.dsb_coefficient_k2.value())
        start = (calc * int(self.lb_value_number_economy_start.text())) / self.DAY
        end = (calc * int(self.lb_value_number_economy_end.text())) / self.DAY
        self.lb_value_start.setText('{:.3f}'.format(start))
        self.lb_value_end.setText('{:.3f}'.format(end))
