import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BASE_URL = os.getenv("BASE_URL")
    VALID_USERNAME = os.getenv("VALID_USERNAME")
    VALID_PASSWORD = os.getenv("VALID_PASSWORD")
    TIMEOUT = 10
