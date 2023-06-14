import mysql.connector 
from database.connect import getConnection

db = getConnection()
cursor=db.cursor() 

def count_airline_tweets (cursor) -> dict:
    """This function will count the amount of conversations in which one of the airlines responded multiple times.
    input: name of cursor
    ooutput: a dictionary with the amount of times each airline responded more than once in a conversations.
    """
    #create a dictionary of all airline user_ids for later on
    airline_counter = {"KLM":0,"AirFrance":0,"British_Airways":0,"AmericanAir":0,"Lufthansa":0, "AirBerlin":0, "AirBerlin assist":0, "easyJet":0,
                       "RyanAir":0,"SingaporeAir":0,"Qantas":0, "EtihadAirways":0, "VirginAtlantic":0}
    
    cursor.execute("SELECT * FROM `conversations` WHERE Airline <> '0'")
    conversations = cursor.fetchall() #all conversations with participating airlines


    for conversation in conversations: #for each conversation with a participating airline
        conv_id = conversation[0]
        airlines= {56377143 : ['KLM',0], 106062176:['AirFrance',0],18332190:['British_Airways',0], 22536055:['AmericanAir',0],
           124476322:['Lufthansa',0],26223583:['AirBerlin',0],2182373406:['AirBerlin assist',0],38676903:['easyJet',0],1542862735:['RyanAir',0],
           253340062:['SingaporeAir',0],218730857:['Qantas',0],45621423:['EtihadAirways',0],20626359:['VirginAtlantic',0]}
        #reset dictionary for each conversation to keep track of the amount of times each airline tweets per conversation
        
        cursor.execute(f"SELECT t.id, t.user_id, po.cID FROM `tweets` t, `part_of` po WHERE po.cID = {conv_id} AND po.tID = t.id")
        conv_tweets = cursor.fetchall() #all tweet and conversation ids of tweets in the current conversation and the user_id of the tweeter.

        for tweet in conv_tweets:
            user_id = tweet[1]

            if user_id in airlines: #if the user is an airline, keep track of it
                airlines[user_id][1] += 1

        for airline in airlines: #after iterating over all tweets, see if you encountered an airline more than once and keep track of that
            if airlines[airline][1] >=2:
                airline_counter[airlines[airline][0]] += 1

    return airline_counter
    
print(count_airline_tweets(cursor))
