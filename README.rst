saspy
======

saspy is an interface module to the SAS System. It works with Linux SAS and python3,
and is currently intended as a support module for the SAS_kernel project. The SAS_kernel
is a Jupyter Notebook kernel which surfaces the SAS Language and SAS ODS Output to
Jupyter Notebooks. With enough interest, this module can be extended to support
interfacing to SAS from the ipykernel and from basic Python.


Usage
~~~~~

As this is currently intended to be used by SAS_kernel, it will be installed automatically
when installing SAS_kernel. There is a configuration file named sascfg.py in the package
along wil the rest of the code, where the path to the SAS installation can be configured
and other SAS startup options can be specified. Defaults are already specified, so this
isn't a necessary step unless SAS is installed in a different location. The sascfg.py file
has commented out examples of how to edit this if necessary

