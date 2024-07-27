if __name__ == "__main__":
    import os
    import sys

    MOTHER_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(MOTHER_PATH)
    import cp2kbrew2 as cb

    trjpdb = f"{MOTHER_PATH}/src/files/cp2k/2022.2/trajectory_format/test.pdb"
    trjxyz = f"{MOTHER_PATH}/src/files/cp2k/2022.2/npt/TEST-pos-1.xyz"
    outlog = f"{MOTHER_PATH}/src/files/cp2k/2022.2/npt/out.log"
    print(f"[SAVE] the Single Point Calculation")
    logopener = cb.LogOpener(outlog)
    cb.save(fmt="deepmd@npy", obj=logopener, path="./tmp", element_order=["H", "O"])
    print(f"[SAVE] the Multi Point Calculation")
    logopener = cb.LogOpener(outlog).gather()
    cb.save(fmt="deepmd@npy", obj=logopener, path="./tmp", element_order=["H", "O"])
