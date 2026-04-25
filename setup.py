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

exec(open('./saspy/version.py').read())

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.md') as f:
    readme = f.read()

setup(name='saspy',
      version = __version__,
      description = 'A Python interface to SAS',
      long_description = readme,
      author = 'Tom Weber',
      author_email = 'Tom.Weber@sas.com',
      url = 'https://github.com/sassoftware/saspy',
      packages = ['saspy'],
      cmdclass = {},
      package_data = {'': ['*.js', '*.md', '*.yaml', '*.css', '*.rst'], 'saspy': ['*.sas', 'scripts/*.*', 'java/*.*', 'java/pyiom/*.*', 'java/iomclient/*.*', 'java/thirdparty/*.*']},
      install_requires = [],
      extras_require = {'iomcom': ['pypiwin32'], 'colorLOG': ['pygments'], 'parquet':['pyarrow'], 'pandas':['pandas']},
      classifiers = [
        'Programming Language :: Python :: 3',
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: System :: Shells",
        'License :: OSI Approved :: Apache Software License'
      ]
      )
