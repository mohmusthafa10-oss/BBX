import requests as req
from dotenv import load_dotenv
import os


load_dotenv()

api_key = os.getenv('OPENWEATHER_API_KEY')