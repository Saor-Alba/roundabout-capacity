from dataclasses import dataclass
import math

import numpy as np

@dataclass
class Capacity_Eval:
    half_lane_width: float
    entry_width: float
    effective_flare_length: float
    entry_radius: float
    inscribed_circle_diameter: float
    conflict_angle: float
    circulatory_flow: int

    def c(self, v, e, l, r, icd, phi, QcX):
        return self.kx(phi, r) * (self.Fx(v, e, l) - self.fcx(e, icd, v, l) * QcX)

    def kx(self, phi, r):
        return 1 - 0.00347 * (phi - 30) - 0.978 * ((1 / r) - 0.05)

    def Fx(self, v, e ,l):
        return 303 * self.x2x(v, e, l)

    def fcx(self, e, icd, v, l):
        return (0.210 * self.td(e, icd)) * (1 + 0.2 * self.x2x(v, e, l))

    def td(self, e, icd):
        return 1 + (0.5 / (1 + pow(e, ((icd - 60) / 10))))

    def S(self, e, v, l):
        return (1.6 * (e - v)) / l

    def x2x(self, v, e, l):
        return v + ((e - v) / 1 + 2 * self.S(e, v, l))

    def compute(self):
        theoretical_capacity = self.c(
            v = self.half_lane_width,
            e = self.entry_width,
            l = self.effective_flare_length,
            r = self.entry_radius,
            icd = self.inscribed_circle_diameter,
            phi = self.conflict_angle,
            QcX = self.circulatory_flow
        )
        return theoretical_capacity