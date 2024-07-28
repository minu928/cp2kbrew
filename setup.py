from pathlib import Path
from setuptools import setup, find_packages


version_dict = {}
with open(Path(__file__).parents[0] / "cp2kbrew/__version__.py") as this_v:
    exec(this_v.read(), version_dict)
version = version_dict["__version__"]
del version_dict


setup(
    name="cp2kbrew",
    version=version,
    author="Knu",
    author_email="minu928@snu.ac.kr",
    url="https://github.com/minu928/cp2kbrew",
    install_requies=[
        "numpy>=1.21.0",
        "pandas<2.0.0",
        "tqdm>=4.0.0",
        "scipy>1.0.0",
    ],
    description="CP2K Dealing Programs",
    packages=find_packages(),
    keywords=["cp2k"],
    python_requires=">=3.9.0",
    package_data={"": ["*"]},
    zip_safe=False,
)
