
import os
import requests
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import logging
import json


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


SERPAPI_KEY = "API_KEY"
GOOGLE_SHEET_ID = "GOOGLE_SHEET_ID"
GOOGLE_CREDENTIALS_FILE = 'google_creds.json' 



businesstype = input("Enter Business Type: ")
businesslocation = input("Enter Location: ")


SEARCH_QUERY = f"{businesstype} in {businesslocation}"


def get_gspread_client():
    logging.info("Connecting to Google Sheets...")
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file(GOOGLE_CREDENTIALS_FILE, scopes=scopes)
    client = gspread.authorize(creds)
    logging.info("Successfully connected to Google!")
    return client


def get_worksheet(client, sheet_id):
    spreadsheet = client.open_by_key(sheet_id)
    worksheet = spreadsheet.sheet1 
    if worksheet.cell(1, 1).value is None:
        headers = ["Name", "Category", "Address", "Rating", "Reviews Count", "Phone", "Website"]
        worksheet.append_row(headers)
        logging.info("Added headers to the empty sheet.")
    return worksheet



def fetch_google_maps_data(api_key, query):
    logging.info(f"Asking Api for: '{query}'...")
    params = {
        "engine": "google_local",
        "q": query,
        "api_key": api_key,
        "num" : "10"
    }
    response = requests.get("https://serpapi.com/search", params=params)
    
    return response.json().get("local_results", [])


def main():
    logging.info("🤖 Robot is starting its job!")

    raw_data = fetch_google_maps_data(SERPAPI_KEY, SEARCH_QUERY)
    if not raw_data:
        logging.warning("The API didn't find any businesses. Stopping.")
        return

    logging.info(f"Found {len(raw_data)} businesses from the API.")
    
    
    new_businesses = []
    for item in raw_data:
        new_businesses.append({
            "Name": item.get("title"),
            "Category": item.get("type"),
            "Address": item.get("address"),
            "Rating": item.get("rating"),
            "Reviews Count": item.get("reviews"),
            "Phone": item.get("phone"),
            "Website": item.get("website"),
        })

    
    new_data_df = pd.DataFrame(new_businesses)

    
    try:
        gspread_client = get_gspread_client()
        worksheet = get_worksheet(gspread_client, GOOGLE_SHEET_ID)
        existing_records = worksheet.get_all_records()
        existing_df = pd.DataFrame(existing_records)
        logging.info(f"Found {len(existing_df)} businesses already in the sheet.")
    except Exception as e:
        logging.error(f"Could not talk to Google Sheets! Error: {e}")
        return

    if not existing_df.empty:
        
        combined_df = pd.concat([existing_df, new_data_df])
        unique_df = combined_df.drop_duplicates(subset=['Name', 'Address'], keep='first')
        
        final_new_rows = unique_df.tail(len(unique_df) - len(existing_df))
    else:
        
        final_new_rows = new_data_df

    
    if not final_new_rows.empty:
        logging.info(f"Adding {len(final_new_rows)} new unique businesses to the sheet...")
        
        rows_to_append = final_new_rows.values.tolist()
        worksheet.append_rows(rows_to_append, value_input_option='USER_ENTERED')
        logging.info("Successfully added the new businesses!")
    else:
        logging.info("No new businesses to add. Everything is up to date!")

    logging.info("✅ Robot has finished the job!")


if __name__ == "__main__":

    main()
