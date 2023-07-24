from modules_python import *

od_model = OD_Eval(
    od_type=Flow_Type.RANDOM
)

def go_optimiser():
    optimiser = Geo_Optimiser(
        half_lane_width=3.56,
        entry_width=5.8,
        effective_flare_length=26.27,
        entry_radius=13.14,
        inscribed_circle_diameter=70.14,
        conflict_angle=41,
        circulatory_flow=od_model.Qc(arm_index=1,od=od_model.rand_od_builder(4)),
        approach_lanes=1,
        junction_type=JunctionType.COMPACT        
    )

    model = optimiser.global_optimisation()

def lp_optimiser():
    optimiser = Geo_Optimiser(
        half_lane_width=3.56,
        entry_width=5.8,
        effective_flare_length=26.27,
        entry_radius=13.14,
        inscribed_circle_diameter=70.14,
        conflict_angle=41,
        circulatory_flow=od_model.Qc(arm_index=1,od=od_model.rand_od_builder(4)),
        approach_lanes=1,
        junction_type=JunctionType.COMPACT
    )

    model = optimiser.lp_model()

if __name__ == "__main__":
    go_optimiser()