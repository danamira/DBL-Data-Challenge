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


def mentions(mention_str: str):
    """
    Takes a list of user_id and returns what airline it corresponds to, or if it is not an airline.
    :param: mention_list: list of user IDs that have been mentioned in a tweet. 
    :returns: list of correponding users, ervyone but airlines as "not_airline" 
    """
    user_mentions_list: list = []
    mention_list = re.findall("\d+", mention_str)

    # Convert every ID to int
    for i, id in enumerate(mention_list):
        mention_list[i] = int(id)

    # For every mention ID
    for mention in mention_list:
        added = False
        # For every airline in airlineIDs        
        for key in airlineIDs:
            # If ID and airline ID match:            
            if mention == airlineIDs[key]:
                user_mentions_list.append(key)
                added = True
            continue
        # If no airline was added:
        if added == False:
            user_mentions_list.append('no_airline')
    
    return user_mentions_list

def identify_airline(mention_list):
    """
    Gets a string and identifies wheather this is an airline or not.
    :param: mention_list: list of usernames.
    :returns: the airline.
    """
    airline = 'no_airline'
    for mention in mention_list:
        for key in airlineIDs:
            if mention == airlineIDs[key]:
                airline = key

    return airline

def mention_count(mention_str):
    """
    Takes a string of a list of mentions and returns the number of mentions.
    :param: mention_list: list of mentions IDs.
    :returns: int value of number of mentions.
    """
    return len(mentions(mention_str))


def airline():
    """
    Takes a string of list of airline names and identifies the airline.
    :param: airline_list: list of airline names.
    :returns: the airline in the mentions
    """



def length(text):
    """
    Returns the length of a string.
    :param:text: a string.
    :returns: the length of the string.
    """
    return len(text)