import os
import sqlite3
import pandas as pd
import pytest
from src.db import store_data_to_sqlite, execute_query, make_dir_if_not_exists

# Fixture to provide a temporary SQLite database
@pytest.fixture
def temp_db_path(tmp_path):
    """Provide a temporary SQLite database file path."""
    return tmp_path / "test_database.db"

@pytest.fixture
def sample_dataframe():
    """Provide a sample DataFrame for testing."""
    data = {
        "name": ["Alice", "Bob"],
        "email": ["alice@example.com", "bob@example.com"],
        "age": [30, 25]
    }
    return pd.DataFrame(data)

def test_make_dir_if_not_exists(temp_db_path):
    """Test the make_dir_if_not_exists function."""
    dir_path = temp_db_path.parent
    make_dir_if_not_exists(dir_path)
    assert dir_path.exists()  # Ensure directory is created

def test_store_data_to_sqlite(temp_db_path, sample_dataframe):
    """Test storing data in SQLite using store_data_to_sqlite."""
    # Ensure the database file doesn't exist before storing data
    assert not os.path.exists(temp_db_path)

    # Store the data in the SQLite database
    store_data_to_sqlite(sample_dataframe, str(temp_db_path))

    # Verify the database file is created
    assert os.path.exists(temp_db_path)

    # Verify data is stored correctly in the database
    conn = sqlite3.connect(temp_db_path)
    result_df = pd.read_sql("SELECT * FROM users", conn)
    conn.close()

    # Check that the stored data matches the original DataFrame
    pd.testing.assert_frame_equal(sample_dataframe, result_df)

def test_execute_query(temp_db_path, sample_dataframe):
    """Test executing a query against SQLite."""
    # Store sample data in the SQLite database
    store_data_to_sqlite(sample_dataframe, str(temp_db_path))

    # Execute a query to fetch all user names
    query = "SELECT name FROM users"
    result = execute_query(str(temp_db_path), query)

    # Verify the query results
    expected_result = [("Alice",), ("Bob",)]  # Expected result from the query
    assert result == expected_result
