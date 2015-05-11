import json
import glob
import preprocess_tweets
import os
import cPickle as pickle

def preproc_name(schoolname):
    return schoolname.strip().replace(" ", "_").lower()

def get_tweets(filename):
    tweets = []
    with open(filename) as fi:
        for line in fi:
            t = json.loads(line)    
            text = t['body'].encode('utf8')
            text = preprocess_tweets.preprocess(text)
            tweets.append(text)
    return tweets

def get_text(filename):
    tweets = []
    with open(filename) as fi:
        for line in fi:
            t = json.loads(line)    
            text = t['body'].encode('utf8')
            tweets.append(text)
    return tweets


def get_tokens(filename):
    tweets = []
    with open(filename) as fi:
        for line in fi:
            t = json.loads(line)    
            text = t['body'].encode('utf8')
            text = preprocess_tweets.preprocess(text)
            tweets.append(text)
    return tweets


def parse_text(dir_path):
    schoolname = os.path.basename(dir_path)
    schoolname = preproc_name(schoolname)
    print schoolname
    files = glob.glob(dir_path + "/*.json")
    out = "/Users/cat/Dropbox (MIT)/LSM/YikYak/data/tokens/" + \
          schoolname + ".tsv"
    print out
    out_pickle = "/Users/cat/Dropbox (MIT)/LSM/YikYak/data/pickles/" + \
          schoolname + ".pickle"  
 
    biglist = []

    with open(out, 'w') as outfile:
        for f in files:
            tweets = get_tweets(f)
            tsv = ["\t".join(t) for t in tweets]
            outfile.write("\n".join(tsv))
            biglist.append(tweets)

    pickle.dump(biglist, open(out_pickle, 'wb'))






