import unittest
import saspy
from saspy.tests.util import Utilities


class TestSASutil(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sas = saspy.SASsession()
        util = Utilities()
        procNeeded = ['hpimpute', 'hpbin', 'hpsample']
        if not util.procFound(procNeeded):
            cls.skipTest("Not all of these procedures were found: %s" % str(procNeeded))

    @classmethod
    def tearDownClass(cls):
        if cls.sas:
            cls.sas._endsas()

    def test_hpimputeSmoke(self):
        util = self.sas.sasutil()
        d = self.sas.sasdata("cars", 'sashelp')
        out1 = util.hpimpute(data=d, )
        #test sasdata method
        cars = self.sas.sasdata('cars', libref='sashelp', results='text')
        self.assertIsInstance(cars, saspy.SASdata, msg="cars = sas.sasdata(...) failed")

