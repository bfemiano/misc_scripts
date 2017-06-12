from pyspark import SparkContext, SparkConf, SparkFiles, StorageLevel
from pyspark.sql import SQLContext, SparkSession
import unittest2


def abbrev_dept_builder(abbrevs_bc):

    def abbrev_dept(record):
        (name, dept) = record
        if dept in abbrevs_bc.value:
            dept = abbrevs_bc.value[dept]
        return (name, dept)

    return abbrev_dept


class SparkEmployeeAnalysisTest(unittest2.TestCase):

    def setUp(self):
        conf = SparkConf().setAppName('testing').setMaster('local[2]').set('spark.driver.host', 'localhost')
        conf.set('spark.ui.showConsoleProgress', False)
        self.session = SparkSession.builder.config(conf=conf).getOrCreate()
        self.test_data = [
            ('Ricardo', 'engineering', 2),
            ('Tisa', 'sales', 3),
            ('Sheree', 'marketing', 4), 
            ('Chantelle', 'engineering', 5),
            ('Kylee', 'finance', 2),
            ('Tamatha', 'marketing', 5),
            ('Trena', 'engineering', 2),
            ('Arica', 'engineering', 1),
            ('Santina', 'finance', 2),
            ('Daria', 'marketing', 1),
            ('Magnolia', 'sales', 2),
            ('Antonina', 'finance', 1),
            ('Sumiko', 'engineering', 1),
            ('Carmen', 'sales', 2),
            ('Delois', 'engineering', 1),
            ('Luetta', 'marketing', 3),
            ('Yessenia', 'sales', 1),
            ('Petra', 'engineering', 3),
            ('Charisse', 'engineering', 4),
            ('Lillian', 'engineering', 3),
            ('Wei', 'engineering', 2),
            ('Lahoma', 'sales', 2),
            ('Lucilla', 'marketing', 1),
            ('Stephaine', 'finance', 2),
        ]

    def tearDown(self):
        self.session.stop()

    def test_abbrev_rdd_transform(self):

        data = [
            ('brian', 'engineering'),
            ('steve', 'marketing'),
            ('jon', 'sales')
        ]
        abbrevs_bc = self.session.sparkContext.broadcast({'engineering': 'eng', 'marketing': 'mkt'})
        data_rdd = self.session.sparkContext.parallelize(data)
        output = data_rdd.map(abbrev_dept_builder(abbrevs_bc)).collect()
        expected = [
            ('brian', 'eng'),
            ('steve', 'mkt'),
            ('jon', 'sales')
        ]
        self.assertEqual(sorted(output), sorted(expected))


    def test_rdd_num_engs_with_3_or_more_years(self):
        '''
            Use self.test_data and self.session to build an RDD and transform into a single output.

        '''
        output = None
        expected = len(filter(lambda (name, dept, years): dept == 'engineering' and years >= 3, self.test_data))
        self.assertEqual(expected, output)

    def test_dataframe_num_employees_per_dept(self):
        '''
            Use self.test_data and self.session to build a Data Frame and transform the results into a single output.
        '''
        output = []
        expected = [
            ("engineering", 10),
            ("marketing", 5),
            ("sales", 5),
            ("finance", 4)
        ]
        self.assertEqual(sorted(expected), sorted(output))