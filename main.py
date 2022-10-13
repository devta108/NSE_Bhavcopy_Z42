import datetime
import logging
from utils import get_url_response
from utils import get_secutites
from utils import get_bhavcopies
import sqlite3


r = get_url_response('https://www.nseindia.com/market-data/securities-available-for-trading')
securites = get_secutites(r.text)
securites = securites.replace(r"^ +| +$", r"", regex=True)
if securites is None:
    logging.info('Securities file not found')
    exit(1)
bhavcopy = get_bhavcopies(datetime.date.today(), 30)
if bhavcopy is None:
    logging.info("No bhav Copy found for desired days, try different days...")
    exit(1)
bhavcopy_normalised = bhavcopy.drop(columns=['SERIES', 'SYMBOL', 'Unnamed: 13'], axis=1)
bhavcopy_normalised = bhavcopy_normalised.replace(r"^ +| +$", r"", regex=True)
connection = sqlite3.connect("nse_securites_data.db")
securites.to_sql('Equity Segment Securities', con=connection, if_exists='replace', index=False)
bhavcopy_normalised.to_sql('Bhavcopy', con=connection, if_exists='replace', index=False)