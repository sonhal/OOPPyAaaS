import unittest
import pandas
from oop_pyaaas.dataset import Dataset
import tempfile
import pathlib

from oop_pyaaas.service import AaaSService


class DatasetTest(unittest.TestCase):

    def setUp(self):

        self.test_data_csv = """age, gender, zipcode\n34, male,81667\n35, female,81668\n6, male,81669\n 37, female,81670\n38, male,81671\n39, female,81672\n40, male,81673\n41, female,81674\n42, male,81675\n43, female,81676\n44, male,81677"""

        self.test_data_dict = {'age': {0: 34,
                                       1: 35,
                                       2: 36,
                                       3: 37,
                                       4: 38,
                                       5: 39,
                                       6: 40,
                                       7: 41,
                                       8: 42,
                                       9: 43,
                                       10: 44},
                               'gender': {0: ' male',
                                           1: ' female',
                                           2: ' male',
                                           3: ' female',
                                           4: ' male',
                                           5: ' female',
                                           6: ' male',
                                           7: ' female',
                                           8: ' male',
                                           9: ' female',
                                           10: ' male'},
                               'zipcode': {0: 81667,
                                            1: 81668,
                                            2: 81669,
                                            3: 81670,
                                            4: 81671,
                                            5: 81672,
                                            6: 81673,
                                            7: 81674,
                                            8: 81675,
                                            9: 81676,
                                            10: 81677}}
        self.test_df = pandas.DataFrame(self.test_data_dict)
        self.test_attributes = {"age":"IDENTIFYING",
                                "gender":"INSENSITIVE",
                                "zipcode":"INSENSITIVE"}
        self.tempdir = tempfile.TemporaryDirectory()
        self.test_csv_path = pathlib.Path(self.tempdir.name).joinpath("testcsv.csv")
        with self.test_csv_path.open("w") as file:
            file.write(self.test_data_csv)

    def tearDown(self):
        self.tempdir.cleanup()

    def test_from_pandas(self):
        dataset = Dataset.from_pandas(self.test_df, self.test_attributes)
        self.assertIsInstance(dataset, Dataset)

    def test_from_csv(self):
        dataset = Dataset.from_csv(self.test_csv_path, ",", self.test_attributes)
        self.assertIsInstance(dataset, Dataset)

    def test_dataset_from_csv_and_pandas_are_equal(self):
        pandas_dataset = Dataset.from_pandas(self.test_df, self.test_attributes)
        csv_dataset = Dataset.from_csv(self.test_csv_path, ",", self.test_attributes)
        self.assertEqual(pandas_dataset, csv_dataset)

    def test_wrong_attribute_field_raises_exception(self):
        error_test_attributes = {"not_a_field_int_the_set": "IDENTIFYING",
                           "gender": "INSENSITIVE",
                           "zipcode": "INSENSITIVE"}
        with self.assertRaises(ValueError):
            Dataset.from_pandas(self.test_df, error_test_attributes)

    def test_re_indentification_risk_analysation(self):
        dataset = Dataset.from_pandas(self.test_df, self.test_attributes, AaaSService("http://localhost:8080"))
        result = dataset.re_identification_risk()
        print(result.text)

