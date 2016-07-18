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
        stat = self.sas.sasstat()
        tr = self.sas.sasdata("class", "sashelp")
        b = stat.reg(data=tr, model='weight=height')
        a = ['ANOVA', 'COOKSDPLOT', 'DFBETASPANEL', 'DFFITSPLOT', 'DIAGNOSTICSPANEL', 'FITPLOT', 'FITSTATISTICS',
             'LOG', 'NOBS', 'OBSERVEDBYPREDICTED', 'PARAMETERESTIMATES', 'QQPLOT', 'RESIDUALBOXPLOT',
             'RESIDUALBYPREDICTED',
             'RESIDUALHISTOGRAM', 'RESIDUALPLOT', 'RFPLOT', 'RSTUDENTBYLEVERAGE', 'RSTUDENTBYPREDICTED']
        self.assertEqual(a, b,
                         msg=u"Simple Regession (reg) model failed to return correct objects expected:{0:s}  returned:{1:s}".format(
                             str(a), str(b)))

    def test_missingVar(self):
        stat = self.sas.sasstat()
        tr = sas.sasdata("class", "sashelp")
        b = stat.mixed(data=tr, weight='novar', model='weight=height')
        a = ['ERROR_LOG']
        self.assertEqual(a, b,
                         msg=u"Simple Regession (mixed) model failed to return correct objects expected:{0:s}  returned:{1:s}".format(
                             str(a), str(b)))

    def test_extraStmt(self):
        # Extra Statements are ignored
        stat = self.sas.sasstat()
        d = self.sas.sasdata('cars', 'sashelp')
        b = stat.hpsplit(data=d, target='MSRP', architecture='MLP', hidden=100, input='enginesize--length', train='')
        a = stat.hpsplit(data=d, target='MSRP', input='enginesize--length', )
        self.assertEqual(a, b, msg=u"Extra Statements not being ignored expected:{0:s}  returned:{1:s}".format(
            str(a), str(b)))

    def test_multiTarget(self):
        # multiple target variables
        stat = self.sas.sasstat()
        nnin = self.sas.sasdata('cars', 'sashelp')
        stat.hpsplit(data=nnin, target='MSRP origin', input='enginesize--length')
        self.assertRaises(SyntaxError)

    def test_outputDset(self):
        stat = self.sas.sasstat()
        tsave = self.sas.sasdata('tsave')
        tr = sas.sasdata("class", "sashelp")
        stat.mixed(data=tr, weight='novar', model='weight=height', out=tsave)
        self.assertIsInstance(tsave, saspy.SASdata, msg="out= dataset not created properly")
