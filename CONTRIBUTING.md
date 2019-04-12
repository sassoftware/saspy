## Contributing Rules

### Opening Issues
* Feel free to open an issue to discuss any questions you have or ask about ideas for contributions
* If you have an idea but don't want to code it up yourself, feel free to run it by us. We can implement it for you if you'd prefer, and we think it's useful - then we have to follow the rules and write the tests

### Tips
* There should be enough examples of each of these patterns in the code already, so 'cut, paste, adjust' is a good way to go about adding something

* The goal of all of this is to be as Pythonic as we can, yet still provide all of the SAS functionality required
    1. For example, we don't have a SASlibname object. This is on purpose because it just doesn't provide much in python and would just add extra 'SASisms' that aren't necessary. Added a datasets() method to the SASsession so you can see the tables for any libref, and a saslib method to assign a libref; that's about all you need. This is less SAS like and more Python like.

### Regression Testing
* Contributions must pass the existing regression tests located in saspy/tests

### Unit test creation/update
* Contributions must add unit tests to saspy/tests to validate the changes being added in the code
* if there's already a test file where your tests would make sense; put them in there
* if it's something new or you feel it needs its own file, create a new file
    
### Consistent Architecture
* contributions should follow the conventions of the saspy architecture
    1. sasbase.py is the main module containing SASsession and SASdata objects
    1. sasio*.py are the access method specific modules that sasbase calls through to
    1. anything that can be common across access methods should be put in sasbase only
        1. if it just generates access method independent SAS code to submit, it goes here
    1. anything that needs to be implemented differently in each access method module follows this:
        1. add entry in sasbase, and do any common checks or generation there
        1. call the access method specific code (should have common signatures/returns)
        1. return the same thing (object, results, ...) regardless of which io module was called

### Adding methods 
* The existing conventions in the code provide the expected format. 
* All added methods must support the following attributes: 
    1. **teach_me_sas** : 
        * can use the 'nosub' (no submit) attr. 
        * If this is set, the method will return the generated code but not execute it.
    1. **batch** : 
        * the batch attr requires that you do not display results
        * in batch, results must be returned as an object/Dict so they can be processed by the user code.
    1. **results=** (HTML attr of SASdata) : 
        * Used for getting HTML results or TEXT results which is usually based upon whether the code is running in a notebook (Jupyter) or command line, or batch. 

    
### Adding PROCs
* To add procs in the sasstat, sasets, sasqc, or sasml modules, follow the directions in the respective modules

### Certificate of Origin

* Contributions to this software are accepted only when they are
properly accompanied by a Contributor Agreement. 

The Contributor
Agreement for this software is the Developer's Certificate of Origin
1.1 (DCO) as provided with and required for accepting contributions
to the Linux kernel.

In each contribution proposed to be included in this software, the
developer must include a "sign-off" that denotes consent to the
terms of the Developer's Certificate of Origin.  The sign-off is
a line of text in the description that accompanies the change,
certifying that you have the right to provide the contribution
to be included.  For changes provided in source code control (for
example, via a Git pull request) the sign-off must be included in
the commit message in source code control.  For changes provided
in email or issue tracking, the sign-off must be included in the
email or the issue, and the sign-off will be incorporated into the
permanent commit message if the contribution is accepted into the
official source code.

If you can certify the below:

        Developer's Certificate of Origin 1.1

        By making a contribution to this project, I certify that:

        (a) The contribution was created in whole or in part by me and I
            have the right to submit it under the open source license
            indicated in the file; or

        (b) The contribution is based upon previous work that, to the best
            of my knowledge, is covered under an appropriate open source
            license and I have the right under that license to submit that
            work with modifications, whether created in whole or in part
            by me, under the same open source license (unless I am
            permitted to submit under a different license), as indicated
            in the file; or

        (c) The contribution was provided directly to me by some other
            person who certified (a), (b) or (c) and I have not modified
            it.

        (d) I understand and agree that this project and the contribution
            are public and that a record of the contribution (including all
            personal information I submit with it, including my sign-off) is
            maintained indefinitely and may be redistributed consistent with
            this project or the open source license(s) involved.

* Then you just add a line like below, using your real name(sorry, no pseudonyms or anonymous contributions.)

        Signed-off-by: Random J Developer <random@developer.example.org>



And **thanks** for contributing! It will make this project better for everyone!
