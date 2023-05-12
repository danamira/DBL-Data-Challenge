import mysql.connector
import JsonHandler
import database.connect


def make_tables(connection):
    try:
        connection.cursor().execute(database.connect.makeTablesQuery())
        print('✅ Tweets table created successfully.')
    except mysql.connector.Error as err:
        print(f"Error while creating tweets table: {err}")
        raise

def insert_tweets(connection, dataFiles):
    for file_path in dataFiles:
        print("ℹ️ Processing: ",file_path)
        data_set = JsonHandler.json_file_reader(file_path)
        for tweet in data_set:
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
                print(f"⚠️ Error while adding record: {err}")
                # print('Tweet object id: ',tweet['id'])
                # print("Tried to execute: ", insertQuery)
        connection.commit()
        print(f"✅ `{file_path}` content was successfully appended to tweets table.")

def connection_valid(connection):
    print("✅ The connection seems to be valid:", connection)

def drop_tables(connection):
    sql="DROP TABLE tweets"
    connection.cursor().execute(sql)
    connection.commit()

def count_tweets(connection, dataFiles):
    counter=0
    for filePath in dataFiles:
        print('ℹ️ Processing: ',filePath)
        with open(filePath) as f:
            for line in f:
                if line[0:8]!="Exceeded":
                    counter+=1                    
    print("💡 total number of tweet objects: ",counter)
