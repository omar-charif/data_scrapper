from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import time

from logging_utils import get_logger

logger = get_logger("UpdateWebpageSelection")


def read_updated_webpage_content(
    url: str, select_menu_id: str, select_menu_value_id: str
) -> str:
    """
    changes option in selection menu and returns the updated webpage content
    :param select_menu_id: id of the select menu to change
    :param select_menu_value_id: id of the value to  switch to
    :return: content of the webpage after the change
    """
    # initiate driver and load webpage
    driver = webdriver.Firefox()
    driver.get(url=url)
    logger.info("Loaded webpage!")

    # change Balance to Exports
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, f"//img[@id='{select_menu_id}']"))
    ).click()
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, f"//li[@id='{select_menu_value_id}']"))
    ).click()
    logger.info("Update balance in webpage!")

    # sleep for three seconds to allow page to load data
    time.sleep(3)
    content = driver.page_source
    logger.info("Done reading updated webpage content!")

    return content


if __name__ == "__main__":

    url = "http://www.jodidb.org/TableViewer/tableView.aspx?ReportId=93906"
    select_menu_id = "selectMenu2"
    select_menu_value_id = "li-el-d2-mi3"
    content = read_updated_webpage_content(
        url=url,
        select_menu_id=select_menu_id,
        select_menu_value_id=select_menu_value_id,
    )
