from .data_access import LayersInfoDAO, CalculationInfoDAO, LanguageDAO, LayerRasterDAO
from .models import LayersData, Language, LayerRaster


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
            NODES_LAYER_ID=LayersInfoDAO.get_nodes_layer_id()[0],
            SEGMENTS_LAYER_ID=LayersInfoDAO.get_segments_layer_id()[0],
            LINEAR_OBSTACLES_LAYER_ID=LayersInfoDAO.get_linear_obstacles_layer_id()[0],
            POINT_OBSTACLES_LAYER_ID=LayersInfoDAO.get_point_obstacles_layer_id()[0],
            ACCESSORIES_LAYER_ID=LayersInfoDAO.get_accessories_layer_id()[0]
        )

    @staticmethod
    def save_layers_id(layers_data: LayersData):
        sucess = (LayersInfoDAO.set_blocks_layer_id(layers_data.BLOCKS_LAYER_ID) and
                  LayersInfoDAO.set_nodes_layer_id(layers_data.NODES_LAYER_ID) and
                  LayersInfoDAO.set_segments_layer_id(layers_data.SEGMENTS_LAYER_ID) and
                  LayersInfoDAO.set_linear_obstacles_layer_id(layers_data.LINEAR_OBSTACLES_LAYER_ID) and
                  LayersInfoDAO.set_point_obstacles_layer_id(layers_data.POINT_OBSTACLES_LAYER_ID) and
                  LayersInfoDAO.set_accessories_layer_id(layers_data.ACCESSORIES_LAYER_ID))
        if sucess:
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
