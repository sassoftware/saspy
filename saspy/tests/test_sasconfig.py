import unittest
import saspy


class TestSASconfigObject(unittest.TestCase):
    @classmethod    
    def setUpClass(cls):
        cls.sas = saspy.SASsession() #cfgname='default')
        #cls.assertIsInstance(cls.sas, saspy.SASsession, msg="sas = saspy.SASsession(...) failed")

    @classmethod
    def tearDownClass(cls):
        if cls.sas:
           cls.sas._endsas()


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


