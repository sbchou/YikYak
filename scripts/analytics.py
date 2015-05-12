import glob
import re

URL_PATT = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"

def get_lengths(dir_path):
    """return a giant vector of char length of ea. tweet"""
    files = glob.glob(dir_path + "/*")
    lengths = []
    for school in files:
        with open(school) as f:
            for line in f:
                lengths.append(len(line.strip()))
    return lengths

def gen_tweet_list(dir_path):
    files = glob.glob(dir_path + "/*")
    vect = []
    for school in files:
        with open(school) as f:
            for line in f:
                vect.append(line.strip())
    return vect


def contains_url(tweet):
    if re.findall(URL_PATT, tweet):
        return 1
    else:
        return 0
