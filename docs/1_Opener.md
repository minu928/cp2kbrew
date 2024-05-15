## Opener
```python
import cp2kbrew as cpb


opener = cpb.Opener("somewhere/out.log", trjfile="somewhere/trj.xyz")
print(f"nFRAME: {opener.nframe}")
print(f"ENERGY: {opener.energy}")
print(f"FORCE : {opener.force}")
print(f"STRESS: {opener.stress}")
print(f"COORD : {opener.coord}")
print(f"CELL  : {opener.cell}")
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
``