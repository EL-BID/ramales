from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class LayersData:
    BLOCKS_LAYER_ID: str = ''
    RESUME_FRAME_LAYER_ID: str = ''
    NODES_LAYER_ID: str = ''
    SEGMENTS_LAYER_ID: str = ''
    LINEAR_OBSTACLES_LAYER_ID: str = ''
    POINT_OBSTACLES_LAYER_ID: str = ''
    ACCESSORIES_LAYER_ID: str = ''
    BUILDINGS_LAYER_ID: str = ''
    SERVICE_LANE_LAYER_ID: str = ''


@dataclass
class Language:
    LANGUAGE: str = ''


@dataclass
class LayerRaster:
    LAYER_RASTER: str = ''


@dataclass
class Costs:
    TRENCH_WIDTH: float = 0.0
    CRADLE_HEIGHT: float = 0.0
    WRAP_HEIGHT: float = 0.0
    SOIL_PERCENT: int = 0
    ROCK_PERCENT: int = 0
    MANUAL_PERCENT: int = 0
    MECHANICAL_PERCENT: int = 0
    OWN_PERCENT: int = 0
    CONTRIBUTION_PERCENT: int = 0
    DISPOSAL_DISTANCE: float = 0.0
    SOIL_BULKING: float = 0.0
    ROCK_SWELLING: float = 0.0

    SERVICES: List = field(
        default_factory=lambda: [10.10, 0.96, 11.93, 10.83, 0.27, 8.47, 1.21, 9.99, 2.77, 8.63, 19.56,
                                 0.28,
                                 0.16, 0.55, 0.22,
                                 35.19, 68.72, 113.04, 103.88, 33.72, 17.48, 11.03, 10.11, 3.03, 38.19,
                                 11.55, 9.53, 14.09, 24.59,
                                 13.68, 77.82, 0.51, 0.60, 4.14, 8.93, 5.97, 6.74, 24.59, 7.67, 17.02])


@dataclass
class Node:
    id: str
    name: str
    name_id: str
    node_type: str
    node_position: str
    down_box: Optional[str]
    branch_id: str
    photo: Optional[str]
    q_terrain: Optional[float]
    q_project: Optional[float]
    depth: Optional[float]
    q_rule: Optional[float]
    coord_x: Optional[float]
    coord_y: Optional[float]
    critical_depth: Optional[float]
    template: Optional[str]
    branch_position: Optional[str]
    h_branch: Optional[float]


@dataclass
class Segment:
    id: str
    length: float
    segment: str
    up_box: str
    down_box: str
    segment_id: str
    branch_id: str
    type: str
    street: str
    paviment_1: Optional[str]
    percent_pav_1: Optional[float]
    paviment_2: Optional[str]
    percent_pav_2: Optional[float]
    protection: Optional[str]
    lgt_protection: Optional[float]
    photo1: Optional[str]
    photo2: Optional[str]
    comments: Optional[str]
    pvc_diameter: Optional[float]
    up_qproject: Optional[float]
    dwn_qproject: Optional[float]
    unevenness_segment: Optional[float]
    coord_Xi: Optional[float]
    coord_Yi: Optional[float]
    coord_Xf: Optional[float]
    coord_Yf: Optional[float]
    tq: bool
    h_tq: Optional[float]
    to_envelop: Optional[bool]
    tq_link1: Optional[str]
    tq_link2: Optional[str]
    branch_position: Optional[str]
    h_branch: Optional[float]

    UpBox: Node = field(default_factory=Node, repr=False)
    DownBox: Node = field(default_factory=Node, repr=False)


@dataclass
class Ramal:
    segments: list[Segment] = field(default_factory=list)
    is_aerial: bool = False


@dataclass
class EconomyMetrics:
    return_coefficient: float = 0.0
    per_capita_endowment: float = 0.0
    number_of_people_per_economy: float = 0.0
    peak_day_coefficient: float = 0.0
    peak_hour_coefficient: float = 0.0

