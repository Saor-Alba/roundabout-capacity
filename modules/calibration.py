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
    
    def slope_intercept(self, z, y, x):
        return

    def intercept_pcu(self, z, y, x):
        return

    def intercept_queue(self, z, y, x):
        return

    def capacity_pcu(self, z, y, x):
        return
    
    def capacity_queue(self, z, y, x):
        return

    def method_caller(self, calibration_type, calibration_targets):
        methods = [method for method in dir(Calibration) if method.startswith("__") is False]
        methods 
        print(methods)

        #methods = dict(zip,list(Calibrations), self.intercept_pcu)
        return

    def calibrator(self):
        methods = self.method_caller(calibration_type=self.calibration_method, calibration_method=self.calibration_method)
        return