from kapsarc_data_scraper.update_web import read_updated_webpage_content

URL = "http://www.jodidb.org/TableViewer/tableView.aspx?ReportId=93906"
SELECT_MENU_ID = "selectMenu2"
SELECT_MENU_VALUE_ID = "li-el-d2-mi3"
WRONG_SELECT_MENU_ID = "selectMenu20000000"
WRONG_SELECT_MENU_VALUE_ID = "li-el-d2-mi30sd0asd0as0d"

EXPECTED_SUCCESS_OUTPUT = (
    '<span title="Exports" alt="Exports" id="OthDimItem2">Exports</span>'
)
EXPECTED_MISSING_PARAM_ERROR = "missing params"
EXPECTED_WRONG_SELECT_MENU_ID = "wrong select menu id"
EXPECTED_WRONG_SELECT_MENU_VALUE_ID = "wrong select menu value id"


def test_read_updated_webpage_content_missing_params():
    response = read_updated_webpage_content(
        url=URL, select_menu_id="", select_menu_value_id=SELECT_MENU_VALUE_ID
    )
    assert EXPECTED_MISSING_PARAM_ERROR == response


def test_read_updated_webpage_content_success():
    reponse = read_updated_webpage_content(
        url=URL,
        select_menu_id=SELECT_MENU_ID,
        select_menu_value_id=SELECT_MENU_VALUE_ID,
    )
    assert EXPECTED_SUCCESS_OUTPUT in reponse


def test_read_updated_webpage_content_wrong_select_menu_id():
    response = read_updated_webpage_content(
        url=URL,
        select_menu_id=WRONG_SELECT_MENU_ID,
        select_menu_value_id=SELECT_MENU_VALUE_ID,
    )
    assert EXPECTED_WRONG_SELECT_MENU_ID == response


def test_read_updated_webpage_content_wrong_select_menu_value_id():
    response = read_updated_webpage_content(
        url=URL,
        select_menu_id=SELECT_MENU_ID,
        select_menu_value_id=WRONG_SELECT_MENU_VALUE_ID,
    )
    assert EXPECTED_WRONG_SELECT_MENU_VALUE_ID == response
