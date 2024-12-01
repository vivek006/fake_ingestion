import sqlite3
import pandas as pd
import os

def make_dir_if_not_exists(path):
    """
    Create a directory if it does not exist.
    """
    os.makedirs(path, exist_ok=True)

def store_data_to_sqlite(dataframe, db_name):
    """
    Stores the data in an SQLite database.

    Args:
        dataframe (pd.DataFrame): Processed data to store.
        db_name (str): Path to the SQLite database file.
    """
    make_dir_if_not_exists(os.path.dirname(db_name))

    # Clean the DataFrame: Replace NaN values with None for SQLite compatibility
    dataframe = dataframe.where(pd.notnull(dataframe), None)

    # Ensure all columns contain only simple types (strings, integers, floats, etc.)
    for column in dataframe.columns:
        if dataframe[column].dtype == 'object':
            dataframe[column] = dataframe[column].apply(lambda x: str(x) if isinstance(x, (dict, list)) else x)

    # Connect to SQLite and store data
    conn = sqlite3.connect(db_name)
    dataframe.to_sql("users", conn, if_exists="replace", index=False)
    conn.close()

def execute_query(db_name, query=""):
    """
    Execute a query against the SQLite database.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result
