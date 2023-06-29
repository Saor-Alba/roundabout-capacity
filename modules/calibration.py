from enum import Enum, auto
from dataclasses import dataclass

class Calibrations(Enum):
    SLOPE = auto()
    INTERCEPT = auto()
    CAPACITY = auto()

class Calibration_Target(Enum):
    PCU = auto()
    QUEUE = auto()

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
        method_idx = list(Calibrations)
        print(method_idx)
        return

    def calibrator(self):
        methods = self.method_caller(calibration_type=self.calibration_method, calibration_method=self.calibration_method)
        return
    
