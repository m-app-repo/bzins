import bzins_con
import pandas as pd
from datetime import datetime
import glob
import os
from datetime import datetime

def process_stock_data_from_excel(file_path, ses_tok):
    # Read the Master sheet from the Excel file
    master_df = pd.read_excel(file_path, sheet_name='Master')
    # Create a Pandas ExcelWriter using openpyxl engine to append new sheets


    with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        # Iterate over each row in the Master DataFrame
        for index, row in master_df.iterrows():
            # Get the stock code, start and end dates, and balance from the Master sheet
            ticker = row['stock_code']
            start_date = row['from_date']
            exchange = row['exchange_code']
            end_date = row['to_date'] if pd.notna(row['to_date']) else pd.Timestamp.today()
            balance = row['balance']
            # Convert balance to a number
            balance = float(balance)
            #end_date = end_date +"T09:15:00.000Z"
            #start_date = start_date.isoformat()[:10] + 'T09:30:00.000Z'
            #start_date_iso = datetime.strptime(start_date).isoformat()[:19] + '.000Z'
            # Convert start_date and end_date to ISO date format
            #start_date_iso = start_date.strftime('%Y-%m-%d')
            #end_date_iso = end_date.strftime('%Y-%m-%d')
            #print(start_date,end_date)

            # Retrieve stock data for the given ticker and date range using the mock function
            fn_name='historical data'
            fdate_iso = start_date.isoformat()[:10] + 'T09:30:00.000Z'
            tdate_iso = end_date.isoformat()[:10] + 'T15:30:00.000Z'
            try:

                stock_data_df=bzins_con.secon(ses_tok,fn_name,start_date=fdate_iso,end_date=tdate_iso,stock_code=ticker,exchange_code=exchange)
                stock_data_df['quantity'] = balance 
                # Calculate investment for each date and close price
                stock_data_df['investment'] = stock_data_df['close'] * balance 
                #stock_data_df['stock_code'] = ticker  # Add the stock_code column
           
                # Write the stock data to a new sheet named after the stock code
            
                #stock_data_df.to_excel(writer, sheet_name=ticker + '_inv', index=False, if_sheet_exists='replace')

                # Write the stock data to a new sheet named after the stock code
                stock_data_df.to_excel(writer, sheet_name=ticker + '_inv', index=False)
            except Exception as e:
                # Code to handle the exception
                print("An error occurred:", str(e))
                continue

def pick_file():
    # Specify the directory where the files are located
    directory = '.'
    # Specify the pattern to match the filename
    pattern = '*_trade_report.xlsx'
    # Get a list of files that match the pattern
    files = glob.glob(os.path.join(pattern))
    # Specify the pattern to match the filename
    pattern = '*_trade_report.xlsx'
    # Sort the files based on the datetime in the filename
    sorted_files = sorted(files, key=lambda x: datetime.strptime(os.path.basename(x).split('_')[0]+"_"+os.path.basename(x).split('_')[1], '%Y-%m-%d_%H-%M-%S'))
    # Get the latest file
    latest_file = sorted_files[-1]
    return latest_file

session_token = '49166619'
latest_file = pick_file()
process_stock_data_from_excel(latest_file, session_token)
