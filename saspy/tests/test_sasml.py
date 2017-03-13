import unittest
import saspy


class TestSASml(unittest.TestCase):
    def setUp(self):
        # Use the first entry in the configuration list
        self.sas = saspy.SASsession(cfgname=saspy.SAScfg.SAS_config_names[0])
        self.assertIsInstance(self.sas, saspy.SASsession, msg="sas = saspy.SASsession(...) failed")
        procNeeded = ['forest', 'hp4score', 'cluster', 'neural', 'treeboost', 'hpbnet']
        if not self.procFound(procNeeded):
            self.skipTest("Not all of these procedures were found: %s" % str(procNeeded))

    def tearDown(self):
        if self.sas:
            self.sas._endsas()

    def procFound(self, plist: list) -> bool:
        assert isinstance(plist, list)
        for proc in plist:
            res = self.sas.submit("proc %s; run;" % proc)
            log = res['LOG'].splitlines()
            for line in log:
                if line == 'ERROR: Procedure %s not found.' % proc.upper():
                    return False
        return True

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
