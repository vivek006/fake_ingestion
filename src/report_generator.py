import yaml
from db import execute_query

def load_report_queries(config_file="/app/src/report_config.yml"):
    """
    Load the report queries from the configuration file.
    """
    with open(config_file, "r") as f:
        config = yaml.safe_load(f)
    
    return config.get("reports", [])

def generate_report(report_name, db_name):
    """
    Generate and print the report for the given report name.
    """
    queries = load_report_queries()

    # Find the query by name
    query = next((item["query"] for item in queries if item["query_name"] == report_name), None)
    if query:
        result = execute_query(db_name, query)
        print(f"Results for {report_name}:")
        for row in result:
            print(row)
    else:
        print(f"Report {report_name} not found in the configuration.")
