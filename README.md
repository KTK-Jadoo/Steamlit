# Steamlit

### Steam Games Data Fetcher (fetch_data.py)

This script fetches details and reviews for games listed on Steam. It uses the Steam API to retrieve the data, and it can handle large datasets efficiently by using concurrency and batch processing. The script also maintains logs and keeps track of processed and failed app IDs to resume from where it left off in case of interruptions.

#### Logging

Logs are saved to fetch_data.log by default. The log file records information about the progress, errors, and other significant events during the script execution.
Data Output

The fetched game details are saved in CSV format in the data/raw directory. The script appends new data to the existing CSV file if it exists.
Resuming Progress

The script keeps track of processed and failed app IDs in processed_ids. If the script is interrupted, it can resume from where it left off by reloading these IDs.

#### Data Collected

The script collects the following data points for each game:
Game Details:

    App ID: Unique identifier for the game.
    Name: The name of the game.
    Description: Short description of the game.
    Price: The current price of the game.
    Release Date: The release date of the game.
    Developer: The developer(s) of the game.
    Publisher: The publisher(s) of the game.
    Tags/Genres: Tags or genres associated with the game.

User Reviews:

    Review Text: The content of the user review.
    Voted Up: Indicates if the review is positive (True) or negative (False).
    Timestamp Created: The date when the review was posted.
    Author Playtime Forever: Total playtime of the reviewer for the game.
    Author Playtime Last Two Weeks: Playtime of the reviewer in the last two weeks.
    Author Number of Reviews: Total number of reviews written by the reviewer.
