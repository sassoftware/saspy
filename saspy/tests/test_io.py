import saspy
import inspect
import unittest


class TestSASIO(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sas = saspy.SASsession()
        cls.io = cls.sas._io

    @classmethod
    def tearDownClass(cls):
        cls.sas._endsas()

    def is_method(self, obj, method):
        """
        Helper function. Tests whether a provided argument is an object with
        a given method.
        """
        return hasattr(obj, method) and inspect.ismethod(getattr(obj, method))

    def test_sasio_mexist_dataframe2sasdata(self):
        """
        Test that the SAS IO object has a `dataframe2sasdata` method.
        """
        self.assertTrue(self.is_method(self.io, 'dataframe2sasdata'))

    def test_sasio_mexist_exist(self):
        """
        Test that the SAS IO object has an `exist` method.
        """
        self.assertTrue(self.is_method(self.io, 'exist'))

    def test_sasio_mexist_read_csv(self):
        """
        Test that the SAS IO object has a `read_csv` method.
        """
        self.assertTrue(self.is_method(self.io, 'read_csv'))

    def test_sasio_mexist_sasdata2dataframe(self):
        """
        Test that the SAS IO object has a `sasdata2dataframe` method.
        """
        self.assertTrue(self.is_method(self.io, 'sasdata2dataframe'))

    def test_sasio_mexist_sasdata2dataframeCSV(self):
        """
        Test that the SAS IO object has a `sasdata2dataframeCSV` method.
        """
        self.assertTrue(self.is_method(self.io, 'sasdata2dataframeCSV'))

    def test_sasio_mexist_saslog(self):
        """
        Test that the SAS IO object has a `saslog` method.
        """
        self.assertTrue(self.is_method(self.io, 'saslog'))

    def test_sasio_mexist_submit(self):
        """
        Test that the SAS IO object has a `submit` method.
        """
        self.assertTrue(self.is_method(self.io, 'submit'))

    def test_sasio_mexist_submit(self):
        """
        Test that the SAS IO object has a `write_csv` method.
        """
        self.assertTrue(self.is_method(self.io, 'write_csv'))

    def test_sasio_mexist_download(self):
        """
        Test that the SAS IO object has a `download` method.
        """
        self.assertTrue(self.is_method(self.io, 'download'))

    def test_sasio_mexist_upload(self):
        """
        Test that the SAS IO object has an `upload` method.
        """
        self.assertTrue(self.is_method(self.io, 'upload'))

    def test_sasio_mexist__asubmit(self):
        """
        Test that the SAS IO object has an `_asubmit` method.

        NOTE: `_asubmit` is considered a private function based on Python
        conventions (see PEP8). However, due to public usage in the library
        the function must be defined in the IO object.
        """
        self.assertTrue(self.is_method(self.io, '_asubmit'))

    def test_sasio_mexist__endsas(self):
        """
        Test that the SAS IO object has an `_endsas` method.

        NOTE: `_endsas` is considered a private function based on Python
        conventions (see PEP8). However, due to public usage in the library
        the function must be defined in the IO object.
        """
        self.assertTrue(self.is_method(self.io, '_endsas'))

    def test_sasio_mexist__getlog(self):
        """
        Test that the SAS IO object has a `_getlog` method.

        NOTE: `_getlog` is considered a private function based on Python
        conventions (see PEP8). However, due to public usage in the library
        the function must be defined in the IO object.
        """
        self.assertTrue(self.is_method(self.io, '_getlog'))

    def test_sasio_mexist__getlst(self):
        """
        Test that the SAS IO object has a `_getlst` method.

        NOTE: `_getlst` is considered a private function based on Python
        conventions (see PEP8). However, due to public usage in the library
        the function must be defined in the IO object.
        """
        self.assertTrue(self.is_method(self.io, '_getlst'))

    def test_sasio_mexist__startsas(self):
        """
        Test that the SAS IO object has a `_startsas` method.

        NOTE: `_startsas` is considered a private function based on Python
        conventions (see PEP8). However, due to public usage in the library
        the function must be defined in the IO object.
        """
        self.assertTrue(self.is_method(self.io, '_startsas'))
