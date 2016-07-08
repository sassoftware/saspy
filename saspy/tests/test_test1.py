import unittest
import saspy


class TestConfig(unittest.TestCase):
    def __init__(self, *args):
        super(TestConfig, self).__init__(*args)

    def setUp(self):
        self.sas = saspy.SASsession()

    def tearDown(self):
        self.sas._endsas()

    def test_SASdata(self):
        self.cars = self.sas.sasdata('cars', libref='sashelp', results='text')
        self.assertIsInstance(self.cars, saspy.SASdata, msg="cars = sas.sasdata(...) failed")

        self.sas.set_batch(True)
        ll = self.cars.head()
        self.assertIn("1 Acura MDX", ll['LST'], msg="cars.head() result didn't contain row 1")

        self.sas.set_batch(True)
        ll = self.cars.tail()
        self.assertIn("428   Volvo   XC70", ll['LST'], msg="cars.head() result didn't contain row 1")


