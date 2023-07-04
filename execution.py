from modules.profiler import Profiler, Profiles
from modules.calibration import Calibration, Calibrations, Calibration_Target

if __name__ == "__main__":
    traffic_profiler = Profiler(profile_type=Profiles.ONEHOUR)
    model_calibration = Calibration(
        calibration_type = Calibrations.INTERCEPT,
        calibration_method = Calibration_Target.PCU,
        rfc=[],
        calibration_variables=[],
        calibration_targets=[]
        )
    model_calibration.method_caller()
