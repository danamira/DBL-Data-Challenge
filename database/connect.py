import mysql.connector
import config.env


<<<<<<< Updated upstream
def getConnection() -> mysql.connector.connection.MySQLConnection:
    """
    Gets a connection to the MySQL database.

    :return: A connection to the MySQL database.
    """
    db = mysql.connector.connect(host=config.env.getConfig('DB_HOST'), user=config.env.getConfig('DB_USERNAME'),
                                 password=config.env.getConfig('DB_PASSWORD'),database=config.env.getConfig('DB_DATABASE'))
=======
def getConnection():
    print(config.env.getConfig('DB_HOST'))
    db = mysql.connector.connect(host='localhost', user='root',
                                 password='Iam1GlobalCitizen!',database='dbl')
>>>>>>> Stashed changes
    return db


def makeTablesQuery() -> str:
    """	
    Returns the query to create the tweets table.
    
    :return: The query to create the tweets table.
    """
    query = """
        CREATE TABLE `dbl`.`tweets` 
        (`id` BIGINT NULL ,
        `text` TEXT NULL ,
        `in_reply_to` BIGINT NULL , 
        `timestamp` BIGINT NULL , 
        `user_mentions` TEXT NULL , 
        `user_id` BIGINT NULL , 
        `user_verified` BOOLEAN NULL , 
        `user_followers_count` INT NULL , 
        `user_tweets_count` INT NULL , 
        PRIMARY KEY (`id`)) ENGINE = InnoDB;
        """
    return query
