import unittest
import saspy
from saspy.tests.util import Utilities


class TestSASViyaML(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sas = saspy.SASsession()
        util = Utilities(cls.sas)
        procNeeded = ['factmac', 'fastknn', 'forest', 'gradboost', 'nnet', 'svdd', 'svmachine']
        if not util.procFound(procNeeded):
            cls.skipTest("Not all of these procedures were found: %s" % str(procNeeded))
        cls.sas.submit("""
        cas mysession;
        libname mycas cas;
        data mycas.class;
        set sashelp.class;
        run;
        """)

    @classmethod
    def tearDownClass(cls):
        if cls.sas:
            cls.sas._endsas()

    def testFactmacSmoke1(self):
        # TODO endable test
        self.skipTest("can't find shipped dataset that works")
        viya = self.sas.sasviyaml()
        dt = self.sas.sasdata("class", "mycas")
        out1 = viya.factmac(data=dt, target='height', input={'interval': 'weight', "nominal": 'sex'})
        self.assertFalse('ERROR_LOG' in out1.__dir__(), msg=u"factmac had errors in the log")

    @unittest.skip("this is just syntax errors")
    def testFastknnSmoke1(self):
        viya = self.sas.sasviyaml()
        # sas.saslib(engine='cas', libref='mycas')
        self.sas.submit("""
        data mycas.hmeq;
                set sampsio.hmeq(obs=4000);
                id=_n_;
        run;
        data mycas.query;
                set sampsio.hmeq(firstobs=4001 obs=4100);
                id=_n_;
        run;
        """)
        hmeq = self.sas.sasdata('hmeq','mycas')
        out1 = viya.fastknn(data=hmeq, input={'interval': ['loan', 'mortdue', 'value']},
                            id='id',
                            procopts='query = mycas.query',
                            output=self.sas.sasdata('knn_out', 'mycas'))
        self.assertFalse('ERROR_LOG' in out1.__dir__(), msg=u"fastknn had errors in the log")

    def testForestSmoke1(self):
        viya = self.sas.sasviyaml()
        dt = self.sas.sasdata("class", "mycas")
        out1 = viya.forest(data=dt, target='height', input={'interval': 'weight', "nominal": 'sex'})
        self.assertFalse('ERROR_LOG' in out1.__dir__(), msg=u"forest had errors in the log")

    def testGradboostSmoke1(self):
        viya = self.sas.sasviyaml()
        dt = self.sas.sasdata("class", "mycas")
        out1 = viya.gradboost(data=dt, target='height', input={'interval': 'weight', "nominal": 'sex'})
        self.assertFalse('ERROR_LOG' in out1.__dir__(), msg=u"gradboost had errors in the log")

    def testNnetSmoke1(self):
        viya = self.sas.sasviyaml()
        dt = self.sas.sasdata("class", "mycas")
        out1 = viya.nnet(data=dt, target='height',
                       input={'interval': 'weight', "nominal": 'sex'},
                       train='outmodel=mycas.nnetmodel1',
                       hidden=5)
        out2 = viya.nnet(data=dt, target='height',
                         input={'interval': 'weight', "nominal": 'sex'},
                         train={'outmodel':'mycas.nnetmodel1'},
                         hidden=5)
        self.assertFalse('ERROR_LOG' in out1.__dir__(), msg=u"nnet had errors in the log")

    def testSvddSmoke1(self):
        viya = self.sas.sasviyaml()
        dt = self.sas.sasdata("class", "mycas")
        out1 = viya.svdd(data=dt, input={'interval': 'weight', "nominal": 'sex'}, kernel = "RBF / bw=2")
        self.assertFalse('ERROR_LOG' in out1.__dir__(), msg=u"svdd had errors in the log")

    def testSvmachineSmoke1(self):
        viya = self.sas.sasviyaml()
        dt = self.sas.sasdata("class", "mycas")
        out1 = viya.svmachine(data=dt, target='sex', input={'interval': ['weight', 'height']})
        self.assertFalse('ERROR_LOG' in out1.__dir__(), msg=u"svmachine had errors in the log")

if __name__ == '__main__':
    unittest.main()
