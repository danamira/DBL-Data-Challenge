# IMPORTS
import mysql.connector 
from database.connect import getConnection
import config.env
from notebooks.Response_time_functions import create_reply_time_column
# Get connection

try:
    connection = getConnection()
except Exception:
    print("✖️ Error while connecting to MySQL engine database.")
    print("ℹ️ Please make sure the environment file `.env` is located at"+
        "the project root directory and contains proper configuration.")
    raise

#create a dictionary of all airline user_ids for later on
airlines= {56377143 : 'KLM', 106062176:'AirFrance',18332190:"British_Airways", 22536055:"AmericanAir",
           124476322:"Lufthansa",26223583:'AirBerlin',2182373406:'AirBerlin assist',38676903:"easyJet",1542862735:"RyanAir",
           253340062:"SingaporeAir",218730857:"Qantas",45621423:"EtihadAirways",20626359:"VirginAtlantic"}

cursor = connection.cursor()
query_columns = ['id', 'text', 'in_reply_to_status_id', 'timestamp_ms', 'user_id', 'language', 'mentions', 'airlines',
                 'sepntiment']
query="""SELECT id, , in_reply_to_status_id, timestamp_ms, user_id, language, mentions, airlines, sentiment
        FROM tweets"""
cursor.execute(query) #get the tweets table into the variable tweets
tweets = cursor.fetchall()

create_reply_time_column(cursor)
