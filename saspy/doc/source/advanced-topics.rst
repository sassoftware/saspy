
.. Copyright SAS Institute

.. currentmodule:: saspy


===============
Advanced Topics
===============

This chapter covers more detailed explanations of functionality in SASPy and advice
for troubleshooting.

*******************************
My SAS Session will not connect
*******************************



My model didn't run
===================

When you run an analytical method there are a number of things that occur.
The goal is to have informative messages when things go wrong and in this section we'll explain what his happening
and how to check the various stages

#. Are the required parameters included?
   Each analytical method has a set of required parameters (there are a few that have an empty set but
   all the methods must have this specified).

   The simplest way to find the required and optional parameters is to use the `'?'` functionality.

   Here are two examples for the forest and hplogistic methods respectively:

   ::

       ?ml.forest()
       ?stat.hplogistic()

   The next best option is to use the API_ reference for the given method
   Both ways will show you the set of required parameters and then the list of optional parameters. The requred set
   and optional make up the complete set of parameters the method will take.

   If you are missing required parameters you will receive a SyntaxError and processing will stop.

   .. parsed-literal::

       SyntaxError: You are missing 1 required statements:
       {'model'}

   Missing optional parameter will produce no warning.

   **NOTE:** The `data` parameter does not appear in the required set but it is required for all modeling methods.

#. Do you have extra parameters
   If you include parameters that are neither required *or* optional then will be removed but as a best practice
   don't test the system.

#. Are the parameter the correct type
   Parameters must be specified with the correct type. If you provided an invalid type you should recieve a
   SyntaxWarning or SyntaxError and processing will stop.

   Here are a few of the most common parametes and their valid types

   * The `data` parameter must be a `SASData`_ object

   * The `model` parameter is a str

   * The `target` and `inputs` can be str, list, or dict types

   * The `nominals` must be a list type

   Making the parameters handle more types is a great way to get involved. Enter an issue and we can help you.

#. Were errors generated during execution
   If you make it this far the error is probably in the running of the genereated SAS code.
   To investigate you can `ERROR_LOG` attribute on your `SASResult`_ object.

   ::

       rf_model.ERROR_LOG

   The resulting output will the SAS log for that generated code. You will be able to see the SAS syntax and then
   and error or warning messages in context.

   **NOTE:** If the `ERROR_LOG` doesn't give you enough information to resolve your issue you can execute the
   following code (assuming your session object is named `sas`)

   ::

       print(sas.saslog())

   This will output the SAS log for then entire session (since you last restarted the kernel or your initial connection)

