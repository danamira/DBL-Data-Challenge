import mysql.connector
import JsonHandler
import database.connect
from time import process_time
import datetime
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

def insert_tweets(connection: mysql.connector.connect, dataFiles: List[Path],silent=True) -> None:
    """
    Insert tweets into the database.

    :param connection: Connection to the database
    :param dataFiles: List of JSON files
    :return: None
    """
    acc_time=0
    for counter,file_path in enumerate(dataFiles):
        print("ℹ️ Processing: ",file_path)
        t_start = process_time() 
        data_set = JsonHandler.json_object_reader(file_path)
        errorCounter=0
        try:
            for tweet in data_set:
                try:
                    cleaned_tweet = JsonHandler.json_cleaner(tweet)
                    if cleaned_tweet is None:
                        continue
                    # values = tuple(cleaned_tweet.values())
                    mydict = cleaned_tweet
            
                    columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in mydict.keys())
                    # values = ', '.join()
                    dictkeys=list(mydict.keys())
                    dictvalues=list(mydict.values())
                    values=""
                    for i,j in enumerate(dictvalues):
                        j=str(j)
                        j=j.replace("/","_")
                        j=j.replace("'","")
                        if(dictkeys[i] in ["text","coordinates","language","airlines","mentions"]):
                            j="'"+j+"'"
                        values+=j
                        if(i!=(len(dictvalues)-1)):
                            values+=','
                    
                    insertQuery = "INSERT INTO `tweets` ( %s ) VALUES ( %s )" % (columns, values)
                    exec = connection.cursor().execute(insertQuery)
                    if not silent:
                        print("✅ Record added successfully.")
                except mysql.connector.Error as err:
                    if not silent:
                        print(f"⚠️ Error while adding record: {err}")
                    errorCounter+=1
                    pass
                except Exception as e:
                    if not silent:
                        print("⚠️ Weird record:", e)
                    errorCounter+=1
                    pass
            connection.commit()
            processedFiles=counter+1
            if(errorCounter==0):
                print(f"✅ `{file_path}` content was successfully appended to tweets table.")
            else:
                print(f"⚠️ `{file_path}` content was processed. {errorCounter} exceptions ignored.")
            t_end=process_time()
            t_diff= t_end - t_start
            acc_time+=t_diff
            time_remaining=(len(dataFiles)-processedFiles)*(acc_time/processedFiles)
            print("📄 {}/{} files are processed. {} done. ⌚ ~Time remaining : {}".format(processedFiles,len(dataFiles),round(processedFiles/len(dataFiles),2),str(datetime.timedelta(seconds=time_remaining))))
        except Exception as e:
            print(e)
            print("⚠️ Bad file!")

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
    print("✅ Tables dropped successfully.")

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
