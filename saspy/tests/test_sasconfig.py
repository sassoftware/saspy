import unittest
import saspy


class TestSASconfigObject(unittest.TestCase):
    def __init__(self, *args):
        super(TestSASconfigObject, self).__init__(*args)
        self.sas = saspy.SASsession()#cfgname='default')
        self.assertIsInstance(self.sas, saspy.SASsession, msg="sas = saspy.SASsession(...) failed")

    def __del__(self, *args):
        if self.sas:
           self.sas._endsas()

    def setUp(self):
        #self.sas = saspy.SASsession()
        pass

    def tearDown(self):
        #if self.sas:
        #   self.sas._endsas()
        pass

    def test_SASconfig(self):
        pass


