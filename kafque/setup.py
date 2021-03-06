"""
Kafque
------

"""
import codecs
import os
import re
from setuptools import setup


def find_version(*file_paths):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, *file_paths), 'r') as f:
        version_file = f.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name="kafque",
    version=find_version("kafque", "__init__.py"),
    url="http://github.com/iromli/kafque",
    license="MIT",
    author="Isman Firmansyah",
    author_email="isman.firmansyah@gmail.com",
    description="",
    long_description=__doc__,
    packages=["kafque"],
    zip_safe=False,
    install_requires=[
        "kafka-python",
        "click",
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
    ],
    entry_points="""
        [console_scripts]
        kafque-worker=kafque.cli:run_worker
    """,
)
