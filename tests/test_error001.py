if __name__ == "__main__":
    import os
    import sys

    MOTHER_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(MOTHER_PATH)

    import cp2kbrew as cb

    print(f"Purpose: Check the Error#001")

    restart_log = f"{MOTHER_PATH}/src/files/cp2k/2022.2/errors/restart_first_frame_error/out.log"
    restart_pdb = f"{MOTHER_PATH}/src/files/cp2k/2022.2/errors/restart_first_frame_error/PROJECT-pos-1.pdb"
    print("=" * 20 + " Load  " + "=" * 20)
    home = cb.Home(restart_log, restart_pdb).gather()
    alchemist = cb.Alchemist(home=home)

    print("=" * 20 + " Check " + "=" * 20)
    alchemist.check(verbose=True)
    print(alchemist.errorcodes)
    print(alchemist.decode_errorcode(alchemist.errorcodes[0]))

    print("=" * 20 + "  Fix  " + "=" * 20)
    alchemist.fix(errorcode=alchemist.errorcodes[0])
    alchemist.check(verbose=True)
    print(alchemist.errorcodes)
    print("=" * 47)
