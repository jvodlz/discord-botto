import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
APPLICATION_ID = os.getenv('APPLICATION_ID')
PUBLIC_KEY = os.getenv('PUBLIC_KEY')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')