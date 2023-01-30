from kapsarc_data_scraper.sqlite_database import database_utils as dbu


def test_get_filters_str():
    # Test with an empty filters dictionary
    filters_dict = {}
    expected = ""
    result = dbu.get_filters_str(filters_dict)
    assert result == expected

    # Test with a single filter
    filters_dict = {"age": "25"}
    expected = "age=25"
    result = dbu.get_filters_str(filters_dict)
    assert result == expected

    # Test with multiple filters
    filters_dict = {"age": "25", "name": "John"}
    expected = "age=25 and name=John"
    result = dbu.get_filters_str(filters_dict)
    assert result == expected
