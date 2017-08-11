
.. Copyright SAS Institute

.. currentmodule:: saspy


===============
Advanced topics
===============

In this chapter we will explore more detailed explanations of specific functionality.


****************
Using Batch mode
****************

Batch mode is meant to be used when you want to automate your code as Python scripts.

In batch mode, any method that would normally display results, returns a Python dictionary
instead and with two keys; LOG, LST. This is the same as how the submit() method works 
normally. 

The LOG has the SAS Log and the LST contains the results. You will likely want to set 
the results parameter to HTML (this was originally the default instead of Pandas). When
you set the results to HTML, not only are plots and graphs in HTML, but also tabular results
too.

The example below shows the contents of a Python script that runs a linear regression and 
writes all the results to a directory. You can access the directory with a web browser to
view these results by clicking on them. Adjust the filesystem path below and you should 
be able to run this code yourself.


.. code-block:: ipython3

    #! /usr/bin/python3.5
    
    import saspy
    sas = saspy.SASsession(results='html')
    
    cars = sas.sasdata('cars', libref='sashelp')
    
    sas.set_batch(True)
    
    stat = sas.sasstat()
    res = stat.reg(model='horsepower = Cylinders EngineSize', data=cars)
    
    for i in range(len(ets_results._names)):
        x = res.__getattr__(res._names[i])
        if type(x) is not str:
            out1 = open("C:\\Public\\saspy_demo\\"+res._names[i]+".html", mode='w+b')
            out1.write(x['LST'].encode())
            out1.close()
        else:
            out1 = open("C:\\Public\\saspy_demo\\"+res._names[i]+".log", mode='w+b')
            out1.write(x.encode())
            out1.close()
    
    
The URL to see these results is: file:///C:/Public/saspy_demo/. Of course, you can
imagine integrating the results into nicer web page for reporting, but with nothing more 
than this few lines of code, you can have the results updated and refreshed by just 
re-running the script.

 
*********
Prompting
*********

There are two types of prompting that can be performed; meaning to stop processing and
prompt the user for input and then resume processing.

The first type of prompting is performed implicity. When you run the 
SASsession() method, if any required parameters for the chosen connection method 
were not specified in the configuration definition (in sascfg.py), processing is interrupted 
so that the user can be prompted for the missing parameters. In addition, when there 
is more than one configuration definition in SAS_config_names, and cfgname is not 
specified in the SASsession() method (or an invalid name is specified), the user will 
be prompted to select the configuration definition to use.

The other kind of prompting is prompting that you control. The submit() method, 
and the saslib() methods both take an optional prompt parameter. This parameter 
is how you request to have the user prompted for input at run time. This option 
is used in conjunction with SAS macro variable names that you enter in the SAS 
code or options for the method.

The prompt parameter takes a Python dictionary. The keys are the SAS macro variable 
names and the values are True or False. The Boolean value indicates whether it 
is to hide what the user types in or not. It also controls whether the macro variables 
stay available to the SAS session or if they are deleted after running that code. 

You will be prompted for the values of your keys, and those values will be assigned
to the SAS macro variables for you in SAS. When your code runs, the macro variables will be 
resolved. If you specified ``True``, then the value the user types is not displayed, 
nor is the macro variable displayed in the SAS log, and the macro variable is deleted 
from SAS so that it is not accessible after that code submission. For ``False``, the 
user can see the value as it is type, the macro variables can be seen in the SAS log 
and the variables remain available in that SAS session for later code submissions.

The following are examples of how to use prompting in your programs. The first example 
uses the saslib() method to assign a libref to a third-party database. This is a
common issue--the user needs to specify credentials, but you do not want to include
user IDs and passwords in your programs. Prompting enables the user to provide
credentials at runtime.

.. code-block:: ipython3

    sas.saslib('Tera', engine='Teradata', options='user=&user pw=&mypw server=teracop1', 
               prompt={'user': False, 'mypw': True})

At runtime, the user is prompted for user and password and sees something like the
following when entering values (the user ID is visible and the password is obscured):

.. parsed-literal::

    Please enter value for macro variable user sasdemo
    Please enter value for macro variable mypw ........
 
Another example might be that you have code that creates a table, but you want to let 
the user choose the table name as well as the name of the column and a hidden value 
to assign to it. By specifing ``False``, the user can see the value, and the SAS log 
shows the non-hidden marco mariables, followed by another code submission that uses 
the previously defined non-hidden variables--which are still available.

.. code-block:: ipython3

    ll = sas.submit('''
    data &dsname;
      do &var1="&pw"; 
        output; 
      end;
    run;
    ''', prompt={'var1': False, 'pw': True, 'dsname': False})


.. parsed-literal::

    Please enter value for macro variable var1 MyColumnName
    Please enter value for macro variable hidden ........
    Please enter value for macro variable dsname TestTable1    
    
    print(ll['LOG'])

    103  ods listing close;ods html5 (id=saspy_internal) file=stdout options(bitmap_mode='inline') device=svg; ods graphics on /
    103! outputfmt=png;
    NOTE: Writing HTML5(SASPY_INTERNAL) Body file: STDOUT
    104  
    105  options nosource nonotes;
    108  %let var1=MyColumnName;
    109  %let dsname=TestTable1;
    110  
    111  data &dsname;
    112    do &var1="&hidden";
    113      output;
    114    end;
    115  run;
    NOTE: The data set WORK.TESTTABLE1 has 1 observations and 1 variables.
    NOTE: DATA statement used (Total process time):
          real time           0.00 seconds
          cpu time            0.00 seconds
          
    116  
    117  proc print data=&dsname;
    118  run;
    NOTE: There were 1 observations read from the data set WORK.TESTTABLE1.
    NOTE: PROCEDURE PRINT used (Total process time):
          real time           0.00 seconds
          cpu time            0.00 seconds
          
    119  
    120  options nosource nonotes;
    123  
    124  ods html5 (id=saspy_internal) close;ods listing;


    HTML(sas.submit('''
    proc print data=&dsname;
    run;
    ''')['LST'])

    Obs     MyColumnName
    1       cant see me


That is a highly contrived example, but you get the idea. You can prompt users 
at runtime for values you want to use in the code, and those values can be 
kept around and used later in the code, or hidden and inaccessible afterward.
