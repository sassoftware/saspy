import unittest
import saspy
from saspy.tests.util import Utilities


class TestSASViyaML(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sas = saspy.SASsession()
        util = Utilities(cls.sas)
        procNeeded = ['factmac', 'fastknn', 'forest', 'gradboost', 'nnet', 'svdd', 'svmachine']
        if not util.procFound(procNeeded):
            cls.skipTest("Not all of these procedures were found: %s" % str(procNeeded))

    @classmethod
    def tearDownClass(cls):
        if cls.sas:
            cls.sas._endsas()

    def testFactmacSmoke1(self):
        ml = self.sas.sasviyaml()
        dt = self.sas.sasdata("class", "sashelp")
        out1 = ml.factmac(data=dt, target='height', input={'interval': 'weight', "nominal": 'sex'})
        self.assertFalse('ERROR_LOG' in out1.__dir__(), msg=u"factmac had errors in the log")

    def testFastknnSmoke1(self):
        ml = self.sas.sasviyaml()
        dt = self.sas.sasdata("class", "sashelp")
        out1 = ml.fastknn(data=dt, input={'interval': 'weight', "nominal": 'sex'})
        self.assertFalse('ERROR_LOG' in out1.__dir__(), msg=u"fastknn had errors in the log")

    def testForestSmoke1(self):
        ml = self.sas.sasviyaml()
        dt = self.sas.sasdata("class", "sashelp")
        out1 = ml.forest(data=dt, target='height', input={'interval': 'weight', "nominal": 'sex'})
        self.assertFalse('ERROR_LOG' in out1.__dir__(), msg=u"forest had errors in the log")

    def testGradboostSmoke1(self):
        ml = self.sas.sasviyaml()
        dt = self.sas.sasdata("class", "sashelp")
        out1 = ml.gradboost(data=dt, target='height', input={'interval': 'weight', "nominal": 'sex'})
        self.assertFalse('ERROR_LOG' in out1.__dir__(), msg=u"gradboost had errors in the log")

    def testNnetSmoke1(self):
        ml = self.sas.sasviyaml()
        dt = self.sas.sasdata("class", "sashelp")
        out1 = ml.nnet(data=dt, target='height', input={'interval': 'weight', "nominal": 'sex'})
        self.assertFalse('ERROR_LOG' in out1.__dir__(), msg=u"nnet had errors in the log")

    def testSvddSmoke1(self):
        ml = self.sas.sasviyaml()
        dt = self.sas.sasdata("class", "sashelp")
        out1 = ml.svdd(data=dt, input={'interval': 'weight', "nominal": 'sex'})
        self.assertFalse('ERROR_LOG' in out1.__dir__(), msg=u"svdd had errors in the log")

    def testSvmachineSmoke1(self):
        ml = self.sas.sasviyaml()
        dt = self.sas.sasdata("class", "sashelp")
        out1 = ml.svmachine(data=dt, target='height', input={'interval': 'weight', "nominal": 'sex'})
        self.assertFalse('ERROR_LOG' in out1.__dir__(), msg=u"svmachine had errors in the log")

if __name__ == '__main__':
    unittest.main()
