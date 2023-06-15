def create_sentim_table (cursor) -> None:
    """This function will create the table to store the sentiment per bin into in your database.
    required imports: config.env, cursor as database.cursor(), mysql.connector
    input: database.cursor() as cursor
    output: nothing."""
    database = config.env.getConfig('DB_DATABASE')

    cursor.execute(f"""CREATE TABLE `{database}`.`binned_sentiment`(begin_id BIGINT NOT NULL, end_id BIGINT NOT NULL, break_id BIGINT NOT NULL, break_position SMALLINT,
                   cID MEDIUMINT NOT NULL, avg_sentiment DECIMAL(7,1), break_airline VARCHAR(20), PRIMARY KEY(begin_id, cID))""")
    return None

import mysql.connector 
from database.connect import getConnection
import config.env  
db = getConnection()
cursor=db.cursor()
create_sentim_table(cursor)
