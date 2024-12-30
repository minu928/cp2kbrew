# cp2kbrew

```BASH
version 0.2.0
```

## Install

### Using Raw Package
```bash
git clone https://github.com/minu928/cp2kbrew.git
cd cp2kbrew
pip install .
```


## Example
### How to open CP2K outlog
```python
import cp2kbrew as cb

logfile = "somewhere/out.log"
brewer = cb.brewer(logfile)
print(f"{brewer=}")
print(f"{brewer.brew(what='force').shape=}")
print(f"{brewer.brew(what='energy').shape=}")
print(f"{brewer.brew(what='virial').shape=}")
print(f"{brewer.brew(what='coord').shape=}")
print(f"{brewer.brew(what='atom').shape=}")
print(f"{brewer.brew(what='stress').shape=}")
print(f"{brewer.brew(what='box').shape=}")
```
### How to open CP2K trj and log
```python
import cp2kbrew as cb

logfile = "somewhere/out.log"
trjfile = "somewhere/out.xyz"
brewer = cb.brewer(logfile, trjfile)
print(f"{brewer=}")
print(f"{brewer.brew(what='force').shape=}")
print(f"{brewer.brew(what='energy').shape=}")
print(f"{brewer.brew(what='virial').shape=}")
print(f"{brewer.brew(what='coord').shape=}")
print(f"{brewer.brew(what='atom').shape=}")
print(f"{brewer.brew(what='stress').shape=}")
print(f"{brewer.brew(what='box').shape=}")
```

### How to open CP2K outlog folders
```python
import cp2kbrew as cb

logfiles = ["somewhere_000/out.log","somewhere_001/out.log", "somewhere_002/out.log"]
brewer = cb.brewer(logfiles)
print(f"{brewer=}")
print(f"{brewer.brew(what='force').shape=}")
print(f"{brewer.brew(what='energy').shape=}")
print(f"{brewer.brew(what='virial').shape=}")
print(f"{brewer.brew(what='coord').shape=}")
print(f"{brewer.brew(what='atom').shape=}")
print(f"{brewer.brew(what='stress').shape=}")
print(f"{brewer.brew(what='box').shape=}")
```

### How to write the data
```python
import cp2kbrew as cb

logfile = "somewhere/out.log"
trjfile = "somewhere/out.xyz"
brewer = cb.brewer(logfile_list)
brewer.write(fmt="deepmd@npy", path="./tmp", frames=":")
brewer.write(fmt="trj@extxyz", path="./tmp.extxyz", frames=[1, 2])
```