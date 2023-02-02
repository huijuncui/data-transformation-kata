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
                # no mrn, move to failed document directory
                if cur is None:
                    output_to_failure(dir)
                    return data

                data[i][col] = cur
            elif col in names:
                data[i][transform_text_csv(col)] = cur if cur is None else cur.lower()
            elif col in demographics:
                demo = {} if 'demographics' not in data[i].keys() else data[i]['demographics']
                demo[transform_text_csv(col)] = to_unix_time_csv(cur) if (col == 'date_of_birth') else cur
                data[i]['demographics'] = demo
            else:
                data[i][col] = list(map(lambda e : { 'code': e, 'name' : None }, cur.split('|')))
        data[i]['source'] = dir[8:]
        output_to_json(data[i], data[i]['mrn'])

    return data

# xml
def process_xml(dir):
    tree = ET.parse(dir)
    root = tree.getroot()
    metrics = ['mrn', 'firstName', 'lastName', 'middleName', 'demographics', 'conditions']
    demo_children = ['dateOfBirth', 'sex']
    names = {'firstName', 'lastName', 'middleName'}
    data = {}
    i = 0
    for metric in metrics:
        child = root[i] if i < len(root) else None
        tag = None if child is None else transform_text_xml(child.tag)
        if tag == metric:
            text = None if pd.isna(child.text) else child.text
            i += 1
        else:
            tag = metric
            text = None
        if tag == metrics[0]:
            # no mrn, move to failed document directory
            if text is None:
                output_to_failure(dir)
                return data

            data[tag] = text
        elif tag in names:
            data[tag] = text if text is None else text.lower()
        elif tag == metrics[4]:
            data[tag] = {}
            j = 0
            for d in demo_children:
                if child is None or j >= len(child) or child[j] is None or d != child[j].tag:
                    data[tag][d] = None
                else:
                    n_text = child[j].text
                    data[tag][d] = n_text[0] if d == 'sex' else to_unix_time_xml(n_text)
                    j += 1
        else:
            data[tag] = []
            if child is None or len(child) < 1:
                data[tag].append(None)
            else:
                for node in child:
                    n_text = None if pd.isna(node.text) else node.text
                    data[tag].append(node.attrib)
                    data[tag][-1]['name'] = n_text

    data['source'] = dir[8:]
    output_to_json(data, data['mrn'])

    return data
