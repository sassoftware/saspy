
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from distutils.command.install import install
from distutils import log
import json
import os
import sys

with open('README.rst') as f:
    readme = f.read()

svem_flag = '--single-version-externally-managed'
if svem_flag in sys.argv:
    # Die, setuptools, die.
    sys.argv.remove(svem_flag)

setup(name='saspy',
      version='0.1',
      description='A SAS interpreter for Python',
      long_description=readme,
      author='Jared Dean',
      author_email='jared.dean@sas.com',
      packages=['saspy'],
      cmdclass={},
      install_requires=[],
      classifiers = [
      #    'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: SAS    :: 9'
      #    'Topic :: System :: Shells',
      ]
)
