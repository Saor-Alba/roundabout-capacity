from modules import *

CALIBRATION = False
PROFILING = False

geometry = [3, 6, 30, 20, 60, 40]

if __name__ == "__main__":
    od_builder = OD_Eval(od_type=Flow_Type.RANDOM)
    od = od_builder.rand_od_builder(arms=4)
    if PROFILING == True:
        profiler = Profiler(profile_type=Profiles.ONEHOUR)
        od = Profiler.one_hour(od, sigma=1, period=1, periods= 4, graph=False)
    if CALIBRATION == True:
        model_calibration = Calibration(
            calibration_type = Calibrations.INTERCEPT,
            calibration_method = Calibration_Target.PCU,
            rfc=[],
            calibration_variables=[],
            calibration_targets=[]
            )
    model = Capacity_Eval(*geometry, circulatory_flow=od_builder.Qc(arm_index=1, od=od))
    arm_capacity = od_builder.Qe_stack(od)[0] / model.compute()
    print(f'RFC: {round(arm_capacity,3)}')