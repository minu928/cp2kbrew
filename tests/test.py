import cp2kbrew as cb


SRC_PATH = "../src/files/cp2k/2022.2"

cluster = [f"{SRC_PATH}/clusters/000/out.log", f"{SRC_PATH}/clusters/001/out.log", f"{SRC_PATH}/clusters/002/out.log"]
try:
    cluster = cb.brewer(cluster)
    print(f"{cluster=}")
except:
    print(f"FAILED:  CLUSTER")
else:
    print(f"SUCCESS: CLUSTER")
