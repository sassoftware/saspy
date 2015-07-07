#
# Copyright SAS Institute
#
#  Licensed under the Apache License, Version 2.0 (the License);
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
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

setup(name='pysas',
      version='0.1',
      description='A SAS interpreter for Python',
      long_description=readme,
      author='Jared Dean',
      author_email='jared.dean@sas.com',
      #url='https://github.com/takluyver/bash_kernel',
      packages=['saspy'],
      cmdclass={},
      install_requires=[],
      classifiers = [
      #    'License :: OSI Approved :: BSD License',
      #    'Programming Language :: Python :: 3',
      #    'Topic :: System :: Shells',
      ]
)
