import unittest
from oop_pyaaas.dataset import Columns, Column


class ColumnsTest(unittest.TestCase):

    def test_to_dict(self):
        data = [1,2,3,4]
        names = ["mike", "fred", "frodo", "long"]
        name = "id"
        attribute_type = "IDENTIFYING"
        column1 = Column(name=name, cells=data, attribute_type=attribute_type)
        column2 = Column(name="name", cells=names, attribute_type=attribute_type)
        columns = Columns(column1, column2)
        result = columns.to_dict()
        print(result)

    def test_cant_add_column_with_different_amount_of_cells(self):
        data = [1,2,3,4]
        names = ["mike", "fred", "frodo"]
        name = "id"
        attribute_type = "IDENTIFYING"
        column1 = Column(name=name, cells=data, attribute_type=attribute_type)
        column2 = Column(name="name", cells=names, attribute_type=attribute_type)

        with self.assertRaises(ValueError):
            Columns(column1, column2)


