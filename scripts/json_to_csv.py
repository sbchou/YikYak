import json
import glob
import twokenize
import os
import cPickle as pickle
import re
import time
import csv

"""
def json_to_csv(outpath="/Users/cat/Dropbox (MIT)/LSM/YikYak/data/csv"):
    with open(outpath, 'wb') as csvfile:
    
    with open('eggs.csv', 'wb') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=' ',
                                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
                spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
                    spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])
"""

def preproc_name(schoolname):
    return schoolname.strip().replace(" ", "_").lower()

def get_text(tweet):
    """Just the pure body of tweets."""
    text = tweet['body'].encode('utf8')
    return text

def is_reply(tweet):
    """Is this an original tweet"""
    if "inReplyTo" in tweet.keys():
        return 1
    else:
        return 0

def favorite_ct(tweet):
    return tweet["favoritesCount"]

def rt_ct(tweet):
    return tweet["retweetCount"]

def contains_vulgarity(tweet):
    pass

def get_sw():
    SWEAR_PATH = "/Users/cat/Dropbox (MIT)/yikyak/analysis/swear_words/swaer_words_list.csv"
    vulgarities = []
    with open(SWEAR_PATH, 'r') as sw:
        vulgarities = sw.read().splitlines()
    return vulgarities

def get_text(filename):
    """ Just the pure body of tweets."""
    tweets = []
    with open(filename) as fi:
        for line in fi:
            t = json.loads(line)    
            text = t['body'].encode('utf8')
            tweets.append(text)
    return tweets

def get_twokens(filename):
    """CMU Twokenizer."""
    tweets = []
    with open(filename) as fi:
        for line in fi:
            t = json.loads(line)    
            text = t['body'].encode('utf8')
            tokens = twokenize.tokenizeRawTweetText(text)
            tweets.append(tokens)
    return tweets


def get_words(filename):
    """For topic model, just find words > 3 letters"""
    tweets = []
    with open(filename) as fi:
        for line in fi:
            t = json.loads(line)    
            text = t['body'].encode('utf8')
            text = text.strip().lower()\
                    .replace("http", "")\
                    .replace("https", "")
            words = re.findall(' (\w{3,})', text)
            if words:
                yield words

def get_school_words(path):
    files = glob.glob(path + "/*.json") 
    all_words = []
    for f in files:
        words = [w for w in get_words(f)]
        all_words += words
    return all_words

def get_tokens_but_cu():
    CU = "Columbia\ University/"
    SCHOOLS_PATH = "/Users/cat/Dropbox (MIT)/LSM/YikYak/tagged_unpacked/"
    schools = glob.glob(SCHOOLS_PATH + "/*")
    rest = schools[:3] + schools[4:]
    cu = schools[3]
    cu_words = process_json.get_school_words(cu)
    rest_words = []
    for school in rest:
        print school
        rest_words += process_json.get_school_words(school)

    return cu_words, rest_words

def parse_tweets_for_topics(dir_path):
    """ FOR TOPIC MODELS, JUST WORDS """
    schoolname = os.path.basename(dir_path)
    schoolname = preproc_name(schoolname)
    print schoolname
    files = glob.glob(dir_path + "/*.json")
    out = "/Users/cat/Dropbox (MIT)/LSM/YikYak/data/words/" + \
          schoolname + ".tsv"
    out_pickle = "/Users/cat/Dropbox (MIT)/LSM/YikYak/data/pickled_words/" + \
          schoolname + ".pickle"  
 
    biglist = []

    with open(out, 'w') as outfile:
        for f in files:
            tweets = [t for t in get_words(f)]
            #import pdb; pdb.set_trace()
            outfile.write("\n".join(tweets))
            biglist += tweets

    pickle.dump(biglist, open(out_pickle, 'wb'))


def parse_tweets(dir_path):
    """ Just pure encoded tweets. Dump to school csvs"""
    schoolname = os.path.basename(dir_path)
    schoolname = preproc_name(schoolname)
    print schoolname
    files = glob.glob(dir_path + "/*.json")
    out = "/Users/cat/Dropbox (MIT)/LSM/YikYak/data/tokens/" + \
          schoolname + ".tsv"

    with open(out, 'w') as outfile:
        for f in files:
            tweets = get_tokens(f)
            tsv = ["\t".join(t) for t in tweets]
            outfile.write("\n".join(tsv))


