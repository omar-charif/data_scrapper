import pandas as pd

from kapsarc_data_scraper.data_scrapper import (
    scrape_data_from_content,
    scrape_data_from_url,
    transform_wide_to_long,
)
from kapsarc_data_scraper.update_web import read_updated_webpage_content

URL = "http://www.jodidb.org/TableViewer/tableView.aspx?ReportId=93906"
SELECT_MENU_ID = "selectMenu2"
SELECT_MENU_VALUE_ID = "li-el-d2-mi3"

DATA_TABLE_ID = "DataTable"
COLUMN_HEADER_CLASS = "TVItemColHeader"

WRONG_DATA_TABLE_ID = "DataTable20000"
WRONG_COLUMN_HEADER_CLASS = "TVItemColHeader200000"

content = read_updated_webpage_content(
    url=URL, select_menu_id=SELECT_MENU_ID, select_menu_value_id=SELECT_MENU_VALUE_ID
)


def test_scrape_data_from_url_missing():
    data_df = scrape_data_from_url(
        url="", data_table_id=DATA_TABLE_ID, column_header_class=COLUMN_HEADER_CLASS
    )
    assert data_df.shape[0] == 0


def test_scrape_data_from_content_missing_content():
    data_df = scrape_data_from_content(
        content="content",
        data_table_id=DATA_TABLE_ID,
        column_header_class=COLUMN_HEADER_CLASS,
    )
    assert data_df.shape[0] == 0


def test_scrape_data_from_content_success():
    data_df = scrape_data_from_content(
        content=content,
        data_table_id=DATA_TABLE_ID,
        column_header_class=COLUMN_HEADER_CLASS,
    )
    assert data_df.shape[0] > 0


def test_transform_wide_to_long_missing_df():
    data_df = transform_wide_to_long(data_df=None)
    assert data_df.shape[0] == 0


def test_transform_wide_to_long_empty_df():
    data_df = transform_wide_to_long(data_df=pd.DataFrame())
    assert data_df.shape[0] == 0
