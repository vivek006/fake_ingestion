import logging
from download_config import APIConfig
from download_config import download_data
from anonymizer import anonymize_data
from db import store_data_to_sqlite
from report_generator import generate_report

DB_NAME = "data/anonymized_users.db"
def main():
    logging.basicConfig(level=logging.INFO)

    # Load configuration
    api_config = APIConfig()

    try:
        # Step 1: Download data
        logging.info("Starting data download...")
        data = download_data(api_config)
        logging.info("Data downloaded successfully!")

        # Step 2: Anonymize data
        logging.info("Anonymizing data...")
        anonymized_data = anonymize_data(data)
        logging.info("Data anonymized successfully!")

        # Step 3: Store data in SQLite
        logging.info("Storing data to SQLite...")
        store_data_to_sqlite(anonymized_data, DB_NAME)
        logging.info("Data stored successfully in SQLite!")

        # Step 4: Generate reports
        logging.info("Generating reports...")
        generate_report("percentage_germany_gmail", DB_NAME)
        generate_report("top_countries_gmail", DB_NAME)
        generate_report("people_over_60_gmail", DB_NAME)
        logging.info("Reports generated successfully!")

    except Exception as e:
        logging.error(f"Pipeline execution failed: {e}", exc_info=True)

if __name__ == "__main__":
    main()
