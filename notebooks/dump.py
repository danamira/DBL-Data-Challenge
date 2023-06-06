
def mentions_airline(mention_list):
    """
    Takes a list of user IDs and returns the associated airline.
    :param: mention_list: list(int) of user IDs.
    :returns: the list of the associated airlines with the mention list.
    """
    airline = 'no_airline'
    
    # Idetify the airline
    for mention in mention_list:
        for key in airlineIDs:
            if mention == airlineIDs[key]:
                airline = key
            break
        break

    return airline



def mentions(mention_str: str):
    """
    Takes a list of user_id and returns what airline it corresponds to, or if it is not an airline.
    :param: mention_list: list of user IDs that have been mentioned in a tweet. 
    :returns: list of correponding users, ervyone but airlines as "not_airline" 
    """
    user_mentions_list: list = []
    mention_list = re.findall("\d+", mention_str)

    # Convert every ID to int
    for i, id in enumerate(mention_list):
        mention_list[i] = int(id)

    # For every mention ID
    mention = identify_airline(mention_str)
    user_mentions_list.append(mention)
    
    return user_mentions_list

def identify_airline(mention_list):
    """
    Gets a string and identifies wheather this is an airline or not.
    :param: mention_list: list of usernames.
    :returns: the airline.
    """

    # Idetify the airline
    airline = 'no_airline'
    for mention in mention_list:
        for key in airlineIDs:
            if mention == airlineIDs[key]:
                airline = key

    return airline

def mention_count(mention_str):
    """
    Takes a string of a list of mentions and returns the number of mentions.
    :param: mention_list: list of mentions IDs.
    :returns: int value of number of mentions.
    """
    return len(mentions(mention_str))


def airline():
    """
    Takes a string of list of airline names and identifies the airline.
    :param: airline_list: list of airline names.
    :returns: the airline in the mentions
    """
