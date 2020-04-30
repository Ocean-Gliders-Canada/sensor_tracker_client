import re
import os
from setuptools import setup, find_packages

VERSIONFILE = "sensor_tracker_client/__init__.py"
ver_file = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, ver_file, re.M)

if mo:
    version = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


setup(
    name="sensor_tracker_client",
    version=version,
    description="library tool to interact with sensor_tracker database",
    author="Xiang Ling",
    author_email="xiang.ling@dal.ca",
    url="https://gitlab.oceantrack.org/ceotr/metadata-tracker/sensor_tracker_client",
    packages=find_packages(exclude=['tests', 'script', 'tools']),
    python_requires='>=3.5',
    long_description=read('README.md'),
    install_requires=[
        "requests==2.18.4",
        "six==1.11.0",
        "urllib3==1.24.2",
    ],
    zip_safe=True
)
