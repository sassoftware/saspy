
.. Copyright SAS Institute

.. currentmodule:: saspy

***************
Getting started
***************

This is an interface module to the SAS System. It connects to SAS 9.4 
(released July 2013) or newer and enables Python programmers to take 
advantage of their licensed SAS infrastructure through Python 3.x.

The interface is designed to enable programmers to use Python 
syntax and constructs to interact with SAS. The interface makes SAS the
analytical engine--or "calculator" for data analysis. In its most simple
form, it is a code translator that accepts Python commands and 
converts them into SAS language statements. The statements are run,
and then the results are returned to Python to be displayed or accessed.

This is an open source project. Your contributions are appreciated 
and encouraged. Please open issues in gitlab for problems that you see!

The rest of this section demonstrates how to use this module with a simple example.
The example uses `Kaggle Resources Analytics 
<https://www.kaggle.com/ludobenistant/hr-analytics>`_ data.

 
Initial import
==============
It is assumed you have already done the :doc:`installation and configuration <install>`.
If you have not, refer to that section for more information.

.. code-block:: ipython3

    import saspy
    import pandas as pd
    from IPython.display import HTML


Start a SAS session
===================
In the following code we start a SAS session named ``sas`` using the default 
configuration. Each SAS session is a connection to a separate SAS instance.
The cfgname parameter specifies the configuration definition (in sascfg.py) 
to use for the connection to SAS.

If sascfg.py has only one connection definition, then you do not need to 
specify the cfgname parameter. If the file has more than one connection
definition and you do not specify the one to use with cfgname, you are 
prompted for the connection to use. 

After a connection is made and a SAS session is started, a note that is 
similar to the the one below is displayed.

.. code-block:: ipython3

    sas = saspy.SASsession(cfgname='default')


.. parsed-literal::

    SAS Connection established. Subprocess id is 28207


Load data into SAS
==================
Data can be loaded easily from many sources. The following examples show 
the most common methods. In each case, ``hr`` is a SASdata object that
represents a SAS data set.


CSV
---
In the following example, the CSV file is accessible to Python. The 
``sas`` object reads the CSV file and creates a SAS data set in the
SAS session.

.. code-block:: ipython3

    hr = sas.read_csv("./HR_comma_sep.csv")


Pandas DataFrame
----------------
In the following example, the CSV file is accessible to Python. First,
the CSV file is read into a data frame. Then the ``sas`` object
reads the data frame and creates a SAS data set in the SAS session.

.. code-block:: ipython3

    hr_pd = pd.read_csv("./HR_comma_sep.csv")
    hr = sas.df2sd(hr_pd)  # the short form of: hr = sas.dataframe2sasdata(hr_pd) 


Existing SAS data set
---------------------
In the following example, no data file is accessible to Python. An existing
SAS data set that is accessible to the SAS session is associated with the
``hr`` object.

.. code-block:: ipython3

    hr = sas.sasdata('hr', 'mylibref')  

    # or simply: hr = sas.sasdata('hr') 
    # ...if hr.sas7bdat is in your 'work' or 'user' library

Explore the data
================
There are a number of tabular and graphical methods to view your data.
The following examples show common methods. See the :doc:`api` for a
complete list.

List the variables
------------------
.. code-block:: ipython3

    hr.columnInfo()

See the first observations
--------------------------
.. code-block:: ipython3

    hr.head()

Summary of numeric columns
--------------------------
.. code-block:: ipython3

    hr.means()

Basic bar chart
---------------
.. code-block:: ipython3

    hr.bar('salary')

Basic histogram
---------------
.. code-block:: ipython3

    hr.hist('last_evaluation')


Basic heatmap
-------------
.. code-block:: ipython3

    hr.heatmap('last_evaluation', 'satisfaction_level')


Submit SAS code directly from Python session
============================================
The proceeding examples demonstrate commonly used Python
methods that are available with this module.


If you encounter a situation where you need to submit SAS
statements directly to the SAS system, the submit method can
accomplish that. The following example creates a side-by-side
panel plot to compare employees who have left versus employees
still working at the company, based on their business unit,
median performance rating, and satisfaction level.

The submit method returns a dictionary with two keys: LOG and LST.
The LST has the results to display and the LOG has the portion 
of the SAS log for the code submission.

.. code-block:: ipython3

    c = sas.submit("""
    proc sgpanel data=work._csv;
        PANELBY left;
        hbar sales / response=last_evaluation    stat=median;
        hbar sales / response=satisfaction_level stat=median;
    run;
    """)
    HTML(c['LST'])


Split the data into training and test
=====================================
Partitioning data is essential to avoid overfitting during
model development. This can be achieved using the partition
method. In this example, the data is partitioned in-place
and performs stratified sampling, based on the variable 
'left.' If you do not specify a variable or the variable
is an interval, then simple random sampling (SRS) is done.

We create two partitions: test and training.

.. code-block:: ipython3

    hr.partition('left')

    hr_train = hr.where('_PartInd_=1')
    hr_test = hr.where('_PartInd_=0')


Build an analytical model
=========================
One of the key activities for this module is analytical modeling. The SAS
system is capable of modeling in a number of distinct areas
(statistics, machine learning, econometric time series, and so on).

These capabilities are organized similarly to make it easier 
for users. Grouping functionality also avoids cluttered tab-complete 
lists with methods that you might not have licensed.

The session object has methods to create an instance for each supported 
product. 

* STAT (SAS/STAT)
* ETS (SAS/ETS)
* Machine learning (SAS Enterprise Miner)
* QC (SAS/QC)
* UTIL (SAS Base procedures)

Here is a code example to create an object for each product:

.. code-block:: ipython3

    stat = sas.sasstat()
    ml   = sas.sasml()
    ets  = sas.sasets()
    qc   = sas.sasqc()
    util = sas.sasutil()

Each of these objects contains a set of methods that perform analytical 
functions, namely modeling. These methods closely follow the SAS procedures 
for naming and organization.  

.. note:: The existing list of methods is not an exhaustive list of the 
          SAS procedures that are available with each product. Please
          consider contributing the methods you've written to do your work. 

The :doc:`api` documentation shows how to add a method that corresponds to
a SAS procedure. The API has a complete list of methods for each object.

You can use the ``dir()`` function to see a list of the available methods. 
For example, ``dir(stat)`` provides a list of the methods that are available. 
**Not** all of the methods correspond to a procedure but the vast majority do.

.. code-block:: python

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



To build a model, you need to supply the required parameters to the modeling 
method. I'll start with an example then explain the syntax. We'll continue 
using the HR data from above.

.. code-block:: ipython3

    t1='left'

    inputs = {
       'nominal':['work_accident','promotion_last_5years','sales','salary'],
       'interval':['satisfaction_level','last_evaluation','number_project','average_montly_hours','time_spend_company']
    }

    rf_model = ml.forest(data=hr, target=t1, input=inputs)

The preceding code creates two variables:

t1
  A string that represents the target variable.

inputs
  A dictionary that represents the model inputs with two keys--interval and 
  nominal--which represent the interval and nominal variables respectively
  to consider for modeling.

Here is another way to specify the same as above--using the nominal parameter 
and a list of inputs. The target variable is now a dictionary.

.. code-block:: ipython3

    t1={'nominal':'left'}

    nom = ['work_accident', 'promotion_last_5years', 'sales', 'salary']

    inputs =['work_accident', 'promotion_last_5years', 'sales', 'salary', 'satisfaction_level',
             'last_evaluation', 'number_project', 'average_montly_hours', 'time_spend_company']

    rf_model = ml.forest(data=hr, target=t1, input=inputs, nominals = nom)


Here is another way--using the nominal parameter and a string of inputs. The 
target is a list (nominals must be a list).

.. code-block:: ipython3

    t1=['left']

    nom = ['work_accident', 'promotion_last_5years', 'sales', 'salary', 'left']

    inputs ='work_accident promotion_last_5years sales salary satisfaction_level last_evaluation number_project
            average_montly_hours time_spend_company'

    rf_model = ml.forest(data=hr, target=t1, input=inputs, nominals = nom)


More about the target and input parameters
------------------------------------------

These rules apply to both target and input:

* The parameters accept strings (str), lists (list), or dictionaries (dict) types.
* The target and input parameters are modified by a nominals parameter to 
  identify the proper variables treatment.
* The nominals parameter must be a list type or you receive a syntax warning.
* Variables are treated as nominals if any of the following are met:

  * The variable is a character type in SAS.
  * The variable is specified in the nominals list.
  * The variable is paired with dictionary key ``'nominal'``.

.. note:: If a variable is a SAS character type then it does not need to be 
          specified in the nominals parameter but does need to be assigned 
          to the ``'nominal'`` dictionary key if you use the dictionary 
          object type.


Evaluating model diagnostics
============================
Perhaps the most important part of modeling is evaluating the quality of the 
model. This is made very easy by leveraging the rich graphical and tabular
output of `SAS ODS <http://support.sas.com/rnd/base/ods/>`_.

The output of a model in is a :any:`SASresults` object. It contains all 
the ODS tables and graphics that were produced by the SAS procedure. You can 
see all the available objects by using ``dir()`` or tab-complete on the object.

.. code-block:: python

    dir(rf_model)

The returned list shows the available diagnostic output for this model. The 
output lists vary slightly, depending on the modeling algorithm, the settings,
and the target type (nominal or interval).

.. parsed-literal::

    ['BASELINE',
     'DATAACCESSINFO',
     'FITSTATISTICS',
     'LOG',
     'MODELINFO',
     'NOBS',
     'PERFORMANCEINFO',
     'VARIABLEIMPORTANCE']

To view a particular diagnostic, submit it as shown below. The default objects 
for tables are Pandas DataFrames and for plots are HTML graphics. You can use 
use the ``results`` option to choose HTML for tables too, if you choose.

.. code-block:: python

    rf_model.FITSTATISTICS


.. note:: If an error occurred during processing, the only artifact is ERROR_LOG.
          This object contains the SAS log to aid you in resolving your error.

Below is an example where the variable name left is typed incorrectly as lefty.


.. code-block:: ipython3

    rf_model = ml.forest(data=hr, target='lefty', input=inputs, nominals = nom)

.. parsed-literal::

    SubmissionError: ERRORS found in SAS log:
    ERROR: Variable LEFTY not found.

We can see a brief detail of the error but if more context is needed, you can 
see the entire log for the model submission with code like the following:

.. code-block:: ipython3

    rf_model.ERROR_LOG

