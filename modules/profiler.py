import math
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Union

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