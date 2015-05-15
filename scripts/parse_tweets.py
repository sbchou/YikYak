import json
import glob
import twokenize
import os
import cPickle as pickle
import re
import time
import csv
import twokenize

USERNAME_RE = re.compile(r"""(?:@[\w_]+)""", re.VERBOSE | re.I | re.UNICODE)
URL_RE = re.compile(r'https?:\/\/.*[\r\n]*', re.VERBOSE | re.I | re.UNICODE)

TEST_PATH ="/Users/cat/Dropbox\ \(MIT\)/LSM/YikYak/tagged_unpacked/Brown\ University/20150405-20150426_rqx9mvr143_2015_04_25_23_50_activities.json"
CU = "Columbia\ University/"
SCHOOLS_PATH = "/Users/cat/Dropbox (MIT)/LSM/YikYak/tagged_unpacked/"

def get_twokens_rt_fave(filename):
    with open(filename) as fi:
        for line in fi:
            t = json.loads(line)
            lang = t["twitter_lang"]
            if lang == "en":
                try:
                    print "english"
                    text = t['body'].decode('utf8').lower()
                    #print text
                    text = URL_RE.sub(" ", text)
                    text = USERNAME_RE.sub(" ", text)
                    #print 'text', text 
                    #words = re.findall(' (\w{3,})', text)
                    toks = twokenize.tokenizeRawTweetText(text)
                    print "toks", toks
                    if toks:
                        #print "has toks"
                        isReply = 1 if "inReplyTo" in t.keys() else 0
                        #import pdb; pdb.set_trace()

                        print (toks, t['retweetCount']
                            , t['favoritesCount'], isReply)
                        yield (toks, t['retweetCount'], t['favoritesCount'], isReply) 
                    else:
                        print "NO TOKS"

                except:
                    continue
                


#filter(lambda x: x in all_tweets[0], ["moon"])
# cu_sw = [set(t) & set(sw) for t in cu if set(t) & set(sw)]
def get_twokens(tweet):
    """CMU Twokenizer."""
    tweets = []
    with open(filename) as fi:
        for line in fi:
            t = json.loads(line)    
            text = t['body'].encode('utf8')
            tokens = twokenize.tokenizeRawTweetText(text)
            tweets.append(tokens)
    return tweets

def sw_ct(tokenized_tweets):
    sw = get_sw()      
    has_sw = [set(t) & set(sw) for t in tokenized_tweets if set(t) & set(sw)]
    return len(sw), len(tokenized_tweets)


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

def contains_vulgarity(tweet, vulgarities):
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




#################################
### CALL this

def get_reply_ct(filename):
    ct = 0
    with open(filename) as fi:
        for line in fi:
            t = json.loads(line)
            if "inReplyTo" in t.keys():
                ct += 1
    return ct 

def get_school_reply_ct(path):
    files = glob.glob(path + "/*.json") 
    ct = 0
    for f in files:
        ct += get_reply_ct(f)
       
    return ct
              
def get_replies_but_cu():
    CU = "Columbia\ University/"
    SCHOOLS_PATH = "/Users/cat/Dropbox (MIT)/LSM/YikYak/tagged_unpacked/"
    schools = glob.glob(SCHOOLS_PATH + "/*")
    rest = schools[:3] + schools[4:]
    cu = schools[3]
    cu_ct = get_school_reply_ct(cu)
    rest_ct = 0
    for school in rest:
        print school
        rest_ct += get_school_reply_ct(school)

    return cu_ct, rest_ct


def get_school_meta(path):
    files = glob.glob(path + "/*.json") 

    all_words = []
    for f in files:
        words = [w for w in get_twokens_rt_fave(f)]
        #import pdb; pdb.set_trace()
        all_words += words
    return all_words

def get_meta_but_cu():
    CU = "Columbia\ University/"
    SCHOOLS_PATH = "/Users/cat/Dropbox (MIT)/LSM/YikYak/tagged_unpacked/"
    schools = glob.glob(SCHOOLS_PATH + "/*")
    rest = schools[:3] + schools[4:]
    cu = schools[3]
    cu_words = get_school_meta(cu)
    rest_words = []
    for school in rest:
        print school
        rest_words += get_school_meta(school)

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


