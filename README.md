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
import cp2kbrew as cb


brewer = cb.Brewer("somewhere/out.log", "somewhere/out.xyz")
print(f"nFRAME: {brewer.nframe}")
print(f"ENERGY: {brewer.energy}")
print(f"FORCE : {brewer.force}")
print(f"STRESS: {brewer.stress}")
print(f"COORD : {brewer.coord}")
print(f"CELL  : {brewer.cell}")
```

## Fix the data
```python
import cp2kbrew as cb


brewer = cb.Brewer("somewhere/out.log", "somewhere/out.xyz")
error = brewer.check()
brewer.fix(error)
```

## ConvertUnit
```python
import cp2kbrew as cb


brewer = cb.Brewer("somewhere/out.log", "somewhere/out.xyz")
brewer.convert_unit(to={"energy": "hatree->eV"})
```

## Save
```python
import cp2kbrew as cb


brewer = cb.Brewer("somewhere/out.log", "somewhere/out.xyz")
brewer.save(fmt="deepmd@npy", path="./tmp", element_order=["H", "O"])
```
