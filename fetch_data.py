import requests
import pandas as pd
import time

API_KEY = 'B5F1E66A3283C04D18D6E917C7BAD776'
BASE_URL = 'http://api.steampowered.com/ISteamApps/GetAppList/v2/'
DETAILS_URL = 'https://store.steampowered.com/api/appdetails'

def fetch_app_list():
    response = requests.get(BASE_URL)
    app_list = response.json()['applist']['apps']
    return app_list

def fetch_app_details(appid):
    response = requests.get(DETAILS_URL, params={'appids': appid})
    data = response.json()
    if data and str(appid) in data and data[str(appid)]['success']:
        return data[str(appid)]['data']
    return None

def main():
    app_list = fetch_app_list()
    print(f"Total apps fetched: {len(app_list)}")

    app_details_list = []

    for app in app_list[:100]:  # Limiting to 100 apps for the sake of example
        appid = app['appid']
        app_details = fetch_app_details(appid)
        if app_details:
            app_details_list.append(app_details)
            print(f"Fetched details for appid: {appid}")
        time.sleep(1)  # Sleep to avoid hitting the API rate limit

    df = pd.DataFrame(app_details_list)
    df.to_csv('steam_games.csv', index=False)
    print("Data saved to steam_games.csv")

if __name__ == '__main__':
    main()
