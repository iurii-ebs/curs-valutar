import requests
import datetime
import json
import os

from bs4 import BeautifulSoup

today = datetime.date.today().strftime("%d.%m.%Y")

PATH = "https://www.bnm.md/en/official_exchange_rates?get_xml=1&date="


def parse_currency(date=today):
    """Date format DD.MM.YYYY returns a json ready object"""
    url = PATH + date
    page = requests.get(url)

    soup_page = BeautifulSoup(page.text, "xml")
    currency_raw = soup_page.find_all("Valute")
    currency_clean = {
        "Date": date,
        "Currency_list": []

    }
    for currency in currency_raw:
        char_code = currency.find("CharCode").string
        name = currency.find("Name").string
        rate = currency.find("Value").string

        currency_obj = {
            "Abbr": char_code,
            "Name": name,
            "Rate": rate,
        }
        currency_clean["Currency_list"].append(currency_obj)
    return currency_clean


if __name__ == '__main__':
    currency = parse_currency()
    file_path = 'history/'
    file_name = currency["Date"].replace('.', '-') + '.json'

    try:
        os.mkdir(file_path)
    except FileExistsError:
        pass

    with open(file_path + file_name, 'w') as out:
        json.dump(currency, out, indent=4)
