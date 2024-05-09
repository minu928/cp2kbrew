# cp2kbrew

```BASH
version 0.0.4
```

## Install

### Using Raw Package
```bash
git clone https://github.com/minu928/cp2kbrew.git
cd cp2kbrew
pip install .
```

## LogOpener
### Single Frame Data

```python
import cp2kbrew as cpb


logfile_path = "somewere/out.log"

logopener = cpb.LogOpener(logfile=logfile_path)
print(f"nFRAME: {logopener.nframe}")
print(f"ENERGY: {logopener.energy}")
print(f"FORCE : {logopener.force}")
print(f"STRESS: {logopener.stress}")
print(f"COORD : {logopener.coord}")
print(f"CELL  : {logopener.cell}")
```
### nFrame Data
```python
import cp2kbrew as cpb


logfile_path = "somewere/out.log"

logopener = cpb.LogOpener(logfile=outlog)
logopener.gather()
print(f"nFRAME: {logopener.nframe}")
print(f"ENERGY: {logopener.energy}")
print(f"FORCE : {logopener.force}")
print(f"STRESS: {logopener.stress}")
print(f"COORD : {logopener.coord}")
print(f"CELL  : {logopener.cell}")
```

### Unit Conversion
```python
import cp2kbrew as cpb


logfile_path = "somewere/out.log"

logopener = cpb.LogOpener(logfile=outlog)
print(f"ENERGY: {logopener.energy[0,0]:.5f} {logopener.unit['energy']}")
logopener.convert_unit(to={"energy": "eV"})
print(f"ENERGY: {logopener.energy[0,0]:.5f} {logopener.unit['energy']}")
```

## TrjOpener
### Single Frame Data

```python
import cp2kbrew as cpb


trjfile_path = "somewere/out.xyz"

trjopener = cpb.TrjOpener(trjfile=trjfile_path)
print(f"nFRAME: {trjopener.nframe}")
print(f"ENERGY: {trjopener.energy}")
print(f"COORD : {trjopener.coord}")
```
### nFrame Data
```python
import cp2kbrew as cpb


trjfile_path = "somewere/out.xyz"

trjopener = cpb.TrjOpener(trjfile=trjfile_path)
trjopener.gather()
print(f"nFRAME: {trjopener.nframe}")
print(f"ENERGY: {trjopener.energy}")
print(f"COORD : {trjopener.coord}")
```

### Unit Conversion
```python
import cp2kbrew as cpb


trjfile_path = "somewere/out.xyz"

trjopener = cpb.TrjOpener(trjfile=trjxyz)
print(f"ENERGY: {trjopener.energy[0,0]:.5f} {trjopener.unit['energy']}")
trjopener.convert_unit(to={"energy": "eV"})
print(f"ENERGY: {trjopener.energy[0,0]:.5f} {trjopener.unit['energy']}")
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