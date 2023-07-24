from modules_python import *

CALIBRATION = False
PROFILING = False

geometry = [3, 6, 30, 20, 60, 40]

def main(geometry):
        
    # Define worksheets and location references for inputs
    app, wb, ctrl, odin, loc_dict = Data_Input.main()

    # Iterate through each parameter to parse values and return checks
    geometry = []
    for param in ["v", "e", "l", "r", "icd", "phi"]:
        geometry.append(Data_Input.import_params(ctrl, param, loc_dict)) 

    od, arms = Data_Input.import_od(ctrl, odin)

    od_builder = OD_Eval(od_type=Flow_Type.RANDOM)
    od = od_builder.rand_od_builder(arms=5)
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
    Data_Input.print_out(app, wb, ctrl, arm_capacity)

if __name__ == "__main__":
    main(geometry=geometry)