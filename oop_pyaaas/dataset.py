from abc import abstractmethod
from collections import Sequence, MutableSequence


import pandas
import csv


class Dataset:

    def __init__(self, data, attribute_types, service):
        self._columns = self._create_columns(data, attribute_types)
        self._service = service

    def re_identification_risk(self):
        return self._service.calc_re_identification_risk(self._columns.to_dict())


    @classmethod
    def from_pandas(cls, dataframe: pandas.DataFrame, attribute_types, service):
        data_dict = dataframe.to_dict(orient='list')
        return Dataset(data_dict, attribute_types, service)

    @classmethod
    def from_csv(cls, file_path, delimiter, attribute_types, service):
        data_dict = cls._create_dict_from_csv_file(file_path, delimiter)
        return Dataset(data_dict, attribute_types, service)

    @staticmethod
    def _create_dict_from_csv_file(file, delimiter):
        df = pandas.read_csv(file, sep=delimiter)
        data_dict = df.to_dict(orient='list')
        return data_dict

    @staticmethod
    def _get_headers(data):
        return [header for header in data.keys()]

    @staticmethod
    def _create_columns(data, field_attribute_type_map):
        columns = Columns()
        try:
            for field, attribute_type in field_attribute_type_map.items():
                cells = data[field]
                columns.append(Column(field, attribute_type, cells))
        except KeyError:
            raise ValueError(f"field='{field}' in field_attribute_type_map={field_attribute_type_map} does not exist in dataset={data}")
        return columns


class Columns(MutableSequence):

    def __init__(self, *column):
        self._column_list = [col for col in column]
        for column in self._column_list:
            if not isinstance(column, Column): raise ValueError("Can only contain Column")
        self._assert_columns_are_valid()

    def insert(self, index: int, column) -> None:
        if not isinstance(column, Column): raise ValueError("Can only contain Column")
        self._column_list.insert(index, column)

    def __getitem__(self, i: int):
        return self._column_list[i]

    def __setitem__(self, i: int, column):
        if not isinstance(column, Column): raise ValueError("Can only contain Column")
        self._column_list[i] = column
        self._assert_columns_are_valid()

    def __delitem__(self, i: int) -> None:
        del self._column_list[i]

    def __len__(self) -> int:
        return len(self._column_list)

    def _assert_columns_are_valid(self):
        if len(self._column_list) > 0:
            cell_amount = self._column_list[0]
            for column in self._column_list[0:]:
                if len(column) != cell_amount: raise ValueError(f"column={column} does not have a valid amount of cells")

    def to_dict(self):
        columns_dict = {}
        for column in self._column_list:
            columns_dict = {**columns_dict, **column.to_dict()}
        return columns_dict


class Column:

    def __init__(self, name, attribute_type, cells):
        self._name = name
        self._attribute_type = attribute_type
        self._cells = cells

    def to_dict(self):
        return {self._name: {"cells": self._cells,
                             "attribute_type": self._attribute_type}}

    def __len__(self):
        return len(self._cells)
