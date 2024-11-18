from breeze_connect import BreezeConnect
from dotenv import load_dotenv, find_dotenv,dotenv_values
import os
import seckey
import urllib
import datetime
import pandas as pd
import openpyxl as xl
from openpyxl import load_workbook
import pytz
from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging

def load_env_variables():
    #dotenv_path = find_dotenv()
    load_dotenv(dotenv_path=".env")
    # Force reload the .env file
    env_values = dotenv_values(".env")
    os.environ.update(env_values)
    usr_slt = os.getenv("PHR")
    logging.info("usr_slt:PHR:  %s", usr_slt)
    # lt_pr = seckey.create_encryption_key(lt_pr)
    # print(lt_pr)
    # usr_slt = seckey.decrypt_data(usr_slt,lt_pr)
    # print(usr_slt)
    lt_pr=os.getenv("qt")
    logging.info("lt_pr: qt  %s", lt_pr)
    #usr_slt = os.getenv("PHR")
    #usr_slt="gAAAAABmcS1dzjpq2sodvebKdtC1AFTZQvDsmNVN8nWiFNjut8SChIsWd_2HGA5sd4CQqfdT5bIDexgt4E4IxGH0OmDXw8fpYg=="
    
    lt_pr = seckey.create_encryption_key(lt_pr)
    logging.info("lt_pr: converted  %s", lt_pr)
    usr_slt = seckey.decrypt_data(usr_slt,lt_pr)
    logging.info("usr_slt: converted  %s", usr_slt)
    logging.info("END")
    usr_slt = seckey.create_encryption_key(usr_slt)
    lap_key = os.getenv("ICBZ_KEY")
    lap_key = seckey.decrypt_data(str_key=seckey.pad_token(lap_key), usr_slt=usr_slt)
    lap_key = lap_key.decode('utf-8')
    lap_sec = os.getenv("ICBZ_S")
    lap_sec = seckey.decrypt_data(str_key=lap_sec, usr_slt=usr_slt)
    lap_sec = lap_sec.decode('utf-8')
    return lap_key, lap_sec

def connect_to_breeze(lap_key,lap_sec,ses_tok):
    try:
        breeze = BreezeConnect(api_key=lap_key)
        breeze.generate_session(api_secret=lap_sec, session_token=ses_tok)
        return breeze
    except Exception as e:
        print("Error in breeze connection")
        print("https://api.icicidirect.com/apiuser/login?api_key=" + urllib.parse.quote_plus(lap_key))
        return None

def generate_trade_list(breeze):
    now = datetime.now(pytz.timezone('Asia/Kolkata'))
    formatted_now = now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    twenty_years_ago = now - relativedelta(years=20)
    formatted_from= twenty_years_ago.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    n_list = breeze.get_trade_list(from_date=formatted_from,
                                   to_date=formatted_now,
                                   exchange_code="NSE",
                                   product_type="",
                                   action="",
                                   stock_code="")
    b_list = breeze.get_trade_list(from_date="2005-01-01T06:00:00.000Z",
                                   to_date=formatted_now,
                                   exchange_code="BSE",
                                   product_type="",
                                   action="",
                                   stock_code="")
    st_rec = n_list['Success']
    st_rec.extend(b_list['Success'])
    return st_rec

def generate_historical_data(breeze,start_date,end_date,stock_code,exchange_code):
    print(start_date, end_date, stock_code, exchange_code)
    data = breeze.get_historical_data_v2(interval="1day", from_date= start_date,
            to_date= end_date , stock_code=stock_code, exchange_code=exchange_code, product_type="cash")
    #print(data)
    put_data = pd.DataFrame(data['Success'])
    if put_data.empty:
        print('Data not found:', start_date)
        df = pd.DataFrame()
    else:
        df = put_data[['datetime', 'open', 'high', 'low', 'close']]
    return df

def secon(ses_tok, fn_name, start_date=None, end_date=None, stock_code=None, exchange_code=None):
    lap_key, lap_sec = load_env_variables()
    #print(lap_key, lap_sec,ses_tok)
    breeze = connect_to_breeze(lap_key, lap_sec, ses_tok)
    if fn_name == 'stock inventory':
        return generate_trade_list(breeze)
    elif fn_name == 'historical data':
        return generate_historical_data(breeze, start_date, end_date, stock_code, exchange_code)
    elif fn_name == 'ticker':
        print(exchange_code,stock_code)
        return breeze.get_names(exchange_code=exchange_code, stock_code=stock_code).get('isec_stock_code')
  