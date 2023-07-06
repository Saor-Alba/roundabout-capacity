from modules import *

if __name__ == "__main__":
    od = OD_Eval.rand_od_builder()
    traffic_profiler = Profiler(profile_type=Profiles.ONEHOUR)
    model_calibration = Calibration(
        calibration_type = Calibrations.INTERCEPT,
        calibration_method = Calibration_Target.PCU,
        rfc=[],
        calibration_variables=[],
        calibration_targets=[]
        )