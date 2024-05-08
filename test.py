import cp2kbrew as cb


if __name__ == "__main__":
    filedict_list = [
        {"log": "./src/2022.2/npt/out.log", "trj": "./src/2022.2/npt/TEST-pos-1.xyz"},
        {"log": "./src/2022.2/nvt/out.log", "trj": "./src/2022.2/npt/TEST-pos-1.xyz"},
    ]
    for filedict in filedict_list:
        file_name = filedict["log"]
        print(f"=" * 48)
        try:
            cp2kbrewer = cb.CP2KBrewer(logfile=filedict["log"], trjfile=filedict["trj"])
            print(f"SUCCESS -> {file_name}")
        except:
            print(f"FAILED  -> {file_name}")
    print(f"=" * 48)
