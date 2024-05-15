# cp2kbrew

```BASH
version 0.0.6
```

## Install

### Using Raw Package
```bash
git clone https://github.com/minu928/cp2kbrew.git
cd cp2kbrew
pip install .
```

## Tutorial

## Open the files
```python
import cp2kbrew as cpb


alchemist = cpb.Alchemist("somewhere/out.log", "somewhere/out.xyz")
print(f"nFRAME: {alchemist.nframe}")
print(f"ENERGY: {alchemist.energy}")
print(f"FORCE : {alchemist.force}")
print(f"STRESS: {alchemist.stress}")
print(f"COORD : {alchemist.coord}")
print(f"CELL  : {alchemist.cell}")
```

## Fix the data
```python
import cp2kbrew as cpb


alchemist = cpb.Alchemist("somewhere/out.log", "somewhere/out.xyz")
print(f"CHECK: {alchemist.doctor.check()}")
print(f"FIX  : {alchemist.doctor.fix()}")
print(f"CHECK: {alchemist.doctor.check()}")
```

## ConvertUnit
```python
import cp2kbrew as cpb


alchemist = cpb.Alchemist("somewhere/out.log", "somewhere/out.xyz")
alchemist.convert_unit(to={"energy": "hatree->eV"})
```

## Save
```python
import cp2kbrew as cpb


alchemist = cpb.Alchemist("somewhere/out.log", "somewhere/out.xyz")
alchemist.save(fmt="deepmd@npy", path="./tmp", element_order=["H", "O"])
```