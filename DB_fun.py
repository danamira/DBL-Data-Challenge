import mysql.connector
import JsonHandler
import database.connect
from typing import List
from pathlib import Path


def make_tables(connection: mysql.connector.connect) -> None:
    """
    Create tables in the database.

    :param connection: Connection to the database
    :return: None
    """
    try:
        connection.cursor().execute(database.connect.makeTablesQuery())
        print('✅ Tweets table created successfully.')
    except mysql.connector.Error as err:
        print(f"Error while creating tweets table: {err}")
        raise

def insert_tweets(connection: mysql.connector.connect, dataFiles: List[Path]) -> None:
    """
    Insert tweets into the database.

    :param connection: Connection to the database
    :param dataFiles: List of JSON files
    :return: None
    """
    # gets the keys of the first tweet object
    first_data = JsonHandler.json_object_reader(dataFiles[0])
    first_tweet = first_data.__next__()
    cleaned_first_tweet = JsonHandler.json_cleaner(first_tweet)
    keys = tuple(cleaned_first_tweet.keys())

    for file_path in dataFiles:
        print("ℹ️ Processing: ",file_path)
        data_set = JsonHandler.json_object_reader(file_path)
        for tweet in data_set:
            #print(tweet)
            try:
                cleaned_tweet = JsonHandler.json_cleaner(tweet)
                values = tuple(cleaned_tweet.values())
                
                mydict = cleaned_tweet


                columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in mydict.keys())
                values = ', '.join("'" + str(x).replace('/', '_').replace("'", "") + "'" for x in mydict.values())  
                insertQuery = "INSERT INTO `tweets` ( %s ) VALUES ( %s )" % (columns, values)

                if "id" in tweet:
                    exec = connection.cursor().execute(insertQuery)
                    print("✅ Record added successfully.")
                else:
                    print("⚠️ Weird record:", tweet)
            except mysql.connector.Error as err:
                print(f"⚠️ Error while adding record: {err}")
                # print('Tweet object id: ',tweet['id'])
                # print("Tried to execute: ", insertQuery)
                pass
            except Exception as e:
                print("⚠️ Weird record:", tweet)
                print(e)
                pass
        connection.commit()
        print(f"✅ `{file_path}` content was successfully appended to tweets table.")

def connection_valid(connection: mysql.connector.connect) -> None:
    """
    Check if the connection to the database is valid.

    :param connection: Connection to the database
    :return: None
    """
    print("✅ The connection seems to be valid:", connection)

def drop_tables(connection: mysql.connector.connect) -> None:
    """
    Drop tables in the database.

    :param connection: Connection to the database
    :return: None
    """
    sql="DROP TABLE tweets"
    connection.cursor().execute(sql)
    connection.commit()

def count_tweets(connection: mysql.connector.connect, dataFiles: List[Path]) -> None:
    """
    Count the number of tweets in the database.

    :param connection: Connection to the database
    :param dataFiles: List of JSON files
    :return: None
    """
    counter=0
    for filePath in dataFiles:
        print('ℹ️ Processing: ',filePath)
        with open(filePath) as f:
            for line in f:
                if line[0:8]!="Exceeded":
                    counter+=1                    
    print("💡 total number of tweet objects: ",counter)
