
def create_reply_time_column (cursor) -> None:
    """This function will alter the `tweets` table and add a column to save the reply times as part of the table.
    """
    query = "ALTER TABLE `tweets` ADD reply_time BIGINT DEFAULT '0'"
    cursor.execute(query) #adds a zero everywhere for reply_time
    return None

def update_reply_time (cursor, tweet: int, tweettime = int) -> None:
    """This function will execute SQL queries to update the replytime of all tweets that reply to tweet
    Inputs: cursor: the name of cursor
    tweet: a tweet id of a tweet for which we want to update its replies their reply_time.
    tweettime: the timestamp_ms value of the tweet"""
    repliers = replies.pop(tweet) #remove the list of repliers to this tweet and save it as 'repliers'
    for replier in repliers: #for each tweet that has replied to the tweet we are working on

        cursor.execute(f"SELECT timestamp_ms FROM `tweets` WHERE id={replier}")
        replier_ms = cursor.fetchall()[0][0] #the timestamp at which this tweet was made.
        
        time_diff = replier_ms-tweettime #the time difference between the original tweet and the reply

        query = f"UPDATE `tweets` SET reply_time={time_diff} WHERE id={replier}" 

        cursor.execute(query) #update the tweets table.
    return None


def reply_time_creation (cursor,db, tweets: list) -> None:
    """This function will, given a list of all tweets with their information sorted by descending timestamps,
    update their response times in the SQL database.

    inputs: cursor:the name of the cursor variable in order to run SQL queries.
    db: the name of the connection

    tweets: the list of tuples including the following attributes: id, in_reply_to_status_id, timestamp_ms
    """
    global replies

    replies = {} #we define a dictionary which will later contain for each tweet what tweets have replied to it.

    n = len(tweets)
    run = 0

    for tweet in tweets: #for each tweet that is in the database, starting at the newest one by ordering.
        tweet_id = tweet[0]
        tweet_reply_id = tweet[1] #define some variables for more clarity
        tweet_ms= tweet[2]

        if tweet_id in replies: #if the dictionary contains replies for this tweet, otherwise do nothing.
            
            update_reply_time(cursor,tweet_id, tweet_ms) #update the replytime of all tweets that replied to this tweet and 
                                                    #remove this information from the replies dictionary

        if tweet_reply_id !=0: #if this tweet replied to another tweet, store it in replies, otherwise do nothing

            if tweet_reply_id in replies: #if the tweet this replies to already has another replier
                
                replies[tweet_reply_id] = replies[tweet_reply_id] + [tweet_id] #add this tweet to the list of replies

            else: #if the tweet this replies to is not in replies yet.

                replies[tweet_reply_id] = [tweet_id] #create the tweet this replies to as a key in replies and
                                                    #store this tweet as its reply.
        
        if run% round(n/10)==0: #run is a multiple of n/10 rounded to an integer
            db.commit() #commit the database to ensure it does not run into an error
        run += 1 #update the amount of runs gone through.
    
    return None

