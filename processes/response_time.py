
def response_time(tweet_id, texts):
    """
    Calculates the response time for a tweet, def. the time for this tweet to respond to it's parent.
    :param tweet_id: the id of the tweet
    :param connection: the connection with sql.
    :param texts: the tweets table from SQL
    :returns: the response time for a tweet id.
    """
    # Keeps track of execution time
    response_time = 'Null'

    cursor.execute(f"SELECT * FROM `tweets` WHERE id ={tweet_id}")
    tweet_info = cursor.fetchall()[0]

    replied_id = tweet_info[2] #in_reply_to is the second column in the tweets table
    self_time = tweet_info[3] #timestamp is the fourth column in the tweets table
    try:
        # Response time -> response_time
        if replied_id != 0:
            cursor.exectue(f"SELECT timestamp FROM `tweets` WHERE id={replied_id}")
            replied_time = cursor.fetchall()[0][3]    
    except Exception:
        print('an error has occurred')
    
    response_time = self_time - replied_time
    return response_time

