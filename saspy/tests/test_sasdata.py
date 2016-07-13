import unittest
import saspy


class TestSASdataObject(unittest.TestCase):
    def __init__(self, *args):
        super(TestSASdataObject, self).__init__(*args)
        #self.sas = saspy.SASsession()#cfgname='default')
        #self.assertIsInstance(self.sas, saspy.SASsession, msg="sas = saspy.SASsession(...) failed")

    def __del__(self, *args):
        #if self.sas:
        #   self.sas._endsas()
        pass

    def setUp(self):
        self.sas = saspy.SASsession()
        #pass

    def tearDown(self):
        if self.sas:
           self.sas._endsas()
        #pass

    def test_SASdata(self):
        #test sasdata method
        self.cars = self.sas.sasdata('cars', libref='sashelp', results='text')
        self.assertIsInstance(self.cars, saspy.SASdata, msg="cars = sas.sasdata(...) failed")

        #test set_batch()
        self.sas.set_batch(True)
        ll = self.cars.head()
        self.assertIsInstance(ll, dict, msg="set_batch(True) didn't return dict")

        #test head()
        self.sas.set_batch(True)
        ll = self.cars.head()
        expected = ['1', 'Acura', 'MDX', 'SUV', 'Asia', 'All', '$36,945', '$33,337',
                    '3.5', '6', '265', '17', '23', '4451', '106', '189']
        rows = ll['LST'].splitlines()
        retrieved = []
        for i in range(len(rows)):
           retrieved.append(rows[i].split())
        self.assertIn(expected, retrieved, msg="cars.head() result didn't contain row 1")

        #test tail()
        self.sas.set_batch(True)
        ll = self.cars.tail()
        expected = ['424', 'Volvo', 'C70', 'LPT', 'convertible', '2dr', 'Sedan', 'Europe', 'Front',
                    '$40,565', '$38,203', '2.4', '5', '197', '21', '28', '3450', '105', '186']
        rows = ll['LST'].splitlines()
        retrieved = []
        for i in range(len(rows)):
           retrieved.append(rows[i].split())
        self.assertIn(expected, retrieved, msg="cars.tail() result didn't contain row 1")

        #test contents()
        self.sas.set_batch(True)
        ll = self.cars.contents()
        expected = ['Data', 'Set', 'Name', 'SASHELP.CARS', 'Observations', '428']
        rows = ll['LST'].splitlines()
        retrieved = []
        for i in range(len(rows)):
           retrieved.append(rows[i].split())
        self.assertIn(expected, retrieved, msg="cars.contents() result didn't contain expected result")
        
        #test describe()
        self.sas.set_batch(True)
        ll = self.cars.describe()
        expected = ['MSRP', '428', '32774.86', '19431.72', '10280.00', '20329.50', '27635.00', '39215.00', '192465.00']
        rows = ll['LST'].splitlines()
        retrieved = []
        for i in range(len(rows)):
           retrieved.append(rows[i].split())
        self.assertIn(expected, retrieved, msg="cars.contents() result didn't contain expected result")
        
        #test set_results()
        self.sas.set_batch(True)
        self.cars.set_results('HTML')
        ll = self.cars.describe()
        expected = '<!DOCTYPE html>'
        row1 = ll['LST'].splitlines()[0]
        self.assertEqual(expected, row1, msg="cars.set_results() result weren't HTML")
        
        self.cars.set_results('TEXT')
        ll = self.cars.describe()
        row1 = ll['LST'].splitlines()[0]
        self.assertNotEqual(expected, row1, msg="cars.set_results() result weren't TEXT")

        #test hist()
        self.sas.set_batch(True)
        self.cars.set_results('TEXT')
        ll = self.cars.hist('MSRP')
        expected = 'alt="The SGPlot Procedure" src="data:image/png;base64'
        self.assertIsInstance(ll, dict, msg="cars.hist(...) didn't return dict")
        self.assertGreater(len(ll['LST']), 40000, msg="cars.hist(...) result were too short")
        self.assertIn(expected, ll['LST'], msg="cars.hist(...) result weren't what was expected")
        self.cars.set_results('HTML')
        
        #test series()
        self.sas.set_batch(True)
        ll = self.sas.submit('''proc sql; 
                                create table sales as 
                                select month, sum(actual) as tot_sales, sum(predict) as predicted_sales 
                                from sashelp.prdsale 
                                group by 1 
                                order by month ;quit;
                             ''')
        sales = self.sas.sasdata('sales') 
        ll = sales.series(y=['tot_sales','predicted_sales'], x='month', title='total vs. predicted sales')
        expected = 'alt="The SGPlot Procedure" src="data:image/png;base64'
        self.assertIsInstance(ll, dict, msg="cars.series(...) didn't return dict")
        self.assertGreater(len(ll['LST']), 70000, msg="cars.series(...) result were too short")
        self.assertIn(expected, ll['LST'], msg="cars.series(...) result weren't what was expected")
        
        #test heatmap()
        self.sas.set_batch(True)
        ll = self.cars.heatmap('MSRP','horsepower')
        expected = 'alt="The SGPlot Procedure" src="data:image/png;base64'
        self.assertIsInstance(ll, dict, msg="cars.heatmap(...) didn't return dict")
        self.assertGreater(len(ll['LST']), 30000, msg="cars.heatmap(...) result were too short")
        self.assertIn(expected, ll['LST'], msg="cars.heatmap(...) result weren't what was expected")
        
        
        
