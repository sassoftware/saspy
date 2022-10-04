
.. Copyright SAS Institute


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

#. Identify the product of the procedure (SAS/STAT, SAS/ETS, SAS Enterprise Miner, etc).
#. Find the corresponding file in saspy sasstat.py, sasets.py, sasml.py, etc.
#. Create a set of valid statements. Here is an example:

    .. code-block:: ipython3

        lset = {'ARIMA', 'BY', 'ID', 'MACURVES', 'MONTHLY', 'OUTPUT', 'VAR'}

    The case and order of the items will be formated.
#. Call the `doc_convert` method to generate then method call as well as the docstring markup

    .. code-block:: ipython3

        import saspy
        print(saspy.sasdecorator.procDecorator.doc_convert(lset, 'x11')['method_stmt'])
        print(saspy.sasdecorator.procDecorator.doc_convert(lset, 'x11')['markup_stmt'])


    The `doc_convert` method takes two arguments: a list of the valid statements and the proc name. It returns a dictionary with two keys, method_stmt and markup_stmt. These outputs can be copied into the appropriate product file.

#. Add the proc decorator to the new method.
    The decorator should be on the line above the method declaration.
    The decorator takes one argument, the required statements for the procedure. If there are no required statements than an empty list `{}` should be passed.
    Here are two examples one with no required arguments:

    .. code-block:: ipython3

        @procDecorator.proc_decorator({})
        def esm(self, data: ['SASdata', str] = None, ...

    And one with required arguments:

    .. code-block:: ipython3

        @procDecorator.proc_decorator({'model'})
        def mixed(self, data: ['SASdata', str] = None, ...

#. Add a link to the SAS documentation plus any additional details will be helpful to users

#. Write at least one test to exercise the procedures and include it in the
   appropriate testing file.

If you have questions, please open an issue in the GitHub repo and the maintainers will be happy to help.

.. Example
.. =======
.. Following the procedure above, I will add a method for the ADAPTIVEREG procedure.
.. I assume you have forked this repository and it is in your home directory.

.. video of forking the repository

.. video of adding the procedure

.. video of writing tests

.. video of creating the pull request

