import modules.profiler as profiler
import modules.calibration as cal

if __name__ == "__main__":
    traffic_profiler = profiler.Profiler(profile_type=profiler.Profiles.ONEHOUR)
    model_calibration = cal.Calibration(
        calibration_type = cal.Calibrations.INTERCEPT,
        calibration_method = cal.Calibration_Target.PCU,
        rfc=[],
        calibration_variables=[],
        calibration_targets=[]
        )
    model_calibration.method_caller()
