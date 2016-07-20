# To contribute to saspy, there are a few rules and conventions to follow.

0. contributions must pass the existing regression tests; see saspy/tests

0. contributions must add unit tests to saspy/tests to validate the changes being added in the code
    0. if there's already a test file where your tests would make sense; put them in there
    0. if it's something new or you feel it needs its own file, create a new file
    
0. contributions should follow the conventions of the saspy architecture
    0. sasbase.py is the main module containing SASsession and SASdata objects
    0. sasio*.py are the access method specific modules that sasbase calls through to
    0. anything that can be common across access methods should be put in sasbase only
        0. if it just generates access method independent SAS code to submit, it goes here
    0. anything that needs to be implemented differently in each access method module follows this:
        0. add entry in sasbase, and do any common checks or generation there
        0. call the access method specific code (should have common signatures/returns)
        0. return the same thing (object, results, ...) regardless of which io module was called
        
0. support the 'teach_me_sas' and 'batch' and results= attributes in all added methods
    0. teach_me_sas used the 'nosub' (no submit) attr. If this is set, return the generated code but don't run it
    0. the batch attr requires that you do not display results, but return them as an object/Dict so they can be processed by the user code
    0. the results (HTML attr of SASdata) is for getting HTML results or TEXT results which is usually based upon whether the code is running in a notebook (Jupyter) or command line, or batch. 
    0. Just follow the existing conventions in the code and you'll be good. 
    
0. to add procs in the sasstat, sasets, sasqc, or sasml modules, follow the directions in them; pretty straight forward

0. there should be enough examples of each of these patterns in the code already, so 'cut, paste, adjust' is a good way to go about adding something

0. the goal of all of this is to be as Pythonic as we can, yet still provide all of the SAS functionality required
    0. for example, we don't have a SASlibname object. This is on purpose because it just doesn't provide much in python and would just add extra 'SASisms' that aren't necessary. Added a datasets() method to the SASsession so you can see the tables for any libref, and a saslib method to assign a libref; that's about all you need. This is less SAS like and more Python like.

0. feel free to open an issue to discuss any questions you have or ask about ideas for contributions

0. if you have an idea but don't want to code it up yourself, feel free to run it by us. We can implement it for you if you'd prefer, and we think it's useful - then we have to follow the rules and write the tests ?

0. Also, follow the instructions in the saspy/ContributorAgreement.txt file 

And **thanks** for contributing! It will make this project better for everyone!
