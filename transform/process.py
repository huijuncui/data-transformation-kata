#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import pandas as pd
from transform.process_utils import *
from load import *

# csv
def process_csv(dir):
    df = pd.read_csv(dir)
    data = []
    names = { 'first_name', 'last_name', 'middle_name' }
    demographics = { 'date_of_birth', 'sex' }
    for i, row in df.iterrows():
        data.append({})
        for col in df.columns:
            cur = None if pd.isna(row[col]) else row[col]
            if col == 'mrn':
                data[i][col] = cur
            elif col in names:
                data[i][transform_text_csv(col)] = cur if cur is None else cur.lower()
            elif col in demographics:
                demo = {} if 'demographics' not in data[i].keys() else data[i]['demographics']
                demo[transform_text_csv(col)] = to_unix_time_csv(cur) if (col == 'date_of_birth') else cur
                data[i]['demographics'] = demo
            else:
                data[i][col] = list(map(lambda e : { 'code': e, 'name' : 'condition' }, cur.split('|')))
        data[i]['source'] = dir[8:]
        output_to_json(data[i], data[i]['mrn'])

    return data

# xml
def process_xml(dir):
    tree = ET.parse(dir)
    root = tree.getroot()
    metrics = ['mrn', 'firstName', 'lastName', 'middleName', 'demographics', 'conditions']
    names = {'firstName', 'lastName', 'middleName'}
    data = {}
    for child in root:
        text = None if pd.isna(child.text) else child.text
        tag = transform_text_xml(child.tag)
        if tag == 'mrn':
            data[tag] = text
        elif tag in names:
            data[tag] = text if text is None else text.lower()
        elif tag == 'demographics':
            data[tag] = {}
            for node in child:
                n_text = None if pd.isna(node.text) else node.text
                data[tag][node.tag] = n_text[0] if node.tag == 'sex' else to_unix_time_xml(n_text)
        else:
            data[tag] = []
            for node in child:
                n_text = None if pd.isna(node.text) else node.text
                data[tag].append(node.attrib)
                data[tag][-1]['name'] = n_text

    data['source'] = dir[8:]
    output_to_json(data, data['mrn'])

    return data
