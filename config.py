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
