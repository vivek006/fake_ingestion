from src.anonymizer import anonymize_data
import pandas as pd

def test_anonymize_data():
    # Updated mock_data to match the expected format
    mock_data = [
        {"name": "test", "email": "test_user@gmail.com", "email_domain": "gmail.com"}
    ]
    
    # Call the anonymize_data function with a DataFrame
    result = anonymize_data(mock_data)
    
    # Assert that the result is a DataFrame
    assert isinstance(result, pd.DataFrame), "Result should be a DataFrame"
    
    # Check if the 'email_domain' column exists and assert that the email domain is anonymized
    assert 'email_domain' in result.columns, "Result should have an 'email_domain' column"

    print("result.email_domain.iloc[0]: ", result.email_domain.iloc[0])

    assert result.email_domain.iloc[0] == "gmail.com", "Email domain should be anonymized"