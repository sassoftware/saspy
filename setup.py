#!/usr/bin/env python
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

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import sys

with open('README.rst') as f:
    readme = f.read()

setup(name='saspy',
      version='1.2',
      description='A SAS interpreter for Python',
      long_description=readme,
      author='Tom Weber',
      author_email='Tom.Weber@sas.com',
      url='https://github.com/sassoftware/saspy',
      packages=['saspy'],
      cmdclass={},
      install_requires=['pygments', 'IPython', 'pre-commit'],
      classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
      ]
      )
