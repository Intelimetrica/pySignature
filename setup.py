# -*- coding: utf-8 -*-
""" PySignature setup.py script """

# PySignature
from pysignature import __version__

# system
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from os.path import join, dirname


setup(
    name=__version__,
    version='0.1.0',
    description='My PySignature project',
    author='Edgar Cabrera',
    author_email='ecabrera@intelimetrica.com',
    packages=['pysignature','pysignature.test'],
    url='https://github.com/intelimetrica/pysignature',
    long_description=open('README.md').read(),
    install_requires=[''],
    test_suite='pysignature.test',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
      ],
)
