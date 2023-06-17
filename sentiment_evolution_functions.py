def create_sentim_table (db, cursor, config) -> None:
    """This function will create the table to store the sentiment per bin into in your database.
    required imports: config.env, cursor as database.cursor(), mysql.connector
    input: database.cursor() as cursor
            config.env as config
            getconneection() as db
    output: nothing."""
    database = config.env.getConfig('DB_DATABASE')

    cursor.execute(f"""CREATE TABLE `{database}`.`binned_sentiment`(bin_id MEDIUMINT NOT NULL, cID MEDIUMINT NOT NULL, 
                   bin_position SMALLINT NOT NULL, break_id BIGINT NOT NULL,break_position SMALLINT NOT NULL,
                   break_airline VARCHAR(20) NOT NULL, sentiment_sum DECIMAL(7,1), PRIMARY KEY(bin_id))""")
    db.commit()
    return None




def drop_sentim_table (db,cursor) -> None:
    """This function will drop the binned sentiment table.
    input: db (name of database connection), cursor (name of cursor)
    output: None
    """
    cursor.execute("DROP TABLE `binned_sentiment`")
    db.commit()
    return None



def fill_bin_table (db, cursor) -> None:
    """This function will fill the drop_sentiment table with the information of all bins in any conversation with 3 or more tweets.
    inputs: getconnection() as db
            db.cursor() as cursor
    ourput: None"""

    cursor.execute("SELECT * FROM `conversations` WHERE Length > 2")
    conversations = cursor.fetchall() #define the list conversations as the information of all airlines we care about.
    n = len(conversations)

    airlines= {56377143 : 'KLM', 106062176:'AirFrance',18332190:"British_Airways", 22536055:"AmericanAir",
           124476322:"Lufthansa",26223583:'AirBerlin',2182373406:'AirBerlin assist',38676903:"easyJet",1542862735:"RyanAir",
           253340062:"SingaporeAir",218730857:"Qantas",45621423:"EtihadAirways",20626359:"VirginAtlantic"}
    #Define airlines as a dictionary with the user_ids of all airlines as keys and their names as corresponding values.

    bin_id = 1 #keep track of how many bins have been made to ensure this is a primary key, we start at id=1

    for conversation in conversations:

        bin_pos = 1 #keep track of how many bins have been made for this conversation
        bin_sentiment = 0
        conversation_length = conversation[4] #define the length of a conversation

        conversation_id = conversation[0] #for ease of reading later define this as a variable

        cursor.execute(f""" SELECT t.id, po.Position, t.user_id, t.sentiment
                            FROM `tweets` t, `part_of` po
                            WHERE t.id=po.tID AND po.cID = {conversation_id}""")
        #Get all the information we need for the new table about every tweet in the current conversation
        conv_tweets = cursor.fetchall()  #and store it in conv_tweets.
        

        for tweet in conv_tweets: #Iterate for every tweet in the conversation.

            #First define the things contained in tweet for more clarity
            tweet_id = tweet[0]
            tweet_position = tweet[1]
            tweet_user = tweet[2]
            tweet_sentiment = tweet[3]

            if tweet_user in airlines and tweet_position != 1: #If this tweet was made by an airline, create a bin up to here
                #If this airline tweet is not the first tweet in the conversation, create the bin.
                                        #If this is the first tweet of a conversation, do not create a bin.
                cursor.execute(f""" INSERT INTO `binned_sentiment`
                                    (bin_id, cID, bin_position, break_id, break_position, break_airline, sentiment_sum)
                                    VALUES ({bin_id}, {conversation_id},{bin_pos}{tweet_id}, {tweet_position}, {airlines[tweet_user]},
                                    {bin_sentiment})""")
                bin_id += 1
                bin_pos += 1 #Increment these values to keep them accurate
            
            elif tweet_position != conversation_length:
                bin_sentiment += tweet_sentiment #keep track of the sum of sentiments in a bin
            
            else: #So if this was not tweeted by an airline, but is the last tweet of a conversation.
                
