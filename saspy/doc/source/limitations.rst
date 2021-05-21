
.. Copyright SAS Institute

.. currentmodule:: saspy


==========================================
Limitations, restrictions and work arounds
==========================================

This chapter covers specific use cases that are problematic, not allowed for some reason, or
require special handling to be able to work correctly. Hopefully this will be a short chapter.
It was initiated while working on `Issue 294 <https://github.com/sassoftware/saspy/issues/294>`_.
That issue was about running batch SAS scripts via the submit() method and some problems that
ensued.
 
Let me preface this section by describing some aspects of saspy that warrant this section. saspy
was designed to be a python interface to an interactive SAS session. Its many methods generate
SAS code, which it submits to the SAS session and then retrieves both the SASLOG (LOG) and any listing/results 
(LST) and then provides that back as objects or by directly rendering in interactive sessions.

Many methods require saspy to query the SAS session to gather information about session, data, configuration,
the environment, and other things. There is no API for these 'queries'. Rather, saspy generates specific
SAS code to gather this information and has it written to the LOG to then parse out on the Python side 
after retirving the LOG. That is a common mode of access. This, then, demands that saspy have access to
the LOG. That is perhaps the first, most important requirement.

SAS has no end of options, configurations, and coding possibilities that allow it to be able to do
just about anything. saspy couldn't possibly provide methods to do 'everything', so there is a submit()
method which allows for running 'any' SAS code needed that isn't already provided by a saspy method.

This then, is the crux of the matter. There can be SAS code submitted that would then cause problems
for saspy to function correctly. These are the things that will be addresses in this section. saspy has
multiple access methods, for connecting to SAS deployed in different ways. Each of these access methods
is implemented very differently, yet they each provide the same functionality and capabilities; at least
to the best of my ability to make that the case. Any divergences between those will also be identified here.


******
SASLOG
******

Proc Printto
------------

Let's start with the first requirement that saspy has access to the SAS Log. SAS has a procedure which
allows you to redirect the LOG and/or LST out from under the currently existing locations, to files or other locations:
`proc printto <https://go.documentation.sas.com/?docsetId=proc&docsetTarget=p1hwvc03z4tqlkn1owzhzo8e7ulu.htm&docsetVersion=9.4&locale=en>`_.

If this is used to redirect the LST, then you just won't get any results back from any methods in saspy.
Your choice, I suppose. However, if redirecting the LOG, then saspy may hang, may have any number of failures
or exceptions in various methods, and will generally be useless other than for other submit() methods, which won't
return anything. 

Not the intent of the design. However, intent not being everything, providing a way to allow for the use of this,
if needed, while addressing this restriction is possible. This would be considered a work around.

Proc Printto has an 'undo' version where you can reset the LOG and LST back to their previous settings. So, to
successfully use Proc Printto within a saspy submit() method, you are simply required to submit
'Proc Printto;run;' (undo) in your code (presumably at the end) that you run within a submit() method. This will
return the LOG and LST back to saspy which will then continue to function correctly. Of course, you won't get
any part of the log or any results that happened while the redirection was enabled, but you knew that. Keep reading
to see, below, that 'you' don't have to do this, there's an option on submit(..., printto=True) which will do this
for you. 

One parting though on this is that you can use saspy's download() method to pull the file(s) you redirected things
to back to the client and then access them in saspy. Don't know why you would, but you could. Maybe there's a use
case where that makes sense.



************************************
Terminating SAS out from under saspy
************************************

%abort macro and abort statement
--------------------------------

SAS also has statements you can submit which will cause the SAS session to immediately terminate; yes, really.
So, if you execute one of these statements, guess what? The interactive SAS session saspy that started and is connected to
vanishes. It's not there anymore. saspy will no longer get any results, and won't get the log from that submit() method
that executed SAS :) (lol)  Well, executed the statement that terminated SAS.

The SAS macro `%abort <https://go.documentation.sas.com/?docsetId=mcrolref&docsetTarget=p0f7j2zr6z71nqn1fpefnmulzazf.htm&docsetVersion=9.4&locale=en>`_
and the data step statement `abort <https://go.documentation.sas.com/?docsetId=lestmtsref&docsetTarget=p0hp2evpgqvfsfn1u223hh9ubv3g.htm&docsetVersion=9.4&locale=en>`_
each have various arguments which cause them to behave differently, and depending upon how the SASsession was started the
behavior can vary as well. 

There are two general behaviors these statements can produce. The first ts to terminate SAS. The other is to stop processing
(some) remaining code that was submitted, but not terminate the SAS session. This second behavior is complicated by the nature of
the SAS session itself. As termination of the SAS session is pretty cut and dry, the following will be addressing the second behavior. 

Canceling submitted statements
------------------------------

There are two variations of this second behavior. The first variation is when you supply no argument to the abort statement
or macro. In this case it only stops executing the current macro and/or data step, but any following submitted statements 
continue to be executed normally. This case is generally not a problem for any access method of saspy.

The second variant is specifying the CANCEL argument: '[%]abort CANCEL;'. This version stops executing all of the following
'submitted statements', and the meaning of 'submitted statements' varies. For both the IOM and HTTP access methods, there is
an actual API to submit code to the SAS session and that submit maps 1:1 with the saspy submit() method. In these cases, all of the
statements you submitted in the submit() method, following the Abort CANCEL, are not executed. But, subsequent submit() methods,
of more code, will be executed.

For STDIO, there is no API of any kind, and what SAS considers to be the 'following submitted statements' is effectively, all
statements to the end of the session. There is no way to 'group' sets of statements into 'submissions'. The STDIN stream itself
is a single 'submit'. In this case, the SASsession is no longer functional; it will execute no more code and nothing can be done but
terminated it (endsas()). That is a SASism, and nothing that can be changed or fixed from the Python side to solve this.


*************
Perfect Storm
*************

Combining proc printto and abort cancel
---------------------------------------

What happens if you issue a the following code, having proc printto to redirect LOG/LST, and have an abort CANCEL, which gets executed,
and you have the undo for the proc printto (proc printto;run;) at the end of your code?

.. code-block:: ipython3

    >>> sas.submitLOG('''
        proc printto LOG='./mylogfile';run;
       
        /* some SAS code */

        /* some conditional check which turns out to be true */
        if (true) then
           abort cancel;

        /* some more SAS code */

        /* give LOG/LST back to saspy */
        proc printto;run;
        ''')

    In this case, neither 'some more SAS code' nor the proc printto;run; will be executed.


So, in this case, the 'undo' won't happen so saspy won't have it's LOG back. In this case, you could
code it in your program before each 'abort cancel;' that could execute. 

So, for IOM and HTTP, this will solve this case:

.. code-block:: ipython3

    >>> sas.submitLOG('''
        proc printto LOG='./mylogfile';run;
       
        /* some SAS code */

        /* some conditional check which turns out to be true - return the log before canceling */
        if true then
           do;
              proc printto;run;
              abort cancel;
           end;

        /* some more SAS code */

        /* give LOG/LST back to saspy - this only happens if abort cancel didn't execute */
        proc printto;run;
        ''')
    >>> # the rest of your Python program ...


printto= option on submit methods
---------------------------------

Now, odds are that if you are submitting code like this, you didn't type it into saspy. You probably
are reading in some existing SAS batch script (.sas file) and just submitting it, as is. You may not
even know what SAS code is even in it. In this case, you don't want to have to edit the file to modify
it as above. For this situation, I've added an option on the submit* mehtods; printto=[False | True].

When set to True, saspy will submit the undo ('proc printto;run;') in a second API submit (IOM and HTTP),
so that, in case there was a redirecting proc printto, and perhapse an abort cancel, the log will be
given back to saspy and it will continue to funtion correctly. This 'undo' will also be submitted in the
STDIO access method, though it's not a seperate API call, since, as described above, there is no API.

Submitting 'proc printto;run;' has no ill effects in any case; even if there had been no original proc
printto submitted, or if there has already been 'proc printo;run;' previously submitted.

.. code-block:: ipython3

    >>> fd = open('MyBattchSreipt.sas'); code = fd.read(); fd.close()
    >>> sas.submitLOG(code, printto=True)
    >>> # the rest of your Python program ...  you are covered either way

The default for the printto= option is False, as that is the existing behavior, so no regressions are possible.
And this is actually a non-standard use case, though is can be allowed and supported by setting the option to True.

