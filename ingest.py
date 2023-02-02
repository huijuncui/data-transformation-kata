#!/usr/bin/env python3

from transform.process import *

input_path = 'data/in/'
file_types = ['csv', 'xml']

# public API
def data_transform():
    for t in file_types:
        read_files(input_path + t, t)

def data_process(file_path, type):
    if type == 'csv':
        process_csv(file_path)
    else:
        process_xml(file_path)

def read_files(folder, type):
    # iterate through all file
    for file in os.listdir(folder):
        # Check whether file is in text format or not
        if file.endswith(f".{type}"):
            file_path = f"{folder}/{file}"
            # call read text file function
            data_process(file_path, type)