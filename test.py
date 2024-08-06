import csv

input_file = './data/raw/steam_games.csv'

max_columns = 0
with open(input_file, 'r', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    for row in reader:
        if len(row) > max_columns:
            max_columns = len(row)

print(f"Maximum number of columns found: {max_columns}")
