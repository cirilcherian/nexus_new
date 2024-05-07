import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    chat_pdf_image_path = "images"
    logs_folder = "logs"
    chrmoadb_persists_directory = "chromadb_db/"

    # # hanadb values
    # hanadb_address = os.getenv('hanadb_address')
    # hanadb_port = os.getenv('hanadb_port')
    # hanadb_user = os.getenv('hanadb_user')
    # hanadb_pass = os.getenv('hanadb_pass')

    # openai values
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    MONGODB_URI_CLUSTER = os.getenv('MONGODB_URI_CLUSTER')
    MONGODB_URI_SERVERLESS = os.getenv('MONGODB_URI_SERVERLESS')

    



