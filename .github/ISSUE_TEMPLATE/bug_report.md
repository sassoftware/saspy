---
name: Bug report
about: Create a report to help us improve
title: ''
labels: ''
assignees: ''

---

**Describe the bug**
A clear and concise description of what the bug is. Also, please run the code and provide all of the output. Also, please execute the following and provide all of the output (you only need the print statements in batch mode, not interactive):
```
import saspy
print(saspy)
print(saspy.SAScfg)
print(saspy.list_configs())
# if you can establish a SASSession, do so then print it too
# if you can't then provide version information for SASPy with your config info below
sas = saspy.SASsession()
print(sas)
```

**To Reproduce**
Steps to reproduce the behavior:
1. Submit the following code '...'
2. See that the results are '...' instead of '...'
3. Or, see error '...' instead of it working

**Expected behavior**
A clear and concise description of what you expected to happen if it's not obvious.

**Screenshots**
If applicable, add screenshots to help explain your problem. But, paste code if it's something I will need to run; I can't cut-n-paste from pictures, and don't like to type a lot :)

**Configuration information. Please provide the configuration you're trying to use (your sascfg_personal.py file) as well as what client system you are on and what kind of SAS deployment you're trying to connect to and where it's deployed. **

**Additional context**
Add any other context about the problem here.
