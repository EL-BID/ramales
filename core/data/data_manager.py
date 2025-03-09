from .data_access import (
    LayersInfoDAO,
    CalculationInfoDAO,
    LanguageDAO,
    LayerRasterDAO,
    CostsDAO,
    SegmentsDAO,
    EconomyMetricsDAO
)

from .models import LayersData, Language, LayerRaster, Costs, Ramal, EconomyMetrics
from typing import Dict


class ProjectDataManager:

    @staticmethod
    def get_language_project() -> Language:
        return Language(LANGUAGE=LanguageDAO.get_language_project()[0])

    @staticmethod
    def save_language_project(language: Language):
        sucess = (LanguageDAO.set_language_project(language.LANGUAGE))
        if sucess:
            LanguageDAO.set_done(True)
            return True
        return False

    @staticmethod
    def get_layer_raster() -> LayerRaster:
        return LayerRaster(LAYER_RASTER=LayerRasterDAO.get_layer_raster()[0])

    @staticmethod
    def save_layer_raster(layer_raster: LayerRaster):
        sucess = (LayerRasterDAO.set_layer_raster(layer_raster.LAYER_RASTER))
        if sucess:
            LayerRasterDAO.set_done(True)
            return True
        return False

    @staticmethod
    def get_layers_id() -> LayersData:
        return LayersData(
            BLOCKS_LAYER_ID=LayersInfoDAO.get_blocks_layer_id()[0],
            RESUME_FRAME_LAYER_ID=LayersInfoDAO.get_resume_frame_layer_id()[0],
            NODES_LAYER_ID=LayersInfoDAO.get_nodes_layer_id()[0],
            SEGMENTS_LAYER_ID=LayersInfoDAO.get_segments_layer_id()[0],
            LINEAR_OBSTACLES_LAYER_ID=LayersInfoDAO.get_linear_obstacles_layer_id()[0],
            POINT_OBSTACLES_LAYER_ID=LayersInfoDAO.get_point_obstacles_layer_id()[0],
            BUILDINGS_LAYER_ID=LayersInfoDAO.get_buildings_layer_id()[0],
            SERVICE_LANE_LAYER_ID=LayersInfoDAO.get_service_lane_layer_id()[0]
        )

    @staticmethod
    def save_layers_id(layers_data: LayersData):
        success = (LayersInfoDAO.set_blocks_layer_id(layers_data.BLOCKS_LAYER_ID) and
                  LayersInfoDAO.set_resume_frame_layer_id(layers_data.RESUME_FRAME_LAYER_ID) and
                  LayersInfoDAO.set_buildings_layer_id(layers_data.BUILDINGS_LAYER_ID) and
                  LayersInfoDAO.set_service_lane_layer_id(layers_data.SERVICE_LANE_LAYER_ID) and
                  LayersInfoDAO.set_nodes_layer_id(layers_data.NODES_LAYER_ID) and
                  LayersInfoDAO.set_segments_layer_id(layers_data.SEGMENTS_LAYER_ID) and
                  LayersInfoDAO.set_linear_obstacles_layer_id(layers_data.LINEAR_OBSTACLES_LAYER_ID) and
                  LayersInfoDAO.set_point_obstacles_layer_id(layers_data.POINT_OBSTACLES_LAYER_ID) and
                  LayersInfoDAO.set_accessories_layer_id(layers_data.ACCESSORIES_LAYER_ID))
        if success:
            LayersInfoDAO.set_done(True)
            return True
        return False

    @staticmethod
    def is_data_layers_id_loaded():
        return LayersInfoDAO.is_done()[0]

    @staticmethod
    def get_status_calculation() -> bool:
        return bool(
            CalculationInfoDAO.get_status_calculation()[0]
        )

    @staticmethod
    def save_status_calculation(status: bool):
        sucess = (CalculationInfoDAO.set_status_calculation(status))
        if sucess:
            CalculationInfoDAO.set_done(True)
            return True
        return False

    @staticmethod
    def is_status_calculation_loaded():
        return CalculationInfoDAO.is_done()[0]

    @staticmethod
    def should_show_costs():
        return CostsDAO.get_show_costs()[0]

    @staticmethod
    def set_show_costs(show_costs: bool) -> bool:
        return CostsDAO.set_show_costs(show_costs)

    @staticmethod
    def get_costs():
        services = CostsDAO.get_services()[0]

        # Se não tem serviços cadastrados, carrega os serviços padrão
        if not services:
            services = Costs().SERVICES
        return Costs(
            TRENCH_WIDTH=CostsDAO.get_trench_width()[0],
            CRADLE_HEIGHT=CostsDAO.get_cradle_height()[0],
            WRAP_HEIGHT=CostsDAO.get_wrap_height()[0],
            SOIL_PERCENT=CostsDAO.get_soil_percent()[0],
            ROCK_PERCENT=CostsDAO.get_rock_percent()[0],
            MANUAL_PERCENT=CostsDAO.get_manual_percent()[0],
            MECHANICAL_PERCENT=CostsDAO.get_mechanical_percent()[0],
            OWN_PERCENT=CostsDAO.get_own_percent()[0],
            CONTRIBUTION_PERCENT=CostsDAO.get_contribution_percent()[0],
            DISPOSAL_DISTANCE=CostsDAO.get_disposal_distance()[0],
            SOIL_BULKING=CostsDAO.get_soil_bulking()[0],
            ROCK_SWELLING=CostsDAO.get_rock_swelling()[0],
            SERVICES=services
        )

    @staticmethod
    def save_costs(costs: Costs) -> bool:
        success = (CostsDAO.set_trench_width(costs.TRENCH_WIDTH) and
                   CostsDAO.set_cradle_height(costs.CRADLE_HEIGHT) and
                   CostsDAO.set_wrap_height(costs.WRAP_HEIGHT) and
                   CostsDAO.set_soil_percent(costs.SOIL_PERCENT) and
                   CostsDAO.set_rock_percent(costs.ROCK_PERCENT) and
                   CostsDAO.set_manual_percent(costs.MANUAL_PERCENT) and
                   CostsDAO.set_mechanical_percent(costs.MECHANICAL_PERCENT) and
                   CostsDAO.set_own_percent(costs.OWN_PERCENT) and
                   CostsDAO.set_contribution_percent(costs.CONTRIBUTION_PERCENT) and
                   CostsDAO.set_disposal_distance(costs.DISPOSAL_DISTANCE) and
                   CostsDAO.set_soil_bulking(costs.SOIL_BULKING) and
                   CostsDAO.set_rock_swelling(costs.ROCK_SWELLING) and
                   CostsDAO.set_services(costs.SERVICES))
        if success:
            CostsDAO.set_done(True)
            return True
        return False

    @staticmethod
    def is_costs_loaded():
        return CostsDAO.is_done()[0]

    @classmethod
    def get_all_segments(cls) -> Dict[str, Ramal]:
        if not cls.get_layers_id().SEGMENTS_LAYER_ID \
                or not cls.get_layers_id().NODES_LAYER_ID \
                or not cls.get_language_project().LANGUAGE:
            return {}
        segs = SegmentsDAO(
            segments_layer_id=cls.get_layers_id().SEGMENTS_LAYER_ID,
            nodes_layer_id=cls.get_layers_id().NODES_LAYER_ID,
            lang=cls.get_language_project().LANGUAGE
        )
        return segs.get_segments()

    @staticmethod
    def get_economy_metrics() -> EconomyMetrics:
        return EconomyMetrics(
            return_coefficient=EconomyMetricsDAO.get_return_coefficient()[0],
            per_capita_endowment=EconomyMetricsDAO.get_per_capita_endowment()[0],
            number_of_people_per_economy=EconomyMetricsDAO.get_number_of_people_economy()[0],
            peak_day_coefficient=EconomyMetricsDAO.get_peak_day_coefficient()[0],
            peak_hour_coefficient=EconomyMetricsDAO.get_peak_hour_coefficient()[0]
        )

    @staticmethod
    def save_economy_metrics(metrics: EconomyMetrics) -> bool:
        success = (
                EconomyMetricsDAO.set_return_coefficient(metrics.return_coefficient) and
                EconomyMetricsDAO.set_per_capita_endowment(metrics.per_capita_endowment) and
                EconomyMetricsDAO.set_number_of_people_economy(metrics.number_of_people_per_economy) and
                EconomyMetricsDAO.set_peak_day_coefficient(metrics.peak_day_coefficient) and
                EconomyMetricsDAO.set_peak_hour_coefficient(metrics.peak_hour_coefficient)
        )
        if success:
            EconomyMetricsDAO.set_done(True)
        return success

    @staticmethod
    def is_save_economy_metrics_loaded() -> bool:
        return EconomyMetricsDAO.is_done()[0]