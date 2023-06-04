from pathlib import Path
import os

import DB_fun
from database.connect import getConnection

# Hello, my
name = 'dana'
# Congratulations on your purchase of the group 6 tweet database system.
# This system is designed to help you find tweets that are relevant to your airline.
# Before we get started please ensure you have done the following:
# 1. Installed the required packages (see requirements.txt)
# 2. Just done all that stuff in the README, if theres a problem there ask Dana not me.
# 3. Have all the JSON tweet files in the data folder.
# 4. Ensure there is nothing else in the data folder.
# 5. I fucking mean it
# 6. Ensure that the tweets table on your server is empty.
# 6a. If its not (eg it has column names present) click the database name.
# 6b. Click operations from the top ribbon.
# 6c. Then scrol alll  the way down.
# 6d. Click `Delete the table (DROP)`
# 6e. Yes you are sure.

# 6. Now uncomment your name from the list below!

# name = 'andrew'
# name = 'oscar'
# name = 'dani'
# name = 'alicia'
# name = 'dillon'
# name = 'dana'

# 7. Thats it! press the little play button in the top right to run the code.
# 8. If any errors occur, stop that, bad pc.
# 9. If no errors occur, relax, sit back, and be sure to do something productive.



# I tried to be fancy but gave up.
if name == 'andrew':
    lines = [0, 95]
elif name == 'oscar':
    lines = [95, 190]
elif name == 'dani':
    lines = [190, 285]
elif name == 'alicia':
    lines = [285, 380]
elif name == 'dillon':
    lines = [380, 475]
elif name == 'dana':
    lines = [475, 567]

# create a list of the files to be read
files = []
with open('filenames.txt') as file:
    for i, line in enumerate(file):
        if lines[0] <= i < lines[1]:
            files.append(line.strip())



dataFiles = [Path("data/"+file) for file in os.listdir('data') if file in files]

    

try:
    connection = getConnection()
except Exception:
    print("✖️ Error while connecting to MySQL engine database.")
    print("ℹ️ Please make sure the environment file `.env` is located at"+
        "the project root directory and contains proper configuration.")
    raise

DB_fun.make_tables(connection)
DB_fun.insert_tweets(connection, dataFiles, silent=True)
