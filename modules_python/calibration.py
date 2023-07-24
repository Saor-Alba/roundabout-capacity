from enum import Enum, auto
from dataclasses import dataclass, field
from modules.capacity_eval import Capacity_Eval

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
    entry_flow: int = None
    circulatory_flow: int = None
    average_circulatory_flow: float = None
    average_entry_flow: float = None
    half_lane_width: float = None
    entry_width: float = None
    effective_flare_length: int = None
    conflict_angle: float = None
    entry_radius: float = None
    inscribed_circle_diameter: float = None

    perms  = {
        "z": rfc,
        "y": calibration_variables, 
        "x": calibration_targets
    }

    def slope_pcu(self):
        return Capacity_Eval.kx(phi=self.conflict_angle, r=self.entry_radius) * Capacity_Eval.fcx(x2=Capacity_Eval.x2x(v=self.half_lane_width, e=self.entry_width, s=Capacity_Eval.S(v=self.half_lane_width, e=self.entry_width, l=self.effective_flare_length)),e=self.entry_width, icd=self.inscribed_circle_diameter)
    
    def slope_queue(self):
        return 

    def intercept_pcu(self):
        return self.entry_flow * self.slope_pcu * self.average_circulatory_flow

    def intercept_queue(self):
        return

    def capacity_pcu(self):
        return self.intercept_pcu + self.slope_pcu * self.circulatory_flow
    
    def capacity_queue(self):
        return

    def calibrator(self):
        
        return