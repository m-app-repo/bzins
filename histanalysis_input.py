import pandas as pd
from openpyxl import load_workbook
import glob
import os
from datetime import datetime

def process_excel(filename):
    """
    Processes the Excel file with stock data, creating or updating a Master sheet while retaining other sheets.

    Args:
        filename (str): The path to the Excel file.
    """

    def create_master_sheet(df):
        """
        Creates the Master sheet with calculated values based on stock_code and trade_date.

        Args:
            df (pd.DataFrame): The DataFrame containing the stock data.

        Returns:
            pd.DataFrame: The DataFrame representing the Master sheet.
        """
        
        df = df.sort_values(by=["stock_code", "trade_date","exchange_code"], ascending=True)
        master_rows = []
        for i in range(len(df)):
            current_row = df.iloc[i]
            next_row = df.iloc[i + 1] if i + 1 < len(df) else None
            prev_row=df.iloc[i-1] if i-1 > 0 else None

            stock_code = current_row["stock_code"]
            exchange_code = current_row["exchange_code"]
            trade_date = current_row["trade_date"]
            action = current_row["action"]
            quantity = current_row["quantity"]

            # Determine to_date based on the next row
            #if next_row is not None and next_row["stock_code"] == stock_code and next_row["exchange_code"] == exchange_code:
            if next_row is not None and next_row["stock_code"] == stock_code:
                to_date = next_row["trade_date"]
            else:
                to_date = None

            # Calculate balance
            #if i == 0 or (prev_row is not None and prev_row["stock_code"] != stock_code) or (prev_row is not None and prev_row["stock_code"] == stock_code and prev_row["exchange_code"] != exchange_code):
            if i == 0 or (prev_row is not None and prev_row["stock_code"] != stock_code):
                current_balance = 0
            if action == "Buy":
                current_balance += quantity
            elif action == "Sell":
                current_balance -= quantity
            new_row = {
                "stock_code": stock_code,
                "exchange_code": exchange_code,
                "from_date": trade_date,
                "to_date": to_date,
                "balance": current_balance
            }
            master_rows.append(new_row)
        


        master_df = pd.DataFrame(master_rows, columns=["stock_code", "exchange_code", "from_date", "to_date", "balance"])
       
        return master_df



    def save_to_excel(all_sheets, master_df, filename):
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            master_df.to_excel(writer, sheet_name="Master", index=False)

            # Write other sheets, excluding the one processed into Master
            for sheet_name, data in all_sheets.items():
                if sheet_name != 'Master':  # Assuming 'Sheet1' is processed into Master
                    data.to_excel(writer, sheet_name=sheet_name, index=False)



    # Load all sheets from the Excel file without specifying engine
    all_sheets = pd.read_excel(filename, sheet_name=None)

    # Process the specific sheet for Master data
    master_df = create_master_sheet(all_sheets['Transactions'])

    # Save all sheets back to the file
    save_to_excel(all_sheets, master_df, filename)

    return pd.read_excel(filename, sheet_name="Master")

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

latest_file = pick_file()
processed_master_df = process_excel(latest_file)



