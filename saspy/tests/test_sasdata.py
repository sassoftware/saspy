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
        expected = ['1', 'Acura', 'MDX', 'SUV', 'Asia', 'All', '$36,945', '$33,337',
                    '3.5', '6', '265', '17', '23', '4451', '106', '189']
        rows = ll['LST'].splitlines()
        retrieved = []
        for i in range(len(rows)):
           retrieved.append(rows[i].split())
        self.assertIn(expected, retrieved, msg="cars.head() result didn't contain row 1")

        self.sas.set_batch(True)
        ll = self.cars.tail()
        expected = ['424', 'Volvo', 'C70', 'LPT', 'convertible', '2dr', 'Sedan', 'Europe', 'Front',
                    '$40,565', '$38,203', '2.4', '5', '197', '21', '28', '3450', '105', '186']
        rows = ll['LST'].splitlines()
        retrieved = []
        for i in range(len(rows)):
           retrieved.append(rows[i].split())
        self.assertIn(expected, retrieved, msg="cars.tail() result didn't contain row 1")
        
