########
Overview
########
.. I used http://documentation-style-guide-sphinx.readthedocs.io/en/latest/style-guide.html


*************
What is this?
*************

This module provides Python APIs to the SAS system. You can start a
SAS session and run analytics from Python through a combination of
object-oriented methods and Python magics.

The APIs provide interfaces for the following:

* Start a SAS session on the same host as Python or a remote host.
* Exchange data between SAS data sets and Pandas data frames.
* Use familiar methods such as ``describe()`` and ``head()`` to work with data.

Additional functionality such as machine learning, econometrics, and quality
control are organized in Python classes.

See :doc:`getting-started` for programming examples.


************
Dependencies
************

- Python3.X or higher.
- SAS 9.4 or higher. SAS Viya 3.1 or higher is also supported.
- An integrated object method (IOM) connection (one of four connection methods)
  requires Java on the client and four JAR files from your SAS installation.

You can connect to SAS on any platform that is supported for the specified SAS
releases.


**************
Jupyter magics
**************
Typically, programming with this module is performed with the Python functions
that are provided by the package.  For example, to view the first few rows
of a data set, you can use the ``head()`` method. However, if you are an
experienced SAS programmer, there might be occasions in which you prefer
to run SAS statements--such as running PROC PRINT to view the first few rows
of a data set. 

The magics that are available with the package enable you to bypass Python 
and submit programming statements to your SAS session.

The ``%%SAS`` magic enables you to submit the contents of a cell to your SAS
session. The cell magic executes the contents of the cell and returns any 
results. ::

  %%SAS
  proc print data=sashelp.class;
  run;

  data work.a;
    set sashelp.cars;
  run;

The ``%%IML`` magic enables you to submit the contents of a cell to your SAS
session for processing with PROC IML. The cell magic executes the contents
of the cell and returns any results. The PROC IML statement and the trailing
QUIT; statement are submitted automatically. ::

  %%IML
  a = I(6); * 6x6 identity matrix;
  b = j(5,5,0); *5x5 matrix of 0's;
  c = j(6,1); *6x1 column vector of 1's;
  d=diag({1 2 4});
  e=diag({1 2, 3 4});

The ``%%OPTMODEL`` magic enables you to submit the contents of a cell to your SAS
session for processing with PROC OPTMODEL. The cell magic executes the contents
of the cell and returns any results. The PROC OPTMODEL statement and the 
trailing QUIT; statement are submitted automatically. ::

  %%OPTMODEL
  /* declare variables */
  var choco >= 0, toffee >= 0;

  /* maximize objective function (profit) */
  maximize profit = 0.25*choco + 0.75*toffee;

  /* subject to constraints */
  con process1:    15*choco +40*toffee <= 27000;
  con process2:           56.25*toffee <= 27000;
  con process3: 18.75*choco            <= 27000;
  con process4:    12*choco +50*toffee <= 27000;
  /* solve LP using primal simplex solver */
  solve with lp / solver = primal_spx;
  /* display solution */
  print choco toffee;

