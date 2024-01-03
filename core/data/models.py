from dataclasses import dataclass


@dataclass
class LayersData:
    BLOCKS_LAYER_ID: str = ''
    NODES_LAYER_ID: str = ''
    SEGMENTS_LAYER_ID: str = ''
    LINEAR_OBSTACLES_LAYER_ID: str = ''
    POINT_OBSTACLES_LAYER_ID: str = ''
    ACCESSORIES_LAYER_ID: str = ''


@dataclass
class Language:
    LANGUAGE: str = ''


@dataclass
class LayerRaster:
    LAYER_RASTER: str = ''
