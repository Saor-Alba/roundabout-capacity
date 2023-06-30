from dataclasses import dataclass
from modules.capacity_eval import Capacity_Eval
from enum import Enum, auto

from pulp import LpMaximize, LpProblem, LpStatus, lpSum, LpVariable

class JunctionType:
    MINI = auto()
    COMPACT = auto()
    NORMAL = auto()

@dataclass
class Geo_Optimiser:
    half_lane_width: float
    entry_width: float
    effective_flare_length: float
    entry_radius: float
    inscribed_circle_diameter: float
    conflict_angle: float
    circulatory_flow: int
    approach_lanes: int
    junction_type: JunctionType
    icd_limit: int


    def lp_model(self):
        icd_limit = [{
            JunctionType.COMPACT: 36,
            JunctionType.NORMAL: 100,
            JunctionType.MINI: 28
        }]

        model = LpProblem(name="geo_optimiser", sense=LpMaximize)
        v = LpVariable(name="v", lowBound=2.5)
        e = LpVariable(name="e", lowBound=3)
        l = LpVariable(name="l", lowBound=0)
        r = LpVariable(name="r", lowBound=0)
        icd = LpVariable(name="ice", lowBound=28)
        phi = LpVariable(name="phi", lowBound=0)
        QcX = LpVariable(name="QcX", lowBound=0)
        al = LpVariable(name="al", lowBound=0)
        jlp = LpVariable(name="jlp")

        model += Capacity_Eval.c(
            v=self.half_lane_width,
            e=self.entry_width,
            l=self.effective_flare_length,
            r=self.entry_radius,
            icd=self.inscribed_circle_diameter,
            phi=self.conflict_angle,
            QcX=self.circulatory_flow
        )

        model += (v <= al * 3, "approach width")
        model += (e >= v, "entry > approach")
        model += (e < 10.5)
        model += (l > 5)
        model += (l < 100)
        model += (phi > 20)
        model += (phi < 60)
        model += (r > 10)
        model += (r < 100)
        model += (QcX == self.circulatory_flow)