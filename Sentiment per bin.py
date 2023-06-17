import mysql.connector 
from database.connect import getConnection
import config.env 
from sentiment_evolution_functions import create_sentim_table, drop_sentim_table
db = getConnection()
cursor=db.cursor()
drop_sentim_table(db, cursor)
create_sentim_table(db,cursor, config)

