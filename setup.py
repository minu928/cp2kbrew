from pathlib import Path
from setuptools import setup, find_packages


version_dict = {}
with open(Path(__file__).parents[0] / "cp2kbrew/_version.py") as this_v:
    exec(this_v.read(), version_dict)
version = version_dict["__version__"]
del version_dict


setup(
    name="cp2kbrew",
    version=version,
    author="Minwoo Kim",
    author_email="minu928@snu.ac.kr",
    url="https://github.com/minu928/cp2kbrew",
    install_requires=[
        "numpy>=1.21.0,<2.0.0",
        "tqdm>=4.0.0",
        "mdbrew>=0.0.2",
    ],
    description="CP2K Dealing Programs",
    packages=find_packages(),
    keywords=["cp2k"],
    python_requires=">=3.10.0",
    package_data={"": ["*"]},
    zip_safe=False,
)
