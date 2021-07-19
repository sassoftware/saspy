
.. Copyright SAS Institute

.. currentmodule:: saspy

.. _api:

*************
API Reference
*************

.. automodule:: saspy
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:

SAS Session Object
------------------
.. autoclass:: SASsession
    :members:

SAS Data Object
---------------

.. autoclass:: saspy.sasdata.SASdata
    :members:

Procedure Syntax Statements
---------------------------

.. autoclass:: saspy.sasproccommons.SASProcCommons
    :members:


SAS Results
-----------
.. autoclass:: saspy.sasresults.SASresults
    :members:

SAS Procedures
--------------

Utility
~~~~~~~

.. autoclass:: saspy.sasutil.SASutil
    :members:


Machine Learning (SAS Enterprise Miner)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: saspy.sasml.SASml
    :members:

.. autosummary:: saspy.sasml.SASml

Statistics
~~~~~~~~~~

.. autoclass:: saspy.sasstat.SASstat
    :members:

Econometic and Time Series
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: saspy.sasets.SASets
    :members:

Quality Control
~~~~~~~~~~~~~~~

.. autoclass:: saspy.sasqc.SASqc
    :members:


SAS Viya VDMML
~~~~~~~~~~~~~~~

.. autoclass:: saspy.sasViyaML.SASViyaML
    :members:


SASPy Scripts
-------------

run_sas.py
~~~~~~~~~~

This user contributed script if for executing a .sas file and writing the LOG and LST to
files, much like running a .sas file from SAS in batch mode.


