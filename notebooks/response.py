# IMPORTS
import sys
sys.path.append("../DBL-Data-Challenge")
from globals import airlineIDs
import re
from database.connect import getConnection



def hello(he):
    return "hello"

"""def response_time(tweets, tuple, keys_list):
    """"""
    Takes a tuple of values and a list of it's keys
    :param: tweets: fetched cursor, i.e. list of tuples.
    :param: tuple: tuple of values.
    :param: keys: list of the keys of the values.
    :returns: The response time of the tweet-tuple.
    """"""
    time = 0
    
    # Get the time stamp and replied id of the self_tweet
    self_time = tuple[keys_list.index('timestamp_ms')]
    replied_id = tuple[keys_list.index('in_reply_to_status_id')]
    print(self_time, replied_id)

    # Check if the tweet is not a reply
    if replied_id == 0:
        dict['response_time'] = 'Null'
    
    # Check for the timestamp of the parent tweet
    else:
        for tuple2 in tweets:
            if tuple2[keys_list.index('id')] == replied_id:
                replied_time = tuple2[keys_list.index('timestamp_ms')]   
                time = self_time - replied_time  # The time for B (child) to reply to A (parent)
    
    return time """


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

my_str = '[38676903, 1000793307688058880, 27892177]'
#print(my_str)
#print(mentions(my_str))


def length(text):
    """
    Returns the length of a string.
    :param:text: a string.
    :returns: the length of the string.
    """
    return len(text)


def response_time(replied_id, self_time, cursor):
    """
    Calculates the response time for a tweet, def. the time for this tweet to respond to it's parent.
    :param in_reply_to: the id of a tweet that we want to find it's parent to.
    :param self_time: the timestamp of the child-tweet.
    :param cursor: a cursor with a connection to tweets database.
    :returns: the response time for a tweet id.
    """
    response_time = 'Null'

    try:
        # Response time -> response_time
        if replied_id != 0:
            cursor.execute(f"SELECT in_reply_to_status_id, timestamp_ms FROM `tweets` WHERE id ={replied_id}")
            replied_time = cursor.fetchall()[0][1]
    except Exception:
        print('an error has occurred')
    
    try:
        response_time = self_time - replied_time
    except Exception:
        # In case the response time is still "Null"
        pass

    return response_time



def response_time_id(tweet_id, cursor):
    """
    Calculates the response time for a tweet, def. the time for this tweet to respond to it's parent.
    :param tweet_id: the id of the tweet.
    :param cursor: a cursor with a connection to tweets database.
    :returns: the response time from the response_time function.
    """
    print('HELLO')
    replied_id = 0
    cursor.execute(f"SELECT in_reply_to_status_id, timestamp_ms FROM `tweets` WHERE id ={tweet_id}")
    try:
        tweet_info = cursor.fetchall()[0]
        replied_id = tweet_info[0] #in_reply_to is the second column in the tweets table
        self_time = tweet_info[1] #timestamp is the fourth column in the tweets table
        print(tweet_info)
    except Exception:
        return 0

    return response_time(replied_id, self_time, cursor)




# Get connection
try:
    connection = getConnection()
except Exception:
    print("✖️ Error while connecting to MySQL engine database.")
    print("ℹ️ Please make sure the environment file `.env` is located at"+
        "the project root directory and contains proper configuration.")
    raise

cursor = connection.cursor()

#print(response_time_id(1131174884103610368, cursor))
#print(response_time(1131340856198389762, 44444444, cursor))

#cursor.close()
connection.close()






texts = [(1131172864147808257, 'text', 0, 1558527601645, '[880417607865815040, 1000793307688058880, 27892177]', 3420691215, -0.462126),
            (1131172864147808257, 'text', 0, 3420691215, '[880417607865815040, 1000793307688058880, 27892177]', 123, -0.462126)]


