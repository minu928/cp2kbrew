# cp2kbrew

```BASH
version 0.0.3
```

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
cp2kbrewer = cb.CP2KBrewer(logfile=logfile_path, trjfile=trjfile_path, is_gather_run=True)

print(f"Force : {cp2kbrewer.force.shape}")
print(f"Cell  : {cp2kbrewer.cell.shape}")
print(f"nframe: {cp2kbrewer.nframe}")
print(f"natoms: {cp2kbrewer.natoms}")
```

### Unit Conversion
```python
import cp2kbrew as cb


logfile_path = "somewere/out.log"
trjfile_path = "somewere/out.xyz"

cp2kbrewer = cb.CP2KBrewer(logfile=logfile_path, trjfile=trjfile_path)
print(cp2kbrewer.units)
print(cp2kbrewer.force[0, 0])

cp2kbrewer.convert_unit(to={"force": "eV/angstrom", "stress": "eV/angstrom^3"})
print(cp2kbrewer.units)
print(cp2kbrewer.force[0, 1])
```
## Further Functions (TODO)

### Doctor
This function will figure out the **Error of LOG or TRJ**  
And change the data
```python
import cp2kbrew as cb


logfile_path = "somewere/out.log"
trjfile_path = "somewere/out.xyz"
cp2kbrewer = cb.CP2KBrewer(logfile=logfile_path, trjfile=trjfile_path, ignore_error=True)
cp2kbrewer.doctor()
```