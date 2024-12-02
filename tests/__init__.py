from dotenv import load_dotenv
import os
import sys

# Load the .env file
load_dotenv()

# Add the PYTHONPATH from the .env file to sys.path
pythonpath = os.getenv("PYTHONPATH")
if pythonpath and pythonpath not in sys.path:
    sys.path.insert(0, pythonpath)