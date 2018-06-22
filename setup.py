import re, uuid
from setuptools import setup, find_packages


VERSIONFILE = "sensor_tracker_api/__init__.py"
ver_file = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, ver_file, re.M)


if mo:
    version = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

setup(name="tracker_api",
      version=version,
      description="library tool to interact with sensor_tracker database",
      author="Xiang Ling",
      author_email="",
      url="https://gitlab.oceantrack.org/ocean-gliders-canada/tracker_api",
      packages=find_packages(exclude=['tests']),
      python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
      install_requires=[
          "requests>=2.11.1",
          "six>=1.10.0",
          "pandas>=0.23.0",
      ],
      zip_safe=True
      )
