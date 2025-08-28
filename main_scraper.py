# main_scraper.py

# First, we are importing some tools that Python needs to work.
# 'requests' helps us talk to the internet (like our API).
# 'pandas' is great for organizing data into tables.
# 'gspread' is a special tool to talk to Google Sheets.
# 'os' helps us read secret keys, and 'logging' prints messages for us.
import os
import requests
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import logging
import json

# --- Configuration Section ---
# Here, we will tell our script what to search for and where to find our secret keys.

# Set up simple messages so we can see what the robot is doing.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# TODO: IMPORTANT!
# You will set these secret keys in the final step right before running the script.
# For now, the script knows to look for them.
SERPAPI_KEY = "API_KEY"
GOOGLE_SHEET_ID = "GOOGLE_SHEET_ID"
GOOGLE_CREDENTIALS_FILE = 'google_creds.json' # This is the secret key file for Google.

# What do you want to search for? Change this to anything you want!

businesstype = input("Enter Business Type: ")
businesslocation = input("Enter Location: ")


SEARCH_QUERY = f"{businesstype} in {businesslocation}"

# --- Google Sheets Functions ---

# This function connects to our Google account using the secret key file.
def get_gspread_client():
    logging.info("Connecting to Google Sheets...")
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file(GOOGLE_CREDENTIALS_FILE, scopes=scopes)
    client = gspread.authorize(creds)
    logging.info("Successfully connected to Google!")
    return client

# This function opens our specific spreadsheet.
def get_worksheet(client, sheet_id):
    spreadsheet = client.open_by_key(sheet_id)
    worksheet = spreadsheet.sheet1 # This gets the very first sheet in the file.
    # Let's write the titles for our columns if the sheet is empty.
    if worksheet.cell(1, 1).value is None:
        headers = ["Name", "Category", "Address", "Rating", "Reviews Count", "Phone", "Website"]
        worksheet.append_row(headers)
        logging.info("Added headers to the empty sheet.")
    return worksheet

# --- Data Fetching Function ---

# This function asks our "magic librarian" (SerpApi) for the business info.
def fetch_google_maps_data(api_key, query):
    logging.info(f"Asking Api for: '{query}'...")
    params = {
        "engine": "google_local",
        "q": query,
        "api_key": api_key,
        "num" : "10"
    }
    response = requests.get("https://serpapi.com/search", params=params)
    # The API sends back a big block of data. We just want the "local_results".
    return response.json().get("local_results", [])

# --- Main Robot Logic ---

def main():
    logging.info("🤖 Robot is starting its job!")

    # 1. Fetch the new data from the API
    raw_data = fetch_google_maps_data(SERPAPI_KEY, SEARCH_QUERY)
    if not raw_data:
        logging.warning("The API didn't find any businesses. Stopping.")
        return

    logging.info(f"Found {len(raw_data)} businesses from the API.")
    
    # Let's organize the data we got from the API.
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

    # Put our list into a neat table using the pandas tool.
    new_data_df = pd.DataFrame(new_businesses)

    # 2. Connect to Google Sheets and get the data that's already there.
    try:
        gspread_client = get_gspread_client()
        worksheet = get_worksheet(gspread_client, GOOGLE_SHEET_ID)
        existing_records = worksheet.get_all_records()
        existing_df = pd.DataFrame(existing_records)
        logging.info(f"Found {len(existing_df)} businesses already in the sheet.")
    except Exception as e:
        logging.error(f"Could not talk to Google Sheets! Error: {e}")
        return

    # 3. Find businesses that are NOT already in our sheet (no duplicates!)
    if not existing_df.empty:
        # We'll merge the two lists and then drop any duplicates based on Name and Address.
        combined_df = pd.concat([existing_df, new_data_df])
        unique_df = combined_df.drop_duplicates(subset=['Name', 'Address'], keep='first')
        # Figure out which rows are the truly new ones.
        final_new_rows = unique_df.tail(len(unique_df) - len(existing_df))
    else:
        # If the sheet was empty, all businesses are new.
        final_new_rows = new_data_df

    # 4. Add the new, unique businesses to our sheet.
    if not final_new_rows.empty:
        logging.info(f"Adding {len(final_new_rows)} new unique businesses to the sheet...")
        # gspread needs a list of lists to add rows, so we convert our table.
        rows_to_append = final_new_rows.values.tolist()
        worksheet.append_rows(rows_to_append, value_input_option='USER_ENTERED')
        logging.info("Successfully added the new businesses!")
    else:
        logging.info("No new businesses to add. Everything is up to date!")

    logging.info("✅ Robot has finished the job!")

# This line makes the script run when you execute the file.
if __name__ == "__main__":
    main()