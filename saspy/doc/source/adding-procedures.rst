
.. Copyright SAS Institute

.. _license:

:tocdepth: 4

************************
Contributing New Methods
************************

Overview
--------
SASPy is broken into product areas that largely follow the SAS product areas.
There are many many procedures, which translate to object methods, that are not currently included in the package.
The aim of this document is to outline the needed steps to add additional methods (procedures) to SASPy.

A copy of the process is included inline of each product file (sasstat.py, sasets.py, sasqc.py and so on)
My hope is that a new contribution should be under 30 minutes the first time and under 15 minutes for subsuquent methods

Your contribution and feedback is greatly appreciated!

Process
=======

To add a new procedure do the following:

#.  Create a new method for the procedure
#.  Create the set of required statements. If there are no required statements then create an empty set {}
#. Create the legal set of statements. This can often be obtained from the documentation of the procedure. 'procopts' should always be included in the legal set to allow flexibility in calling the procedure.
#. Create the doc string with the following parts at a minimum:

    - Procedure Name
    - Required set
    - Legal set
    - Link to the procedure documentation

#. Add the return call for the method using an existing procedure as an example
#. Verify that all the statements in the required and legal sets are listed in _makeProcCallMacro method of sasproccommons.py
#. Write at least one test to exercise the procedures and include it in the appropriate testing file

Example
=======
Following the procedure above I will add the adaptivereg procedure.
I assume you have forked the SASPy repository and it is in your home directory

.. video of forking the repository


.. video of adding the procedure

.. video of writing tests

.. video of creating the pull request


FAQ
===