import os
import numpy as np
import math
import matplotlib.pyplot as plt
import scipy.integrate as integrate
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Union


"""
lgax = log of gap accepted by ith driver
lgay = log of the largest gap rejected by the ith drvier
r = entry radius
e = entry width
l = flare length
Qc = average circulating flow
Qe = average entering flow
"""

def c(v, e, l, r, icd, phi, QcX):
    return kx(phi, r) * (Fx(x2x(v, e, S(e, v, l))) - fcx(x2=x2x(v, e, S(e, v, l)), e=e, icd=icd) * QcX)

def kx(phi, r):
    return 1 - 0.00347 * (phi - 30) - 0.978 * ((1 / r) - 0.05)

def Fx(x2x):
    return 303 * x2x

def fcx(x2, e, icd):
    return (0.210 * td(e, icd)) * (1 + 0.2 * x2)

def td(e, icd):
    return 1 + (0.5 / (1 + pow(e, ((icd - 60) / 10))))

def x2x(v, e, s):
    return v + ((e - v) / 1 + 2 * s)

def S(e, v, l):
    return (1.6 * (e - v)) / l

def rand_od_builder(arms):
    od = np.random.randint(50, 200, (arms, arms))
    np.fill_diagonal(od, 0)
    return od

def Qc(arm_index, od):
    n = len(od)
    QcX = 0
    for i in range (1, n):
        aai = (arm_index + i) % n # aai = actual arm index
        for j in range(i):
            adi = (arm_index + j + 1) % n # adi = actual destination index
            QcX += od[aai][adi]
    return QcX

def Qc_stack(arms, od):
    y = [0] * arms
    x = dict(zip(range(arms), y))
    for arm in range(len(od)):
        x[arm] = Qc(arm, od)
    return x

def Qe_stack(od):
    y = np.sum(od, axis=1)
    x = dict(zip(range(len(od)), y))
    return x

class Profiles(Enum):
    ONEHOUR = auto()
    FLAT = auto()
    DIRECT = auto()

class Calibrations(Enum):
    SLOPE = auto()
    INTERCEPT = auto()
    CAPACITY = auto()

class Calibration_Target(Enum):
    PCU = auto()
    QUEUE = auto()

@dataclass
class Profiler:
    profile_type: Profiles
    od: list = None
    sigma: float = 1
    period: int = 60
    periods: int = 4
    direct_levels: list = field(default_factory=list)

    def gausian_function(self, x, u, sigma=1) -> Union[str, int]:
        return lambda x: u * math.exp(-1*((pow(x - 0,2))/2 * pow(sigma,2)))
        
    def int_gausian_function(self, x, u, sigma, a, b):
        return integrate.quad(self.gausian_function(x, u, sigma), a, b)

    def one_hour(self, od, sigma, period, periods, graph):
        if graph == True:
            xi = np.arange(-4,4,0.1).tolist()
            yi = [self.gausian_function(x, u=1, sigma=1)(xi[xi.index(x)]) for x in xi]
            plt.plot(xi, yi)
            plt.show()
        else:
            for arm in range(len(od)):
                QcX = sum(od[arm])
                intervals = 8 / periods
                a, b = -4, -4 + intervals
                sectors = []
                for i in range(periods):
                    v = self.int_gausian_function(x, u=1, sigma=1, a=a, b=b)
                    full = self.int_gausian_function(x, u=1, sigma=1, a=-4, b=4)
                    sectors.append(v[0]/full[0])
                    a += intervals
                    b += intervals
                print(f"{QcX}: {sectors}")
        return dict(zip(range(len(od)), [[sectors[i] * sum(od[j]) for i in range(len(sectors))] for j in range(len(od))]))

    def flat():
        
        return
    
    def direct(self, od, period, periods):

        return

@dataclass
class Calibration:
    calibration_type: Calibrations
    calibration_method: Calibration_Target
    rfc: list
    calibration_variables: list
    calibration_targets: list

    def intercept_pcu(self):
        return

    def method_caller(self):
        method_idx = [*list(Calibrations)]
        t = self.calibration_method
        print(method_idx)
        return

    def calibrator(self):
        methods = self.method_caller(calibration_type=self.calibration_method, calibration_method=self.calibration_method)
        return

def junction_capacity(circulatory_flows, entry_flow, geometry):
    if len(geometry) != len(circulatory_flows):
        raise ValueError('Number of arms not equal')
    degSatOut = [] 
    for arm in range(len(geometry)):
        try:
            v, e, l, r, icd, phi = geometry[arm]
        except ValueError:
            print("Geometry has too many arguments")
        armCap = c(v, e, l, r, icd, phi, circulatory_flows[arm])
        print(f"ARM {arm+1}:")
        print(f"    ETNRY FLOW: {entry_flow[arm]}")
        print(f"    CIRCULATORY FLOW: {circulatory_flows[arm]}")
        print(f"    CAPACITY: {round(armCap,2)}") 
        degSat = entry_flow[arm] / armCap
        degSatOut.append(degSat)
        if degSat > 10:
            raise Warning("DoS high, check geometry and vehicle flows")
        if degSat < 0:
            raise Warning("DoS is negative")
    return degSatOut

if __name__ == "__main__":
    print(f"{'-' * os.get_terminal_size().columns}ROUNDABOUT CAPACITY\n{'-' * os.get_terminal_size().columns}")
    
    geometry = np.genfromtxt("geometry.csv", delimiter=",").tolist()
    od = rand_od_builder(len(geometry))
    
    x = dict(zip((range(len(geometry))), junction_capacity(Qc_stack(len(geometry), od), Qe_stack(od), geometry)))
    
    print(f"{'-' * os.get_terminal_size().columns}")
    
    for i in range(len(geometry)):
        print(f"Arm {i+1} RFC: {x[i]}")

    profile_eval = Profiler(profile_type=Profiles.ONEHOUR)
    t = profile_eval.one_hour(od=od, sigma=1,period=profile_eval.period, periods=profile_eval.periods, graph=False)
    print(t)

    y = Calibration(calibration_type=Calibrations.INTERCEPT, calibration_method=Calibration_Target.PCU, rfc=t, calibration_variables=[], calibration_targets=[])
    y = y.calibration_method()