from abc import ABC, abstractmethod

from PyQt5.QtCore import QLocale
from qgis.core import QgsProject, QgsVectorLayer, QgsMapLayer
from typing import Tuple, Dict, List

from ..data.models import Ramal, Segment, Node
import os
import json
import importlib
from ...helpers.globals import get_language_file


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
    KEY_RESUME_FRAME_LAYER = 'RESUME_FRAME_LAYER'
    KEY_NODES_LAYER = 'NODES_LAYER'
    KEY_SEGMENTS_LAYER = 'SEGMENTS_LAYER'
    KEY_LINEAR_OBSTACLES_LAYER = 'LINEAR_OBSTACLES_LAYER'
    KEY_POINT_OBSTACLES_LAYER = 'POINT_OBSTACLES_LAYER'
    KEY_ACCESSORIES_LAYER = 'ACCESSORIES_LAYER'
    KEY_BUILDINGS_LAYER = 'BUILDINGS_LAYER'
    KEY_SERVICE_LANE_LAYER = 'SERVICE_LANE_LAYER'

    @classmethod
    def get_blocks_layer_id(cls):
        return cls.proj.readEntry(cls.SCOPE, cls.KEY_BLOCKS_LAYER, None)

    @classmethod
    def get_resume_frame_layer_id(cls):
        return cls.proj.readEntry(cls.SCOPE, cls.KEY_RESUME_FRAME_LAYER, None)

    @classmethod
    def get_buildings_layer_id(cls):
        return cls.proj.readEntry(cls.SCOPE, cls.KEY_BUILDINGS_LAYER, None)

    @classmethod
    def get_service_lane_layer_id(cls):
        return cls.proj.readEntry(cls.SCOPE, cls.KEY_SERVICE_LANE_LAYER, None)

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
    def set_resume_frame_layer_id(cls, resume_frame_layer):
        return cls.proj.writeEntry(cls.SCOPE, cls.KEY_RESUME_FRAME_LAYER, resume_frame_layer)

    @classmethod
    def set_buildings_layer_id(cls, buildings_layer):
        return cls.proj.writeEntry(cls.SCOPE, cls.KEY_BUILDINGS_LAYER, buildings_layer)

    @classmethod
    def set_service_lane_layer_id(cls, service_lane_layer):
        return cls.proj.writeEntry(cls.SCOPE, cls.KEY_SERVICE_LANE_LAYER, service_lane_layer)

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


class CostsDAO(DAO):
    SCOPE = 'RamalesCostsScope'
    KEY_TRENCH_WIDTH = 'TRENCH_WIDTH'
    KEY_CRADLE_HEIGHT = 'CRADLE_HEIGHT'
    KEY_WRAP_HEIGHT = 'WRAP_HEIGHT'
    KEY_SOIL_PERCENT = 'SOIL_PERCENT'
    KEY_ROCK_PERCENT = 'ROCK_PERCENT'
    KEY_MANUAL_PERCENT = 'MANUAL_PERCENT'
    KEY_MECHANICAL_PERCENT = 'MECHANICAL_PERCENT'
    KEY_OWN_PERCENT = 'OWN_PERCENT'
    KEY_CONTRIBUTION_PERCENT = 'CONTRIBUTION_PERCENT'
    KEY_DISPOSAL_DISTANCE = 'DISPOSAL_DISTANCE'
    KEY_SOIL_BULKING = 'SOIL_BULKING'
    KEY_ROCK_SWELLING = 'ROCK_SWELLING'
    KEY_SERVICES = 'SERVICES'
    KEY_SHOW_COSTS = 'SHOW_COSTS'

    @classmethod
    def get_show_costs(cls) -> Tuple[bool, bool]:
        return cls.proj.readBoolEntry(cls.SCOPE, cls.KEY_SHOW_COSTS, False)

    @classmethod
    def set_show_costs(cls, value: bool) -> bool:
        return cls.proj.writeEntryBool(cls.SCOPE, cls.KEY_SHOW_COSTS, value)

    @classmethod
    def get_services(cls) -> Tuple[List[float], bool]:
        # O QgsProject só salva strings, então temos que fazer essa conversão para
        # float em cada elemento.
        services, success = cls.proj.readListEntry(cls.SCOPE, cls.KEY_SERVICES, [])
        try:
            services_double = [float(x) for x in services]

            return services_double, success
        except ValueError:
            return [], False

    @classmethod
    def set_services(cls, value: List[float]) -> bool:
        # O QgsProject só salva strings, então temos que garantir que só estamos inserindo números
        # em nossa lista
        if any(not isinstance(x, (float, int)) for x in value):
            return False

        services_str = [str(x) for x in value]
        return cls.proj.writeEntry(cls.SCOPE, cls.KEY_SERVICES, services_str)

    @classmethod
    def get_trench_width(cls) -> Tuple[float, bool]:
        return cls.proj.readDoubleEntry(cls.SCOPE, cls.KEY_TRENCH_WIDTH)

    @classmethod
    def set_trench_width(cls, trench_width: float) -> bool:
        return cls.proj.writeEntryDouble(cls.SCOPE, cls.KEY_TRENCH_WIDTH, trench_width)

    @classmethod
    def get_cradle_height(cls) -> Tuple[float, bool]:
        return cls.proj.readDoubleEntry(cls.SCOPE, cls.KEY_CRADLE_HEIGHT)

    @classmethod
    def set_cradle_height(cls, cradle_height: float) -> bool:
        return cls.proj.writeEntryDouble(cls.SCOPE, cls.KEY_CRADLE_HEIGHT, cradle_height)

    @classmethod
    def get_wrap_height(cls) -> Tuple[float, bool]:
        return cls.proj.readDoubleEntry(cls.SCOPE, cls.KEY_WRAP_HEIGHT)

    @classmethod
    def set_wrap_height(cls, wrap_height: float) -> bool:
        return cls.proj.writeEntryDouble(cls.SCOPE, cls.KEY_WRAP_HEIGHT, wrap_height)

    @classmethod
    def get_soil_percent(cls) -> Tuple[int, bool]:
        return cls.proj.readNumEntry(cls.SCOPE, cls.KEY_SOIL_PERCENT)

    @classmethod
    def set_soil_percent(cls, soil_percent: int) -> bool:
        return cls.proj.writeEntry(cls.SCOPE, cls.KEY_SOIL_PERCENT, soil_percent)

    @classmethod
    def get_rock_percent(cls) -> Tuple[int, bool]:
        return cls.proj.readNumEntry(cls.SCOPE, cls.KEY_ROCK_PERCENT)

    @classmethod
    def set_rock_percent(cls, rock_percent: int) -> bool:
        return cls.proj.writeEntry(cls.SCOPE, cls.KEY_ROCK_PERCENT, rock_percent)

    @classmethod
    def get_manual_percent(cls) -> Tuple[int, bool]:
        return cls.proj.readNumEntry(cls.SCOPE, cls.KEY_MANUAL_PERCENT)

    @classmethod
    def set_manual_percent(cls, manual_percent: int) -> bool:
        return cls.proj.writeEntry(cls.SCOPE, cls.KEY_MANUAL_PERCENT, manual_percent)

    @classmethod
    def get_mechanical_percent(cls) -> Tuple[int, bool]:
        return cls.proj.readNumEntry(cls.SCOPE, cls.KEY_MECHANICAL_PERCENT)

    @classmethod
    def set_mechanical_percent(cls, mechanical_percent: int) -> bool:
        return cls.proj.writeEntry(cls.SCOPE, cls.KEY_MECHANICAL_PERCENT, mechanical_percent)

    @classmethod
    def get_own_percent(cls) -> Tuple[int, bool]:
        return cls.proj.readNumEntry(cls.SCOPE, cls.KEY_OWN_PERCENT)

    @classmethod
    def set_own_percent(cls, own_percent: int) -> bool:
        return cls.proj.writeEntry(cls.SCOPE, cls.KEY_OWN_PERCENT, own_percent)

    @classmethod
    def get_contribution_percent(cls) -> Tuple[int, bool]:
        return cls.proj.readNumEntry(cls.SCOPE, cls.KEY_CONTRIBUTION_PERCENT)

    @classmethod
    def set_contribution_percent(cls, contribution_percent: int) -> bool:
        return cls.proj.writeEntry(cls.SCOPE, cls.KEY_CONTRIBUTION_PERCENT, contribution_percent)

    @classmethod
    def get_disposal_distance(cls) -> Tuple[float, bool]:
        return cls.proj.readDoubleEntry(cls.SCOPE, cls.KEY_DISPOSAL_DISTANCE)

    @classmethod
    def set_disposal_distance(cls, disposal_distance: float) -> bool:
        return cls.proj.writeEntryDouble(cls.SCOPE, cls.KEY_DISPOSAL_DISTANCE, disposal_distance)

    @classmethod
    def get_soil_bulking(cls) -> Tuple[float, bool]:
        return cls.proj.readDoubleEntry(cls.SCOPE, cls.KEY_SOIL_BULKING)

    @classmethod
    def set_soil_bulking(cls, soil_bulking: float) -> bool:
        return cls.proj.writeEntryDouble(cls.SCOPE, cls.KEY_SOIL_BULKING, soil_bulking)

    @classmethod
    def get_rock_swelling(cls) -> Tuple[float, bool]:
        return cls.proj.readDoubleEntry(cls.SCOPE, cls.KEY_ROCK_SWELLING)

    @classmethod
    def set_rock_swelling(cls, rock_swelling: float) -> bool:
        return cls.proj.writeEntryDouble(cls.SCOPE, cls.KEY_ROCK_SWELLING, rock_swelling)


class LayerDAO(ABC):
    def __init__(self, segments_layer_id, nodes_layer_id, lang):
        self.segments_layer_id = segments_layer_id
        self.nodes_layer_id = nodes_layer_id
        self.lang = lang
        self.data_json = None
        self.loc = QLocale()

    def get_segments_layer(self) -> QgsVectorLayer:
        return QgsProject.instance().mapLayer(self.segments_layer_id)


class SegmentsDAO(LayerDAO):
    def __init__(self, segments_layer_id, nodes_layer_id, lang):
        super().__init__(segments_layer_id, nodes_layer_id, lang)
        from ...helpers.utils import Utils  # devido a um erro de importação circular, foi necessário importar aqui
        self.utils = Utils()

    def get_segments(self) -> Dict[str, Ramal]:
        """
        Get all the segments from the segments layer
        @return: A dict of segments, with key being the branch_id, and value being a list of segments
        """
        result: Dict[str, Ramal] = {}
        all_segs = self.get_segments_layer().getFeatures()
        segments = []
        for s in all_segs:
            segments.append(s)
        segments = sorted(segments, key=lambda item:
        (item[self.utils.get_idx_attr(self.get_segments_layer(), 'segments', 'branch_id')],
         item[self.utils.get_idx_attr(self.get_segments_layer(), 'segments', 'segment_id')]))

        branchs = []
        for feat in segments:
            branchs.append(feat[self.utils.get_idx_attr_segments('branch_id')])

        branchs = set(branchs)

        # Initialize the result dict, getting the aerial info and h_branch.
        for branch in branchs:
            result[branch] = Ramal()
            for feat in segments:
                if feat[self.utils.get_idx_attr_segments('branch_id')] == branch:
                    branch_position = int(feat[self.utils.get_idx_attr_segments("branch_position")])
                    if branch_position == 2:
                        result[branch].is_aerial = True
                        is_aerial = True
                        h_branch = self.utils.get_element_layer_nodes(
                            node=feat[self.utils.get_idx_attr_segments('up_box')], name_attr='h_branch')
                    break
        for i, feat in enumerate(segments):
            branch_id = feat[self.utils.get_idx_attr_segments('branch_id')]
            upBox = Node(
                id=self.utils.get_element_layer_nodes(node=feat[self.utils.get_idx_attr_segments('up_box')], name_attr='id'),
                name=self.utils.get_element_layer_nodes(node=feat[self.utils.get_idx_attr_segments('up_box')],
                                                    name_attr='name'),
                name_id=self.utils.get_element_layer_nodes(node=feat[self.utils.get_idx_attr_segments('up_box')],
                                                       name_attr='name_id'),
                node_type=self.utils.get_element_layer_nodes(node=feat[self.utils.get_idx_attr_segments('up_box')],
                                                         name_attr='node_type'),
                node_position=self.utils.get_element_layer_nodes(node=feat[self.utils.get_idx_attr_segments('up_box')],
                                                             name_attr='node_position'),
                down_box=self.utils.get_element_layer_nodes(node=feat[self.utils.get_idx_attr_segments('up_box')],
                                                        name_attr='down_box'),
                branch_id=self.utils.get_element_layer_nodes(node=feat[self.utils.get_idx_attr_segments('up_box')],
                                                         name_attr='branch_id'),
                photo=self.utils.get_element_layer_nodes(node=feat[self.utils.get_idx_attr_segments('up_box')],
                                                     name_attr='photo'),
                q_terrain=self.utils.get_element_layer_nodes(node=feat[self.utils.get_idx_attr_segments('up_box')],
                                                         name_attr='q_terrain'),
                q_project=self.utils.get_element_layer_nodes(node=feat[self.utils.get_idx_attr_segments('up_box')],
                                                         name_attr='q_project'),
                depth=self.utils.get_element_layer_nodes(node=feat[self.utils.get_idx_attr_segments('up_box')],
                                                     name_attr='depth'),
                q_rule=self.utils.get_element_layer_nodes(node=feat[self.utils.get_idx_attr_segments('up_box')],
                                                      name_attr='q_rule'),
                coord_x=self.utils.get_element_layer_nodes(node=feat[self.utils.get_idx_attr_segments('up_box')],
                                                       name_attr='coord_x'),
                coord_y=self.utils.get_element_layer_nodes(node=feat[self.utils.get_idx_attr_segments('up_box')],
                                                       name_attr='coord_y'),
                critical_depth=self.utils.get_element_layer_nodes(node=feat[self.utils.get_idx_attr_segments('up_box')],
                                                              name_attr='critical_depth'),
                template=self.utils.get_element_layer_nodes(node=feat[self.utils.get_idx_attr_segments('up_box')],
                                                        name_attr='template'),
                branch_position=self.utils.get_element_layer_nodes(node=feat[self.utils.get_idx_attr_segments('up_box')],
                                                               name_attr='branch_position'),
                h_branch=self.utils.get_element_layer_nodes(node=feat[self.utils.get_idx_attr_segments('up_box')],
                                                        name_attr='h_branch')
            )
            downBox = Node(
                id=self.utils.get_element_layer_nodes(node=feat[self.utils.get_idx_attr_segments('down_box')], name_attr='id'),
                name=self.utils.get_element_layer_nodes(node=feat[self.utils.get_idx_attr_segments('down_box')],
                                                    name_attr='name'),
                name_id=self.utils.get_element_layer_nodes(node=feat[self.utils.get_idx_attr_segments('down_box')],
                                                       name_attr='name_id'),
                node_type=self.utils.get_element_layer_nodes(node=feat[self.utils.get_idx_attr_segments('down_box')],
                                                         name_attr='node_type'),
                node_position=self.utils.get_element_layer_nodes(node=feat[self.utils.get_idx_attr_segments('down_box')],
                                                             name_attr='node_position'),
                down_box=self.utils.get_element_layer_nodes(node=feat[self.utils.get_idx_attr_segments('down_box')],
                                                        name_attr='down_box'),
                branch_id=self.utils.get_element_layer_nodes(node=feat[self.utils.get_idx_attr_segments('down_box')],
                                                         name_attr='branch_id'),
                photo=self.utils.get_element_layer_nodes(node=feat[self.utils.get_idx_attr_segments('down_box')],
                                                     name_attr='photo'),
                q_terrain=self.utils.get_element_layer_nodes(node=feat[self.utils.get_idx_attr_segments('down_box')],
                                                         name_attr='q_terrain'),
                q_project=self.utils.get_element_layer_nodes(node=feat[self.utils.get_idx_attr_segments('down_box')],
                                                         name_attr='q_project'),
                depth=self.utils.get_element_layer_nodes(node=feat[self.utils.get_idx_attr_segments('down_box')],
                                                     name_attr='depth'),
                q_rule=self.utils.get_element_layer_nodes(node=feat[self.utils.get_idx_attr_segments('down_box')],
                                                      name_attr='q_rule'),
                coord_x=self.utils.get_element_layer_nodes(node=feat[self.utils.get_idx_attr_segments('down_box')],
                                                       name_attr='coord_x'),
                coord_y=self.utils.get_element_layer_nodes(node=feat[self.utils.get_idx_attr_segments('down_box')],
                                                       name_attr='coord_y'),
                critical_depth=self.utils.get_element_layer_nodes(node=feat[self.utils.get_idx_attr_segments('down_box')],
                                                              name_attr='critical_depth'),
                template=self.utils.get_element_layer_nodes(node=feat[self.utils.get_idx_attr_segments('down_box')],
                                                        name_attr='template'),
                branch_position=self.utils.get_element_layer_nodes(node=feat[self.utils.get_idx_attr_segments('down_box')],
                                                               name_attr='branch_position'),
                h_branch=self.utils.get_element_layer_nodes(node=feat[self.utils.get_idx_attr_segments('down_box')],
                                                        name_attr='h_branch')
            )
            segment = Segment(
                id=feat[self.utils.get_idx_attr_segments('id')],
                length=self.utils.str_to_float_locale(feat[self.utils.get_idx_attr_segments('length')]),
                segment=feat[self.utils.get_idx_attr_segments('segment')],
                up_box=feat[self.utils.get_idx_attr_segments('up_box')],
                segment_id=feat[self.utils.get_idx_attr_segments('segment_id')],
                branch_id=branch_id,
                down_box=feat[self.utils.get_idx_attr_segments('down_box')],
                type=feat[self.utils.get_idx_attr_segments('type')],
                street=feat[self.utils.get_idx_attr_segments('street')],
                paviment_1=feat[self.utils.get_idx_attr_segments('paviment_1')],
                percent_pav_1=self.utils.str_to_float_locale(feat[self.utils.get_idx_attr_segments('percent_pav_1')]),
                paviment_2=feat[self.utils.get_idx_attr_segments('paviment_2')],
                percent_pav_2=self.utils.str_to_float_locale(feat[self.utils.get_idx_attr_segments('percent_pav_2')]),
                protection=feat[self.utils.get_idx_attr_segments('protection')],
                lgt_protection=self.utils.str_to_float_locale(feat[self.utils.get_idx_attr_segments('lgt_protection')]),
                photo1=feat[self.utils.get_idx_attr_segments('photo1')],
                photo2=feat[self.utils.get_idx_attr_segments('photo2')],
                comments=feat[self.utils.get_idx_attr_segments('comments')],
                pvc_diameter=int(feat[self.utils.get_idx_attr_segments('pvc_diameter')]),
                up_qproject=self.utils.str_to_float_locale(feat[self.utils.get_idx_attr_segments('up_qproject')]),
                dwn_qproject=self.utils.str_to_float_locale(feat[self.utils.get_idx_attr_segments('dwn_qproject')]),
                unevenness_segment=self.utils.str_to_float_locale(feat[self.utils.get_idx_attr_segments('unevenness_segment')]),
                coord_Xi=self.utils.str_to_float_locale(feat[self.utils.get_idx_attr_segments('coord_Xi')]),
                coord_Yi=self.utils.str_to_float_locale(feat[self.utils.get_idx_attr_segments('coord_Yi')]),
                coord_Xf=self.utils.str_to_float_locale(feat[self.utils.get_idx_attr_segments('coord_Xf')]),
                coord_Yf=self.utils.str_to_float_locale(feat[self.utils.get_idx_attr_segments('coord_Yf')]),
                tq=str(feat[self.utils.get_idx_attr_segments('tq')]) == 'True',
                h_tq=self.utils.str_to_float_locale(feat[self.utils.get_idx_attr_segments('h_tq')]),
                to_envelop=feat[self.utils.get_idx_attr_segments('to_envelop')],
                tq_link1=feat[self.utils.get_idx_attr_segments('tq_link1')],
                tq_link2=feat[self.utils.get_idx_attr_segments('tq_link2')],
                branch_position=feat[self.utils.get_idx_attr_segments('branch_position')],
                h_branch=self.utils.get_element_layer_nodes(
                    node=feat[self.utils.get_idx_attr_segments('up_box')], name_attr='h_branch'),
                UpBox=upBox,
                DownBox=downBox
            )
            result[branch_id].segments.append(segment)
        return result


class EconomyMetricsDAO(DAO):
    SCOPE = 'EconomyMetricsScope'
    KEY_RETURN_COEFFICIENT = 'RETURN_COEFFICIENT'
    KEY_PER_CAPITA_ENDOWMENT = 'PER_CAPITA_ENDOWMENT'
    KEY_NUMBER_OF_PEOPLE_ECONOMY = 'NUMBER_OF_PEOPLE_ECONOMY'
    KEY_PEAK_DAY_COEFFICIENT = 'PEAK_DAY_COEFFICIENT'
    KEY_PEAK_HOUR_COEFFICIENT = 'PEAK_HOUR_COEFFICIENT'

    @classmethod
    def get_return_coefficient(cls) -> Tuple[float, bool]:
        return cls.proj.readDoubleEntry(cls.SCOPE, cls.KEY_RETURN_COEFFICIENT)

    @classmethod
    def set_return_coefficient(cls, value: float) -> bool:
        return cls.proj.writeEntryDouble(cls.SCOPE, cls.KEY_RETURN_COEFFICIENT, value)

    @classmethod
    def get_per_capita_endowment(cls) -> Tuple[float, bool]:
        return cls.proj.readDoubleEntry(cls.SCOPE, cls.KEY_PER_CAPITA_ENDOWMENT)

    @classmethod
    def set_per_capita_endowment(cls, value: float) -> bool:
        return cls.proj.writeEntryDouble(cls.SCOPE, cls.KEY_PER_CAPITA_ENDOWMENT, value)

    @classmethod
    def get_number_of_people_economy(cls) -> Tuple[float, bool]:
        return cls.proj.readDoubleEntry(cls.SCOPE, cls.KEY_NUMBER_OF_PEOPLE_ECONOMY)

    @classmethod
    def set_number_of_people_economy(cls, value: float) -> bool:
        return cls.proj.writeEntryDouble(cls.SCOPE, cls.KEY_NUMBER_OF_PEOPLE_ECONOMY, value)

    @classmethod
    def get_peak_day_coefficient(cls) -> Tuple[float, bool]:
        return cls.proj.readDoubleEntry(cls.SCOPE, cls.KEY_PEAK_DAY_COEFFICIENT)

    @classmethod
    def set_peak_day_coefficient(cls, value: float) -> bool:
        return cls.proj.writeEntryDouble(cls.SCOPE, cls.KEY_PEAK_DAY_COEFFICIENT, value)

    @classmethod
    def get_peak_hour_coefficient(cls) -> Tuple[float, bool]:
        return cls.proj.readDoubleEntry(cls.SCOPE, cls.KEY_PEAK_HOUR_COEFFICIENT)

    @classmethod
    def set_peak_hour_coefficient(cls, value: float) -> bool:
        return cls.proj.writeEntryDouble(cls.SCOPE, cls.KEY_PEAK_HOUR_COEFFICIENT, value)