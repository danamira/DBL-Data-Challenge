import mysql.connector
import config.env


def getConnection():
    db = mysql.connector.connect(host=config.env.getConfig('DB_HOST'), user=config.env.getConfig('DB_USERNAME'),
                                 password=config.env.getConfig('DB_PASSWORD'),database=config.env.getConfig('DB_DATABASE'))
    return db


def makeTablesQuery():
    return "CREATE TABLE `dbl`.`tweets` (`id` BIGINT NULL , `text` TEXT NULL , `in_reply_to` BIGINT NULL , `timestamp` BIGINT NULL , `user_mentions` TEXT NULL , `user_id` BIGINT NULL , `user_verified` BOOLEAN NULL , `user_followers_count` INT NULL , `user_tweets_count` INT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB;";
