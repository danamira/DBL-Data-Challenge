import json
from typing import Generator, Dict, List, Optional
from pathlib import Path
import re
from analysis import detect_lang

def json_cleaner(data: Dict) -> Dict:
    """
    Clean a JSON object by keeping only the specified keys.

    :param data: JSON object to clean
    :return: Function to clean a JSON object
    """
    status_keys = ['id', 
            'text', 
            'in_reply_to_status_id', 
            'timestamp_ms',
            'coordinates',
            ]
    
    user_info_keys = ['id',
                      'verified',
                      'followers_count',
                      'statuses_count',
                      ]
        
    output = {k: v for k, v in data.items() if k in status_keys}
    user_info = {k: v for k, v in data['user'].items() if k in user_info_keys}
    # rename id to user_id
    user_info['user_id'] = user_info.pop('id')

    mentions = [mention['id'] for mention in data['entities']['user_mentions']]
    mentions_dict = {'mentions': mentions}

    # gets the full text
    if 'extended_tweet' in data.keys():
        text = data['extended_tweet']['full_text']
    else:
        text = data['text']

    # remove all urls
    re.sub(r'http\S+', 'http', data['text'])

    if not text:
        print(data)

    language = detect_lang(text)
    extended_tweet = {'text': text, 'language': language}

    output.update(user_info)
    output.update(extended_tweet)
    output.update(mentions_dict)

    # sets potential None values to NULL
    null_keys = ['in_reply_to_status_id', 'coordinates']
    for key in null_keys:
        if output[key] is None:
            output[key] = 'NULL'

    return output

def json_object_reader(file_path: Path) -> Generator:
    """
    Read a JSON file and yields JSON objects.
    
    :param file_path: Path to JSON file
    :return: Generator of JSON objects
    """
    with open(file_path) as f:
        for line in f:
            yield json.loads(line)

def json_file_reader(file_path: Path) -> List:
    """
    Read a JSON file and returns a list of JSON objects.
    
    :param file_path: Path to JSON file
    :return: List of JSON objects
    """
    with open(file_path) as f:
        result=[]
        lineCounter=0
        for line in f:
            try:
                result.append(json.loads(line))
            except:
                print(lineCounter,line)
            lineCounter+=1
        return result

def create_json(file_path: Path) -> None:
    """
    Create a JSON file.
    
    :param file_path: Path to JSON file
    :return: None
    """
    with open(file_path, 'w') as f:
        f.write('[\n')

def json_append(data: Dict, file_path: Path) -> None:
    """
    Append a JSON object to a JSON file.
    
    :param data: JSON object to append
    :param file_path: Path to JSON file
    :return: None
    """
    with open(file_path, 'a') as f:
        json.dump(data, f)
        f.write('\n')

def json_close(file_path: Path) -> None:
    """
    Close a JSON file.
    
    :param file_path: Path to JSON file
    :return: None
    """
    with open(file_path, 'a') as f:
        f.write(']')