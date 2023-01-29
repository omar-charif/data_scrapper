import sqlite3
import sys

import pandas as pd

from typing import Dict, List

from kapsarc_data_scraper.logging_utils import get_logger

logger = get_logger("DatabaseUtils")


def get_filters_str(filters_dict: Dict[str, str]) -> str:
    """
    create and returns a str to be use in the where clause
    :param filters_dict: list of filters to apply when querying the data
    :return: filter string to be used in the where clause
    """
    filter_str = ""
    num_filters = filters_dict.__len__()
    count = 0
    for key, value in filters_dict.items():
        if count < num_filters - 1:
            filter_str += f"{key}={value} and "
        else:
            filter_str += f"{key}={value}"
        count += 1

    return filter_str


class DataBase:
    def __init__(self, database_name: str):
        self.database_name = database_name
        self.connection = sqlite3.connect(database=database_name)
        self.cursor = self.connection.cursor()

    def connect_database(self):
        # reopen connection to database
        self.connection = sqlite3.connect(database=self.database_name)

    def close_connetion(self):
        self.connection.close()

    def table_exist(self, table_name: str) -> bool:
        """
        checks if a table exists in the specified database
        :param table_name: name of the table to check existence
        :return: True if exists and False if not
        """
        logger.info(f"checking if {table_name} exists in {self.database_name}")

        # Getting all tables from sqlite_master
        sql_query = """SELECT name FROM sqlite_master
        WHERE type='table';"""

        # executing get table names query
        self.cursor.execute(sql_query)

        # printing all tables list
        list_of_tables = self.cursor.fetchone()

        table_exists_flag = False
        if list_of_tables is not None:
            table_exists_flag = table_name in list_of_tables

        return table_exists_flag

    def get_column_names(self, table_name: str) -> List[str]:
        """
        extracts number of columns
        :param table_name: name of the table
        :return: list of columns names
        """
        if self.table_exist(table_name=table_name) is False:
            return []

        columns_query = f"SELECT * from ({table_name})"
        self.cursor.execute(columns_query)
        column_names = list(map(lambda x: x[0], self.cursor.description))

        return column_names

    def get_number_of_column(self, table_name: str) -> int:
        """
        counts the number of columns in a table
        :param table_name: name of the table
        :return: count number of column
        """
        number_of_columns = len(self.get_column_names(table_name=table_name))

        return number_of_columns

    def get_number_of_row(self, table_name: str):
        """
        counts number of rows
        :param table_name: name of the table
        :return: number of rows
        """
        rows_query = f"SELECT Count() FROM {table_name}"
        self.cursor.execute(rows_query)
        number_of_rows = self.cursor.fetchone()[0]

        return number_of_rows

    def create_table(
        self,
        table_name: str,
        schema: Dict[str, Dict[str, str]],
        primary_key_list: List[str],
    ) -> int:
        """
        creates table with the provided schema
        :param table_name: name of the table to create
        :param schema: schema as dict
            example: schema = {
                "country": {"data_type": "TEXT", "null_str": "NOT NULL"},
                "mont-year": {"data_type": "TEXT", "null_str": "NOT NULL"},
            }
        :param primary_key_list: list of column to use for primary key
        :return: 0 if create successful and 1 otherewise
        """
        if table_name is None or table_name == "":
            logger.error("missing table name!")
            return 1

        if schema is None or schema.__len__() == 0:
            logger.error("Empty schema!")
            return 1

        if self.table_exist(table_name=table_name) is True:
            logger.error(f"Unable to create {table_name}. {table_name} already exists!")
            return 1

        try:

            # format primary key string
            primary_key_str = f"PRIMARY KEY ({','.join(primary_key_list)})"

            # create query string
            query = f"CREATE TABLE {table_name} ("
            for name, settings in schema.items():
                column_str = f"{name}   {settings['data_type']} {settings['null_str']},"
                query = query + column_str
            query = query + primary_key_str + ");"

            # execute query
            self.connection.execute(query)
            self.connection.commit()

            logger.info(f"{table_name} created!")

        except RuntimeError:
            logger.error(f"Unable to create table: {table_name}")
            return 1

        return 0

    def drop_table(self, table_name: str) -> int:
        """
        drops a table if it exists
        :param table_name: name of the table to drop
        :return: 0 if drop successfull and 0 otherwise
        """
        if table_name == "":
            logger.error("Missing table name. Please set the table name!")
            return 1

        if self.table_exist(table_name=table_name) is False:
            logger.warning(f"Unable to drop {table_name}, it does not exists!")
            return 0

        self.cursor.execute(f"DROP TABLE {table_name}")

        return 0

    def insert_df_table(
        self, table_name: str = "", data_df: pd.DataFrame = None
    ) -> int:
        """
        inserts pandas dataframe into table
        :param table_name: name of the table to insert dataframe
        :param data_df: data pandas dataframe
        :return: number if added rows
        """
        # performing checks of input data
        if table_name == "":
            logger.error("Missing table name. Please set the table name!")
            return -1

        if self.table_exist(table_name=table_name) is False:
            return -1

        if data_df is None or data_df.empty:
            logger.error("Empty dataframe!")
            return -1

        # check the compatibility of the pandas dataframe
        number_of_columns = self.get_number_of_column(table_name=table_name)
        if number_of_columns != data_df.shape[1]:
            logger.error(
                "number of column in database table and input pandas dataframe not matching!"
            )
            return -1

        # ietrate over query reponse and load data into table
        str_value_querying = f"({', '.join(['?'] * number_of_columns)})"
        # insert data in table one by one
        for _, row in data_df.iterrows():
            try:
                self.cursor.execute(
                    f"INSERT INTO {table_name} VALUES {str_value_querying}",
                    row.values.tolist(),
                )
            except sqlite3.IntegrityError:
                logger.error(
                    "Unable to insert row. Primary key already exists in data!"
                )

        self.connection.commit()
        logger.info("Done loading data into database!")
        return data_df.shape[0]

    def retrieve_data(
        self,
        table_name: str,
        extract_column_list: List[str] = None,
        filters_dict: Dict[str, str] = None,
    ) -> List[dict]:
        """
        retrieve data from data table
        :param table_name: name of the tabele
        :param extract_column_list: list of column to retrieves
        :param filters_dict: conditions for data retrieval
        :return: dict of retrieved data
        """

        if table_name == "":
            logger.error("Missing table name. Please set the table name!")
            return 1

        if extract_column_list is not None and len(extract_column_list) > 0:
            extract_columns_str = ", ".join(extract_column_list)
        else:
            extract_columns_str = "*"

        if filters_dict is not None and filters_dict.__len__() > 0:
            filters_str = get_filters_str(filters_dict=filters_dict)
            query_str = (
                f"SELECT {extract_columns_str} from {table_name} where {filters_str}"
            )
        else:
            query_str = f"SELECT {extract_columns_str} from {table_name}"

        table_column_name_list = self.get_column_names(table_name=table_name)

        self.cursor.execute(query_str)

        data_rows = []
        for data_row in self.cursor.fetchall():
            dict_row = {}
            for name, value in zip(table_column_name_list, data_row):
                dict_row[name] = value
            data_rows.append(dict_row)

        logger.info("Done retrieving data for table!")

        return data_rows


if __name__ == "__main__":
    data_path = "C:/repos/data_scrapper/kapsarc_data_scraper/data.parquet"
    database_name = "beyond_2020.db"
    table_name = "exports"
    schema = {
        "country": {"data_type": "TEXT", "null_str": "NOT NULL"},
        "month_year": {"data_type": "TEXT", "null_str": "NOT NULL"},
        "value": {"data_type": "INTEGER", "null_str": "NOT NULL"},
    }
    data_base = DataBase(database_name=database_name)

    data_base.create_table(
        table_name="exports",
        schema=schema,
        primary_key_list=["country", "month_year"],
    )

    data_df = pd.read_parquet(data_path)

    data_base.insert_df_table(table_name=table_name, data_df=data_df)
    data_base.retrieve_data(table_name=table_name)
    sys.exit()
