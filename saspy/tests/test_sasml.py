import unittest

import saspy
from saspy.tests.util import Utilities


class TestSASml(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sas = saspy.SASsession()
        util = Utilities(cls.sas)
        procNeeded = ['hpforest', 'hp4score', 'hpclus', 'hpneural', 'treeboost', 'hpbnet', 'hpcluster']
        if not util.procFound(procNeeded):
            cls.skipTest("Not all of these procedures were found: %s" % str(procNeeded))

    @classmethod
    def tearDownClass(cls):
        if cls.sas:
            cls.sas._endsas()

    def testHPForestSmoke1(self):
        ml = self.sas.sasml()
        dt = self.sas.sasdata("class", "sashelp")
        out1 = ml.hpforest(data=dt, target='height',
                           input={'interval': 'weight', "nominal": 'sex'}
                           )
        a = ['BASELINE', 'DATAACCESSINFO', 'FITSTATISTICS', 'LOG',
             'MODELINFO', 'NOBS', 'PERFORMANCEINFO', 'VARIABLEIMPORTANCE']
        self.assertEqual(sorted(a), sorted(out1.__dir__()),
                         msg=u"Simple HPForest  model failed to return correct objects expected:{0:s}  returned:{1:s}".format(
                             str(a), ' '.join(out1.__dir__())))

    def testHPNeuralSmoke1(self):
        ml = self.sas.sasml()
        dt = self.sas.sasdata("class", "sashelp")
        out1 = ml.hpneural(data=dt, target='height',
                           input={'interval': 'weight', "nominal": 'sex'},
                           train={'numtries': 3, 'maxiter': 300},
                           hidden=5)
        a = ['CLASSLEVELS', 'DATAACCESSINFO', 'ERRORSUMMARY', 'FITSTATISTICS', 'ITERATION', 'MODELINFORMATION', 'NOBS',
             'PERFORMANCEINFO', 'TRAINING', 'LOG']
        self.assertEqual(sorted(a), sorted(out1.__dir__()),
                         msg=u"Simple HPNeural  model failed to return correct objects expected:{0:s}  returned:{1:s}".format(
                             str(a), ' '.join(out1.__dir__())))

    def testtreeboostSmoke1(self):
        ml = self.sas.sasml()
        dt = self.sas.sasdata("class", "sashelp")
        out1 = ml.treeboost(data=dt, target='height',
                            input={'interval': 'weight', "nominal": 'sex'}, save=True)
        a = ['FIT', 'IMPORTANCE', 'MODEL', 'NODESTATS', 'RULES', 'LOG']
        self.assertEqual(sorted(a), sorted(out1.__dir__()),
                         msg=u"Simple treeboost  model failed to return correct objects expected:{0:s}  returned:{1:s}".format(
                             str(a), ' '.join(out1.__dir__())))

    def testHPBnetSmoke1(self):
        ml = self.sas.sasml()
        dt = self.sas.sasdata("iris", "sashelp")
        out1 = ml.hpbnet(data=dt, target='species',
                         procopts='numbin=3 structure=Naive maxparents=1 prescreening=0 varselect=0',
                         input={'interval': ['PetalWidth', "PetalLength", 'SepalLength', 'SepalWidth']})
        self.assertFalse('ERROR_LOG' in out1.__dir__(), msg=u"HPBNET had errors in the log")

    def testHP4scoreSmoke1(self):
        pass

    def testHPclusterSmoke1(self):
        ml = self.sas.sasml()
        dt = self.sas.sasdata("iris", "sashelp")
        out1 = ml.hpcluster(data=dt,
                            id=['PetalWidth', "PetalLength", 'SepalLength', 'SepalWidth'],
                            input={'interval': ['PetalWidth', "PetalLength", 'SepalLength', 'SepalWidth']})
        self.assertFalse('ERROR_LOG' in out1.__dir__(), msg=u"HPCLUSTER had errors in the log")
