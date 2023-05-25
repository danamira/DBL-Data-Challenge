from pathlib import Path
from JsonHandler import json_file_reader, json_cleaner

data_path = Path(r"C:\Users\Vuijk\Programming projects\JBG030 DBL\DBL-Data-Challenge\data\airlines-1558527599826-1.json")
data = json_file_reader(data_path)
cleaned_data = json_cleaner(data[0])
print(tuple(cleaned_data.values()))