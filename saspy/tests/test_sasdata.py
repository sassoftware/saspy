from saspy.sasdata import SASdata
from saspy.sasresults import SASresults
from pandas.util.testing import assert_frame_equal
from tempfile import TemporaryDirectory
import unittest
import saspy
import pandas as pd
import os


SALES_QUERY = """
    proc sql;
        create table sales as
        select
            month,
            sum(actual) as tot_sales,
            sum(predict) as predicted_sales
        from sashelp.prdsale
        group by month
        order by month;
    quit;
"""


class TestSASdataObject(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sas = saspy.SASsession(results='html')
        cls.sas.set_batch(True)

        # Contruct a SASdata object that returns results as text
        cls.cars = cls.sas.sasdata('cars', libref='sashelp', results='text')

    @classmethod
    def tearDownClass(cls):
        cls.sas._endsas()

    def setUp(self):
        """
        Make sure self.cars defaults to 'text' result type, even if a test
        modifies it without changing it back. This prevents a cascade of
        failing tests.
        """
        self.cars.set_results('text')

    def helper_wkcars(self):
        """
        Create a copy of sashelp.cars in WORK.
        :return [SASdata]:
        """
        self.sas.submit("data cars; set sashelp.cars; id = _n_; run;")

        return self.sas.sasdata('cars')

    def helper_wkclass(self):
        """
        Create a copy of sashelp.class in WORK.
        :return [SASdata]:
        """
        self.sas.submit("data class; set sashelp.class; run;")

        return self.sas.sasdata('class')

    def test_sasdata_construct(self):
        """
        Test creation of SASdata object returns the correct type.
        """
        self.assertIsInstance(self.cars, SASdata)

    def test_sasdata_contruct_noexist(self):
        """
        Test creating a SASdata object for a table that does not exist still
        returns a SASdata object
        """
        notable = self.sas.sasdata('notable', results='text')

        self.assertIsInstance(notable, saspy.SASdata, msg="sas.sasdata(...) failed")

    def test_sasdata_batch_true(self):
        """
        Test method set_batch with True argument forces SASdata objects to
        return dict types on other method calls.
        """
        ll = self.cars.head()

        self.assertIsInstance(ll, dict)

    def test_sasdata_head(self):
        """
        Test method head returns the first few rows of a dataset.
        """
        EXPECTED = ['1', 'Acura', 'MDX', 'SUV', 'Asia', 'All', '$36,945',
            '$33,337', '3.5', '6', '265', '17', '23', '4451', '106', '189']

        ll = self.cars.head()
        rows = ll['LST'].splitlines()
        retrieved = [x.split() for x in rows]

        self.assertIn(EXPECTED, retrieved, msg="cars.head() result didn't contain first row")

    @unittest.skip("Test fails with extra header info")
    def test_sasdata_tail(self):
        """
        Test method tail returns the last few rows of a dataset.
        """
        EXPECTED = ['424', 'Volvo', 'C70', 'LPT', 'convertible', '2dr', 'Sedan',
            'Europe', 'Front', '$40,565', '$38,203', '2.4', '5', '197', '21',
            '28', '3450', '105', '186']

        ll = self.cars.tail()
        rows = ll['LST'].splitlines()
        retrieved = [x.split() for x in rows]

        self.assertIn(EXPECTED, retrieved, msg="cars.tail() result didn't contain last row")

    def test_sasdata_tail_pandas_instance(self):
        """
        Test method tail returns a pandas DataFrame if requested.
        """
        self.cars.set_results('pandas')
        ll = self.cars.tail()

        self.assertIsInstance(ll, pd.DataFrame, "Is return type correct")

    def test_sasdata_tail_pandas_shape(self):
        """
        Test method tail returns a correctly shaped pandas DataFrame.
        """
        self.cars.set_results('pandas')
        ll = self.cars.tail()

        self.assertEqual(ll.shape, (5, 15), msg="Wrong shape returned")

    def test_sasdata_contents(self):
        """
        Test method contents returns the expected data.
        """
        EXPECTED = ['Data', 'Set', 'Name', 'SASHELP.CARS', 'Observations', '428']

        ll = self.cars.contents()
        rows = ll['LST'].splitlines()
        retrieved = [x.split() for x in rows]

        self.assertIn(EXPECTED, retrieved, msg="cars.contents() result didn't contain expected result")

    @unittest.skip("Column output doesn't match the current method. I'm skipping the test for now")
    def test_sasdata_describe(self):
        """
        Test method describe returns the expected data.
        """
        EXPECTED = ['MSRP', '428', '0', '27635', '32775', '19432', '10280', '20330', '27635']

        ll = self.cars.describe()
        rows = ll['LST'].splitlines()
        retrieved = [x.split() for x in rows]

        self.assertIn(EXPECTED, retrieved, msg="cars.describe() result didn't contain expected result")

    def test_SASdata_describe_pandas_instance(self):
        """
        Test method describe returns a pandas DataFrame if requested.
        """
        self.cars.set_results('pandas')
        ll = self.cars.describe()

        self.assertIsInstance(ll, pd.DataFrame, msg='ll is not a dataframe')

    def test_sasdata_describe_pandas_numbers(self):
        """
        Test method describe returns the correct data using a DataFrame.
        """
        EXPECTED = [428, 0, 27635, 32774, 19431, 10280, 20329, 27635, 39215, 192465]

        self.cars.set_results('pandas')
        ll = self.cars.describe()
        actual = [int(x) for x in ll.select_dtypes(include=['number']).iloc[0]]

        self.assertEqual(EXPECTED, actual, msg="cars.describe() result didn't contain expected result")

    def test_sasdata_describe_pandas_chars(self):
        """
        Test method describe returns the correct data using a DataFrame.
        """
        EXPECTED = 'MSRP'

        self.cars.set_results('pandas')
        ll = self.cars.describe()
        actual = ll.iloc[0][0]

        self.assertEqual(EXPECTED, actual, msg="cars.describe() result didn't contain expected result")

    def test_sasdata_results_html(self):
        """
        Test method set_results appropriately sets the return container.
        """
        EXPECTED = '<!DOCTYPE html>'

        self.cars.set_results('html')
        ll = self.cars.describe()
        row1 = ll['LST'].splitlines()[0]

        self.assertEqual(EXPECTED, row1, msg="cars.set_results() result weren't HTML")

    def test_sasdata_results_not_html(self):
        """
        Test method set_results appropriately sets the return container.
        """
        EXPECTED = '<!DOCTYPE html>'

        self.cars.set_results('text')
        ll = self.cars.describe()
        row1 = ll['LST'].splitlines()[0]

        self.assertNotEqual(EXPECTED, row1, msg="cars.set_results() result were HTML")

    def test_sasdata_hist_instance(self):
        """
        Test method hist returns a dict.
        """
        ll = self.cars.hist('MSRP')

        self.assertIsInstance(ll, dict, msg="cars.hist(...) didn't return dict")

    def test_sasdata_hist_length(self):
        """
        Test method hist returns a listing that is long enough?
        """
        ll = self.cars.hist('MSRP')

        # FIXME: How do we know 40,000 is an ok threshold?
        self.assertGreater(len(ll['LST']), 40000, msg="cars.hist(...) result were too short")

    def test_sasdata_hist_values(self):
        """
        Test method hist returns the correct data.
        """
        EXPECTED = 'alt="The SGPlot Procedure" src="data:image/png;base64'

        ll = self.cars.hist('MSRP')

        self.assertIn(EXPECTED, ll['LST'], msg="cars.hist(...) result weren't what was expected")

    def test_sasdata_series_instance(self):
        """
        Test method series returns a dict.
        """
        self.sas.submit(SALES_QUERY)
        sales = self.sas.sasdata('sales')

        ll = sales.series(y=['tot_sales', 'predicted_sales'], x='month', title='total vs. predicted sales')
        self.assertIsInstance(ll, dict, msg="cars.series(...) didn't return dict")

    def test_sasdata_series_length(self):
        """
        Test method series returns a listing that is long enough?
        """
        self.sas.submit(SALES_QUERY)
        sales = self.sas.sasdata('sales')

        # FIXME: How do we know 70,000 is an ok threshold?
        ll = sales.series(y=['tot_sales', 'predicted_sales'], x='month', title='total vs. predicted sales')

        self.assertGreater(len(ll['LST']), 70000, msg="cars.series(...) result were too short")

    def test_sasdata_series_values(self):
        """
        Test method series returns the correct data.
        """
        EXPECTED = 'alt="The SGPlot Procedure" src="data:image/png;base64'

        self.sas.submit(SALES_QUERY)
        sales = self.sas.sasdata('sales')

        ll = sales.series(y=['tot_sales', 'predicted_sales'], x='month', title='total vs. predicted sales')

        self.assertIn(EXPECTED, ll['LST'], msg="cars.series(...) result weren't what was expected")

    def test_sasdata_heatmap_instance(self):
        """
        Test method heatmap returns a dict.
        """
        ll = self.cars.heatmap('MSRP', 'horsepower')

        self.assertIsInstance(ll, dict, msg="cars.heatmap(...) didn't return dict")

    def test_sasdata_heatmap_length(self):
        """
        Test method heatmap returns a listing that is long enough?
        """
        ll = self.cars.heatmap('MSRP', 'horsepower')

        # FIXME: How do we know 30,000 is an ok threshold?
        self.assertGreater(len(ll['LST']), 30000, msg="cars.heatmap(...) result were too short")

    def test_sasdata_heatmap_values(self):
        """
        Test method heatmap returns the correct data.
        """
        EXPECTED = 'alt="The SGPlot Procedure" src="data:image/png;base64'

        ll = self.cars.heatmap('MSRP', 'horsepower')

        self.assertIn(EXPECTED, ll['LST'], msg="cars.heatmap(...) result weren't what was expected")

    def test_sasdata_sort_1var(self):
        """
        Test method sort using one variable
        """
        wkcars = self.helper_wkcars()
        wkcars.sort('type')

        # FIXME: This is not testing sort, only sasdata construction.
        self.assertIsInstance(wkcars, SASdata, msg="Sort didn't return SASdata Object")

    def test_sasdata_sort_2var(self):
        """
        Test method sort using two variables
        """
        wkcars = self.helper_wkcars()
        wkcars.sort('type descending origin')

        # FIXME: This is not testing sort, only sasdata construction.
        self.assertIsInstance(wkcars, SASdata, msg="Sort didn't return SASdata Object")

    def test_sasdata_sort_compare_equal(self):
        """
        Test method sort returns a sorted SASdata object
        """
        wkcars = self.helper_wkcars()
        dup = wkcars.sort('type')

        # FIXME: This is not testing sort, as `dup` always equals `wkcars`
        # regardless of sort order. This is because `sort()` always returns
        # `self` if no `out=` is specified. Therefore, `dup` is a reference
        # to the same address as `wkcars`. You can confirm this by doing the
        # following:
        #   >>> id(wkcars)
        #   >>> id(dup)
        #
        # Effectively, this test is doing the following:
        #   >>> wkcars = 'Whatever'
        #   >>> dup = wkcars
        #   >>> wkcars == dup   # True, because dup points to wkcars
        self.assertEqual(wkcars, dup, msg="Sort objects are not equal but should be")

    def test_sasdata_sort_compare_notequal(self):
        """
        Test method sort with out= returns a copy sorted differently than
        the source.
        """
        wkcars = self.helper_wkcars()
        diff = self.sas.sasdata('diff')
        diff = wkcars.sort('origin', out=diff)

        self.assertNotEqual(wkcars, diff, msg="Sort objects are equal but should not be")

    def test_sasdata_sort_out(self):
        """
        Test method sort with out= returns a new SASdata object.
        """
        wkcars = self.helper_wkcars()
        wkcars.sort('type')
        out1 = wkcars.sort('origin', self.sas.sasdata('out1'))

        self.assertIsInstance(out1, SASdata, msg="Sort didn't return new SASdata Object")

    def test_sasdata_sort_invalidcol(self):
        """
        Test method sort raises a RuntimError if provided an invalid column.
        """
        wkcars = self.helper_wkcars()

        with self.assertRaises(RuntimeError):
            wkcars.sort('foobar')

    def test_sasdata_score_columninfo(self):
        """
        Test method score adds a new column.
        """
        wkcars = self.helper_wkcars()
        original = wkcars.columnInfo()

        wkcars.score(code='P_originUSA = origin;')
        w_newcol = wkcars.columnInfo()

        self.assertNotEqual(original, w_newcol, msg="B should have an extra column P_originUSA")

    def test_sasdata_score_out_source(self):
        """
        Test method score does not modify the original table when out= is
        specified.
        """
        wkcars = self.helper_wkcars()
        wkcars.set_results('pandas')

        wkcars2 = self.sas.sasdata('cars2', 'work')
        wkcars2.set_results('pandas')

        a = wkcars.columnInfo()
        wkcars.score(code='P_originUSA = origin;', out=wkcars2)
        b = wkcars.columnInfo()

        self.assertFalse(assert_frame_equal(a, b), msg="B should be identical to a")

    def test_sasdata_score_out_copy(self):
        """
        Test method score writes to a new table if out= is specified.
        """
        wkcars = self.helper_wkcars()
        wkcars.set_results('pandas')

        wkcars2 = self.sas.sasdata('cars2', 'work')
        wkcars2.set_results('pandas')

        wkcars.score(code='P_originUSA = origin;', out=wkcars2)

        # FIXME: Always passes because sasdate returns a SASdata object on
        # construction. Need to check that wkcars2 actually contains data.
        self.assertIsInstance(wkcars2, SASdata, "Does out dataset exist")

    def test_sasdata_score_file_out(self):
        """
        Test method score accepts a file path as input and uses the contents
        to generate score columns. If out= is specified write to a different
        table.
        """
        with TemporaryDirectory() as temppath:
            with open(os.path.join(temppath, 'score.sas'), 'w') as f:
                f.write('P_originUSA = origin;')

        wkcars = self.helper_wkcars()
        wkcars.set_results('pandas')

        wkcars2 = self.sas.sasdata('cars2', 'work')
        wkcars2.set_results('pandas')

        a = wkcars.columnInfo()
        wkcars.score(file=f.name, out=wkcars2)
        b = wkcars.columnInfo()

        self.assertFalse(assert_frame_equal(a, b), msg="B should be identical to a")

    def test_sasdata_score_file(self):
        """
        Test method score accepts a file path as input and uses the contents
        to generate score columns.
        """
        with TemporaryDirectory() as temppath:
            with open(os.path.join(temppath, 'score.sas'), 'w') as f:
                f.write('P_originUSA = origin;')

        wkcars = self.helper_wkcars()

        a = wkcars.columnInfo()
        wkcars.score(file=f.name)
        b = wkcars.columnInfo()

        self.assertNotEqual(a, b, msg="B should have an extra column P_originUSA")

    def test_regScoreAssess(self):
        # FIXME: Consider moving to test_sasstat.py
        stat = self.sas.sasstat()
        tr = self.helper_wkclass()
        tr.set_results('pandas')

        fname = self.sas.workpath+'hpreg_code.sas'
        b = stat.hpreg(data=tr, model='weight=height', code=fname)
        tr.score(file=fname)
        
        # check that p_weight is in columnInfo
        # FIXME: Only assert once
        self.assertTrue('P_Weight' in tr.columnInfo()['Variable'].values, msg="Prediction Column not found")

        res1 = tr.assessModel(target='weight', prediction='P_weight', nominal=False)
        a = ['ASSESSMENTBINSTATISTICS', 'ASSESSMENTSTATISTICS', 'LOG']
        self.assertEqual(sorted(a), sorted(res1.__dir__()),
                         msg=u" model failed to return correct objects expected:{0:s}  returned:{1:s}".format(
                             str(a), str(b)))
        self.assertIsInstance(res1, SASresults, "Is return type correct")

    def test_regScoreAssess2(self):
        # FIXME: Consider moving to test_sasstat.py
        stat = self.sas.sasstat()
        tr = self.helper_wkclass()
        tr.set_results('pandas')

        fname = self.sas.workpath+'hpreg_code.sas'
        b = stat.hplogistic(data=tr, cls= 'sex', model='sex = weight height', code=fname)
        # This also works with hardcoded strings
        # b = stat.hplogistic(data=tr, cls='sex', model='sex = weight height', code=r'c:\public\foo.sas')
        tr.score(file=fname)

        # check that P_SexF is in columnInfo
        # FIXME: Only assert once
        self.assertTrue('P_SexF' in tr.columnInfo()['Variable'].values, msg="Prediction Column not found")

        res1 = tr.assessModel(target='sex', prediction='P_SexF', nominal=True, event='F')
        a = ['ASSESSMENTBINSTATISTICS', 'ASSESSMENTSTATISTICS', 'LOG', 'SGPLOT']
        self.assertEqual(sorted(a), sorted(res1.__dir__()),
                         msg=u" model failed to return correct objects expected:{0:s}  returned:{1:s}".format(
                             str(a), str(b)))
        self.assertIsInstance(res1, SASresults, "Is return type correct")

    def test_partition_partind(self):
        """
        TODO: Add documentation
        """
        tr = self.helper_wkclass()
        tr.set_results('pandas')

        tr.partition(var='sex', fraction=.5, kfold=1, out=None, singleOut=True)

        self.assertTrue('_PartInd_' in tr.columnInfo()['Variable'].values, msg="Partition Column not found")

    def test_partition_cvfold2(self):
        """
        TODO: Add documentation
        """
        tr = self.helper_wkclass()
        tr.set_results('pandas')

        tr.partition(var='sex', fraction=.5, kfold=2, out=None, singleOut=True)

        self.assertTrue('_cvfold2' in tr.columnInfo()['Variable'].values, msg="Partition Column not found")

    def test_partition_out(self):
        """
        TODO: Add documentation
        """
        tr = self.helper_wkclass()
        tr = self.sas.sasdata("class", "work")
        tr.set_results('pandas')

        out = self.sas.sasdata("class2", "work")
        out.set_results('pandas')

        tr.partition(var='sex', fraction=.5, kfold=2, out=out, singleOut=True)

        # FIXME: Only assert once
        self.assertFalse('_cvfold1' in tr.columnInfo()['Variable'].values, msg="Writing to wrong table")
        self.assertFalse('_PartInd_ ' in tr.columnInfo()['Variable'].values, msg="Writing to wrong table")
        self.assertTrue('_cvfold2' in out.columnInfo()['Variable'].values, msg="Partition Column not found")

    def test_partition_out2(self):
        """
        TODO: Add documentation
        """
        tr = self.helper_wkclass()
        tr.set_results('PANDAS')

        out = self.sas.sasdata("class2", "work")
        out.set_results('PANDAS')

        res1 = tr.partition(var='sex', fraction=.5, kfold=2, out=out, singleOut=False)

        # FIXME: Only assert once
        self.assertFalse('_cvfold1' in tr.columnInfo()['Variable'].values, msg="Writing to wrong table")
        self.assertFalse('_PartInd_ ' in tr.columnInfo()['Variable'].values, msg="Writing to wrong table")
        self.assertTrue('_cvfold2' in out.columnInfo()['Variable'].values, msg="Partition Column not found")
        self.assertIsInstance(res1, list, "Is return type correct")
        self.assertIsInstance(res1[0], tuple, "Is return type correct")
        self.assertIsInstance(res1[0][1], SASdata, "Is return type correct")

    def test_partition_partind_novar(self):
        """
        TODO: Add documentation
        """
        tr = self.helper_wkclass()
        tr.set_results('pandas')
        tr.partition(fraction=.5, kfold=1, out=None, singleOut=True)

        self.assertTrue('_PartInd_' in tr.columnInfo()['Variable'].values, msg="Partition Column not found")

    def test_info_pandas_instance(self):
        """
        Test method info works with pandas result type.
        """
        tr = self.sas.sasdata("class", "sashelp")
        tr.set_results('pandas')
        res = tr.info()

        self.assertIsInstance(res, pd.DataFrame, msg='Data frame not returned')

    def test_info_pandas_shape(self):
        """
        Test method info works with pandas result type.
        """
        tr = self.sas.sasdata("class", "sashelp")
        tr.set_results('pandas')
        res = tr.info()

        self.assertEqual(res.shape, (5, 4), msg="wrong shape returned")

    def test_info_text(self):
        """
        Test method info does not work with text result type.
        """
        tr = self.sas.sasdata("class", "sashelp")
        tr.set_results('text')
        res = tr.info()

        self.assertIsNone(res, msg="only works with Pandas")

    def test_info_html(self):
        """
        Test method info does not work with html result type.
        """
        tr = self.sas.sasdata("class", "sashelp")
        tr.set_results('html')
        res = tr.info()

        self.assertIsNone(res, msg="only works with Pandas")

    def test_outencoding(self):
        """
        Test outencoding option and encoding dsopts
        """
        df = self.sas.sd2df("class", "sashelp")
        sd = self.sas.df2sd(df, 'class2', outencoding='ebcdic500')
        self.assertTrue('encoding' in sd.dsopts.keys(), msg="encoding not set in dsopts")
        self.assertTrue('ebcdic500'== sd.dsopts['encoding'], msg="encoding not correct")

        ll = sd.add_vars({'tom':'"hi tom"'})
        self.assertTrue('Cross Environment Data Access' in ll['LOG'], msg="CEDA msg not found")



