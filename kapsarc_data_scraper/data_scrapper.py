import requests
import pandas as pd

from bs4 import BeautifulSoup

from kapsarc_data_scraper.logging_utils import get_logger

logger = get_logger("DataScapper")

# set constant variable
WEBPAGE_URL = "http://www.jodidb.org/TableViewer/tableView.aspx?ReportId=93906"
SELECT_MENU_ID = "selectMenu2"
SELECT_MENU_VALUE_ID = "li-el-d2-mi3"
COUNTRY_COLUMN_NAME = "country"
MONTH_YEAR_COLUMN_NAME = "month_year"
VALUE_COLUMN_NAME = "value"


def scrape_data_from_url(
    url: str, data_table_id: str, column_header_class: str
) -> pd.DataFrame:
    """
    scrape tabular data from url based on a table id
    :param url: url of webpage to scrape from
    :param data_table_id: id of data table to scrape data from
    :param column_header_class: class to use to detect headers
    :return: data in pandas dataframe
    """
    if url == "" or data_table_id == "" or column_header_class == "":
        logger.error("Missing param. Please make sure to set all required parameters!")
        return pd.DataFrame()

    response = requests.get(url)
    logger.info("Requested URL!")
    scrapped_df = scrape_data_from_content(
        content=response.text,
        data_table_id=data_table_id,
        column_header_class=column_header_class,
    )
    return scrapped_df


def scrape_data_from_content(
    content: str, data_table_id: str, column_header_class: str
) -> pd.DataFrame:
    """
    scrapes data from website
    :param url: url of the website to grab data from
    :param content: webpage content as a string
    :param data_table_id: id of data table to scrape data from
    :param column_header_class: class to use to detect headers
    :return: table data as pandas dataframe
    """
    if content == "":
        logger.error(
            "Content is empty. Please make sure to pass a webpage to the scrapper!"
        )
        return pd.DataFrame()

    # load webpage content into soup object
    soup = BeautifulSoup(content, "html.parser")

    # extract table content by table id
    table = soup.find("table", {"id": data_table_id})
    if table is None:
        logger.error("Wrong data table id. Please check the id you passed")
        return pd.DataFrame()

    logger.info("Loaded table content!")

    # read thead text to extract month-year data
    column_names = table.find("thead")
    month_year = column_names.find_all("tr")[0]
    month_year_th_list = month_year.find_all("th", {"class": column_header_class})
    if month_year_th_list is None:
        logger.error(
            "Wrong column header class. Please check the class for column header you passed"
        )
        return pd.DataFrame()

    month_year_list = []
    for row_column in month_year_th_list:
        month_year_list.append(row_column.text)

    logger.info("extracted data column name. Month-year data!")

    # read info data
    data_table = table.find("tbody")
    data_row_list = data_table.find_all("tr")
    country_value_list = []
    for data_row in data_row_list:
        country_values = [data_row.find("th").text]
        for value in data_row.find_all("td"):
            country_values.append(value.text)
        country_value_list.append(country_values)
    logger.info("Extracted data from table!")
    column_list = [COUNTRY_COLUMN_NAME] + month_year_list
    data_df = pd.DataFrame(data=country_value_list, columns=column_list)
    logger.info("Scraping data done!")
    return data_df


def transform_wide_to_long(data_df: pd.DataFrame) -> pd.DataFrame:
    """
    transform data from wide to long
    :param data_df: scrapped data from website
    :return: return a long format data
    """
    if data_df is None:
        logger.error("Passed a None instead of a dataframe!")
        return pd.DataFrame()

    if data_df.shape[0] == 0:
        logger.error("Passed an empty dataframe!")
        return pd.DataFrame()

    logger.info("Started transforming data")
    transformed_data_df = data_df.copy(deep=True)
    transformed_data_df.set_index(keys=COUNTRY_COLUMN_NAME, inplace=True)

    # stacked data and converted to long data
    transformed_data_df = transformed_data_df.stack().to_frame()

    transformed_data_df.reset_index(inplace=True)
    transformed_data_df.rename(
        columns={"level_1": MONTH_YEAR_COLUMN_NAME, 0: VALUE_COLUMN_NAME}, inplace=True
    )
    logger.info("Done transforming!")

    return transformed_data_df


if __name__ == "__main__":
    from kapsarc_data_scraper.update_web import read_updated_webpage_content

    url = "http://www.jodidb.org/TableViewer/tableView.aspx?ReportId=93906"
    select_menu_id = "selectMenu2"
    select_menu_value_id = "li-el-d2-mi3"
    content = read_updated_webpage_content(
        url=WEBPAGE_URL,
        select_menu_id=select_menu_id,
        select_menu_value_id=select_menu_value_id,
    )
    DATA_TABLE_ID = "DataTable"
    COLUMN_HEADER_CLASS = "TVItemColHeader"
    data_df = scrape_data_from_content(
        content=content,
        data_table_id=DATA_TABLE_ID,
        column_header_class=COLUMN_HEADER_CLASS,
    )

    transformed_data = transform_wide_to_long(data_df=data_df)
