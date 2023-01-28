from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import time


def change_selection_menu_option(url: str, select_menu_id: str, select_menu_value_id: str) -> str:
    """
    changes option in selection menu
    :param select_menu_id: id of the select menu to change
    :param select_menu_value_id: id of the value to  switch to
    :return: content of the webpage after the change
    """
    # initiate driver and load webpage
    driver = webdriver.Firefox()
    driver.get(url=url)

    # change Balance to Exports
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, f"//img[@id='{select_menu_id}']"))).click()
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, f"//li[@id='{select_menu_value_id}']"))).click()

    # sleep for three seconds to allow page to load data
    time.sleep(3)
    content = driver.page_source

    return content


if __name__ == "__main__":
    import pandas as pd

    url = "http://www.jodidb.org/TableViewer/tableView.aspx?ReportId=93906"
    select_menu_id = "selectMenu2"
    select_menu_value_id = "li-el-d2-mi3"
    content = change_selection_menu_option(
        url=url,
        select_menu_id=select_menu_id,
        select_menu_value_id=select_menu_value_id
    )

