if __name__ == "__main__":
    import os
    import sys

    MOTHER_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(MOTHER_PATH)
    import cp2kbrew as cb

    paths = {
        "pdb": f"{MOTHER_PATH}/src/files/cp2k/2022.2/trajectory_format/test.pdb",
        "xyz": f"{MOTHER_PATH}/src/files/cp2k/2022.2/npt/TEST-pos-1.xyz",
    }

    for fmt, path in paths.items():
        print(f"=" * 20 + f" {fmt.upper()} " + "=" * 20)
        trjopener = cb.TrjOpener(trjfile=path)
        print(f"natom       : {trjopener.natom}")
        print(f"nframe      : {trjopener.nframe}")
        print(f"coord  shape: {trjopener.coord.shape}")
        print(f"energy shape: {trjopener.energy.shape}")
        print(f"energy shape: {trjopener.energy.shape}")

        trjopener.gather()
        print(f"natom       : {trjopener.natom}")
        print(f"nframe      : {trjopener.nframe}")
        print(f"coord  shape: {trjopener.coord.shape}")
        print(f"energy shape: {trjopener.energy.shape}")
        print(f"energy shape: {trjopener.energy.shape}")
