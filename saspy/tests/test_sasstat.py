import unittest
import saspy


class TestSASstat(unittest.TestCase):
    def setUp(self):
        # Use the first entry in the configuration list
        self.sas = saspy.SASsession(cfgname=saspy.SAScfg.SAS_config_names[0])
        self.assertIsInstance(self.sas, saspy.SASsession, msg="sas = saspy.SASsession(...) failed")
        procNeeded=['reg', 'mixed', 'hpsplit']
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
        stat = self.sas.sasstat()
        tr = self.sas.sasdata("class", "sashelp")
        b = stat.reg(data=tr, model='weight=height')
        a = ['ANOVA', 'COOKSDPLOT', 'DFBETASPANEL', 'DFFITSPLOT', 'DIAGNOSTICSPANEL', 'FITPLOT', 'FITSTATISTICS',
             'LOG', 'NOBS', 'OBSERVEDBYPREDICTED', 'PARAMETERESTIMATES', 'QQPLOT', 'RESIDUALBOXPLOT',
             'RESIDUALBYPREDICTED',
             'RESIDUALHISTOGRAM', 'RESIDUALPLOT', 'RFPLOT', 'RSTUDENTBYLEVERAGE', 'RSTUDENTBYPREDICTED']
        self.assertEqual(sorted(a), sorted(b.__dir__()),
                         msg=u"Simple Regession (reg) model failed to return correct objects expected:{0:s}  returned:{1:s}".format(
                             str(a), str(b)))

    def test_missingVar(self):
        stat = self.sas.sasstat()
        tr = self.sas.sasdata("class", "sashelp")
        b = stat.mixed(data=tr, weight='novar', model='weight=height')
        a = ['ERROR_LOG']
        self.assertEqual(a, b.__dir__(),
                         msg=u"Simple Regession (mixed) model failed to return correct objects expected:{0:s}  returned:{1:s}".format(
                             str(a), str(b)))

    def test_extraStmt(self):
        # Extra Statements are ignored
        stat = self.sas.sasstat()
        d = self.sas.sasdata('cars', 'sashelp')
        b = stat.hpsplit(data=d, target='MSRP / level=interval', architecture='MLP', hidden=100, input='enginesize--length', train='', procopts='maxdepth=3')
        a = stat.hpsplit(data=d, target='MSRP / level=interval', input='enginesize--length', procopts='maxdepth=3' )
        self.assertEqual(a.__dir__(), b.__dir__(), msg=u"Extra Statements not being ignored expected:{0:s}  returned:{1:s}".format(str(a), str(b)))

    def test_multiTarget(self):
        # multiple target variables
        stat = self.sas.sasstat()
        nnin = self.sas.sasdata('cars', 'sashelp')
        self.assertRaises(SyntaxError, lambda: stat.hpsplit(data=nnin, target='MSRP origin', input='enginesize--length'))

    def test_outputDset(self):
        stat = self.sas.sasstat()
        tsave = self.sas.sasdata('tsave')
        tr = self.sas.sasdata("class", "sashelp")
        stat.mixed(data=tr, weight='novar', model='weight=height', out=tsave)
        self.assertIsInstance(tsave, saspy.SASdata, msg="out= dataset not created properly")
