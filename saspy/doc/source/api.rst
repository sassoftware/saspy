
.. Copyright SAS Institute


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

Usage: run_sas.py [-h] [-s SAS_FNAME] [-l LOG_FNAME] [-o LST_FNAME]
                  [-r RESULTS_FORMAT] [-c CFGNAME]

Required argument:
  -s SAS_FNAME, --sas_fname SAS_FNAME
                        Name of the SAS file to be executed.
Optional arguments:
  -h, --help            show this help message and exit
  -l LOG_FNAME, --log_fname LOG_FNAME
                        Name of the output LOG file name. If not specified
                        then it is the same as the sas_fname with .sas removed
                        and .log added.
  -o LST_FNAME, --lst_fname LST_FNAME
                        Name of the output LST file. If not specified then it
                        is the same as the sas_fname with .sas removed and
                        .lst/.html added depending on the results format.
  -r RESULTS_FORMAT, --results_format RESULTS_FORMAT
                        Results format for sas_session.submit(). It may be
                        either TEXT or HTML. If not specified it is TEXT by
                        default. It is case incesensitive.
  -c CFGNAME, --cfgname CFGNAME
                        Name of the Configuration Definition to use for the
                        SASsession. If not specified then just
                        saspy.SASsession() is executed.

Examples:

.. code-block:: ipython3

    ./run_sas.py -s example_1.sas
    ./run_sas.py -s example_1.sas -l out1.log -o out1.lst
    ./run_sas.py -s example_1.sas -r TEXT
    ./run_sas.py -s example_1.sas -r HTML
    ./run_sas.py -s example_1.sas -r htMl -l out2.log -o out2.html
    ./run_sas.py -s example_1.sas -r teXt -l out3.log -o out3.lst
    ./run_sas.py -s /home/a/b/c/example_1.sas
    ./run_sas.py -s example_1.sas -r text -l out4.log -o out4.lst -c ssh

