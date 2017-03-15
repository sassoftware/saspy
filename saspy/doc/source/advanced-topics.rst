
.. Copyright SAS Institute

.. currentmodule:: saspy


===============
Advanced Topics
===============

In this chapter we will explore more detailed explanations of specific functionality in SASPy.


****************
Using Batch_mode
****************

Batch mode is meant to be used when you want to automate your code as python scripts.
In batch mode, any methods that would normally display results, will insted return a python dictionary
with 2 keys; LOG, LST. This is the same as how the submit() method works normally. The LOG has the SAS Log
and the LST contains the results. You will likely want to set the results= to HTML (this was the original
default instead of Pandas), so that not only plots and graphs are html, but also tabular results too.

The example below shows the contents of a python script that runs a linear regression and has all of the
results written to a directory which you can access from a web browser and display these results by just
clicking on them. Adjust the filesystem path below and you should be able to run this code yourself.


.. code:: ipython3

    #! /usr/bin/python3.5
    
    import saspy
    sas = saspy.SASsession(results='html')
    
    cars = sas.sasdata('cars', libref='sashelp')
    
    sas.set_batch(True)
    
    stat = sas.sasstat()
    res = stat.reg(model='horsepower = Cylinders EngineSize', data=cars)
    
    for i in range(len(ets_results._names)):
        x = ets_results.__getattr__(ets_results._names[i])
        if type(x) is not str:
            out1 = open("C:\\Public\\saspy_demo\\"+ets_results._names[i]+".html", mode='w+b')
            out1.write(x['LST'].encode())
            out1.close()
        else:
            out1 = open("C:\\Public\\saspy_demo\\"+ets_results._names[i]+".log", mode='w+b')
            out1.write(x.encode())
            out1.close()
    
    
The url to see these reults would be: file:///C:/Public/saspy_demo/. Of course, you can imagine integrating the
results into nicer webpage for reporting, but with nothing more than this few lines of code, you can have the
results updated and refreshed by just re-running the script.

 

*********
Prompting
*********

There are two types of prompting that saspy will do. Meaning prompting the user for input while running.

The first is prompting saspy does on its own. When running the SASsession() method, any required parameters for the
chosen access method that were not specified in the Configuration Definition will be prompted for. Also, when there is
more than one Configuration Definition Name in SAS_config_names, and cfgname= is not specified on the SASsession() method 
(or an invalid name is specified), saspy will prompt for which Configuration Definition to use.

The other kind of prompting is prompting you control. The submit() method, and the saslib() methods both take an
optional 'prompt=' parameter. This parameter is how you can request that saspy prompt the user for input at run time.
This option is used in conjunction with SAS Macro variables that you code in the sas code or options for the method.
The prompt= parameter taked a python Dictionay where the keys are the names of your macro variable and the value is
True or False. The boolean value tells saspy whether it is to hide what the user types in or not. It also controls
whether the macro variables stay available to the SAS session or if they are deleted after running that code. 

What happens is that saspy will prompt for the values of your keys, and will then assign those values to SAS Macro variables
for you in SAS so that when your code runs the macro variables will be resolved. If you specified 'True', then the value
the user types will not be displayed, nor will the macro variable in SAS be displayed in the log, and the Marco Variable
will be deleted from SAS so as to not be accessible after that code submission. For 'False, you can see what the user types,
the Macro Variables can be seen in the log and they will remain available in that SAS session for later code submissions.

The following are examples of how to use this in your programs. The first example is using the saslib() method to
assign a libref to a third party database where the user needs to specify credentials. You don't want to hardcode
userid and passwords in your program, so the user should provide those at runtime.

.. code:: ipython3

    sas.saslib('Tera', engine='Teradata', options='user=&user pw=&mypw server=teracop1', prompt={'user': False, 'mypw': True})

At runtime, the user would be prompted for user and password and they would see something like this when they entered values:

.. code:: ipython3


    sas.saslib('Tera', engine='Teradata', options='user=&user pw=&mypw server=teracop1', prompt={'user': False, 'mypw': True})
    Please enter value for macro variable user sastpw
    Please enter value for macro variable mypw ........
 
Here's another example where you want to create a table, but you will let the user choose the table name as well as the name
of the column and a hidden value to assign to it. You can see what the user is prompted for and enters, and then you can see
the SAS Log showing the non-hidden Marco Variables, followed by another code submission that uses the previously defined non-hidden
variables which are still available.

.. code:: ipython3

    ll = sas.submit('''
    data &dsname;
      do &var1="&pw"; 
        output; 
      end;
    run;
    ''', prompt={'var1': False, 'pw': True, 'dsname': False})
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


Sure, that's kind of a cheesy example, but you get the idea. You can prompt users at runtime for values you want to
use in your code, and those values can be kept around an used again later, or hidden and inaccessible later.















