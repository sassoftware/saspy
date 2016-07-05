PLEASE DON'T USE THIS REPO AT THE MOMENT
======
This repo was accidently synched with 3 month old code. Until we can reapply all the changes we've lost, this code is to be considered broke. We have the 'latest' good code in a pypi package which can be installed from Pypi. I'll remove this warning once the repo has been restored. 

saspy
======

saspy is an interface module to the SAS System. It works with Linux SAS and python3.
It is designed to be a native python interface with objects and methods for SAS
functionality. It already supports a lot of SAS base as well as SAS analytic functionality
and can be extended to support much more. saspy can be used in Jupyter notebooks via
the python kernel (the default) as well as directly from a python shell and in python
batch scripts too. This module provides the same results you get with the SAS_Kernel;
ODS HTML5 results, but also can provide text results for many methods for use in python
shell. In batch mode you can get access to the HTML results to write out to files to
be viewed directly in a browser later.


Usage
~~~~~

This module can be installed independent of the SAS_Kernel and used directly in python.
It is currently installed automatically when installing SAS_kernel. There is a configuration
file named sascfg.py in the package along with the rest of the code, where the path to the
SAS installation can be configured and other SAS startup options can be specified. Defaults
are already specified, so this isn't a necessary step unless SAS is installed in a different
location. The sascfg.py file has commented out examples of how to edit this if necessary.
There is also pydoc to describe the interface available at this time.



