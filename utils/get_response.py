import datetime
import requests
from requests.adapters import HTTPAdapter, Retry
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date


def get_url_response(url, count=0):
    session = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[502, 503, 504, 443, 429],
    )
    session.mount(url, HTTPAdapter(max_retries=retries))
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/93.0.4577.63 Safari/537.36 ',
        'Connection': 'keep-alive',
        'Accept': '*/*'
    }
    r = session.get(url, headers=headers, timeout=10)
    if not r.ok and count < 2:
        sleep(1)
        return get_url_response(url, count + 1)
    return r


def get_secutites(page_data):
    page_soup = BeautifulSoup(page_data, features='lxml')
    req_div = page_soup.find_all('div', 'tab-pane active')
    for div in req_div:
        for anchor in div.find_all('a'):
            if anchor.getText() == 'Securities available for Equity segment (.csv)':
                securites = pd.read_csv(anchor['href'])
                return securites
    return None


def get_bhavcopies(lastday=date.today(), days=1):
    days_fetched = 0
    current_day = lastday
    bhavcopies = None
    while days_fetched < days:
        previous_day = current_day - datetime.timedelta(1)
        year = current_day.year
        month = current_day.strftime('%b').upper()
        day = current_day.strftime("%d")
        url = f"https://archives.nseindia.com/content/historical/EQUITIES/{year}/{month}/cm{day}{month}{year}bhav.csv.zip"
        r = get_url_response(url)
        if r.ok:
            current_day_bhav = pd.read_csv(url)
            if bhavcopies is None:
                bhavcopies = current_day_bhav
            else:
                bhavcopies = pd.concat([bhavcopies, current_day_bhav], axis=0)
            days_fetched += 1
        current_day = previous_day
        if current_day < date(2000, 1, 1):
            break
    return bhavcopies
