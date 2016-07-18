import unittest

import saspy


class TestSASsessionObject(unittest.TestCase):
    """
    def __init__(self, *args):
        super(TestSASsessionObject, self).__init__(*args)
        self.sas = saspy.SASsession(cfgname='default')
        self.assertIsInstance(self.sas, saspy.SASsession, msg="sas = saspy.SASsession(...) failed")
        # TODO: check that SAS/STAT is installed

    def __del__(self, *args):
        if self.sas:
            self.sas._endsas()
    """

    def setUp(self):
        # Use the first entry in the configuration list
        self.sas = saspy.SASsession(cfgname=saspy.SAScfg.SAS_config_names[0])
        self.assertIsInstance(self.sas, saspy.SASsession, msg="sas = saspy.SASsession(...) failed")

    def tearDown(self):
        if self.sas:
            self.sas._endsas()

    def test_smoke(self):
        # Basic model returns objects
        ets = self.sas.sasets()
        air = self.sas.sasdata('air', 'sashelp')
        b = ets.arima(data=air, identify='var=air(1,12)')
        a = ['CHISQAUTO', 'DESCSTATS', 'LOG', 'SERIESCORRPANEL']
        self.assertEqual(a, b,
                         msg=u"Simple Regession (reg) model failed to return correct objects expected:{0:s}  returned:{1:s}".format(
                             str(a), str(b)))

    def test_missingVar(self):
        ets = self.sas.sasets()
        d = self.sas.sasdata('air', 'sashelp')
        b = ets.arima(data=d, by='novar', identify='var=air(1,12)')
        a = ['ERROR_LOG']
        self.assertEqual(a, b,
                         msg=u"arima model failed to return correct objects expected:{0:s}  returned:{1:s}".format(
                             str(a), str(b)))

    def test_extraStmt(self):
        # Extra Statements are ignored
        ets = self.sas.sasets()
        d = self.sas.sasdata('air', 'sashelp')
        b = ets.arima(data=d, by='novar', identify='var=air(1,12)', crosscorr='date', decomp='air')
        a = ets.arima(data=d, by='novar', identify='var=air(1,12)')
        self.assertEqual(a, b, msg=u"Extra Statements not being ignored expected:{0:s}  returned:{1:s}".format(
            str(a), str(b)))

    def test_outputDset(self):
        ets = self.sas.sasets()
        air = self.sas.sasdata('air', 'sashelp')
        outAir = self.sas.sasdata('air')
        ets.arima(data=air, weight='novar', model='weight=height', out=outAir)
        self.assertIsInstance(outAir, saspy.SASdata, msg="out= dataset not created properly")

    def test_overridePlot(self):
        # Test that user can override plot options
        ets = self.sas.sasets()
        air = self.sas.sasdata('air', 'sashelp')
        outAir = self.sas.sasdata('air')
        b = ets.arima(data=air, identify='var=air(1,12)', out=outAir, procopts='plots=none')
        a = ['CHISQAUTO', 'DESCSTATS', 'LOG']
        self.assertEqual(a, b, msg=u"plots overridden and disabled expected:{0:s}  returned:{1:s}".format(
            str(a), str(b)))
