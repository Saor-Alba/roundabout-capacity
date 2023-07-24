import math
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Union

import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate

class Profiles(Enum):
    ONEHOUR = auto()
    FLAT = auto()
    DIRECT = auto()

@dataclass
class Profiler:
    profile_type: Profiles
    od: list = None
    sigma: float = 1
    period: int = 60
    periods: int = 4
    direct_levels: list = field(default_factory=list)
    sectors: list = field(default_factory=list)

    def gausian_function(self, x, u, sigma=1) -> Union[str, int]:
        return lambda x: u * math.exp(-1*((pow(x - 0,2))/2 * pow(sigma,2)))
        
    def int_gausian_function(self, x, u, sigma, a, b):
        return integrate.quad(self.gausian_function(x, u, sigma), a, b)

    def one_hour(self, od, periods, graph):
        self.sectors = []
        if graph == True:
            xi = np.arange(-4,4,0.1).tolist()
            yi = [self.gausian_function(x, u=1, sigma=self.sigma)(xi[xi.index(x)]) for x in xi]
            plt.plot(xi, yi)
            plt.show()
        for arm in range(len(od)):
            QcX = sum(od[arm])
            intervals = 8 / periods
            a, b = -4, -4 + intervals
            for i in range(periods):
                v = self.int_gausian_function(x, u=1, sigma=self.sigma, a=a, b=b)
                full = self.int_gausian_function(x, u=1, sigma=self.sigma, a=-4, b=4)
                self.sectors.append(v[0]/full[0])
                a += intervals
                b += intervals
            print(f"{QcX}: {self.sectors}")
        return dict(zip(range(len(od)), [[self.sectors[i] * sum(od[j]) for i in range(len(self.sectors))] for j in range(len(od))]))

    def flat(self, od, periods):
        self.sectors = []
        for arm in range(len(od)):
            QcX = sum(od[arm]) / periods
            self.sectors.append(QcX)
        return dict(zip(range(len(od)), [self.sectors * len(od)]))
    
    def direct(self, od, period, periods):
        """
        Need to make an importer for this
        """
        return