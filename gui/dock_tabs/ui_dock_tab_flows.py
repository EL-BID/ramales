from qgis._core import QgsProject
from ...core.data.data_manager import ProjectDataManager
from .base.ui_dock_tab_flows_base import DockTabFlowsBase


class DockTabflows(DockTabFlowsBase):
    def __init__(self, dock):
        super().__init__(dock)

    def set_logic(self):
        self.dsb_return_coefficient.valueChanged.connect(self.on_data_changed)
        self.dsb_per_capita_allocation.valueChanged.connect(self.on_data_changed)
        self.dsb_number_people_economy.valueChanged.connect(self.on_data_changed)
        self.dsb_coefficient_k1.valueChanged.connect(self.on_data_changed)
        self.dsb_coefficient_k2.valueChanged.connect(self.on_data_changed)

    def load_data(self):
        resume_lyr = QgsProject.instance().mapLayer(ProjectDataManager.get_layers_id().RESUME_FRAME_LAYER_ID)
        resume_fields = [field.name() for field in resume_lyr.fields()]
        resume_values = [f.attributes() for f in resume_lyr.getFeatures()]
        resume_dict = dict(zip(resume_fields, resume_values[0]))
        economy_star = str(resume_dict[self.translate('economias')])
        self.lb_value_number_economy_start.setText(economy_star)
        self.lb_value_number_economy_end.setText(economy_star)

    def reload(self):
        self.load_data()

    def on_data_changed(self):
        start = ((self.dsb_return_coefficient.value() * self.dsb_per_capita_allocation.value()
                  * self.dsb_number_people_economy.value() * self.dsb_coefficient_k1.value()
                  * self.dsb_coefficient_k2.value() + int(self.lb_value_number_economy_start.text())) / 86400)
        end = ((self.dsb_return_coefficient.value() * self.dsb_per_capita_allocation.value()
                * self.dsb_number_people_economy.value() * self.dsb_coefficient_k1.value()
                * self.dsb_coefficient_k2.value() + int(self.lb_value_number_economy_end.text())) / 86400)
        self.lb_value_start.setText('{:.3f}'.format(start))
        self.lb_value_end.setText('{:.3f}'.format(end))
