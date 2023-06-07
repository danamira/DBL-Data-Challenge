
def create_reply_time_column (cursor) -> None:
    """This function will alter the `tweets` table and add a column to save the reply times as part of the table.
    """
    query = "ALTER TABLE `tweets` ADD reply_time MEDIUMINT DEFAULT '0'"
    cursor.execute(query) #adds a zero everywhere for reply_time
    return None

def update_reply_time (tweet: int, tweettime = int) -> None:
    """This function will execute SQL queries to update the replytime of all tweets that reply to tweet
    Inputs: tweet: a tweet id of a tweet for which we want to update its replies their reply_time.
    tweettime: the timestamp_ms value of the tweet"""
    repliers = replies.pop(tweet) #remove the list of repliers to this tweet and save it as 'repliers'
    for replier in repliers: #for each tweet that has replied to the tweet we are working on

    
    return None


def reply_time_creation (cursor, tweets: list) -> None:
    """This function will, given a list of all tweets with their information sorted by descending timestamps,
    update their response times in the SQL database.
    
    inputs: the name of the cursor variable in order to run SQL queries.
    tweets: the list of tuples including the following attributes: id, in_reply_to_status_id, timestamp_ms
    """
    global replies
    replies = {} #we define a dictionary which will later contain for each tweet what tweets have replied to it.

    for tweet in tweets: #for each tweet that is in the database, starting at the newest one by ordering.
        tweet_id = tweet[0]
        tweet_reply_id = tweet[1] #define some variables for more clarity
        tweet_ms= tweet[2]

        if tweet in replies: #if the dictionary contains replies for this tweet, otherwise do nothing.
            update_reply_time(tweet_id, tweet_ms) #update the replytime of all tweets that replied to this tweet and 
                                                    #remove this information from the replies dictionary
            
        


