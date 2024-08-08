import requests
import sqlite3
import time
import os
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

API_KEY = os.getenv('STEAM_API_KEY')
BASE_URL = 'http://api.steampowered.com/ISteamApps/GetAppList/v2/'
DETAILS_URL = 'https://store.steampowered.com/api/appdetails'
MAX_RETRIES = 2
RATE_LIMIT = 1  # requests per second
BATCH_SIZE = 100  # Save progress in batches
MAX_WORKERS = 5  # Number of concurrent threads

def setup_logging():
    logging.basicConfig(
        filename='fetch_data.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger()

logger = setup_logging()

def fetch_app_list():
    logger.info("Fetching app list...")
    response = requests.get(BASE_URL)
    response.raise_for_status()
    app_list = response.json()['applist']['apps']
    logger.info(f"Fetched {len(app_list)} apps.")
    return app_list

def fetch_app_details(appid):
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(DETAILS_URL, params={'appids': appid})
            if response.status_code == 429:  # Too Many Requests
                logger.warning(f"Rate limit exceeded for appid {appid}. Retrying after delay.")
                time.sleep(30)  # wait 30 seconds before retrying
                continue
            response.raise_for_status()
            data = response.json()
            if data and str(appid) in data and data[str(appid)]['success']:
                details = data[str(appid)]['data']
                game_data = {
                    'appid': appid,
                    'name': details.get('name'),
                    'description': details.get('short_description'),
                    'price': details.get('price_overview', {}).get('final_formatted', 'N/A'),
                    'release_date': details.get('release_date', {}).get('date', 'N/A'),
                    'developer': details.get('developers', ['N/A'])[0],
                    'publisher': details.get('publishers', ['N/A'])[0],
                    'tags': ', '.join([genre['description'] for genre in details.get('genres', [])])
                }
                return game_data
            else:
                logger.warning(f"Failed to fetch game details for appid: {appid}")
                return None
        except requests.RequestException as e:
            logger.warning(f"Attempt {attempt + 1} failed for appid {appid}: {str(e)}")
            time.sleep(2 ** attempt)  # Exponential backoff
    return None

def fetch_app_reviews(appid, num_reviews=100):
    try:
        url = f"https://store.steampowered.com/appreviews/{appid}?json=1&num_per_page={num_reviews}"
        response = requests.get(url)
        data = response.json()
        if 'reviews' in data:
            reviews = data['reviews']
            review_entries = []
            for review in reviews:
                review_data = {
                    'appid': appid,
                    'review_text': review['review'],
                    'voted_up': review['voted_up'],
                    'timestamp_created': review['timestamp_created'],
                    'author_playtime_forever': review['author']['playtime_forever'],
                    'author_playtime_last_two_weeks': review['author']['playtime_last_two_weeks'],
                    'author_num_reviews': review['author']['num_reviews']
                }
                review_entries.append(review_data)
            return review_entries
        else:
            logger.warning(f"Failed to fetch reviews for appid: {appid}")
            return []
    except Exception as e:
        logger.error(f"Error fetching reviews for appid: {appid} - {e}")
        return []

def save_game_details_to_db(game_data):
    conn = sqlite3.connect('steam_games.db')
    c = conn.cursor()
    try:
        c.execute('''
            INSERT OR IGNORE INTO game_details (appid, name, description, price, release_date, developer, publisher, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (game_data['appid'], game_data['name'], game_data['description'], game_data['price'], 
              game_data['release_date'], game_data['developer'], game_data['publisher'], game_data['tags']))
        conn.commit()
    except sqlite3.OperationalError as e:
        logger.error(f"Error inserting game details for appid {game_data['appid']}: {e}")
    finally:
        conn.close()

def save_reviews_to_db(reviews):
    conn = sqlite3.connect('steam_games.db')
    c = conn.cursor()
    try:
        for review in reviews:
            c.execute('''
                INSERT INTO game_reviews (appid, review_text, voted_up, timestamp_created, author_playtime_forever, author_playtime_last_two_weeks, author_num_reviews)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (review['appid'], review['review_text'], review['voted_up'], review['timestamp_created'],
                  review['author_playtime_forever'], review['author_playtime_last_two_weeks'], review['author_num_reviews']))
        conn.commit()
    except sqlite3.OperationalError as e:
        logger.error(f"Error inserting review for appid {reviews[0]['appid']}: {e}")
    finally:
        conn.close()

def fetch_data(appid):
    game_data = fetch_app_details(appid)
    if game_data:
        save_game_details_to_db(game_data)
        reviews = fetch_app_reviews(appid, num_reviews=100)
        if reviews:
            save_reviews_to_db(reviews)
        return game_data
    else:
        return None

def main():
    setup_logging()
    app_list = fetch_app_list()
    total_apps = len(app_list)

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(fetch_data, app['appid']): app['appid'] for app in app_list[:5000]}  # Limiting to 5000 apps for the sake of example
        with tqdm(total=len(futures)) as pbar:
            for future in as_completed(futures):
                appid = futures[future]
                try:
                    future.result()
                    logger.info(f"Fetched details for appid: {appid}")
                except Exception as e:
                    logger.warning(f"Failed to fetch details for appid: {appid} - {e}")
                # Update progress bar
                pbar.update(1)
                # Rate limiting
                time.sleep(1 / RATE_LIMIT)

    logger.info(f"Data collection complete.")

if __name__ == '__main__':
    main()
