# --------------------------------------------------------
# FUNCTIONS FOR reply_time4.ipynb Jupyter Notebook
# Author: Alicia Larsen
# Data of creation: 2023-06-18
# --------------------------------------------------------

# IMPORTS
import sys
import DB_fun
import JsonHandler
from pathlib import Path
from database.connect import getConnection
import os
import pandas as pd


def reply_set_up():
    """
    Initiates connection and cursor, queries the relevand data, and returns a dataframe.
    :returns: a dataframe with columns: [airline, reply_time, sentiment_change]
    """
    # Initialize the connection
    connection = getConnection()
    cursor = connection.cursor()
    
    # Select conversations where airlines participated, airline
    # get the reply time of the breakpoint (airline), reply_time
    # calculate the sentiment change between 'before-and-after' airline reply, sentiment_change
    # (and, gets topic) 
    query = """
    SELECT
        break.break_airline as airline, 
        tweets.reply_time/(1000*60*60) as reply_time, 
        (sentiment.sentiment_sum - break.sentiment_sum) as sentiment_change
    FROM 
        tweets, 
	    (SELECT break_id, break_airline, sentiment_sum, cID, bin_position 
            FROM binned_sentiment 
            WHERE break_id != '0' as break,
	    (SELECT sentiment_sum, cID, bin_position 
            FROM binned_sentiment 
            WHERE break_id != '0' as sentiment
    WHERE tweets.id = break.break_id and
        sentiment.cID = break.cID and
        sentiment.bin_position = (break.bin_position + 1)
    """
    
    # Query data and store as a dataframe
    cursor.execute(query) 
    df_tweets = pd.DataFrame(cursor.fetchall())

    # Close connection
    cursor.close()
    connection.close()

    return df_tweets




def reply_time():
    """
    Calculates the reply time of an airline in a conversation
    """
    pass



def sentiment_change():
    """
    Retrieves the sentiment change between the bins, before and after the airline response.
    """
    pass