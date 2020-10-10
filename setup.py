import os
import re
from setuptools import find_packages, setup


DESCRIPTION = ""
AUTHOR = "Kyle Emrick"
GITID = "kremrik"


def get_package_name() -> str:
    packagefile = ".package-name"
    package = open(packagefile, "rt")\
        .read()\
        .strip()\
        .replace("-", "_")
    return package


def get_version() -> str:
    package = get_package_name()
    versionfile = os.path.join(package, "_version.py")
    verstr = "unknown"

    try:
        verstrline = open(versionfile, "rt").read()
    except EnvironmentError:
        pass  # no file
    else:
        VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
        mo = re.search(VSRE, verstrline, re.M)
        if mo:
            verstr = mo.group(1)
        else:
            raise RuntimeError("Error loading version")
    
    return verstr


setup(
    name=get_package_name(),
    version=get_version(),
    author=AUTHOR,
    url="https://github.com/{}/{}".format(GITID, get_package_name()),
    description=DESCRIPTION,
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=("docs")),
    include_package_data=True,
)
