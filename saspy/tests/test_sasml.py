import unittest
import saspy
from saspy.tests.util import Utilities


class TestSASml(unittest.TestCase):
    def setUp(self):
        # Use the first entry in the configuration list
        self.sas = saspy.SASsession(cfgname=saspy.SAScfg.SAS_config_names[0])
        self.assertIsInstance(self.sas, saspy.SASsession, msg="sas = saspy.SASsession(...) failed")
        self.util = Utilities(self.sas)
        procNeeded = ['forest', 'hp4score', 'cluster', 'neural', 'treeboost', 'hpbnet']
        if not self.util.procFound(procNeeded):
            self.skipTest("Not all of these procedures were found: %s" % str(procNeeded))

    def tearDown(self):
        if self.sas:
            self.sas._endsas()

    def testForestSmoke1(self):
        ml = self.sas.sasml()
        dt = self.sas.sasdata("class", "sashelp")
        out1 = ml.forest(data=dt, target='height',
                         input={'interval':'weight', "nominal":'sex'}
                         )
        a = ['BASELINE', 'DATAACCESSINFO', 'FITSTATISTICS', 'LOG',
             'MODELINFO', 'NOBS', 'PERFORMANCEINFO', 'VARIABLEIMPORTANCE']
        self.assertEqual(sorted(a), sorted(out1.__dir__()),
                         msg=u"Simple Forest  model failed to return correct objects expected:{0:s}  returned:{1:s}".format(
                             str(a), str(out1)))
