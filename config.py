"""General app configuration."""

import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()
DB_NAME = os.getenv('DB_NAME')