
=============
Installation
=============

This package installs just like any other Python package.
It is a pure Python package and works with Python 3.x
installations. To install the latest version using `pip`, you execute the following::

    pip install saspy

or, for a specific release::

    pip install http://github.com/sassoftware/saspy/releases/saspy-X.X.X.tar.gz

or, for a given branch (put the name of the branch after @)::

    pip install git+https://git@github.com/sassoftware/saspy.git@branchname

The best way to update and existing deployment to the latest SASPy version is to simply
uninstall and then install, picking up the latest production version from PyPI:

.. code-block:: ipython3

    pip uninstall -y saspy
    pip install saspy


Also, if you prefer conda install, you can use that from the conda-forge channel:

    see: https://github.com/conda-forge/saspy-feedstock#installing-saspy


To use this module after installation, you need to copy the example sascfg.py file to a
sascfg_personal.py and edit sascfg_personal.py per the instructions in the next section.

* If you run into any problems, see :doc:`troubleshooting`.
* If you have questions, open an issue at https://github.com/sassoftware/saspy/issues.




