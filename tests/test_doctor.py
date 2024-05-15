if __name__ == "__main__":
    import os
    import sys

    MOTHER_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(MOTHER_PATH)

    test_list = {
        "default": {
            "log": f"{MOTHER_PATH}/src/files/cp2k/2022.2/npt/out.log",
            "trj": f"{MOTHER_PATH}/src/files/cp2k/2022.2/npt/TEST-pos-1.xyz",
        },
        "restart_firstframe": {
            "log": f"{MOTHER_PATH}/src/files/cp2k/2022.2/errors/restart_first_frame_error/out.log",
            "trj": f"{MOTHER_PATH}/src/files/cp2k/2022.2/errors/restart_first_frame_error/PROJECt-pos-1.pdb",
        },
        "restart_noisy": {
            "log": f"{MOTHER_PATH}/src/files/cp2k/2022.2/errors/noisy_restart/out.log",
            "trj": f"{MOTHER_PATH}/src/files/cp2k/2022.2/errors/noisy_restart/out-pos-1.xyz",
        },
    }

    import cp2kbrew as cpb

    for name, val in test_list.items():
        print(f"=" * 20 + f"{name.upper():^20s}" + f"=" * 20)
        alchemist = cpb.Alchemist(val["log"], val["trj"]).gather()
        print(f"CHECK: {alchemist.doctor.check()}")
        print(f"FIX  : {alchemist.doctor.fix()}")
        print(f"CHECK: {alchemist.doctor.check()}")
        print(f"=" * 60)
