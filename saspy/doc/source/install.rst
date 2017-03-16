
.. Copyright SAS Institute

Installation
============

The SASPy package installs just like any other Python package.
It is a pure Python package and works with Python 3.x
installations.  To install the latest version using `pip`, you execute the following::

    pip install saspy

or, for a specific release::

    pip install http://github.com/sassoftware/saspy/releases/saspy-X.X.X.tar.gz

Dependencies
------------

SASPy has dependencies on a SAS 9.4 as well as Python 3.x. Also, in order to use SASPy after installation, you
will need to edit the sascfg.py file to configure it to be able to connect to your SAS System. Plese see the
:doc:`configuration` chapter to see how to do this. If you run into any problems, please see the :doc:`troubleshooting` 
chapter for help. If you have any questions, just open an Issue at https://github.com/sassoftware/saspy/issues.
