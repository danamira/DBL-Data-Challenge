import sys

import mysql.connector
import JsonHandler
import database.connect
from database.connect import getConnection

dataFiles = ['data/airlines-1558527599826.json']

try:
    connection = getConnection()
except Exception:
    print("✖️ Error while connecting to MySQL engine database.")
    print(
        "ℹ️ Please make sure the environment file `.env` is located at the project root directory and contains proper configuration.")
    sys.exit(1)
    quit()

if (len(sys.argv) <= 1):
    print("ℹ️ Use one of the following commands:")
    print("1. `python main.py make:tables` | create the tweets table.")
    print(
        "2. `python main.py insert:records` | insert JSON object tweets as record in the MySQL database. Configure `dataFiles` variables before using.")
    quit()
command = sys.argv[1]
if (command == 'make:tables'):
    try:
        connection.cursor().execute(database.connect.makeTablesQuery())
        print('✅ Tweets table created successfully.')
    except mysql.connector.Error as err:
        print("Error while creating tweets table: {}".format(err))
        exit(1)
if (command == 'insert:tweets'):
    for filePath in dataFiles:
        for tweet in JsonHandler.json_file_reader(filePath):
            insertQuery = "INSERT INTO `tweets` (`id`, `text`, `in_reply_to`, `timestamp`, `user_mentions`, `user_id`, `user_verified`, `user_followers_count`, `user_tweets_count`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            try:
                if "id" in tweet:
                    exec = connection.cursor().execute(insertQuery, (tweet['id'], tweet['text'], (
                        'NULL' if tweet['in_reply_to_status_id'] is None else tweet['in_reply_to_status_id']),
                                                                     tweet['timestamp_ms'],
                                                                     str(tweet['entities']['user_mentions']),
                                                                     tweet['user']['id'],
                                                                     int(tweet['user']['verified']),
                                                                     tweet['user']['followers_count'],
                                                                     tweet['user']['statuses_count']))

                else:
                    print("⚠️ Weird record:", tweet)
            except mysql.connector.Error as err:
                print("✖️ Error while adding record: {}".format(err))
                print("Tried to execute: ", insertQuery)
                exit(1)
        connection.commit()
        print('✅ `{}` content was successfully appended to tweets table.'.format(filePath))

if command == 'check:connection':
    print("✅ The connection seems to be valid:", connection)
