# cp2kbrew

## Install

### Using Raw Package
```bash
git clone https://github.com/minu928/cp2kbrew.git
cd cp2kbrew
pip install .
```

## Basis Tutorial

### One Frame Data

```python
import cp2kbrew as cb


logfile_path = "somewere/out.log"
trjfile_path = "somewere/out.xyz"
cp2kbrewer = cb.CP2KBrewer(logfile=logfile_path, trjfile=trjfile_path)

print(f"Current Frame: {cp2kbrewer.frame}")
print(f"Current Data : {cp2kbrewer.data}")
```
### All Frame Data

```python
import cp2kbrew as cb


logfile_path = "somewere/out.log"
trjfile_path = "somewere/out.xyz"
cp2kbrewer = cb.CP2KBrewer(logfile=logfile_path, trjfile=trjfile_path)
gathered_data = cp2kbrewer.gather()

print(f"All Data : {gathered_data}")
print(f"All Data : {cp2kbrewer.gathered_data}")
```


## Further Functions (TODO)

### Doctor
This function will figure out the **Error of LOG or TRJ**  
And change the data
```python
logfile_path = "somewere/out.log"
trjfile_path = "somewere/out.xyz"
cp2kbrewer = cb.CP2KBrewer(logfile=logfile_path, trjfile=trjfile_path, ignore_error=True)
cp2kbrewer.doctor()
```

### Units
This property will show the units of data
```python
logfile_path = "somewere/out.log"
trjfile_path = "somewere/out.xyz"
cp2kbrewer = cb.CP2KBrewer(logfile=logfile_path, trjfile=trjfile_path)
print(cp2kbrewer.units)
cp2kbrewer.change_units(what="energy", units="eV")
```