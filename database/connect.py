import mysql.connector
import config.env


def getConnection() -> mysql.connector.connection.MySQLConnection:
    """
    Gets a connection to the MySQL database.

    :return: A connection to the MySQL database.
    """
    db = mysql.connector.connect(host=config.env.getConfig('DB_HOST'), user=config.env.getConfig('DB_USERNAME'),
                                 password=config.env.getConfig('DB_PASSWORD'),database=config.env.getConfig('DB_DATABASE'))
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
        `language` TEXT NULL ,
        `in_reply_to_status_id` BIGINT NULL , 
        `timestamp_ms` BIGINT NULL , 
        `coordinates` TEXT NULL ,
        `mentions` TEXT NULL , 
        `user_id` BIGINT NULL , 
        `verified` BOOLEAN NULL , 
        `followers_count` INT NULL , 
        `statusses_count` INT NULL , 
        PRIMARY KEY (`id`)) ENGINE = InnoDB;
        """
    return query
