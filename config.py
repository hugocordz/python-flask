import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DEBUG = True
    DEVELOPMENT = True
    FIXER_ACCESS_KEY = '55d8ede1c07f1464a94c20812c71945a'
    BANXICO_XML_URL = os.environ['BANXICO_XML_URL']
    BANXICO_URL = os.environ['BANXICO_URL']
    FIXER_URL = os.environ['FIXER_URL']
    DB_HOST = os.environ['DB_HOST']
    DB_PORT = os.environ.get('DB_PORT', 3306)
    DB_DATABASE = os.environ['DB_DATABASE']
    DB_USER = os.environ['DB_USER']
    DB_PASSWORD = os.environ['DB_PASSWORD']
    sqlalchemy_connection_string = (
        'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{db}'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = sqlalchemy_connection_string.format(
        port=DB_PORT, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, db=DB_DATABASE,
    )
