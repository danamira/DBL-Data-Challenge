# IMPORTS
import sys
sys.path.append("../DBL-Data-Challenge")
from globals import airlineIDs
import re
from database.connect import getConnection


def response_time_calc(replied_id, self_time, cursor):
    """
    Calculates the response time for a tweet, def. the time for this tweet to respond to it's parent.
    :param in_reply_to: the id of a tweet that we want to find it's parent to.
    :param self_time: the timestamp of the child-tweet.
    :param cursor: a cursor with a connection to tweets database.
    :returns: the response time for a tweet id.
    """
    response_time = 'no_reply'

    try:
        # Response time -> response_time
        if replied_id != 0:
            cursor.execute(f"SELECT in_reply_to_status_id, timestamp_ms FROM `tweets` WHERE id ={replied_id}")
            replied_time = cursor.fetchall()[0][1]
    except Exception:
        pass

    try:
        response_time = abs(self_time - replied_time)/(1000*60*60) # In hours
    except Exception:
        pass
    
    return response_time


def response_time_id(tweet_id, cursor):
    """
    Calculates the response time for a tweet, def. the time for this tweet to respond to it's parent.
    :param tweet_id: the id of the tweet.
    :param cursor: a cursor with a connection to tweets database.
    :returns: the response time from the response_time function.
    """
    replied_id = 0
    #cursor.execute(f"SELECT in_reply_to_status_id, timestamp_ms FROM `tweets` WHERE id ={tweet_id}")
    cursor.execute("SELECT in_reply_to_status_id, timestamp_ms FROM `tweets` WHERE id = ( %s )" % (tweet_id))
    tweet_info = cursor.fetchall()[0]
    try:
        #tweet_info = cursor.fetchall()[0]
        replied_id = tweet_info[0] #in_reply_to is the second column in the tweets table
        self_time = tweet_info[1] #timestamp is the fourth column in the tweets table
        response_time = response_time_calc(replied_id, self_time, cursor)
    except Exception:
        response_time = 'no_reply'

    """#tweet_info = cursor.fetchall()[0]
    replied_id = tweet_info[0] #in_reply_to is the second column in the tweets table
    self_time = tweet_info[1] #timestamp is the fourth column in the tweets table
    response_time = response_time_calc(replied_id, self_time, cursor)"""

    return response_time


def mentions_length(mention_str: str):
    """
    Takes a str(list) of user IDs and returns the length of list(int) of user IDs.
    :param: mention_str2: str(list) of user IDs.
    :returns: list of mentioned user IDs.
    """
    mention_list = re.findall("\d+", mention_str)

    # Convert every ID to int
    for i, id in enumerate(mention_list):
        mention_list[i] = int(id)

    return int(len(mention_list))


def length(text):
    """
    Returns the length of a string.
    :param:text: a string.
    :returns: the length of the string.
    """
    return len(text)