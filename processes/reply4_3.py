# --------------------------------------------------------
# FUNCTIONS FOR reply_time4.ipynb Jupyter Notebook
# Author: Alicia Larsen
# Data of creation: 2023-06-18
# --------------------------------------------------------

# IMPORTS
import sys
sys.path.append("../DBL-Data-Challenge")
from pathlib import Path
import os

# Own functions
import DB_fun
import JsonHandler
from processes.reply4_2 import reply_set_up
from database.connect import getConnection

# Packages 
import pandas as pd
from scipy.stats import ttest_ind
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()


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
    tweets.timestamp_ms,
	ROUND(tweets.reply_time/(1000*60), 0) AS reply_time, 
	null,
    break.sentiment_mean AS sentiment1,
    sentiment.sentiment_mean AS sentiment2,
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
                                                         'timestamp_ms',
                                                         'reply_time',
                                                         'sentiment_change', 
                                                         'sentiment1', 
                                                         'sentiment2',
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



# Function that splits the data
def split_df(df, df_qua):
    "Takes a dataframe and splits it into 5 quantiles"
    df = df[['reply_time', 'sentiment_change']].astype(float)
    df25 = df[(df['reply_time'] >= df_qua[0.0]) & (df['reply_time'] < df_qua[0.25])]
    df50 = df[(df['reply_time'] >= df_qua[0.25]) & (df['reply_time'] < df_qua[0.5])]
    df75 = df[(df['reply_time'] >= df_qua[0.5]) & (df['reply_time'] < df_qua[0.75])]
    df90 = df[(df['reply_time'] >= df_qua[0.75])]

    return df25, df50, df75, df90

def welch_test(tuple_df, topic):
    """"
    Takes two lists and calculates their p-values
    """
    qua = 25
    p_values_dict = {}
    p_values_dict['topic'] = topic
    for i in range(0, len(tuple_df)-1):
        t, p = ttest_ind(tuple_df[i]['sentiment_change'], tuple_df[i+1]['sentiment_change'], equal_var=False, alternative='less')
        p_values_dict[f'{qua} vs. {qua + 25}'] = p
        qua += 25
    df_lo = pd.concat([tuple_df[0], tuple_df[1]], ignore_index=True, sort=False)
    df_hi = pd.concat([tuple_df[2], tuple_df[3]], ignore_index=True, sort=False)

    t, p = ttest_ind(df_lo['sentiment_change'], df_hi['sentiment_change'], equal_var=False, alternative='less')
    p_values_dict[f'low vs high'] = p
    
    return p_values_dict