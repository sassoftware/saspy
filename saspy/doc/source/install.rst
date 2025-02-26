
=============
Installation
=============

This package can be installed via pip, uv, pixi, or conda.
This will pull down the latest PyPI package and install it.
It is a pure Python package and works with Python 3.x
installations.

Installation via pip
-------------

pip is the default Python package manager that comes with Python when downloaded from python.org

To install the latest version using `pip`, you execute the following::

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

.. _python.org: https://www.python.org/

Installation via uv
-------------

`uv`_ Is a Python package and project manager, written in Rust.::

    uv init name-of-project
    cd name-of-project
    uv add saspy # adds saspy to your project from PyPI

Installing a specific release can be done from the `SASpy project releases page`_, where the X.X.X is the release version you want.::

    uv init name-of-project
    cd name-of-project
    uv add https://github.com/sassoftware/saspy/archive/vX.X.X.tar.gz

.. _uv: https://github.com/astral-sh/uv
.. _SASpy project releases page: https://github.com/sassoftware/saspy/releases

Installation via pixi
-------------

`pixi`_ is a language-agnostic and cross-platform package management tool built on the foundation of the conda ecosystem. You can install packages from the `conda-forge channel`_, or PyPI.::

    pixi init name-of-project
    pixi cd name-of-project
    pixi add saspy # Installs latest version from conda-forge channel by default.
    pixi add saspy==X.X.X # Where X.X.X is the version you'd like to install.

    # If you'd like to install saspy from PyPI.
    pixi add python # Python is a required dependency for packages installed from PyPI.
    pixi add --pypi saspy # Installs latest version from PyPI.
    pixi add --pypi saspy==X.X.X # Where X.X.X is the version you'd like to install.

.. _pixi: https://github.com/prefix-dev/pixi
.. _conda-forge channel: https://anaconda.org/conda-forge/saspy

Installation via conda
-------------

If you prefer conda install, you can use that from the conda-forge channel:

    see: https://github.com/conda-forge/saspy-feedstock#installing-saspy


To use this module after installation, you need to copy the example sascfg.py file to a
sascfg_personal.py and edit sascfg_personal.py per the instructions in the next section.

* If you run into any problems, see :doc:`troubleshooting`.
* If you have questions, open an issue at https://github.com/sassoftware/saspy/issues.




