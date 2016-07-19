import unittest

import saspy


class TestSASets(unittest.TestCase):
    def setUp(self):
        # Use the first entry in the configuration list
        self.sas = saspy.SASsession(cfgname=saspy.SAScfg.SAS_config_names[0])
        self.assertIsInstance(self.sas, saspy.SASsession, msg="sas = saspy.SASsession(...) failed")
        procNeeded=['arima']
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
                if line=='ERROR: Procedure %s not found.' % proc.upper():
                    return False
        return True

    def test_smoke(self):
        # Basic model returns objects
        ets = self.sas.sasets()
        air = self.sas.sasdata('air', 'sashelp')
        b = ets.arima(data=air, identify='var=air(1,12)')
        a = ['CHISQAUTO', 'DESCSTATS', 'LOG', 'SERIESCORRPANEL']
        self.assertEqual(sorted(a), sorted(b.__dir__()),
                         msg=u"Simple Regession (reg) model failed to return correct objects expected:{0:s}  returned:{1:s}".format(
                             str(a), str(b)))

    def test_missingVar(self):
        ets = self.sas.sasets()
        d = self.sas.sasdata('air', 'sashelp')
        b = ets.arima(data=d, by='novar', identify='var=air(1,12)')
        a = ['ERROR_LOG']
        self.assertEqual(a, b.__dir__(),
                         msg=u"arima model failed to return correct objects expected:{0:s}  returned:{1:s}".format(
                             str(a), str(b)))

    def test_extraStmt(self):
        # Extra Statements are ignored
        ets = self.sas.sasets()
        d = self.sas.sasdata('air', 'sashelp')
        b = ets.arima(data=d, by='novar', identify='var=air(1,12)', crosscorr='date', decomp='air')
        a = ets.arima(data=d, by='novar', identify='var=air(1,12)')
        self.assertEqual(a.__dir__(), b.__dir__(), msg=u"Extra Statements not being ignored expected:{0:s}  returned:{1:s}".format(
            str(a), str(b)))

    def test_outputDset(self):
        ets = self.sas.sasets()
        air = self.sas.sasdata('air', 'sashelp')
        outAir = self.sas.sasdata('air')
        ets.arima(data=air, identify='var=air(1,12)', out=outAir)
        self.assertIsInstance(outAir, saspy.SASdata, msg="out= dataset not created properly")

    def test_overridePlot(self):
        # Test that user can override plot options
        ets = self.sas.sasets()
        air = self.sas.sasdata('air', 'sashelp')
        outAir = self.sas.sasdata('air')
        b = ets.arima(data=air, identify='var=air(1,12)', out=outAir, procopts='plots=none')
        a = ['CHISQAUTO', 'DESCSTATS', 'LOG']
        self.assertEqual(sorted(a), sorted(b.__dir__()), msg=u"plots overridden and disabled expected:{0:s}  returned:{1:s}".format(
            str(a), str(b)))
