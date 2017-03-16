
.. Copyright SAS Institute

.. currentmodule:: saspy

***************
Getting started
***************

SASPy is an interface module to the SAS System. It connects to SAS 9.4 (released July 2013) or newer and allows users
to take advantage of their licenced SAS infrastructure through Python 3.x
It is the communication layer for the `sas_kernel <https://github.com/sassoftware/sas_kernel>`_
SASPy is an open source project and your contributions are appreciated and encouraged.

The SASPy interface is designed to allow users to use Python syntax and
constructs to interact with MVA SAS (SAS 9.4). It makes SAS the
analytical engine or "calculator" for data analysis. In its most simple
form, SASPy is a code translator taking python commands and converting
them into SAS language statements and then displaying the results.

Please open issues for things you see!

We will start with a basic example using `Kaggle Resources Analytics <https://www.kaggle.com/ludobenistant/hr-analytics>`_ data

Initial import
==============
It is assumed you have already :doc:`installed <install>` and :doc:`configured <configuration>` SASPy but if not please
 see the respective links to get started

.. code:: ipython3

    import saspy
    import pandas as pd
    from IPython.display import HTML

Create SAS session
==================
In this code we have created a SASsession named `sas` using the default configuration. Each SASsession is a connection to a
seperated SAS instance. The cfgname= paramter specifies which Configuration Definition you want to connect to (in sascfg.py).
If there is only one defined, you don't need to specify cfgname=. If there are more then one, and you don't specify one,
you will be prompted for which one to use. 

Once a connection is ready a note similar to the the one below will be displayed.

.. code:: ipython3

    sas = saspy.SASsession(cfgname='default')


.. parsed-literal::

    SAS Connection established. Subprocess id is 28207


Load sata into SAS
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
    hr = sas.df2sd(hr_pd)  # the short for of: hr = sas.dataframe2sasdata(hr_pd) 


Existing SAS data set
---------------------
.. code:: ipython3

    hr = sas.sasdata('hr', 'mylibref')  # or simpley hr = sas.sasdata('hr') if hr is in your 'work' or 'user' library

Explore the data
================
There are a number of tabular and graphical methods to view your data here are a few. Please see the :doc:`api` for a
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


Submit SAS code directly from Python session
============================================
If you encounter a situation where you need to submit code directly to the SAS system, there is a submit method to
accomplish that. Here we are creating a side by side panel plot to compare employees who have left vs those still
working at the company based on their business unit and median performance rating and satisifaction level.
The submit method returns a dictionary with two keys: LOG and LST. The LST has the results to display and the LOG has the
portion of the SAS log for that code submittal. 

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
Partitioning data is essential to avoid overfitting during model development. this can be achived using the partition
method. In this example we are going to partion inplace stratifying based on the variable left. If no variable is
provided or the variable is interval then simple random sampling (SRS) is done.
We can then create two partitions; test and training.
.. code:: ipython3

    hr.partition('left')

    hr_train = hr.where('_PartInd_=1')
    hr_test = hr.where('_PartInd_=0')


Building an analytical model
============================
One of the key activities for SASPy is analtycal modeling. This is
The SAS System is capable of modeling in a number of distinct areas
(statisics, machine learning, econometric time series, and so on). The capabilities of SASPy are similarly divided
to make it easier for users and not clutter tab-complete lists with methods you might not actually have.
Under the session object there are methods to create an instance for each supported product.
Here is a code example to create objects for each product:
-  STAT (SAS/STAT)
-  ETS (SAS/ETS)
-  Machine learning (SAS Enterprise Miner)
-  QC (SAS/QC)
-  UTIL (SAS Base procedures)

.. code:: ipython3

    stat = sas.sasstat()
    ml   = sas.sasml()
    ets  = sas.sasets()
    qc   = sas.sasqc()
    util = sas.sasutil()

Each of these objects contain a set of methods that can perform analytical functions, namely modeling.
These methods closely follow the SAS procedures for naming and organization.
**NOTE:** The existing list of methods is not an exhaustive list of the SAS Procedures that are available and I hope you'll consider contributing
the methods you've written to do your work. Here is documentation on how to add a method (SAS Procedure).

The :doc:`api' has a complete list of methods for each object.


To see a list of the available methods you can `dir()` function for example `dir(stat)` will give you a list of the
methods available. *Not* all of the methods are procedures but the vast majority are.

.. code:: python

    dir(stat)




.. parsed-literal::

    ['__class__', '__delattr__',  '__dict__',  '__dir__',  '__doc__',  '__eq__',  '__format__', '__ge__',
    '__getattribute__', '__gt__', '__hash__',  '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__',
    '__new__', '__reduce__', '__reduce_ex__',  '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__',
     'glm',
     'hplogistic',
     'hpreg',
     'hpsplit',
     'logger',
     'logistic',
     'mixed',
     'reg',
     'sas',
     'sasproduct',
     'tpspline']



To build a model you will need to supply the required parameters to the modeling method. I'll start with an example
then explain the syntax. We'll continue using the HR data from above.

.. code:: ipython3

    t1='left'
    inputs = {'nominal':['work_accident','promotion_last_5years','sales','salary'],
        'interval':['satisfaction_level','last_evaluation','number_project','average_montly_hours','time_spend_company']
        }
    rf_model = ml.forest(data=hr, target=t1, input=inputs)

The code above creates two variables
-  `t1` which is a string that represents the target variable
-  `inputs` which is a dictionary that represents the model inputs with two keys `interval` and `nominal` which
represent the interval and nominal variables respectively to consider for modeling

Here are ways to specify the same as above using the nominal parameter and a list of inputs.
The target variable is now a dictionary

.. code:: ipython3

    t1={'nominal':'left'}
    nom = ['work_accident', 'promotion_last_5years', 'sales', 'salary']
    inputs =['work_accident', 'promotion_last_5years', 'sales', 'salary', 'satisfaction_level',
             'last_evaluation', 'number_project', 'average_montly_hours', 'time_spend_company']
    rf_model = ml.forest(data=hr, target=t1, input=inputs, nominals = nom)


Here using the nominal parameter and a string of inputs and the target is a list (`nominals` must be a list)

.. code:: ipython3

    t1=['left']
    nom = ['work_accident', 'promotion_last_5years', 'sales', 'salary', 'left']
    inputs ='work_accident promotion_last_5years sales salary satisfaction_level last_evaluation number_project
            average_montly_hours time_spend_company'
    rf_model = ml.forest(data=hr, target=t1, input=inputs, nominals = nom)


More about the target and input parameters
------------------------------------------

These rules apply to both the `target` and `input`

-  The parameters accept strings (str), lists (list), or dictionaries (dict) types
-  The `target` and `input` parameters are modified by a `nominals` parameter to identify the proper variables treatment.
    The `nominals` parameter must be a list type or you will recieve a Syntax warning
-  Variables will be treated as nominals if any of the following are met:
    -  The variable is a character type in SAS
    -  The variable is specificed in the nominals list
    -  The variable is paired with dictionary key ``'nominal'``

**Note:** If a variable is a SAS Character type then it does not need to be specified on the `nominals` parameter but
does need to be assigned to the ``'nominal'`` dictionary key if you use the dictionary object type


Evaluating model diagnostics
============================
Perhaps the most important part of modeling is evaluating the quality of the model. SASPy makes this very easy by
leverging the rich graphical and tabular output of `SAS ODS <http://support.sas.com/rnd/base/ods/>`_

The output of a model in SASPy is a `SASresults`_ <add link> Object. It contains all the ODS tables and graphics that
were produced by the SAS procedure. You can see all the available objects by using `dir()` or tab-complete on the object.

.. code:: python

    dir(rf_model)

The returned list shows the available diagnoist output for this model. The output lists will vary slightly depending on
the modeling algorthm, the settings, and the target type (nominal vs interval)

.. parsed-literal::

    ['BASELINE',
     'DATAACCESSINFO',
     'FITSTATISTICS',
     'LOG',
     'MODELINFO',
     'NOBS',
     'PERFORMANCEINFO',
     'VARIABLEIMPORTANCE']

To view a particular diagnostic, submit it as shown below. The default objects for tables are Pandas DataFrames and for plots
are HTML graphics. You can use use the `results=` option to choose HTML for tables too, if you choose.

.. code:: python

    rf_model.FITSTATISTICS


**Note:** If an error occured during processing, the only artifact will be `ERROR_LOG` which contains the SAS log to aid
you in resolving your error.

Below is an example were a the variable `left` has been typed incorrectly as `lefty`


.. code:: ipython3

    rf_model = ml.forest(data=hr, target='lefty', input=inputs, nominals = nom)

.. parsed-literal::

    SubmissionError: ERRORS found in SAS log:
    ERROR: Variable LEFTY not found.

We can see a brief detailing of the error but if more context is needed you can see the entire log for the model
submission

.. code:: ipython3

    rf_model.ERROR_LOG




Assessing model quality
=======================




Scoring new data
================




