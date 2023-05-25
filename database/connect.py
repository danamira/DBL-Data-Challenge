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
    query = f"""
        CREATE TABLE `{config.env.getConfig('DB_DATABASE')}`.`tweets` 
        (`id` BIGINT NULL ,
        `text` TEXT NULL ,
        `in_reply_to_status_id` BIGINT NULL , 
        `coordinates` TEXT NULL ,
        `timestamp_ms` BIGINT NULL , 
        `verified` BOOLEAN NULL ,
        `followers_count` INT NULL ,
        `statuses_count` INT NULL ,
        `user_id` BIGINT NULL ,
        `language` VARCHAR(3) NULL ,
        `mentions` TEXT NULL ,
        PRIMARY KEY (`id`)) ENGINE = InnoDB;
        """
    return query
