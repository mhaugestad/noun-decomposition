#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="noun_decomposition",
    version="0.0.1",
    author="Mathias Haugestad",
    author_email="mhaugestad@gmail.com",
    description="Python module to decompose nouns based on the SECOS algorithm",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mhaugestad/noun-decomposition",
    packages=setuptools.find_packages(include=['Secos']),
    install_requires=['scipy', 'numpy', 'pytest', 'importlib-resources'],
    python_requires='>=3.6',
)