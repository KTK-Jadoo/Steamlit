import requests
import pandas as pd
import time
import os
import logging

API_KEY = 'YOUR_STEAM_API_KEY'
BASE_URL = 'http://api.steampowered.com/ISteamApps/GetAppList/v2/'
DETAILS_URL = 'https://store.steampowered.com/api/appdetails'
PROCESSED_IDS_FILE = 'processed_ids.txt'
FAILED_IDS_FILE = 'failed_ids.txt'
OUTPUT_DIR = 'data/raw'
OUTPUT_FILE = f'{OUTPUT_DIR}/steam_games.csv'
MAX_RETRIES = 2
RATE_LIMIT = 1  # requests per second

def setup_logging():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    logging.basicConfig(
        filename=f'{OUTPUT_DIR}/fetch_data.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def fetch_app_list():
    logging.info("Fetching app list...")
    response = requests.get(BASE_URL)
    response.raise_for_status()
    app_list = response.json()['applist']['apps']
    logging.info(f"Fetched {len(app_list)} apps.")
    return app_list

def fetch_app_details(appid):
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(DETAILS_URL, params={'appids': appid})
            if response.status_code == 429:  # Too Many Requests
                logging.warning(f"Rate limit exceeded for appid {appid}. Retrying after delay.")
                time.sleep(30)  # wait 30 seconds before retrying
                continue
            response.raise_for_status()
            data = response.json()
            if data and str(appid) in data and data[str(appid)]['success']:
                return data[str(appid)]['data']
        except requests.RequestException as e:
            logging.warning(f"Attempt {attempt + 1} failed for appid {appid}: {str(e)}")
            time.sleep(2 ** attempt)  # Exponential backoff
    return None

def load_ids(filename):
    if os.path.exists(filename):
        try:
            df = pd.read_csv(filename, header=None, dtype=int)
            return set(df[0])  # Assuming the IDs are in the first column
        except pd.errors.EmptyDataError:
            return set()
    return set()

def save_ids(ids, filename):
    pd.Series(list(ids)).to_csv(filename, index=False, header=False)

def save_entry_to_csv(entry_df, output_file):
    if os.path.exists(output_file):
        entry_df.to_csv(output_file, mode='a', header=False, index=False)
    else:
        entry_df.to_csv(output_file, index=False)

def main():
    setup_logging()
    app_list = fetch_app_list()
    total_apps = len(app_list)
    processed_ids = load_ids(PROCESSED_IDS_FILE)
    failed_ids = load_ids(FAILED_IDS_FILE)
    
    logging.info(f"Continuing from previous run. {len(processed_ids)} apps already processed.")
    print(f"Continuing from previous run. {len(processed_ids)} apps already processed.")
    
    app_list = [app for app in app_list if app['appid'] not in processed_ids | failed_ids]
    
    for app in app_list[:5000]:  # Limiting to 500 apps for the sake of example
        appid = app['appid']
        app_details = fetch_app_details(appid)
        
        if app_details:
            save_entry_to_csv(pd.json_normalize(app_details), OUTPUT_FILE)
            processed_ids.add(appid)
            logging.info(f"Fetched details for appid: {appid}")
        else:
            failed_ids.add(appid)
            logging.warning(f"Failed to fetch details for appid: {appid}")
        
        # Log and save progress after every 100 apps
        if len(processed_ids) % 10 == 0:
            logging.info(f"Progress update: {len(processed_ids)}/{total_apps} records processed")
            save_ids(processed_ids, PROCESSED_IDS_FILE)
            save_ids(failed_ids, FAILED_IDS_FILE)
        
        # Rate limiting
        time.sleep(1 / RATE_LIMIT)

    logging.info(f"Data saved to {OUTPUT_FILE}")
    save_ids(processed_ids, PROCESSED_IDS_FILE)
    save_ids(failed_ids, FAILED_IDS_FILE)

if __name__ == '__main__':
    main()
