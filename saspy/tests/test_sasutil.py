import unittest

import saspy
from saspy.tests.util import Utilities


class TestSASutil(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sas = saspy.SASsession()
        util = Utilities(cls.sas)
        procNeeded = ['hpimpute', 'hpbin', 'hpsample', 'univariate']
        if not util.procFound(procNeeded):
            cls.skipTest("Not all of these procedures were found: %s" % str(procNeeded))

    @classmethod
    def tearDownClass(cls):
        if cls.sas:
            cls.sas._endsas()

    def test_hpimputeSmoke(self):
        util = self.sas.sasutil()
        d = self.sas.sasdata("hmeq", 'sampsio')
        out1 = util.hpimpute(data=d, input = 'mortdue value clage debtinc', impute= 'mortdue / value  = 70000' )
        self.assertFalse('ERROR_LOG' in out1.__dir__(), msg=u"hpimpute had errors in the log")

    def test_hpbinSmoke(self):
        util = self.sas.sasutil()
        cars = self.sas.sasdata("cars", 'sashelp')
        out1 = util.hpbin(data=cars, output=True, input='msrp')
        self.assertFalse('ERROR_LOG' in out1.__dir__(), msg=u"hpbin had errors in the log")

    def test_hpsampleSmoke(self):
        util = self.sas.sasutil()
        d = self.sas.sasdata("hmeq", 'sampsio')
        out1 = util.hpsample(data=d, output=True, cls='job reason', var='loan value delinq derog')
        self.assertFalse('ERROR_LOG' in out1.__dir__(), msg=u"hpsample had errors in the log")

    def test_univariateSmoke(self):
        util = self.sas.sasutil()
        d = self.sas.sasdata("hmeq", 'sampsio')
        out1 = util.univariate(data=d, var='loan value delinq derog')
        self.assertFalse('ERROR_LOG' in out1.__dir__(), msg=u"univariate had errors in the log")



