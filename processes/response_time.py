



def response_time(in_reply_to, self_time, cursor):
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
        if in_reply_to != 0:
            cursor.exectue("SELECT timestamp FROM `tweets` WHERE id= %s" % (in_reply_to))
            replied_time = cursor.fetchone()[0]   
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
    
    cursor.execute(f"SELECT in_reply_to, timestamp FROM `tweets` WHERE id ={tweet_id}")
    tweet_info = cursor.fetchall()[0]

    replied_id = tweet_info[0] #in_reply_to is the second column in the tweets table
    self_time = tweet_info[1] #timestamp is the fourth column in the tweets table

    return(response_time(replied_id, self_time, cursor))