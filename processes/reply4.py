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
    SELECT DISTINCT
	break.break_airline AS airline, 
	tweets.reply_time/(1000*60*60) AS reply_time, 
	(sentiment.sentiment_mean - break.sentiment_mean) AS sentiment_change,
	topics.canceling,
	topics.boarding,
	topics.stuck,
	topics.booking,
	topics.customers,
	topics.dm,
	topics.waiting,
	topics.money,
	topics.information,
	topics.staff,
	topics.baggage
    FROM 
        tweets, 
        (SELECT break_id, break_airline, sentiment_sum/tweet_count as sentiment_mean, cID, bin_position 
            FROM binned_sentiment 
            WHERE break_id != '0')
            AS break,
        (SELECT sentiment_sum/tweet_count as sentiment_mean, cID, bin_position 
            FROM binned_sentiment 
            WHERE break_id != '0')
            AS sentiment,
        (SELECT 
            part_of.cID,
            sum(t.canceling) AS canceling, 
            sum(t.boarding) AS boarding, 
            sum(t.stuck) AS stuck, 
            sum(t.booking) AS booking, 
            sum(t.customers) AS customers, 
            sum(t.dm) AS dm, 
            sum(t.waiting) AS waiting, 
            sum(t.money) AS money, 
            sum(t.information) AS information, 
            sum(t.staff) AS staff, 
            sum(t.baggage) AS baggage
        FROM tweets AS t, part_of
        WHERE t.id = part_of.tID
        GROUP BY part_of.cID)
        AS topics
    WHERE tweets.id = break.break_id AND
        sentiment.cID = break.cID AND
        sentiment.bin_position = (break.bin_position + 1) AND
        topics.cID = break.cID
    """
    
    # Query data and store as a dataframe
    cursor.execute(query) 
    df_tweets = pd.DataFrame(cursor.fetchall(), columns=['airline', 
                                                         'reply_time', 
                                                         'sentiment_change', 
                                                         'canceling',
                                                         'boarding',
                                                         'stuck',
                                                         'booking',
                                                         'customers',
                                                         'dm',
                                                         'waiting',
                                                         'money',
                                                         'information',
                                                         'staff',
                                                         'baggage'])
 

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