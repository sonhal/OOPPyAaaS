from oop_pyaaas.connector import AaaSConnector
import pandas


class AaaSService:

    def __init__(self, url, connector=AaaSConnector):
        self._conn = connector(url)

    def calc_re_identification_risk(self, dataset):
        payload = self._covert_dataset_to_payload(dataset)
        return self._conn.analyse_data(payload=payload)

    def _covert_dataset_to_payload(self, dataset):
        data_dict = {}
        attribute_type_dict = {}
        for key, value in dataset.items():
            data_dict[key] = value["cells"]
            attribute_type_dict[key] = value["attribute_type"]
        df = pandas.DataFrame.from_dict(data_dict)
        csv_string = df.to_csv(sep=",", index=False)
        payload = {"data": csv_string, "attributeTypes": attribute_type_dict}
        return payload
