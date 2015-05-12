import json
import glob
import twokenize
import os
import cPickle as pickle
import re

def preproc_name(schoolname):
    return schoolname.strip().replace(" ", "_").lower()

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
            words = re.findall(' (\w{3,} )', text)
            words = " ".join(words)\
                        .strip()\
                        .lower()\
                        .replace("http", "")\
                        .replace("https", "")
            if words:
                yield words

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


