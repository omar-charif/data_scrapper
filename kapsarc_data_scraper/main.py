# This is a sample Python script.

import sys
from typing import Dict, List

from kapsarc_data_scraper.update_web import read_updated_webpage_content
from kapsarc_data_scraper.data_scrapper import (
    scrape_data_from_content,
    transform_wide_to_long,
)
from kapsarc_data_scraper.sqlite_database.database_utils import DataBase

from kapsarc_data_scraper.logging_utils import get_logger

logger = get_logger("Main")

# set constant variables
WEBPAGE_URL = "http://www.jodidb.org/TableViewer/tableView.aspx?ReportId=93906"
SELECT_MENU_ID = "selectMenu2"
SELECT_MENU_VALUE_ID = "li-el-d2-mi3"
DATA_TABLE_ID = "DataTable"
COLUMN_HEADER_CLASS = "TVItemColHeader"
VALUE_COLUMN_NAME = "value"
DATABASE_NAME = "beyond_2020.db"
TABLE_NAME = "exports"
SCHEMA = {
    "country": {"data_type": "TEXT", "null_str": "NOT NULL"},
    "month_year": {"data_type": "TEXT", "null_str": "NOT NULL"},
    "value": {"data_type": "INTEGER", "null_str": "NOT NULL"},
}
PRIMARY_KEY_LIST = ["country", "month_year"]


def refresh_data() -> int:
    # refresh data in database
    try:
        data_base = DataBase(database_name=DATABASE_NAME)
        data_base.drop_table(table_name=TABLE_NAME)
        data_base.create_table(
            table_name=TABLE_NAME, schema=SCHEMA, primary_key_list=PRIMARY_KEY_LIST
        )
        logger.info(f"Cleaned {TABLE_NAME}!")
        content = read_updated_webpage_content(
            url=WEBPAGE_URL,
            select_menu_id=SELECT_MENU_ID,
            select_menu_value_id=SELECT_MENU_VALUE_ID,
        )

        data_df = scrape_data_from_content(
            content=content,
            data_table_id=DATA_TABLE_ID,
            column_header_class=COLUMN_HEADER_CLASS,
        )
        logger.info("Finished scraping data!")

        transformed_data = transform_wide_to_long(data_df=data_df)
        count_rows = data_base.insert_df_table(
            table_name=TABLE_NAME, data_df=transformed_data
        )
        data_base.close_connetion()
        logger.info(f"{count_rows} rows were loaded in {TABLE_NAME}")
        return 0
    except RuntimeError:
        return 1


def retrieve_all_data() -> List[Dict[str, str]]:
    # retrieve all data from exports table
    data_base = DataBase(database_name=DATABASE_NAME)
    data = data_base.retrieve_data(table_name=TABLE_NAME)
    data_base.close_connetion()
    return data


def retrieve_filtered_data(
    extract_column_list: List[str] = None,
    filters_dict: Dict[str, str] = None,
) -> List[Dict[str, str]]:
    """
    retrieve data with specific columns and filters
    :param extract_column_list: list of column to retrieves
    :param filters_dict: conditions for data retrieval
    :return:
    """
    data_base = DataBase(database_name=DATABASE_NAME)
    data = data_base.retrieve_data(
        table_name=TABLE_NAME,
        extract_column_list=extract_column_list,
        filters_dict=filters_dict,
    )
    data_base.close_connetion()
    return data


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    data = retrieve_all_data()
    sys.exit(len(data))
