
.. Copyright SAS Institute

.. currentmodule:: saspy

***************
Getting Started
***************

SASPy is an interface module to the SAS System. It connects to SAS 9.4 (released July 2013) or newer and allows users
to take advantage of their licenced SAS infrastructure through Python 3.3+
It is the communication layer for the `sas_kernel <https://github.com/sassoftware/sas_kernel>`_
SASPY is an open source project and your contributions are appreciated and encouraged.

The SASPY interface is designed to allow users to use Python syntax and
constructs to interact with MVA SAS (SAS 9.4). It makes SAS the
analytical engine or "calculator" for data analysis. In its most simple
form, SASPY is a code translator taking python commands and converting
them into SAS procedure and data step calls and then displaying the
results.

Please open issues for things you see!

We will start with a basic example using `Kaggle Resources Analytics <https://www.kaggle.com/ludobenistant/hr-analytics>`_ data

Initial import
==============
It is assumed you have already `:any:Installation` installed and `configured` saspy but if not please see the respective links to get started

.. code:: ipython3

    import saspy
    import pandas as pd
    from IPython.display import HTML

Create SAS Instance
===================
In this code we have created an instance named `sas` using the default configuration. Each SAS instance is linked to a
distinct SAS session. If no cfgname is provided the user will be prompted from the set defined in the sascfg.py file.
Once a connection is ready a note similar to the the one below will be displayed.
.. code:: ipython3

    sas = saspy.SASsession(cfgname='default')


.. parsed-literal::

    SAS Connection established. Subprocess id is 28207


Load Data Into SAS
==================
Data can be loaded easily from many sources. Below are examples of the most common sources. In each case `hr` is a
SASdata object.

CSV
---
.. code:: ipython3

    hr = sas.read_csv("./HR_comma_sep.csv")


Pandas DataFrame
----------------
.. code:: ipython3

    hr_pd = pd.read_csv("./HR_comma_sep.csv")
    hr = sas.df2sd(hr_pd)


Existing SAS data set
---------------------
.. code:: ipython3

    hr = sas.sasdata('hr', 'mylib')

Explore the data
================
There are a number of tabular and graphical methods to view your data here are a few see the API reference for a
complete list.

List the variables
------------------
.. code:: ipython3

    hr.columnInfo()

See the first observations
--------------------------
.. code:: ipython3

    hr.head()

Summary of numeric columns
--------------------------
.. code:: ipython3

    hr.means()

Basic bar chart
---------------
.. code:: ipython3

    hr.bar('salary')

Basic histogram
---------------
.. code:: ipython3

    hr.hist('last_evaluation')


Basic heatmap
-------------
.. code:: ipython3

    hr.heatmap('last_evaluation', 'satisfaction_level')


Submit SAS Code directly from Python session
============================================
If you encounter a situation where you need to submit code directly to the SAS system, there is a submit method to
accomplish that. Here we are creating a side by side panel plot to compare employees who have left vs those still
working at the company based on their business unit and median performance rating and satisifaction level.
The submit method returns a dictionary with two keys: LOG and LST

.. code:: ipython3

    c = sas.submit("""
    proc sgpanel data=work._csv;
        PANELBY left;
        hbar sales / response=last_evaluation stat=median;
        hbar sales / response=satisfaction_level stat=median ;
    run;
    """)
    HTML(c['LST'])


Split the data into training and test
=====================================
Partioning data is essential to avoid overfitting during model development. this can be achived using the partition
method. In this example we are going to partion inplace stratifying based on the variable left. If no variable is
provided or the variable is interval then simple random sampling (SRS) is done.
We can then create two
.. code:: ipython3

    hr.partition('left')

    hr_train = hr.where('_PartInd_=1')
    hr_test = hr.where('_PartInd_=0')