import falcon
import json

from kapsarc_data_scraper.logging_utils import get_logger
from kapsarc_data_scraper.main import refresh_data, retrieve_all_data


class Version(object):
    logger = get_logger("Version")

    def on_get(self, request, response):
        response_json = {"version": "0.1.0", "stage": "beta"}

        self.logger.info(f"response_json: {response_json}")
        response.body = json.dumps(response_json, ensure_ascii=False)


class Refresh_Data(object):
    logger = get_logger("RefreshData")

    def on_get(self, request, response):
        num_rows = refresh_data()
        response_json = {"number_of_loaded_rows": num_rows}

        self.logger.info(f"response_json: {response_json}")
        response.body = json.dumps(response_json, ensure_ascii=False)


class Retrieve_Data(object):
    logger = get_logger("RetrieveData")

    def on_get(self, request, response):
        data = retrieve_all_data()
        response_json = {"number_of_retrieved_rows": len(data), "data": data}

        self.logger.info(f"response_json: {response_json}")
        response.body = json.dumps(response_json, ensure_ascii=False)
