import json
from typing import Generator, Dict, List
from pathlib import Path

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
        return [json.loads(line) for line in f]

def create_json(file_path: Path) -> None:
    """
    Create a JSON file.
    
    :param file_path: Path to JSON file
    :return: None
    """
    with open(file_path, 'w') as f:
        f.write('[ \n')

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


