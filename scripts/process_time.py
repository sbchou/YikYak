import json
import time
import glob
import os
from process_json import preproc_name
from collections import Counter
import cPickle as pickle

def get_hr_day(tweet):
    t = time.strptime(tweet['postedTime'], "%Y-%m-%dT%H:%M:%S.%fZ")
    hour = t.tm_hour
    day = t.tm_wday
    return hour, day


def get_time_info(filename):
    """ Just the pure body of tweets."""
    hours = []
    days = []
    with open(filename) as fi:
        for line in fi:
            t = json.loads(line)
            hour, day = get_hr_day(t)
            hours.append(hour)
            days.append(day)
    return Counter(hours), Counter(days)

def process_school(path):
    #schoolname = os.path.basename(path)
    hours = Counter()
    days = Counter()
    files = glob.glob(path + "/*.json")
    for fi in files:
        h, d = get_time_info(fi)
        hours += h
        days += d
    return hours, days

def run_locations():
    full_path = "/Users/cat/Dropbox (MIT)/LSM/YikYak/tagged_unpacked/"
    schools = glob.glob(full_path + "/*")
    for school in schools:
        schoolname = os.path.basename(school)
        schoolname = preproc_name(schoolname)
        print schoolname    
        hours, days = process_school(school)
        hour_path = "/Users/cat/Dropbox (MIT)/LSM/YikYak/data/pickles/"\
                    + schoolname + "_hours.pickle"
        day_path = "/Users/cat/Dropbox (MIT)/LSM/YikYak/data/pickles/"\
                    + schoolname + "_days.pickle"
        pickle.dump(hours, open(hour_path, 'wb'))
        pickle.dump(days, open(day_path, 'wb'))

def run_all():
    hours = Counter()
    days = Counter()
    full_path = "/Users/cat/Dropbox (MIT)/LSM/YikYak/tagged_unpacked/"
    schools = glob.glob(full_path + "/*")
    for school in schools:
        print school   
        h, d = process_school(school)
        hours += h
        days += d

    hour_path = "/Users/cat/Dropbox (MIT)/LSM/YikYak/data/pickles/"\
                + "all_hours.pickle"
    day_path = "/Users/cat/Dropbox (MIT)/LSM/YikYak/data/pickles/"\
                + "all_days.pickle"
    pickle.dump(hours, open(hour_path, 'wb'))
    pickle.dump(days, open(day_path, 'wb'))

