from dataclasses import dataclass
from modules import *
from enum import Enum, auto

import scipy.optimize as optimise
from pulp import LpMaximize, LpProblem, LpStatus, lpSum, LpVariable

class JunctionType(Enum):
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

    def global_optimisation(self):
        icd_limit = {
            JunctionType.COMPACT: 36,
            JunctionType.NORMAL: 100,
            JunctionType.MINI: 28
        }

        capacity = Capacity_Eval(
        half_lane_width=self.half_lane_width,
        entry_width=self.entry_width,
        effective_flare_length=self.effective_flare_length,
        entry_radius=self.entry_radius,
        inscribed_circle_diameter=self.inscribed_circle_diameter,
        conflict_angle=self.conflict_angle,
        circulatory_flow=self.circulatory_flow
        )

        def objective(params):
            """
            v[0], e[1], l[2], r[3], icd[4], phi[5], QcX[6] = params
            """
            v, e, l, r, icd, phi, QcX = params
            return capacity.kx(phi, r) * (capacity.Fx(capacity.x2x(v, e, capacity.S(e, v, l))) - capacity.fcx(x2=capacity.x2x(v, e, capacity.S(e, v, l)), e=e, icd=icd) * QcX)

        init = [3, 5, 10, 30, 40, 30, 300]
        optimiser = optimise.minimize(objective, x0=init, method='Nelder-Mead', options={'disp': True, 'return_all': True}, bounds=
                                        ((3, 3, 0, 10, 20, 20, None),
                                         (10, 15, 40, 200, 100, 60, None))) #PU IN BOUNDS
        if optimiser.success:
            fitted_params = optimiser.x
            print(fitted_params)
        else:
            raise ValueError(optimiser.message)

    def lp_model(self):
        icd_limit = {
            JunctionType.COMPACT: 36,
            JunctionType.NORMAL: 100,
            JunctionType.MINI: 28
        }

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

        capacity = Capacity_Eval(
            half_lane_width=self.half_lane_width,
            entry_width=self.entry_width,
            effective_flare_length=self.effective_flare_length,
            entry_radius=self.entry_radius,
            inscribed_circle_diameter=self.inscribed_circle_diameter,
            conflict_angle=self.conflict_angle,
            circulatory_flow=self.circulatory_flow
            )

        model += capacity.kx(phi, r) * (capacity.Fx(capacity.x2x(v, e, capacity.S(e, v, l))) - capacity.fcx(capacity.x2x(v, e, capacity.S(e, v, l)), e, icd) * QcX)

        print(capacity.c)

        model += (v <= al * 3, "approach width")
        model += (e >= v, "entry > approach")
        model += (e <= 10.5)
        model += (l >= 5)
        model += (l <= 100)
        model += (phi >= 20)
        model += (phi <= 60)
        model += (r >= 10)
        model += (r <= 100)
        model += (QcX == self.circulatory_flow)
        model += (icd <= icd_limit[self.junction_type])
        
        status = model.solve()
        print(status)