.. Copyright SAS Institute

:tocdepth: 4

*****
SASPy
*****

.. module:: saspy

**Date**: |today| **Version**: |version|

**Source Repository:** `<http://github.com/sassoftware/saspy>`_

**Issues and Ideas:** `<https://github.com/sassoftware/saspy/issues>`_

**Example Repo:** `<https://github.com/sassoftware/saspy-examples>`_


*************
What is this?
*************

This module provides Python APIs to the SAS system. You can start a
SAS session and run analytics from Python through a combination of
object-oriented methods or explicit SAS code submission. You can move
data between SAS data sets and Pandas dataframes and exchange values between
python variables and SAS macro variables.

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

- Python3.4 or higher.
- SAS 9.4 or higher. SAS Viya 3.1 or higher is also supported.
- To use the integrated object method (IOM) access method (one of four connection methods)
  requires Java 7 or higher on the client.

You can connect to SAS on any platform that is supported for the specified SAS
releases.


.. toctree::

   install
   configuration
   getting-started
   api
   advanced-topics
   adding-procedures
   limitations
   troubleshooting
   license


Index
=====

* :ref:`genindex`

