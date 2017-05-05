
.. Copyright SAS Institute

.. _license:

:tocdepth: 4

************************
Contributing new methods
************************

Overview
--------
This module is broken into product areas that largely follow the SAS product areas.
There are many many procedures, which translate to object methods, that are not 
currently included in the package. The aim of this document is to outline the 
steps you can take to add additional methods (procedures).

A copy of the process is included inline of each product file (sasstat.py, 
sasets.py, sasqc.py, and so on). The project maintainers expect that a new 
contribution should take less than 30 minutes the first time and less than 15 
minutes for subsequent methods.

Your contribution and feedback is greatly appreciated!

Process
=======

To add a new procedure follow these steps:

#. Create a new method for the procedure.
#. Create the set of required statements. If there are no required statements 
   then create an empty set {}.
#. Create the legal set of statements. This can often be obtained from the 
   documentation for the procedure. procopts should always be included in the 
   legal set to permit flexibility in calling the procedure.
#. Create the doc string with the following parts at a minimum:

    - Procedure name
    - Required set
    - Legal set
    - Link to the procedure documentation

#. Add the return call for the method using an existing procedure as an example.
#. Verify that all the statements in the required and legal sets are listed in 
   _makeProcCallMacro method of sasproccommons.py.
#. Write at least one test to exercise the procedures and include it in the 
   appropriate testing file.

.. Example
.. =======
.. Following the procedure above, I will add a method for the ADAPTIVEREG procedure.
.. I assume you have forked this repository and it is in your home directory.

.. video of forking the repository

.. video of adding the procedure

.. video of writing tests

.. video of creating the pull request

