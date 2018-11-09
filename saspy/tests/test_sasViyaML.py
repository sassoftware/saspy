import unittest
import saspy
from saspy.tests.util import Utilities


class TestSASViyaML(unittest.TestCase):
    def setUp(self):
        # Use the first entry in the configuration list
        self.sas = saspy.SASsession(cfgname=saspy.SAScfg.SAS_config_names[0])
        self.assertIsInstance(self.sas, saspy.SASsession, msg="sas = saspy.SASsession(...) failed")
        self.util = Utilities(self.sas)
        procNeeded = ['factmac', 'fastknn', 'forest', 'gradboost', 'nnet', 'svdd', 'svmachine']
        if not self.util.procFound(procNeeded):
            self.skipTest("Not all of these procedures were found: %s" % str(procNeeded))

    def tearDown(self):
        if self.sas:
            self.sas._endsas()

    def testFactmacSmoke1(self):
        ml = self.sas.sasviyaml()
        dt = self.sas.sasdata("class", "sashelp")
        out1 = ml.factmac(data=dt, target='height', input={'interval': 'weight', "nominal": 'sex'})
        a = ['BASELINE', 'DATAACCESSINFO', 'FITSTATISTICS', 'LOG',
             'MODELINFO', 'NOBS', 'PERFORMANCEINFO', 'VARIABLEIMPORTANCE']
        self.assertEqual(sorted(a), sorted(out1.__dir__()),
                         msg=u"Simple FACTMAC  model failed to return correct objects expected:{0:s}  returned:{1:s}".format(
                             str(a), str(out1)))

    def testFastknnSmoke1(self):
        ml = self.sas.sasviyaml()
        dt = self.sas.sasdata("class", "sashelp")
        out1 = ml.fastknn(data=dt, input={'interval': 'weight', "nominal": 'sex'})
        a = ['BASELINE', 'DATAACCESSINFO', 'FITSTATISTICS', 'LOG',
             'MODELINFO', 'NOBS', 'PERFORMANCEINFO', 'VARIABLEIMPORTANCE']
        self.assertEqual(sorted(a), sorted(out1.__dir__()),
                         msg=u"Simple FASTKNN  model failed to return correct objects expected:{0:s}  returned:{1:s}".format(
                             str(a), str(out1)))

    def testForestSmoke1(self):
        ml = self.sas.sasviyaml()
        dt = self.sas.sasdata("class", "sashelp")
        out1 = ml.forest(data=dt, target='height', input={'interval': 'weight', "nominal": 'sex'})
        a = ['BASELINE', 'DATAACCESSINFO', 'FITSTATISTICS', 'LOG',
             'MODELINFO', 'NOBS', 'PERFORMANCEINFO', 'VARIABLEIMPORTANCE']
        self.assertEqual(sorted(a), sorted(out1.__dir__()),
                         msg=u"Simple FOREST  model failed to return correct objects expected:{0:s}  returned:{1:s}".format(
                             str(a), str(out1)))

    def testGradboostSmoke1(self):
        ml = self.sas.sasviyaml()
        dt = self.sas.sasdata("class", "sashelp")
        out1 = ml.gradboost(data=dt, target='height', input={'interval': 'weight', "nominal": 'sex'})
        a = ['BASELINE', 'DATAACCESSINFO', 'FITSTATISTICS', 'LOG',
             'MODELINFO', 'NOBS', 'PERFORMANCEINFO', 'VARIABLEIMPORTANCE']
        self.assertEqual(sorted(a), sorted(out1.__dir__()),
                         msg=u"Simple GRADBOOST  model failed to return correct objects expected:{0:s}  returned:{1:s}".format(
                             str(a), str(out1)))

    def testNnetSmoke1(self):
        ml = self.sas.sasviyaml()
        dt = self.sas.sasdata("class", "sashelp")
        out1 = ml.nnet(data=dt, target='height', input={'interval': 'weight', "nominal": 'sex'})
        a = ['BASELINE', 'DATAACCESSINFO', 'FITSTATISTICS', 'LOG',
             'MODELINFO', 'NOBS', 'PERFORMANCEINFO', 'VARIABLEIMPORTANCE']
        self.assertEqual(sorted(a), sorted(out1.__dir__()),
                         msg=u"Simple NNET model failed to return correct objects expected:{0:s}  returned:{1:s}".format(
                             str(a), str(out1)))

    def testSvddSmoke1(self):
        ml = self.sas.sasviyaml()
        dt = self.sas.sasdata("class", "sashelp")
        out1 = ml.svdd(data=dt, input={'interval': 'weight', "nominal": 'sex'})
        a = ['BASELINE', 'DATAACCESSINFO', 'FITSTATISTICS', 'LOG',
             'MODELINFO', 'NOBS', 'PERFORMANCEINFO', 'VARIABLEIMPORTANCE']
        self.assertEqual(sorted(a), sorted(out1.__dir__()),
                         msg=u"Simple SVDD model failed to return correct objects expected:{0:s}  returned:{1:s}".format(
                             str(a), str(out1)))

    def testSvmachineSmoke1(self):
        ml = self.sas.sasviyaml()
        dt = self.sas.sasdata("class", "sashelp")
        out1 = ml.svmachine(data=dt, target='height', input={'interval': 'weight', "nominal": 'sex'})
        a = ['BASELINE', 'DATAACCESSINFO', 'FITSTATISTICS', 'LOG',
             'MODELINFO', 'NOBS', 'PERFORMANCEINFO', 'VARIABLEIMPORTANCE']
        self.assertEqual(sorted(a), sorted(out1.__dir__()),
                         msg=u"Simple SVMACHINE model failed to return correct objects expected:{0:s}  returned:{1:s}".format(
                             str(a), str(out1)))

if __name__ == '__main__':
    unittest.main()
