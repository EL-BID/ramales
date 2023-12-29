from abc import ABC, abstractmethod

from qgis.core import QgsProject


class DAO(ABC):
    KEY_DONE = 'done'

    proj: QgsProject = QgsProject.instance()

    @property
    @classmethod
    @abstractmethod
    def SCOPE(cls):
        return NotImplementedError

    @classmethod
    def is_done(cls):
        return cls.proj.readBoolEntry(cls.SCOPE, cls.KEY_DONE, False)

    @classmethod
    def set_done(cls, done=True):
        return cls.proj.writeEntryBool(cls.SCOPE, cls.KEY_DONE, done)


class LayerRasterDAO(DAO):
    SCOPE = 'RamalesLayerRasterScope'
    KEY_LAYER_RASTER = 'LAYER_RASTER'

    @classmethod
    def get_layer_raster(cls):
        return cls.proj.readEntry(cls.SCOPE, cls.KEY_LAYER_RASTER, None)

    @classmethod
    def set_layer_raster(cls, layer_raster: str):
        return cls.proj.writeEntry(cls.SCOPE, cls.KEY_LAYER_RASTER, layer_raster)


class LanguageDAO(DAO):
    SCOPE = 'RamalesLanguageScope'
    KEY_LANGUAGE = 'LANGUAGE'

    @classmethod
    def get_language_project(cls):
        return cls.proj.readEntry(cls.SCOPE, cls.KEY_LANGUAGE, None)

    @classmethod
    def set_language_project(cls, language: str):
        return cls.proj.writeEntry(cls.SCOPE, cls.KEY_LANGUAGE, language)


class LayersInfoDAO(DAO):
    SCOPE = 'RamalesLayersInfoScope'
    KEY_BLOCKS_LAYER = 'BLOCKS_LAYER'
    KEY_NODES_LAYER = 'NODES_LAYER'
    KEY_SEGMENTS_LAYER = 'SEGMENTS_LAYER'
    KEY_LINEAR_OBSTACLES_LAYER = 'LINEAR_OBSTACLES_LAYER'
    KEY_POINT_OBSTACLES_LAYER = 'POINT_OBSTACLES_LAYER'
    KEY_ACCESSORIES_LAYER = 'ACCESSORIES_LAYER'

    @classmethod
    def get_blocks_layer_id(cls):
        return cls.proj.readEntry(cls.SCOPE, cls.KEY_BLOCKS_LAYER, None)

    @classmethod
    def get_nodes_layer_id(cls):
        return cls.proj.readEntry(cls.SCOPE, cls.KEY_NODES_LAYER, None)

    @classmethod
    def get_segments_layer_id(cls):
        return cls.proj.readEntry(cls.SCOPE, cls.KEY_SEGMENTS_LAYER, None)

    @classmethod
    def get_linear_obstacles_layer_id(cls):
        return cls.proj.readEntry(cls.SCOPE, cls.KEY_LINEAR_OBSTACLES_LAYER, None)

    @classmethod
    def get_point_obstacles_layer_id(cls):
        return cls.proj.readEntry(cls.SCOPE, cls.KEY_POINT_OBSTACLES_LAYER, None)

    @classmethod
    def get_accessories_layer_id(cls):
        return cls.proj.readEntry(cls.SCOPE, cls.KEY_ACCESSORIES_LAYER, None)

    @classmethod
    def set_blocks_layer_id(cls, blocks_layer):
        return cls.proj.writeEntry(cls.SCOPE, cls.KEY_BLOCKS_LAYER, blocks_layer)

    @classmethod
    def set_nodes_layer_id(cls, nodes_layer):
        return cls.proj.writeEntry(cls.SCOPE, cls.KEY_NODES_LAYER, nodes_layer)

    @classmethod
    def set_segments_layer_id(cls, segments_layer):
        return cls.proj.writeEntry(cls.SCOPE, cls.KEY_SEGMENTS_LAYER, segments_layer)

    @classmethod
    def set_linear_obstacles_layer_id(cls, linear_obstacles_layer):
        return cls.proj.writeEntry(cls.SCOPE, cls.KEY_LINEAR_OBSTACLES_LAYER, linear_obstacles_layer)

    @classmethod
    def set_point_obstacles_layer_id(cls, points_obstacles_layer):
        return cls.proj.writeEntry(cls.SCOPE, cls.KEY_POINT_OBSTACLES_LAYER, points_obstacles_layer)

    @classmethod
    def set_accessories_layer_id(cls, accessories_layer):
        return cls.proj.writeEntry(cls.SCOPE, cls.KEY_ACCESSORIES_LAYER, accessories_layer)


class CalculationInfoDAO(DAO):
    SCOPE = 'RamalesCalculationInfoScope'
    KEY_CALCULATION_STATUS = None

    @classmethod
    def get_status_calculation(cls):
        return cls.proj.readBoolEntry(cls.SCOPE, cls.KEY_CALCULATION_STATUS)

    @classmethod
    def set_status_calculation(cls, status: bool):
        return cls.proj.writeEntryBool(cls.SCOPE, cls.KEY_CALCULATION_STATUS, status)
