from dataclasses import dataclass
from enum import Enum, auto

import numpy as np

class Flow_Type:
    IMPORT = auto()
    RANDOM = auto()

@dataclass
class OD_Eval:
    od_type: Flow_Type
    od: list
    arms: int

    def rand_od_builder(self, arms):
        od = np.random.randint(50, 200, (arms, arms))
        np.fill_diagonal(od, 0)
        return od
    
    def od_importer(self):
        """
        This needs to be considered
        """
        return

    def Qc(self, arm_index, od):
        """
        Return the circulatory flow for a given arm
        """
        n = len(od)
        QcX = 0
        for i in range (1, n):
            aai = (arm_index + i) % n # aai = actual arm index
            for j in range(i):
                adi = (arm_index + j + 1) % n # adi = actual destination index
                QcX += od[aai][adi]
        return QcX
    
    def Qc_stack(self, arms, od):
        """
        Evaluate the circulating flow for all arms and stack into dictionary
        """
        y = [0] * arms
        x = dict(zip(range(arms), y))
        for arm in range(len(od)):
            x[arm] = self.Qc(arm, od)
        return x

    def Qe_stack(od):
        """
        Evaluate the entry flow for each arm and stack into dictionary
        """
        y = np.sum(od, axis=1)
        x = dict(zip(range(len(od)), y))
        return x

    def eval(self, od_type):
        if od_type == Flow_Type.RANDOM:
            od = self.rand_od_builder(self.arms)
        else:
            od = self.od_importer()
        return od
    
    



