from enum import Enum, auto
from dataclasses import dataclass, field

class Calibrations(Enum):
    SLOPE = auto()
    INTERCEPT = auto()
    CAPACITY = auto()

class Calibration_Target(Enum):
    PCU = auto()
    QUEUE = auto()

@dataclass
class Calibration:
    calibration_type: Calibrations = None
    calibration_method: Calibration_Target = None
    rfc: list = field(default_factory=list)
    calibration_variables: list = field(default_factory=list)
    calibration_targets: list = field(default_factory=list)

    perms  = {
        "z": rfc,
        "y": calibration_variables, 
        "x": calibration_targets
    }

    def slope_pcu(self, z, y, x):
        return
    
    def slope_queue(self, z, y, x):
        return

    def intercept_pcu(self, z, y, x):
        return

    def intercept_queue(self, z, y, x):
        return

    def capacity_pcu(self, z, y, x):
        return
    
    def capacity_queue(self, z, y, x):
        return

    def method_caller(self):
        methods = {
            "self.slope_pcu": [Calibrations.SLOPE,Calibration_Target.PCU],
            "self.slope_queue": [Calibrations.SLOPE,Calibration_Target.QUEUE],
            "self.intercept_pcu": [Calibrations.INTERCEPT,Calibration_Target.PCU],
            "self.intercept_queue": [Calibrations.INTERCEPT,Calibration_Target.QUEUE],
            "self.capacity_pcu": [Calibrations.CAPACITY,Calibration_Target.PCU],
            "self.capacity_queue": [Calibrations.CAPACITY,Calibration_Target.QUEUE]
            }
        op = [method for method in methods.keys() if methods.values() == [self.calibration_type,self.calibration_targets]]
        print(op)


        #methods = dict(zip,list(Calibrations), self.intercept_pcu)
        return

    def calibrator(self):
        methods = self.method_caller(calibration_type=self.calibration_method, calibration_method=self.calibration_method)
        return