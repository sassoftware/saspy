import unittest
import saspy


class TestSASdataObject(unittest.TestCase):
    def __init__(self, *args):
        super(TestSASdataObject, self).__init__(*args)
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

    def test_SASsession(self):
        self.cars = self.sas.sasdata('cars', libref='sashelp', results='text')
        self.assertIsInstance(self.cars, saspy.SASdata, msg="cars = sas.sasdata(...) failed")

        self.sas.set_batch(True)
        ll = self.cars.head()
        self.assertIn("1 Acura MDX", ll['LST'], msg="cars.head() result didn't contain row 1")

        self.sas.set_batch(True)
        ll = self.cars.tail()
        self.assertIn("428   Volvo   XC70", ll['LST'], msg="cars.tail() result didn't contain row 1")


