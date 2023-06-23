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



def reply_df_set_up():
    """
    Returns the dataframes used in the visualisation
    """
    df_tweets = reply_set_up()
    
    # Convert sentiment score to pos, neu, neg
    df_tweets.loc[df_tweets['sentiment1'] < -0.2, 'sentiment1'] = -1
    df_tweets.loc[df_tweets['sentiment1'] > -0.2, 'sentiment1'] = 1
    df_tweets.loc[(df_tweets['sentiment1']  >= -0.2) & (df_tweets['sentiment1'] <= 0.2), 'sentiment1'] = 0

    df_tweets.loc[df_tweets['sentiment2'] < -0.2, 'sentiment2'] = -1
    df_tweets.loc[df_tweets['sentiment2'] > -0.2, 'sentiment2'] = 1
    df_tweets.loc[(df_tweets['sentiment2']  >= -0.2) & (df_tweets['sentiment2'] <= 0.2), 'sentiment2'] = 0

    # Calculate the difference between sentiment 1 and 2
    df_tweets['sentiment_change'] = df_tweets['sentiment2'] - df_tweets['sentiment1']

    # Creating a data frame per topic
    df_canceling = df_tweets[df_tweets['canceling'] != 0][['airline', 'reply_time', 'sentiment_change']]
    df_boarding = df_tweets[df_tweets['boarding'] != 0][['airline', 'reply_time', 'sentiment_change']]
    df_stuck = df_tweets[df_tweets['stuck'] != 0][['airline', 'reply_time', 'sentiment_change']]
    df_booking = df_tweets[df_tweets['booking'] != 0][['airline', 'reply_time', 'sentiment_change']]
    df_customers = df_tweets[df_tweets['customers'] != 0][['airline', 'reply_time', 'sentiment_change']]
    df_dm = df_tweets[df_tweets['dm'] != 0][['airline', 'reply_time', 'sentiment_change']]
    df_waiting = df_tweets[df_tweets['waiting'] != 0][['airline', 'reply_time', 'sentiment_change']]
    df_money = df_tweets[df_tweets['money'] != 0][['airline', 'reply_time', 'sentiment_change']]
    df_information = df_tweets[df_tweets['information'] != 0][['airline', 'reply_time', 'sentiment_change']]
    df_staff = df_tweets[df_tweets['staff'] != 0][['airline', 'reply_time', 'sentiment_change']]
    df_baggage = df_tweets[df_tweets['baggage'] != 0][['airline', 'reply_time', 'sentiment_change']]

    df_clean = (df_canceling, df_boarding, df_stuck, df_booking, df_customers, df_dm, df_waiting, df_money, df_information, df_staff, df_baggage)

    # Binned of 1 min
    df_canceling_gro = df_canceling[['reply_time', 'sentiment_change']].groupby('reply_time').agg('mean').rolling(window=15).mean()
    df_boarding_gro = df_boarding[['reply_time', 'sentiment_change']].groupby('reply_time').agg('mean').rolling(window=15).mean()
    df_stuck_gro = df_stuck[['reply_time', 'sentiment_change']].groupby('reply_time').agg('mean').rolling(window=15).mean()
    df_booking_gro = df_booking[['reply_time', 'sentiment_change']].groupby('reply_time').agg('mean').rolling(window=15).mean()
    df_customers_gro = df_customers[['reply_time', 'sentiment_change']].groupby('reply_time').agg('mean').rolling(window=15).mean()
    df_dm_gro = df_dm[['reply_time', 'sentiment_change']].groupby('reply_time').agg('mean').rolling(window=15).mean()
    df_waiting_gro = df_waiting[['reply_time', 'sentiment_change']].groupby('reply_time').agg('mean').rolling(window=15).mean()
    df_money_gro = df_money[['reply_time', 'sentiment_change']].groupby('reply_time').agg('mean').rolling(window=15).mean()
    df_information_gro = df_information[['reply_time', 'sentiment_change']].groupby('reply_time').agg('mean').rolling(window=15).mean()
    df_staff_gro = df_staff[['reply_time', 'sentiment_change']].groupby('reply_time').agg('mean').rolling(window=15).mean()
    df_baggage_gro = df_baggage[['reply_time', 'sentiment_change']].groupby('reply_time').agg('mean').rolling(window=15).mean()

    df_grouped = (df_canceling_gro, df_boarding_gro, df_stuck_gro, df_booking_gro, df_customers_gro, df_dm_gro, df_waiting_gro, df_money_gro, df_information_gro, df_staff_gro, df_baggage_gro)

    return df_clean, df_grouped

def reply_significance_test_and_set_up():
    """
    sets up the data frame for the t-test
    """
    df = reply_df_set_up()[0]

    # The data frames to make significance testing on
    df_baggage = df[10][['reply_time', 'sentiment_change']]
    df_boarding = df[1][['reply_time', 'sentiment_change']]
    df_booking = df[3][['reply_time', 'sentiment_change']]
    df_information = df[8][['reply_time', 'sentiment_change']]
    df_money = df[7][['reply_time', 'sentiment_change']]
    df_waiting = df[6][['reply_time', 'sentiment_change']]

    # Gets quantiles of the 6 most interesting topics
    baggage_qua5 = df_baggage['reply_time'].astype(float).quantile([0, 0.25, 0.5, 0.75, 1])
    boarding_qua5 = df_boarding['reply_time'].astype(float).quantile([0, 0.25, 0.5, 0.75, 1])
    booking_qua5 = df_booking['reply_time'].astype(float).quantile([0, 0.25, 0.5, 0.75, 1])
    information_qua5 = df_information['reply_time'].astype(float).quantile([0, 0.25, 0.5, 0.75, 1])
    money_qua5 = df_money['reply_time'].astype(float).quantile([0, 0.25, 0.5, 0.75, 1])
    waiting_qua5 = df_waiting['reply_time'].astype(float).quantile([0, 0.25, 0.5, 0.75, 1])

    qua5 = (baggage_qua5, boarding_qua5, booking_qua5, information_qua5)

    # Data frames
    df_baggage_4 = split_df(df_baggage, baggage_qua5)
    df_boarding_4 = split_df(df_boarding, boarding_qua5)
    df_booking_4 = split_df(df_booking, booking_qua5)
    df_information_4 = split_df(df_information, information_qua5)
    df_money_4 = split_df(df_money, money_qua5)
    df_waiting_4 = split_df(df_waiting, waiting_qua5)

    # Calculates the p-values
    p_baggage = welch_test(df_baggage_4, 'baggage')
    p_boarding = welch_test(df_boarding_4, 'boarding')
    p_booking = welch_test(df_booking_4, 'booking')
    p_information = welch_test(df_information_4, 'information')
    p_money = welch_test(df_money_4, 'money')
    p_waiting = welch_test(df_waiting_4, 'waiting')

    # Adds the p-values to a data-frame
    ds = [p_baggage, p_boarding, p_booking, p_information, p_money, p_waiting]
    df_p = pd.DataFrame(ds)

    return df_p, qua5

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



def visualise_reply_time():
    """
    Creates the visualisations
    """
    df_grouped = reply_df_set_up()[1]
    qua5 = reply_significance_test_and_set_up()[1]

    fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(15,7), sharey=True, sharex=True, layout="constrained")
    plt.setp(ax, ylim=(-2,2))
    plt.setp(ax, xlim=(-2,720))

    # ROW 1
    # Baggage
    sns.lineplot(data=df_grouped[10], x='reply_time', y='sentiment_change', ax=ax[0,0])
    ax[0,0].axvline(x = qua5[0][0.25], c='purple', label='0.25')
    ax[0,0].axvline(x = qua5[0][0.5], c='green', label='0.5')
    ax[0,0].axvline(x = qua5[0][0.75], c='orange', label='0.75')
    ax[0,0].legend(title = 'Quartile')
    ax[0,0].set_title('Baggage', size=20)
    ax[0,0].set_ylabel('Sentiment Change [XLM-RoBERTA]')

    # Boarding
    sns.lineplot(data=df_grouped[1], x='reply_time', y='sentiment_change', ax=ax[0,1])
    ax[0,1].axvline(x = qua5[1][0.25], c='purple', label='0.25')
    ax[0,1].axvline(x = qua5[1][0.5], c='green', label='0.5')
    ax[0,1].axvline(x = qua5[1][0.75], c='orange', label='0.75')
    ax[0,1].legend(title = 'Quartile')
    ax[0,1].set_title('Boarding', size=20)

    # Booking
    sns.lineplot(data=df_grouped[3], x='reply_time', y='sentiment_change', ax=ax[0,2])
    ax[0,2].axvline(x = qua5[2][0.25], c='purple', label='0.25')
    ax[0,2].axvline(x = qua5[2][0.5], c='green', label='0.5')
    ax[0,2].axvline(x = qua5[2][0.75], c='orange', label='0.75')
    ax[0,2].legend(title = 'Quartile')
    ax[0,2].set_title('Booking', size=20)

    # ROW 2
    # Information
    sns.lineplot(data=df_grouped[8], x='reply_time', y='sentiment_change', ax=ax[1,0])
    ax[1,0].axvline(x = qua5[3][0.25], c='purple', label='0.25')
    ax[1,0].axvline(x = qua5[3][0.5], c='green', label='0.5')
    ax[1,0].axvline(x = qua5[3][0.75], c='orange', label='0.75')
    ax[1,0].legend(title = 'Quartile')
    ax[1,0].set_title('Information', size=20)
    ax[1,0].set_xlabel('Reply Time [min]', size=18)
    ax[1,0].set_ylabel('Sentiment Change [XLM-RoBERTA]')

    # Waiting
    sns.lineplot(data=df_grouped[7], x='reply_time', y='sentiment_change', ax=ax[1,1])
    ax[1,1].axvline(x = qua5[4][0.25], c='purple', label='0.25')
    ax[1,1].axvline(x = qua5[4][0.5], c='green', label='0.5')
    ax[1,1].axvline(x = qua5[4][0.75], c='orange', label='0.75')
    ax[1,1].legend(title = 'Quartile')
    ax[1,1].set_xlabel('Reply Time [min]', size=18)
    ax[1,1].set_title('Waiting', size=20)

    # Money
    sns.lineplot(data=df_grouped[6], x='reply_time', y='sentiment_change', ax=ax[1,2])
    ax[1,2].axvline(x = qua5[5][0.25], c='purple', label='0.25')
    ax[1,2].axvline(x = qua5[5][0.5], c='green', label='0.5')
    ax[1,2].axvline(x = qua5[5][0.75], c='orange', label='0.75')
    ax[1,2].legend(title = 'Quartile')
    ax[1,2].set_title('Money', size=20)
    ax[1,2].set_xlabel('Reply Time [min]', size=18)

    fig.suptitle('Sentiment Change over Airline Reply-Time in Conversations, Per Topic', weight='bold', size=26, y=1.07)


def topic_in_reply_check_length():
    """
    Returns the number of tweets in each topic used for the reply-time.
    """
    df_tuple = reply_df_set_up()[0]
    # Checking the number ineach category

    canceling_len = len(df_tuple[0][0].index)
    boarding_len = len(df_tuple[0][1].index)
    stuck_len = len(df_tuple[0][2].index)
    booking_len = len(df_tuple[0][3].index)
    customers_len = len(df_tuple[0][4].index)
    dm_len = len(df_tuple[0][5].index)
    waiting_len = len(df_tuple[0][6].index)
    money_len = len(df_tuple[0][7].index)
    information_len = len(df_tuple[0][8].index)
    staff_len = len(df_tuple[0][9].index)
    baggage_len = len(df_tuple[0][10].index)

    return print(f"""
        TOPIC COUNT
        canceling: {canceling_len}
        boarding: {boarding_len}
        stuck: {stuck_len}
        booking: {booking_len}
        customers: {customers_len}
        dm: {dm_len}
        waiting: {waiting_len}
        money: {money_len}
        information: {information_len}
        staff: {staff_len}
        baggage: {baggage_len}
        """)
