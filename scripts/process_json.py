import json
import glob
import twokenize
import os
import cPickle as pickle
import re
import time
import csv

# Twitter username:
USERNAME_RE = re.compile(r"""(?:@[\w_]+)""", re.VERBOSE | re.I | re.UNICODE)
URL_RE = re.compile(r'https?:\/\/.*[\r\n]*', re.VERBOSE | re.I | re.UNICODE)
 

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
            text = t['body'].decode('utf8')
            tokens = twokenize.tokenizeRawTweetText(text)
            tweets.append(tokens)
    return tweets

### CALL this
def get_words(filename):
    """For topic model, just find words > 3 letters"""
    tweets = []
    with open(filename) as fi:
        for line in fi:
            t = json.loads(line)   
            lang = t["twitter_lang"]
            if lang == "en":
                try:
                    text = t['body'].decode('utf8').lower()
                    text = URL_RE.sub(" ", text)
                    text = USERNAME_RE.sub(" ", text)
                    words = re.findall(' (\w{3,})', text)
                    if words:
                        yield words
                except:
                    continue

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
    cu_words = get_school_words(cu)
    rest_words = []
    for school in rest:
        print school
        rest_words += get_school_words(school)

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


