from setuptools import setup, find_packages
import os

with open("README.md", encoding="utf-8") as fh:
    readme = "\n" + fh.read()

VERSION = '0.0.4'
DESCRIPTION = 'Managing the text files txt, csv and json'
LONG_DESCRIPTION = 'A package that includes friendly API for using the text files in the formats csv, ' \
                   'txt and json.'

# Setting up
setup(
    name="textfiles",
    version=VERSION,
    author="Yael Ben Yair, Hemed Tov",
    author_email=" <yaelmadmon1011@gmail.com>, <hemedbz@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=readme,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'text', 'file', 'csv', 'json', 'txt'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)