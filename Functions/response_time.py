"""
FUNCTION FOR SENTIMENT ANALYSIS.
This script imports the relevant modules to perform the sentiment analysis, 
as well as contians a function that takes a string and returns a sentiment score 
on the form; score: int = positive - negative
"""


# This is a mid-though process
# Alicia: I had to stop to run to a meeting
# but feel free to have a look/continue

def response_time(tweet_id, texts):
    """
    Calculates the response time for a tweet, def. the time for this tweet to respond to it's parent.
    :param tweet_id: the id of the tweet
    :param connection: the connection with sql.
    :returns: the response time for a tweet id.
    """
    # Keeps track of execution time
    response_time = 'Null'
    try:
        # Response time -> response_time
        self_time = texts[i][timestamp]
        replied_id = texts[i][in_reply_to]
        if replied_id != 0:
            for tuple in texts:
                if tuple[id] == replied_id:
                    replied_time = tuple[timestamp]
                    time = self_time - replied_time
                    dict['response_time'] = time      
    except Exception:
        print('an error has occurred')


