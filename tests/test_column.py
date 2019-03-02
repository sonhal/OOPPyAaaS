import unittest
from oop_pyaaas.dataset import Column


class ColumnTest(unittest.TestCase):

    def test_to_dict(self):
        data = [1,2,3,4]
        name = "id"
        attribute_type = "IDENTIFYING"
        column = Column(name=name, cells=data, attribute_type=attribute_type)
        column_dict = column.to_dict()
        for num in data:
            self.assertIn(num, column_dict[name]["cells"])
        self.assertEqual(attribute_type, column_dict[name]["attribute_type"])


