if __name__ == "__main__":
    import os
    import sys

    MOTHER_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(MOTHER_PATH)
    import cp2kbrew as cb

    trjpdb = f"{MOTHER_PATH}/src/files/cp2k/2022.2/trajectory_format/test.pdb"
    trjxyz = f"{MOTHER_PATH}/src/files/cp2k/2022.2/npt/TEST-pos-1.xyz"
    outlog = f"{MOTHER_PATH}/src/files/cp2k/2022.2/npt/out.log"
    logopener = cb.LogOpener(outlog)
    print(f"=" * 20 + f" No GATHER " + f"=" * 20)
    print(f"FRAME : {logopener.nframe}")
    print(f"ENERGY: {logopener.energy[0][0]:.5f} {logopener.unit['energy']}")
    print(f"=" * 20 + f" GATHER " + f"=" * 20)
    logopener.gather()
    print(f"FRAME : {logopener.nframe}")
    print(f"ENERGY: {logopener.energy[0][0]:.5f} {logopener.unit['energy']}")
    print(f"ENERGY SHAPE: {logopener.energy.shape}")
    print(f"=" * 20 + f"  RESET " + f"=" * 20)
    logopener.reset()
    print(f"FRAME : {logopener.nframe}")
    print(f"ENERGY: {logopener.energy[0][0]:.5f} {logopener.unit['energy']}")
    print(f"=" * 20 + f" {logopener.unit['energy']}->eV " + f"=" * 20)
    logopener.convert_unit(to={"energy": "eV"})
    print(f"FRAME : {logopener.nframe}")
    print(f"ENERGY: {logopener.energy[0][0]:.5f} {logopener.unit['energy']}")
