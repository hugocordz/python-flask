import requests
import logging
import config
from datetime import datetime, timedelta
from urllib.request import urlopen
from bs4 import BeautifulSoup


def create_result_object(value, date):
    r = {
        "updated": date,
        "value": value
    }
    return r


data = {}


def get_exchange_rate_fixer(base, symbol):
    response = requests.get(config.Config.FIXER_URL.format(config.Config.FIXER_ACCESS_KEY, base, symbol))
    return create_result_object(response.json()['rates']['MXN'],
                                datetime.fromtimestamp(response.json()['timestamp']).isoformat())


def get_exchange_rate_diario_oficial():
    page = urlopen(config.Config.BANXICO_URL)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    exchange_value = soup.find_all("tr", class_="renglonNon")[0].contents[7].contents[0].strip()
    return create_result_object(float(exchange_value), datetime.utcnow().isoformat())


def get_exchange_rate_xml():
    try:
        today = datetime.now()
        response = requests.get(config.Config.BANXICO_XML_URL.format(today.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d')))
        soup = BeautifulSoup(response.content, features="xml")
        # Validates if in the current day the prices is published and if is not, look for the value from previous day
        if hasattr(soup.find("dato"), 'contents'):
            value = soup.find("dato").contents[0]
        else:
            previous_day = requests.get(
                config.Config.BANXICO_XML_URL.format((today - timedelta(days=1)).strftime('%Y-%m-%d'),
                                                     (today - timedelta(days=1)).strftime('%Y-%m-%d')))
            soup = BeautifulSoup(previous_day.content, features="xml")
            value = soup.find("dato").contents[0]
        date = datetime.strptime(soup.find("fecha").contents[0], '%d/%m/%Y').isoformat()
        return create_result_object(float(value), date)
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        return {'error_code': 1, "message": "A problem has occurred with Banxico service try later"}
