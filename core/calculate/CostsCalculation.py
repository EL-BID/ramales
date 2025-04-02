from ..data.models import Costs, Ramal, Segment
from typing import Dict
import math


class CostCalculationRamal:
    def __init__(self, costs: Costs, ramal: Ramal):
        self.costs = costs
        self.ramal = ramal

    def get_total_extension(self):
        return sum([segment.length for segment in self.ramal.segments])

    def get_total_extension_100(self):
        return sum([segment.length for segment in self.ramal.segments if segment.pvc_diameter in (100, 110)])

    def get_total_extension_150(self):
        return sum([segment.length for segment in self.ramal.segments if segment.pvc_diameter in (150, 160)])

    def get_total_volume(self):
        if self.ramal.is_aerial:
            return 0
        total_volume = 0
        for segment in self.ramal.segments:
            prof_media = (segment.up_qproject + segment.dwn_qproject) / 2
            width = self.costs.TRENCH_WIDTH
            area = width * segment.length
            cradle_height = self.costs.CRADLE_HEIGHT
            volume = area * (prof_media + cradle_height)
            total_volume += volume
        return total_volume

    def get_soil_volume(self):
        return self.get_total_volume() * self.costs.SOIL_PERCENT / 100

    def get_rock_volume(self):
        return self.get_total_volume() * self.costs.ROCK_PERCENT / 100

    def get_manual_volume(self):
        return self.get_soil_volume() * self.costs.MANUAL_PERCENT / 100

    def get_mechanical_volume(self):
        return self.get_soil_volume() * self.costs.MECHANICAL_PERCENT / 100

    def get_total_volume_tube_100(self):
        if self.ramal.is_aerial:
            return 0
        return math.pi * (0.1 / 2) ** 2 * self.get_total_extension_100()

    def get_total_volume_tube_150(self):
        if self.ramal.is_aerial:
            return 0
        return math.pi * (0.15 / 2) ** 2 * self.get_total_extension_150()

    def get_total_backfill(self):
        if self.ramal.is_aerial or self.get_total_volume() == 0:
            return 0
        return self.get_total_volume() - self.get_total_volume_tube_100() - self.get_total_volume_tube_150()

    def get_total_backfill_soil(self):
        if self.ramal.is_aerial or self.get_soil_volume() == 0:
            return 0

        return self.get_total_backfill() - self.get_total_backfill_rock() - self.get_total_backfill_enclosure() - \
            self.get_total_backfill_cradle()

    def get_total_backfill_rock(self):
        if self.ramal.is_aerial or self.costs.ROCK_PERCENT == 0:
            return 0

        return self.get_rock_volume()

    def get_total_backfill_enclosure(self):
        if self.ramal.is_aerial:
            return 0
        return self.get_total_extension() * self.costs.TRENCH_WIDTH * self.costs.WRAP_HEIGHT

    def get_total_backfill_cradle(self):
        if self.ramal.is_aerial:
            return 0
        return self.get_total_extension() * self.costs.TRENCH_WIDTH * self.costs.CRADLE_HEIGHT

    def get_total_backfill_own(self):
        if self.ramal.is_aerial:
            return 0
        return self.get_total_backfill_soil() * self.costs.OWN_PERCENT / 100

    def get_total_backfill_contribution(self):
        if self.ramal.is_aerial:
            return 0

        return self.get_total_backfill_soil() * self.costs.CONTRIBUTION_PERCENT / 100 + \
            self.get_total_backfill_rock() + self.get_total_backfill_enclosure() + self.get_total_backfill_cradle()

    def get_total_area(self):
        return self.get_total_extension() * self.costs.TRENCH_WIDTH

    def get_pavement_areas(self) -> Dict[str, float]:
        result = {}
        for segment in self.ramal.segments:
            if str(segment.paviment_1).isnumeric():
                result[segment.paviment_1] = result.get(segment.paviment_1, 0) + \
                                             segment.percent_pav_1 / 100 * segment.length * self.costs.TRENCH_WIDTH
            if str(segment.paviment_2).isnumeric():
                result[segment.paviment_2] = result.get(segment.paviment_2, 0) + \
                                             segment.percent_pav_2 / 100 * segment.length * self.costs.TRENCH_WIDTH
        return result

    def get_protection_ramal(self):
        total_protection = 0
        for segment in self.ramal.segments:
            if str(segment.protection) != "NULL" and str(segment.lgt_protection) != "NULL":
                try:
                    ext_protection = float(segment.lgt_protection)
                except ValueError:
                    ext_protection = 0
                total_protection += ext_protection * segment.length * (segment.pvc_diameter / 1000 + 0.1)
        return total_protection

    def get_protection_tq(self):
        result = 0
        for segment in self.ramal.segments:
            if segment.tq > 0 and str(segment.protection) != "NULL":
                result += segment.h_tq * 2 * (segment.pvc_diameter / 1000 + 0.1)
        return result

    def get_protection_total(self):
        return self.get_protection_ramal() + self.get_protection_tq()

    def get_total_extension_100_material(self):
        return sum([segment.length + segment.h_tq
                    for segment in self.ramal.segments if segment.pvc_diameter in (100, 110)]) * 1.05

    def get_total_extension_150_material(self):
        return sum([segment.length + segment.h_tq
                    for segment in self.ramal.segments if segment.pvc_diameter in (150, 160)]) * 1.05


class CostCalculation:
    def __init__(self, costs: Costs, ramals: Dict[str, Ramal]):
        self.costs = costs
        self.ramals = ramals
        self.calculations = {}
        for key, ramal in ramals.items():
            self.calculations[key] = CostCalculationRamal(costs, ramal)

    def get_total_extension(self):
        return sum([calc.get_total_extension() for calc in self.calculations.values()])

    def get_total_extension_100(self):
        return sum([calc.get_total_extension_100() for calc in self.calculations.values()])

    def get_total_extension_150(self):
        return sum([calc.get_total_extension_150() for calc in self.calculations.values()])

    def get_total_volume(self):
        return sum([calc.get_total_volume() for calc in self.calculations.values()])

    def get_soil_volume(self):
        return sum([calc.get_soil_volume() for calc in self.calculations.values()])

    def get_rock_volume(self):
        return sum([calc.get_rock_volume() for calc in self.calculations.values()])

    def get_manual_volume(self):
        return sum([calc.get_manual_volume() for calc in self.calculations.values()])

    def get_mechanical_volume(self):
        return sum([calc.get_mechanical_volume() for calc in self.calculations.values()])

    def get_total_volume_tube_100(self):
        return sum([calc.get_total_volume_tube_100() for calc in self.calculations.values()])

    def get_total_volume_tube_150(self):
        return sum([calc.get_total_volume_tube_150() for calc in self.calculations.values()])

    def get_total_disposal_soil(self):
        if self.get_total_backfill_soil() == 0:
            return 0

        return self.get_total_backfill() - self.get_total_backfill_rock() - self.get_total_backfill_own()

    def get_total_disposal_soil_with_bulking(self):
        return self.get_total_disposal_soil() * self.costs.SOIL_BULKING

    def get_total_disposal_rock(self):
        return self.get_rock_volume()

    def get_total_disposal_rock_with_swelling(self):
        return self.get_total_disposal_rock() * self.costs.ROCK_SWELLING

    def get_total_backfill(self):
        return sum([calc.get_total_backfill() for calc in self.calculations.values()])

    def get_total_backfill_soil(self):
        return sum([calc.get_total_backfill_soil() for calc in self.calculations.values()])

    def get_total_backfill_rock(self):
        return sum([calc.get_total_backfill_rock() for calc in self.calculations.values()])

    def get_total_backfill_enclosure(self):
        return sum([calc.get_total_backfill_enclosure() for calc in self.calculations.values()])

    def get_total_backfill_cradle(self):
        return sum([calc.get_total_backfill_cradle() for calc in self.calculations.values()])

    def get_total_backfill_own(self):
        return sum([calc.get_total_backfill_own() for calc in self.calculations.values()])

    def get_total_backfill_contribution(self):
        return sum([calc.get_total_backfill_contribution() for calc in self.calculations.values()])

    def get_total_area(self):
        return sum([calc.get_total_area() for calc in self.calculations.values()])

    def get_pavement_areas(self) -> Dict[str, float]:
        total_pavement_areas = {}
        for calc in self.calculations.values():
            pavement_areas = calc.get_pavement_areas()
            for pavement, area in pavement_areas.items():
                if pavement not in total_pavement_areas:
                    total_pavement_areas[pavement] = 0
                total_pavement_areas[pavement] += area
        return total_pavement_areas

    def get_node_counts(self):
        result = {}
        used_nodes = set()
        for ramal_id, ramal in self.ramals.items():
            for i, segment in enumerate(ramal.segments):
                c1, c1_name = segment.UpBox.node_type, segment.UpBox.name
                c2, c2_name = segment.DownBox.node_type, segment.DownBox.name
                if c1 not in result:
                    result[c1] = 0
                if c2 not in result and i == len(ramal.segments) - 1:
                    result[c2] = 0
                if c1_name not in used_nodes:
                    result[c1] += 1
                    used_nodes.add(c1_name)

                if i == len(ramal.segments) - 1 and c2_name not in used_nodes:
                    result[c2] += 1
                    used_nodes.add(c2_name)
        return result

    def get_protection_ramals(self):
        return sum([calc.get_protection_ramal() for calc in self.calculations.values()])

    def get_protection_tqs(self):
        return sum([calc.get_protection_tq() for calc in self.calculations.values()])

    def get_protection_total(self):
        return self.get_protection_ramals() + self.get_protection_tqs()

    def get_security_plate(self):
        return math.ceil(self.get_total_extension() / 100 * 10) / 10

    def get_security_fence(self):
        return self.get_total_extension() * 1.2

    def get_security_wood(self):
        return math.ceil(self.get_total_extension() / 50 * 10) / 10

    def get_security_metal(self):
        return math.ceil(self.get_total_extension() / 150 * 10) / 10

    def get_total_extension_100_material(self):
        return sum([calc.get_total_extension_100_material() for calc in self.calculations.values()])

    def get_total_extension_150_material(self):
        return sum([calc.get_total_extension_150_material() for calc in self.calculations.values()])

    def get_connections_count(self) -> Dict[str, int]:
        result = {}
        used_nodes = set()
        for ramal_id, ramal in self.ramals.items():
            for i, segment in enumerate(ramal.segments):
                c1, c1_name = segment.UpBox.node_type, segment.UpBox.name
                c2, c2_name = segment.DownBox.node_type, segment.DownBox.name
                if c1 == '10' and c1_name not in used_nodes:
                    result['selim'] = result.get('selim', 0) + 1
                    used_nodes.add(c1_name)
                if c2 == '10' and i == len(ramal.segments) - 1 and c2_name not in used_nodes:
                    result['selim'] = result.get('selim', 0) + 1
                    used_nodes.add(c2_name)
                if segment.tq:
                    for link in [segment.tq_link1, segment.tq_link2]:
                        if link == '1' and segment.pvc_diameter in (100, 110):
                            result['c90_100'] = result.get('c90_100', 0) + 1
                        elif link == '1' and segment.pvc_diameter in (150, 160):
                            result['c90_150'] = result.get('c90_150', 0) + 1
                        elif link == '2' and segment.pvc_diameter in (100, 110):
                            result['tee_100'] = result.get('tee_100', 0) + 1
                        elif link == '2' and segment.pvc_diameter in (150, 160):
                            result['tee_150'] = result.get('tee_150', 0) + 1

                    if str(segment.tq_link1).isnumeric():
                        result[segment.tq_link1] = result.get(segment.tq_link1, 0) + 1
                    if str(segment.tq_link2).isnumeric():
                        result[segment.tq_link2] = result.get(segment.tq_link2, 0) + 1

        return result


class QuantitiesCalculations:
    def __init__(self, costs: Costs, ramals: Dict[str, Ramal]):
        self.costs = costs
        self.costs_calculation = CostCalculation(self.costs, ramals)

    # SINALIZAÇÃO E SEGURANÇA
    def get_01_01_01(self):
        return self.costs_calculation.get_security_plate()

    def get_01_01_02(self):
        return self.costs_calculation.get_security_fence()

    def get_01_01_03(self):
        return self.costs_calculation.get_security_wood()

    def get_01_01_04(self):
        return self.costs_calculation.get_security_metal()

    # SERVIÇOS TOPOGRAFICOS
    def get_01_02_01(self):
        return self.costs_calculation.get_total_extension()

    # ESCAVAÇÕES
    def get_01_03_01(self):
        return self.costs_calculation.get_manual_volume()

    def get_01_03_02(self):
        return self.costs_calculation.get_mechanical_volume()

    def get_01_03_03(self):
        return self.costs_calculation.get_rock_volume()

    # ATERROS E ENVOLTORIAS
    def get_01_04_01(self):
        return self.costs_calculation.get_total_backfill_own()

    def get_01_04_02(self):
        return (self.costs_calculation.get_total_backfill_contribution()
                - self.costs_calculation.get_total_backfill_enclosure()
                - self.costs_calculation.get_total_backfill_cradle())

    def get_01_04_03(self):
        return (self.costs_calculation.get_total_backfill_enclosure()
                + self.costs_calculation.get_total_backfill_cradle())

    # TRANSPORTE DE MATERIAIS
    def get_01_05_01(self):
        return self.costs_calculation.get_total_disposal_soil()

    def get_01_05_02(self):
        return self.get_01_05_01() * self.costs.DISPOSAL_DISTANCE

    def get_01_05_03(self):
        return self.costs_calculation.get_rock_volume()

    def get_01_05_04(self):
        return self.get_01_05_03() * self.costs.DISPOSAL_DISTANCE

    # CAIXAS E POÇOS DE VISITA
    def get_01_06_01(self):
        return self.costs_calculation.get_node_counts().get('1', 0)

    def get_01_06_02(self):
        return self.costs_calculation.get_node_counts().get('2', 0)

    def get_01_06_03(self):
        return self.costs_calculation.get_node_counts().get('4', 0)

    def get_01_06_04(self):
        return self.costs_calculation.get_node_counts().get('3', 0)

    def get_01_06_05(self):
        return self.costs_calculation.get_node_counts().get('13', 0)

    # DEMOLIÇÕES
    # 01.07.01 até 01.07.10, return 0 por enquanto em tudo
    def get_01_07_01(self):
        return (self.costs_calculation.get_pavement_areas().get('1', 0.0) +
                self.costs_calculation.get_pavement_areas().get('4', 0.0) +
                self.costs_calculation.get_pavement_areas().get('8', 0.0))

    def get_01_07_02(self):
        return self.costs_calculation.get_pavement_areas().get('10', 0.0)

    def get_01_07_03(self):
        return self.costs_calculation.get_pavement_areas().get('12', 0.0)

    def get_01_07_04(self):
        return self.costs_calculation.get_pavement_areas().get('13', 0.0)

    def get_01_07_05(self):
        return self.costs_calculation.get_pavement_areas().get('2', 0.0)

    def get_01_07_06(self):
        return self.costs_calculation.get_pavement_areas().get('3', 0.0)

    def get_01_07_07(self):
        return self.costs_calculation.get_pavement_areas().get('5', 0.0)

    def get_01_07_08(self):
        return self.costs_calculation.get_pavement_areas().get('6', 0.0)

    def get_01_07_09(self):
        return self.costs_calculation.get_pavement_areas().get('7', 0.0)

    def get_01_07_10(self):
        return self.costs_calculation.get_pavement_areas().get('9', 0.0)

    # SERVIÇOS DIRETOS
    def get_01_08_01(self):
        return self.costs_calculation.get_protection_total()

    # ASSENTAMENTO DE TUBULAÇÕES
    def get_01_09_01(self):
        return self.costs_calculation.get_total_extension_100()

    def get_01_09_02(self):
        return self.costs_calculation.get_total_extension_150()

    # MATERIAIS
    # TUBULAÇÕES
    def get_02_01_01(self):
        return self.costs_calculation.get_total_extension_100_material()

    def get_02_01_02(self):
        return self.costs_calculation.get_total_extension_150_material()

    # PEÇAS E CONEXÕES
    def get_02_02_01(self):
        return self.costs_calculation.get_connections_count().get('selim', 0)

    def get_02_02_02(self):
        return self.costs_calculation.get_connections_count().get('c90_100', 0)

    def get_02_02_03(self):
        return self.costs_calculation.get_connections_count().get('c90_150', 0)

    def get_02_02_04(self):
        return self.costs_calculation.get_connections_count().get('tee_100', 0)

    def get_02_02_05(self):
        return self.costs_calculation.get_connections_count().get('tee_150', 0)
