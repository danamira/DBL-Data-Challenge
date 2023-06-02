import sys
import DB_fun
import JsonHandler
from pathlib import Path
from database.connect import getConnection
import os


dataFiles = [Path("data/"+file) for file in os.listdir('data')]

    

try:
    connection = getConnection()
except Exception:
    print("✖️ Error while connecting to MySQL engine database.")
    print("ℹ️ Please make sure the environment file `.env` is located at"+
        "the project root directory and contains proper configuration.")
    raise

if (len(sys.argv) <= 1):
    print("ℹ️ Use one of the following commands:")
    print("1. `python main.py make:tables` | create the tweets table.")
    print(
        "2. `python main.py insert:tweets` | insert JSON object tweets as record in the MySQL database. Configure `dataFiles` variables before using.")
    quit()

command = sys.argv[1]

silent=False
if(len(sys.argv)>=3):
    if(sys.argv[2]=='--silent'):
        silent=True
if (command == 'make:tables'):
    DB_fun.make_tables(connection)
if(command=="count:tweets"):
    DB_fun.count_tweets(connection,dataFiles,silent)
if (command == 'insert:tweets'):
    DB_fun.insert_tweets(connection, dataFiles, silent=silent)
if command == 'check:connection':
    DB_fun.connection_valid(connection)
if command=="drop:tables":
    DB_fun.drop_tables(connection)
if command=="reset:tables":
    DB_fun.drop_tables(connection)
    DB_fun.make_tables(connection)
