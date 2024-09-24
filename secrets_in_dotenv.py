from dotenv import load_dotenv
import os


# Load environment variables from .env file
load_dotenv()
'''
Load the environment variables from .env file. 
Create .env file if you don't have it. 
.env file will not be pushed to code repo.'''
api_token = os.getenv('API_TOKEN')