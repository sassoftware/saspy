
.. Copyright SAS Institute

.. currentmodule:: saspy


===============
Advanced Topics
===============

This chapter covers more detailed explanations of functionality in SASPy and advice
for troubleshooting.

****************
Using Batch_mode
****************

Batch mode is meant to be used when you want to automate your code as python scripts.
In batch mode, any methods that would normally display results, will insted return a python dictionary
with 2 keys; LOG, LST. This is the same as how the submit() method works normally. The LOG has the SAS Log
and the LST contains the results. You will likely want to set the results= to HTML (this was the original
default instead of Pandas), so that not only plots and graphs are html, but also tabular results too.

The example below shows the contents of a python script that runs a linear regression and has all of the
results written to a directory which you can accewss from a web browser and display these results by just
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

 
