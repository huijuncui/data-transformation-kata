#!/usr/bin/env python3

import datetime
import time

# csv utils
def transform_text_csv(text):
    l = text.split("_")
    res = ""
    for i in range(len(l)):
        if i > 0:
            res += l[i].capitalize()
        else: res += l[i]
    return res

def to_unix_time_csv(t):
    l = list(map(lambda n : int(n), t.split('-')))
    date_time = datetime.datetime(l[0], l[1], l[2])
    return int(time.mktime(date_time.timetuple()))

# xml utils
def transform_text_xml(text):
    if text == 'medicalRecordNum':
        return 'mrn'
    elif text == 'diagnoses':
        return 'conditions'
    else: return text

def to_unix_time_xml(t):
    (d, t) = t.split(' ')
    d_list = list(map(lambda n : int(n), d.split('-')))
    t_list = list(map(lambda n : int(float(n)), t.split(':')))
    date_time = datetime.datetime(d_list[0], d_list[1], d_list[2], t_list[0], t_list[1], t_list[2])
    return int(time.mktime(date_time.timetuple()))